#!/usr/bin/env python
# This file is part of the markdown-svgbob project
# https://gitlab.com/mbarkhau/markdown-svgbob
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
import os
import sys
import json
import typing as typ
import subprocess as sp

import markdown_svgbob


# To enable pretty tracebacks:
#   echo "export ENABLE_BACKTRACE=1;" >> ~/.bashrc
if os.environ.get('ENABLE_BACKTRACE') == '1':
    import backtrace

    backtrace.hook(align=True, strip_path=True, enable_on_envvar_only=True)


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
    import markdown_svgbob.wrapper as wrp

    print("Command options:")
    print(json.dumps(wrp.parse_options(), indent=4))
    print()

    svg_data = wrp.text2svg(TEST_IMAGE)
    if not svg_data:
        return 1

    with open("test.svg", mode="wb") as fh:
        fh.write(svg_data)

    print("Created test image to 'test.svg'")
    return 0


def main(args: typ.List[str] = sys.argv[1:]) -> ExitCode:
    """Basic wrapper around the svgbob command.

    This is mostly just used for self testing.
    """
    if "--markdown-svgbob-selftest" in args:
        return _selftest()

    if "--version" in args or "-V" in args:
        version = markdown_svgbob.__version__
        print("markdown-svgbob version: ", version)

    binpath = markdown_svgbob.get_bin_path()
    return sp.call([str(binpath)] + args)


if __name__ == '__main__':
    sys.exit(main())
