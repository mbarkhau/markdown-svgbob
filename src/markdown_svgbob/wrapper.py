# This file is part of the markdown-svgbob project
# https://gitlab.com/mbarkhau/markdown-svgbob
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
import os
import re
import platform
import typing as typ
import pathlib2 as pl
import subprocess as sp


LIBDIR: pl.Path = pl.Path(__file__).parent
PKG_BIN_DIR     = LIBDIR / "bin"
DEFAULT_BIN_DIR = pl.Path("~") / ".cargo" / "bin"
DEFAULT_BIN_DIR = DEFAULT_BIN_DIR.expanduser()


def _get_usr_bin_path() -> typ.Optional[pl.Path]:
    env_path = os.environ.get('PATH')
    env_paths: typ.List[pl.Path] = []

    if env_path:
        path_strs = env_path.split(os.pathsep)
        env_paths.extend([pl.Path(p) for p in path_strs])

    # search in ~/.cargo/bin regardless of path
    if DEFAULT_BIN_DIR not in env_paths:
        env_paths.append(DEFAULT_BIN_DIR)

    for path in env_paths:
        local_bin = path / "svgbob"
        if local_bin.exists():
            return local_bin

        local_bin = path / "svgbob.exe"
        if local_bin.exists():
            return local_bin

    return None


# https://pymotw.com/3/platform/
OSNAME  = platform.system()
MACHINE = platform.machine()


def _get_pkg_bin_path(osname: str = OSNAME, machine: str = MACHINE) -> pl.Path:
    glob_expr = f"*_{machine}-{osname}"
    bin_files = list(PKG_BIN_DIR.glob(glob_expr))
    if bin_files:
        return max(bin_files)

    err_msg = (
        "Platform not supported, "
        "svgbob binary not found. "
        "Install manually using "
        "'cargo install svgbob'."
    )

    raise NotImplementedError(err_msg)


def get_svgbob_bin_path() -> pl.Path:
    usr_bin_path = _get_usr_bin_path()
    if usr_bin_path:
        return usr_bin_path
    else:
        return _get_pkg_bin_path()


def read_output(proc: sp.Popen) -> typ.Iterable[bytes]:
    buf: typ.IO[bytes] = proc.stdout

    while True:
        output = buf.readline()
        if output:
            yield output
        else:
            return


ArgValue = typ.Union[str, int, float, bool]
Options  = typ.Dict[str, ArgValue]


def text2svg(image_text: str, options: Options = None) -> bytes:
    binpath   = get_svgbob_bin_path()
    cmd_parts = [str(binpath)]

    if options:
        for option_name, option_value in options.items():
            if option_name.startswith("--"):
                arg_name = option_name
            else:
                arg_name = "--" + option_name

            if option_value is True:
                cmd_parts.append(arg_name)
            elif option_value is False:
                continue
            else:
                arg_value = str(option_value)
                cmd_parts.append(arg_name)
                cmd_parts.append(arg_value)

    proc = sp.Popen(cmd_parts, stdin=sp.PIPE, stdout=sp.PIPE)

    image_data = image_text.encode("utf-8")
    proc.stdin.write(image_data)
    proc.stdin.close()

    return b"".join(read_output(proc))


# NOTE: in order to not have to update the code
#   of the extension any time an option is added,
#   we parse the help text of the svgbob command.


DEFAULT_HELP_TEXT = """
OPTIONS:
    NL
    --font-family <font-family>
    text will be rendered with this font (default: 'arial')
    NL
    --font-size <font-size>
    text will be rendered with this font size (default: 14)
    NL
 -o --output <output>
    where to write svg output [default: STDOUT]
    NL
    --scale <scale>
    scale the entire svg (dimensions, font size, stroke width)
    by this factor
    NL
    (default: 1)
    NL
    --stroke-width <stroke-width>
    stroke width for all lines (default: 2)
"""

DEFAULT_HELP_TEXT = DEFAULT_HELP_TEXT.replace("\n", " ").replace("NL", "\n")


def _get_cmd_help_text() -> str:
    binpath   = get_svgbob_bin_path()
    cmd_parts = [str(binpath), "--help"]
    proc      = sp.Popen(cmd_parts, stdout=sp.PIPE)
    help_data = b"".join(read_output(proc))
    return help_data.decode("utf-8")


OptionsHelp = typ.Dict[str, str]

# https://regex101.com/r/287NYS/2
OPTION_PATTERN = r"""
    --(?P<name>[a-z\-]+)
    \s+<[a-z\-]+>
    \s+
    (?P<text>[\s\w(),:;.'"\[\]]*)
"""
OPTION_REGEX = re.compile(OPTION_PATTERN, flags=re.VERBOSE | re.DOTALL | re.MULTILINE)


def _parse_options_help_text(help_text: str) -> OptionsHelp:
    options: OptionsHelp = {}

    options_text = help_text.split("OPTIONS:", 1)[-1]
    options_text = options_text.split("ARGS:", 1)[0]

    for match in OPTION_REGEX.finditer(options_text):
        name = match.group("name")
        text = match.group("text")
        text = " ".join(l.strip() for l in text.splitlines())
        options[name] = text

    options.pop("output", None)

    return options


_PARSED_OPTIONS: OptionsHelp = {}


def parse_options() -> OptionsHelp:
    if _PARSED_OPTIONS:
        return _PARSED_OPTIONS

    options = _parse_options_help_text(DEFAULT_HELP_TEXT)
    try:
        help_text   = _get_cmd_help_text()
        cmd_options = _parse_options_help_text(help_text)
        options.update(cmd_options)
    except NotImplementedError:
        # NOTE: no need to fail just for the options
        pass

    _PARSED_OPTIONS.update(options)
    return options
