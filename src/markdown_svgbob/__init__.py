# This file is part of the markdown-svgbob project
# https://gitlab.com/mbarkhau/markdown-svgbob
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
"""markdown_svgbob extension.

This is an extension for Python-Markdown which
uses svgbob to generate images from ascii
diagrams in fenced code blocks.
"""

__version__ = "v201905.0007-beta"


from markdown_svgbob.extension import SvgbobExtension
from markdown_svgbob.wrapper import text2svg, get_bin_path

get_svgbob_bin_path = get_bin_path


def makeExtension(**kwargs) -> SvgbobExtension:
    return SvgbobExtension(**kwargs)


__all__ = ['makeExtension', '__version__', 'get_bin_path', 'get_svgbob_bin_path', 'text2svg']
