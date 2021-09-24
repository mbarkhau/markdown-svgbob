# -*- coding: utf-8 -*-
# This file is part of markdown-svgbob.
# https://github.com/mbarkhau/markdown-svgbob
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT

# pytest fixtures work this way
# pylint: disable=redefined-outer-name
# for wrp._get_pkg_bin_path
# pylint: disable=protected-access

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import re
import textwrap

import markdown as md

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


BASIC_BLOCK_TXT = "```bob\n" + BASIC_FIG_TXT + "\n```"


OPTIONS_BLOCK_TXT = '```bob {"stroke-width": 4}\n' + BASIC_FIG_TXT + "\n```"


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
    block_texts = [
        BASIC_BLOCK_TXT,
        BASIC_BLOCK_TXT.replace("```", "~~~"),
        BASIC_BLOCK_TXT.replace("```", "~~~~"),
        BASIC_BLOCK_TXT.replace("```", "````"),
    ]

    for block_text in block_texts:
        assert ext.BLOCK_START_RE.match(block_text)
        assert ext.BLOCK_CLEAN_RE.match(block_text)


def test_determinism_svg():
    fig_data1 = markdown_svgbob.text2svg(BASIC_FIG_TXT)
    fig_data2 = markdown_svgbob.text2svg(BASIC_FIG_TXT)
    assert fig_data1 == fig_data2


def test_basic_svg():
    fig_data = markdown_svgbob.text2svg(BASIC_FIG_TXT)

    # with open("debug_img_output_svgbob.svg", mode='wb') as fobj:
    #     fobj.write(fig_data)

    assert b"<svg" in fig_data
    assert b"</svg>" in fig_data

    inline_svg     = ext.draw_bob(BASIC_BLOCK_TXT, default_options={'tag_type': "inline_svg"})
    default_output = ext.draw_bob(BASIC_BLOCK_TXT)
    assert inline_svg == default_output
    assert inline_svg
    assert inline_svg.startswith("<svg")
    expected = "<p>{}</p>".format(inline_svg)

    assert "xmlns" in inline_svg

    result = md.markdown(BASIC_BLOCK_TXT, extensions=['markdown_svgbob'])

    assert inline_svg in result

    assert result == expected


def test_trailing_whitespace():
    default_output = ext.draw_bob(BASIC_BLOCK_TXT)

    trailing_space_result = md.markdown(BASIC_BLOCK_TXT + "  ", extensions=['markdown_svgbob'])
    assert default_output in trailing_space_result
    assert "```" not in trailing_space_result


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
    fig_text_default = fig_data_default.decode("utf-8")

    assert re.search(r"stroke-width:\s*2", fig_text_default)
    assert not re.search(r"stroke-width:\s*4", fig_text_default)

    options  = {'stroke-width': 4}
    fig_data = markdown_svgbob.text2svg(BASIC_FIG_TXT, options)
    fig_text = fig_data.decode("utf-8")

    assert not re.search(r"stroke-width:\s*2", fig_text)
    assert re.search(r"stroke-width:\s*4", fig_text)

    assert "<svg" in fig_text
    assert "</svg>" in fig_text

    result = md.markdown(OPTIONS_BLOCK_TXT, extensions=['markdown_svgbob'])

    html_tag = ext.draw_bob(OPTIONS_BLOCK_TXT)
    expected = "<p>{}</p>".format(html_tag)

    assert result == expected


def test_svgbob_config():
    result = md.markdown(
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
    result     = md.markdown(EXTENDED_BLOCK_TXT, extensions=extensions)

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

    # TODO (mb 2021-07-22): brittle test, perhaps switch to image diff
    #   based testing.
    return

    assert '<svg class="bob"' in html_tag

    assert re.search(r"\.bg_fill\s*\{\s*fill:\s*white;", html_tag)
    # NOTE (mb 2020-06-05): Some versions of svgbob produce
    #   a backdrop rect with a class, some with an inline fill.
    backdrop_rect = re.search(r'</style>\s*<rect\s+fill="white"', html_tag) or (
        re.search(r'</style>\s*<rect\s+class="backdrop"', html_tag)
        and re.search(r"rect\.backdrop\s*\{\s*fill:\s*white", html_tag)
    )
    assert backdrop_rect
    assert re.search(r"\.fg_fill\s*\{\s*fill:\s*black;", html_tag)

    html_tag = ext.draw_bob(BASIC_BLOCK_TXT, {'bg_color': "red", 'fg_color': "green"})

    assert '<svg class="bob"' in html_tag
    assert re.search(r"\.bg_fill\s*\{\s*fill:\s*red;", html_tag)
    backdrop_rect = re.search(r'</style>\s*<rect\s+fill="red"', html_tag) or (
        re.search(r'</style>\s*<rect\s+class="backdrop"', html_tag)
        and re.search(r"rect\.backdrop\s*\{\s*fill:\s*red", html_tag)
    )
    assert backdrop_rect
    assert re.search(r"\.fg_fill\s*\{\s*fill:\s*green;", html_tag)


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
    result     = md.markdown(
        HTMLTEST_TXT,
        extensions=extensions,
        extension_configs={'markdown_svgbob': {'min_char_width': "60"}},
    )
    with io.open("/tmp/svgbob.html", mode="w", encoding="utf-8") as fobj:
        fobj.write(result)


def test_ignore_non_bob_blocks():
    md_text = textwrap.dedent(
        r"""
        Look at this literal asciiart:

        ```
        Literal asciiart
               .---.
              /-o-/--
           .-/ / /->
          ( *  \/
           '-.  \
              \ /
               '
        ```

        And also this code:

        ```python
        def randint() -> int:
            return 4
        ```

        And this code:

        ~~~javascript
        function randint() {
            return 4;
        }
        ~~~
        """
    )
    result_a = md.markdown(
        md_text,
        extensions=DEFAULT_MKDOCS_EXTENSIONS + ['markdown_svgbob'],
    )
    result_b = md.markdown(
        md_text,
        extensions=DEFAULT_MKDOCS_EXTENSIONS,
    )
    assert "bob" not in result_a
    assert "bob" not in result_b

    assert result_a == result_b
    assert "<pre><code>Literal asciiart" in result_a
    assert re.search(r'<pre><code class="(language-)?python">def randint', result_a)
    assert re.search(r'<pre><code class="(language-)?javascript">function randint', result_a)
