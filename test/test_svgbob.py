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

import re
from xml.sax.saxutils import unescape

from markdown import markdown

import markdown_svgbob
import markdown_svgbob.wrapper as wrp
import markdown_svgbob.extension as ext


BASIC_FIG_TXT = r"""
       .---.                      .
      /-o-/--         /\        .' `.
   .-/ / /->         /  \     .'     `.
  ( *  \/           '----'     `.   .'
   '-.  \                        `.'   ^ /
      \ /            ---->    | ^     / /
       '             <----    | |    / v
                              v |
 +------+   .------.    .------.    ^  \
 |      |   |      |   (        )    \  \
 +------+   '------'    '------'      \  v
   _______            ________
  /       \      /\   \       \
 /         \    /  \   )       )
 \         /    \  /  /_______/
  \_______/      \/
  .-----------.       .   <.      .>  .
 (             )     (      )    (     )
  '-----+ ,---'       `>   '      `  <'
        |/
""".strip(
    "\n"
)


BASIC_BLOCK_TXT = "```bob\n" + BASIC_FIG_TXT + "```"


OPTIONS_BLOCK_TXT = '```bob {"stroke-width": 4}\n' + BASIC_FIG_TXT + "```"


DEFAULT_MKDOCS_EXTENSIONS = ['meta', 'toc', 'tables', 'fenced_code']


EXTENDED_BLOCK_TXT = r"""
# Heading

prelude

```bob
{0}
```

postscript
"""

EXTENDED_BLOCK_TXT = EXTENDED_BLOCK_TXT.format(BASIC_FIG_TXT)


EXTENDED_HTML_TEMPLATE = r"""
<h1 id="heading">Heading</h1>
<p>prelude</p>
<p>{0}</p>
<p>postscript</p>
"""


HTMLTEST_TXT = """
# Heading

prelude

```bob {"tag_type":"img_utf8_svg"}
<figtxt>
```

interlude

```bob {"tag_type":"img_base64_svg", "stroke-width": 1.5}
<figtxt>
```

interlude

```bob {"tag_type":"inline_svg", "stroke-width": 2.5}
<figtxt>
```

postscript
"""

HTMLTEST_TXT = HTMLTEST_TXT.replace("<figtxt>", BASIC_FIG_TXT)


def test_regexp():
    assert ext.SvgbobPreprocessor.RE.match(BASIC_BLOCK_TXT)
    alt_block_text = BASIC_BLOCK_TXT.replace("```", "~~~")
    assert ext.SvgbobPreprocessor.RE.match(alt_block_text)


def test_determinism_svg():
    fig_data1 = markdown_svgbob.text2svg(BASIC_FIG_TXT)
    fig_data2 = markdown_svgbob.text2svg(BASIC_FIG_TXT)
    assert fig_data1 == fig_data2


def test_basic_svg():
    fig_data = markdown_svgbob.text2svg(BASIC_FIG_TXT)

    # with open("debug_img_output_svgbob.svg", mode='wb') as fh:
    #     fh.write(fig_data)

    assert b"<svg" in fig_data
    assert b"</svg>" in fig_data

    inline_svg     = ext.draw_bob(BASIC_BLOCK_TXT, default_options={'tag_type': "inline_svg"})
    default_output = ext.draw_bob(BASIC_BLOCK_TXT)
    assert inline_svg == default_output
    assert inline_svg
    assert inline_svg.startswith("<svg")
    expected = "<p>{}</p>".format(inline_svg)

    assert "xmlns" in inline_svg

    result = markdown(BASIC_BLOCK_TXT, extensions=['markdown_svgbob'])

    assert inline_svg in result

    assert result == expected


