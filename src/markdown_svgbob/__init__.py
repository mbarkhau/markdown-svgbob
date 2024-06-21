# This file is part of the markdown-svgbob project
# https://github.com/mbarkhau/markdown-svgbob
#
# Copyright (c) 2019-2024 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
"""markdown_svgbob extension.

This is an extension for Python-Markdown which
uses svgbob to generate images from ascii
diagrams in fenced code blocks.
"""

__version__ = "v202406.1023"


from markdown_svgbob.wrapper import text2svg
from markdown_svgbob.wrapper import get_bin_path
from markdown_svgbob.extension import SvgbobExtension

get_svgbob_bin_path = get_bin_path


def _make_extension(**kwargs) -> SvgbobExtension:
    return SvgbobExtension(**kwargs)


# Name that conforms with the Markdown extension API
# https://python-markdown.github.io/extensions/api/#dot_notation
makeExtension = _make_extension


__all__ = ['makeExtension', '__version__', 'get_bin_path', 'get_svgbob_bin_path', 'text2svg']
