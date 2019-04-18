#!/usr/bin/env python
# This file is part of the markdown-svgbob project
# https://gitlab.com/mbarkhau/markdown-svgbob
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
import os
import sys
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
    svg_data = markdown_svgbob.text2svg(TEST_IMAGE)
    if not svg_data:
        return 1

    with open("test.svg", mode="wb") as fh:
        fh.write(svg_data)

    print("Created test image to 'test.svg'")
    return 0


def main(args=sys.argv[1:]) -> ExitCode:
    """Basic wrapper around the svgbob command.

    This is mostly just used for self testing.
    """
    if "--pysvgbob-selftest" in args:
        return _selftest()

    if "--version" in args or "-V" in args:
        print(f"markdown-svgbob version: ", markdown_svgbob.__version__)

    binpath = markdown_svgbob.get_svgbob_bin_path()
    return sp.call([binpath] + args)


if __name__ == '__main__':
    sys.exit(main())
