# -*- coding: utf-8 -*-
# This file is part of markdown-svgbob.
# https://gitlab.com/mbarkhau/markdown-svgbob
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from xml.sax.saxutils import unescape

from markdown import markdown
import markdown_svgbob
import markdown_svgbob.wrapper
import markdown_svgbob.extension as ext

import pytest


BASIC_FIG_TXT = r"""
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
""".strip()


BASIC_BLOCK_TXT = "```svgbob\n" + BASIC_FIG_TXT + "```"


OPTIONS_BLOCK_TXT = '```svgbob {"stroke-width": 4}\n' + BASIC_FIG_TXT + "```"


DEFAULT_MKDOCS_EXTENSIONS = ['meta', 'toc', 'tables', 'fenced_code']


EXTENDED_BLOCK_TXT = """
# Heading

prelude

```svgbob
{}
```

postscript
""".format(BASIC_FIG_TXT)


EXTENDED_HTML_TEMPLATE = r"""
<h1 id="heading">Heading</h1>
<p>prelude</p>
<p><img src='{}' /></p>
<p>postscript</p>
"""


def test_regexp():
    assert ext.SvgbobPreprocessor.RE.match(BASIC_BLOCK_TXT)


def test_basic_svg():
    fig_data = markdown_svgbob.text2svg(BASIC_FIG_TXT)

    # with open("debug_img_output_svgbob.svg", mode='wb') as fh:
    #     fh.write(fig_data)

    assert b"<svg" in fig_data
    assert b"</svg>" in fig_data

    img_uri = ext.draw_svgbob(BASIC_BLOCK_TXT)
    assert img_uri.startswith("data:image/svg+xml;base64,")
    expected = "<p><img src='{}' /></p>".format(img_uri)

    result = markdown(BASIC_BLOCK_TXT, extensions=['markdown_svgbob'])

    assert img_uri in result

    assert result == expected


def test_determinism_svg():
    fig_data1 = markdown_svgbob.text2svg(BASIC_FIG_TXT)
    fig_data2 = markdown_svgbob.text2svg(BASIC_FIG_TXT)
    assert fig_data1 == fig_data2


def test_svgbob_options():
    fig_data_default = markdown_svgbob.text2svg(BASIC_FIG_TXT)
    assert b"stroke-width: 2" in fig_data_default
    assert b"stroke-width: 4" not in fig_data_default

    options  = {'stroke-width': 4}
    fig_data = markdown_svgbob.text2svg(BASIC_FIG_TXT, options)
    assert b"stroke-width: 2" not in fig_data
    assert b"stroke-width: 4" in fig_data

    assert b"<svg" in fig_data
    assert b"</svg>" in fig_data

    result = markdown(OPTIONS_BLOCK_TXT, extensions=['markdown_svgbob'])

    img_uri  = ext.draw_svgbob(OPTIONS_BLOCK_TXT)
    expected = "<p><img src='{}' /></p>".format(img_uri)

    assert result == expected


def test_extended_svgbob():
    extensions = DEFAULT_MKDOCS_EXTENSIONS + ['markdown_svgbob']
    result     = markdown(EXTENDED_BLOCK_TXT, extensions=extensions)

    img_uri  = ext.draw_svgbob(BASIC_BLOCK_TXT)
    expected = EXTENDED_HTML_TEMPLATE.format(img_uri)
    expected = expected.replace("\n", "")
    result   = result.replace("\n", "")

    assert result == expected


def test_options_parsing():
    wrp = markdown_svgbob.wrapper

    default_options = wrp._parse_options_help_text(wrp.DEFAULT_HELP_TEXT)

    expected_option_keys = {"font-family", "font-size", "scale", "stroke-width"}
    assert set(default_options.keys()) == expected_option_keys

    cmd_help_text = wrp._get_cmd_help_text()
    cmd_options   = wrp._parse_options_help_text(cmd_help_text)

    assert set(cmd_options.keys()) >= expected_option_keys

    options = wrp.parse_options()
    assert set(options.keys()) >= expected_option_keys

    assert "output" not in options