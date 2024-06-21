#!/usr/bin/env python
# This file is part of the markdown-svgbob project
# https://github.com/mbarkhau/markdown-svgbob
#
# Copyright (c) 2019-2024 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
import os
import sys
import json
import typing as typ
import subprocess as sp

import markdown_svgbob

# To enable pretty tracebacks:
#   echo "export ENABLE_RICH_TB=1;" >> ~/.bashrc
if os.environ.get('ENABLE_RICH_TB') == '1':
    try:
        import rich.traceback

        rich.traceback.install()
    except ImportError:
        # don't fail just because of missing dev library
        pass


TEST_IMAGE = r"""
 +------+   .------.    .------.      /\        .' `.
 |      |   |      |   (        )    /  \     .'     `.
 +------+   '------'    '------'    '----'     `.   .'
   _______            ________                   `.'   ^ /
  /       \      /\   \       \      ---->    | ^     / /
 /         \    /  \   )       )     <----    | |    / v
 \         /    \  /  /_______/               v |
  \_______/      \/
  .-----------.       .   <.      .>  .          ^  \
 (             )     (      )    (     )          \  \
  '-----+ ,---'       `>   '      `  <'            \  v
        |/

"""


ExitCode = int


def _selftest() -> ExitCode:
    # pylint:disable=import-outside-toplevel  ; lazy import to improve cli responsiveness
    import markdown_svgbob.wrapper as wrp

    print("Command options:")
    print(json.dumps(wrp.parse_options(), indent=4))
    print()

    svg_data = wrp.text2svg(TEST_IMAGE)
    if not svg_data:
        return 1

    with open("test.svg", mode="wb") as fobj:
        fobj.write(svg_data)

    print("Created test image to 'test.svg'")
    return 0


def main(args: typ.Sequence[str] = sys.argv[1:]) -> ExitCode:
    """Basic wrapper around the svgbob command.

    This is mostly just used for self testing.
    """
    # pylint:disable=dangerous-default-value   ; mypy will detect if we mutate args
    if "--markdown-svgbob-selftest" in args:
        return _selftest()

    if "--version" in args or "-V" in args:
        version = markdown_svgbob.__version__
        print("markdown-svgbob version: ", version)

    binpath = markdown_svgbob.get_bin_path()
    return sp.check_call([str(binpath)] + list(args))


if __name__ == '__main__':
    sys.exit(main())