def test_encoding():
    html_tag = ext.draw_bob(BASIC_BLOCK_TXT, default_options={'tag_type': "inline_svg"})
    assert "xmlns" in html_tag
    assert "<svg" in html_tag
    assert "%3Csvg" not in html_tag
    assert "svg+xml;base64" not in html_tag
    assert "svg+xml;utf-8" not in html_tag
    assert "<img" not in html_tag

    html_tag = ext.draw_bob(BASIC_BLOCK_TXT, default_options={'tag_type': "img_base64_svg"})
    assert "xmlns" not in html_tag
    assert "<svg" not in html_tag
    assert "%3Csvg" not in html_tag
    assert "svg+xml;base64" in html_tag
    assert "svg+xml;utf-8" not in html_tag
    assert '<img class="bob" src=' in html_tag

    html_tag = ext.draw_bob(BASIC_BLOCK_TXT, default_options={'tag_type': "img_utf8_svg"})
    assert "xmlns" in html_tag
    assert "<svg" not in html_tag
    assert "%3Csvg" in html_tag
    assert "svg+xml;base64" not in html_tag
    assert "svg+xml;utf-8" in html_tag
    assert '<img class="bob" src=' in html_tag


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

    html_tag = ext.draw_bob(OPTIONS_BLOCK_TXT)
    expected = "<p>{}</p>".format(html_tag)

    assert result == expected


def test_svgbob_config():
    result = markdown(
        BASIC_BLOCK_TXT,
        extensions=['markdown_svgbob'],
        extension_configs={'markdown_svgbob': {'stroke-width': 3}},
    )

    html_tag   = ext.draw_bob(BASIC_BLOCK_TXT)
    unexpected = "<p>{}</p>".format(html_tag)
    assert result != unexpected

    html_tag = ext.draw_bob(BASIC_BLOCK_TXT, {'stroke-width': 3})
    expected = "<p>{}</p>".format(html_tag)

    assert result == expected


def test_extended_svgbob():
    extensions = DEFAULT_MKDOCS_EXTENSIONS + ['markdown_svgbob']
    result     = markdown(EXTENDED_BLOCK_TXT, extensions=extensions)

    html_tag = ext.draw_bob(BASIC_BLOCK_TXT)
    expected = EXTENDED_HTML_TEMPLATE.format(html_tag)
    expected = expected.replace("\n", "")
    result   = result.replace("\n", "")

    assert result == expected


def test_options_parsing():
    default_options = wrp._parse_options_help_text(wrp.DEFAULT_HELP_TEXT)

    expected_option_keys = {"font-family", "font-size", "scale", "stroke-width"}
    assert set(default_options.keys()) == expected_option_keys

    cmd_help_text = wrp._get_cmd_help_text()
    cmd_options   = wrp._parse_options_help_text(cmd_help_text)

    assert set(cmd_options.keys()) >= expected_option_keys

    options = wrp.parse_options()
    assert set(options.keys()) >= expected_option_keys

    assert "output" not in options


def test_postproc():
    html_tag = ext.draw_bob(BASIC_BLOCK_TXT, {'tag_type': "img_base64_svg"})
    assert '<img class="bob"' in html_tag
    html_tag = ext.draw_bob(BASIC_BLOCK_TXT)

    assert '<svg class="bob"' in html_tag
    assert re.search(r"\.bg_fill\s*\{\s*fill:\s*white;", html_tag)
    assert re.search(r"\.fg_fill\s*\{\s*fill:\s*black;", html_tag)

    html_tag = ext.draw_bob(BASIC_BLOCK_TXT, {'bg_color': "black", 'fg_color': "white"})

    assert '<svg class="bob"' in html_tag
    assert re.search(r"\.bg_fill\s*\{\s*fill:\s*black;", html_tag)
    assert re.search(r"\.fg_fill\s*\{\s*fill:\s*white;", html_tag)


def test_bin_paths():
    assert wrp._get_pkg_bin_path().exists()
    assert wrp._get_pkg_bin_path(machine="x86_64", osname="Windows").exists()
    assert wrp._get_pkg_bin_path(machine="AMD64", osname="Windows").exists()
    assert wrp._get_pkg_bin_path(machine="x86_64", osname="Linux").exists()
    assert wrp._get_pkg_bin_path(machine="x86_64", osname="Darwin").exists()


def test_html_output():
    # NOTE: This generates html that is to be tested
    #   in the browser (for warnings in devtools).
    extensions = DEFAULT_MKDOCS_EXTENSIONS + ['markdown_svgbob']
    result     = markdown(HTMLTEST_TXT, extensions=extensions)
    with open("/tmp/svgbob.html", mode="w") as fh:
        fh.write(result)
