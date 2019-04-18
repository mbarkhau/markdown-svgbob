# This file is part of the markdown-svgbob project
# https://gitlab.com/mbarkhau/markdown-svgbob
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
"""markdown_svgbob extension.

This is an extension for the python Markdown
libarary which uses svgbob to generate images
from ascii diagrams in fenced code blocks.
"""

import os
import platform
import typing as typ
import pathlib2 as pl
import subprocess as sp


__version__ = "v201904.0001-alpha"


LIBDIR: pl.Path = pl.Path(__file__).parent
PKG_BIN_DIR     = LIBDIR / "bin"
DEFAULT_BIN_DIR = pl.Path("~") / ".cargo" / "bin"
DEFAULT_BIN_DIR = DEFAULT_BIN_DIR.expanduser()


def _get_usr_bin_path() -> typ.Optional[pl.Path]:
    env_path = os.environ.get('PATH')
    if env_path is None:
        env_paths = [DEFAULT_BIN_DIR]
    else:
        env_paths = [pl.Path(path_str) for path_str in env_path.split(os.pathsep)]

    for path in env_paths:
        local_bin = path / "svgbob"
        if local_bin.exists():
            return local_bin

        local_bin = path / "svgbob.exe"
        if local_bin.exists():
            return local_bin

    return None


def _get_pkg_bin_path() -> pl.Path:
    osname  = platform.system()
    machine = platform.machine()

    bin_fname = f"svgbob_{machine}-{osname}"
    bin_fpath = PKG_BIN_DIR / bin_fname
    if bin_fpath.exists():
        return bin_fpath

    err_msg = (
        f"Platform not supported, "
        f"svgbob binary not found {bin_fpath}. "
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
    while True:
        output = proc.stdout.readline()
        if output:
            yield output
        else:
            return


def text2svg(image_text: str) -> bytes:
    binpath    = get_svgbob_bin_path()
    image_data = image_text.encode("utf-8")
    cmd_parts  = [binpath]
    proc       = sp.Popen(
        cmd_parts,
        stdin=sp.PIPE,
        stdout=sp.PIPE,
        # stderr=sp.PIPE,
    )
    proc.stdin.write(image_data)
    proc.stdin.close()
    return b"".join(read_output(proc))
