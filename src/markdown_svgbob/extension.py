# This file is part of the markdown-svgbob project
# https://gitlab.com/mbarkhau/markdown-svgbob
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
import re
import json
import base64
import typing as typ

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote  # type: ignore

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor

import markdown_svgbob.wrapper as wrapper

# TagType enumeration: inline_svg|img_utf8_svg|img_base64_svg
TagType = str


def svg2html(svg_data: bytes, tag_type: str = 'inline_svg') -> str:
    svg_data = svg_data.replace(b"\n", b"")
    if tag_type == 'img_base64_svg':
        img_b64_data: bytes = base64.standard_b64encode(svg_data)
        img_text = img_b64_data.decode('ascii')
        return f'<img class="bob" src="data:image/svg+xml;base64,{img_text}"/>'
    elif tag_type == 'img_utf8_svg':
        img_text = svg_data.decode("utf-8")
        img_text = quote(img_text)
        return f'<img class="bob" src="data:image/svg+xml;utf-8,{img_text}"/>'
    elif tag_type == 'inline_svg':
        return svg_data.decode("utf-8")
    else:
        err_msg = f"Invalid tag_type='{tag_type}'"
        raise NotImplementedError(err_msg)


def _clean_block_text(block_text: str) -> str:
    if block_text.startswith("```bob"):
        block_text = block_text[len("```bob") :]
    elif block_text.startswith("~~~bob"):
        block_text = block_text[len("~~~bob") :]

    if block_text.endswith("```"):
        block_text = block_text[: -len("```")]
    elif block_text.endswith("~~~"):
        block_text = block_text[: -len("~~~")]
    return block_text


# https://regex101.com/r/BQkg5t/2/
BG_STYLE_PATTERN = r"""
(
  rect\.backdrop\s*\{\s*fill:\s*white;
| \.bg_fill\s*\{\s*fill:\s*white;
)
"""
BG_STYLE_RE = re.compile(BG_STYLE_PATTERN.encode("ascii"), flags=re.VERBOSE)

FG_STYLE_PATTERN = r"""
(
  \.fg_stroke\s*\{\s*stroke:\s*black;
| \.fg_fill\s*\{\s*fill:\s*black;
| text\s*{\s*fill:\s*black;
)
"""
FG_STYLE_RE = re.compile(FG_STYLE_PATTERN.encode("ascii"), flags=re.VERBOSE)


def _postprocess_svg(svg_data: bytes, bg_color: str = None, fg_color: str = None) -> bytes:
    if bg_color:
        pos = 0
        while True:
            match = BG_STYLE_RE.search(svg_data, pos)
            if match is None:
                break

            repl = match.group(0).replace(b"white", bg_color.encode("ascii"))
            begin, end = match.span()
            pos      = end
            svg_data = svg_data[:begin] + repl + svg_data[end:]

    if fg_color:
        pos = 0
        while True:
            match = FG_STYLE_RE.search(svg_data, pos)
            if match is None:
                break

            repl = match.group(0).replace(b"black", fg_color.encode("ascii"))
            begin, end = match.span()
            pos      = end
            svg_data = svg_data[:begin] + repl + svg_data[end:]

    return svg_data


def draw_bob(block_text: str, default_options: wrapper.Options = None) -> str:
    options: wrapper.Options = {}

    if default_options:
        options.update(default_options)

    block_text = _clean_block_text(block_text)
    header, rest = block_text.split("\n", 1)
    if "{" in header and "}" in header:
        options.update(json.loads(header))
        block_text = rest

    tag_type = typ.cast(str, options.pop('tag_type', 'inline_svg'))

    bg_color = options.pop("bg_color", "")
    fg_color = options.pop("fg_color", "")
    if not isinstance(bg_color, str):
        bg_color = ""
    if not isinstance(fg_color, str):
        fg_color = ""

    svg_data = wrapper.text2svg(block_text, options)
    svg_data = _postprocess_svg(svg_data  , bg_color, fg_color)

    return svg2html(svg_data, tag_type=tag_type)


class SvgbobExtension(Extension):
    def __init__(self, **kwargs) -> None:
        self.config = {
            'tag_type': ["inline_svg", "Format to use (inline_svg|img_utf8_svg|img_base64_svg)"],
            'bg_color': ["white"     , "Set the background color"],
            'fg_color': ["black"     , "Set the foreground color"],
        }
        for name, options_text in wrapper.parse_options().items():
            self.config[name] = ["", options_text]

        self.images: typ.Dict[str, str] = {}
        super(SvgbobExtension, self).__init__(**kwargs)

    def reset(self) -> None:
        self.images.clear()

    def extendMarkdown(self, md, *args, **kwargs) -> None:
        preproc = SvgbobPreprocessor(md, self)
        md.preprocessors.register(preproc, name='svgbob_fenced_code_block', priority=50)

        postproc = SvgbobPostprocessor(md, self)
        md.postprocessors.register(postproc, name='svgbob_fenced_code_block', priority=0)
        md.registerExtension(self)


class SvgbobPreprocessor(Preprocessor):

    RE = re.compile(r"^(```|~~~)bob")

    def __init__(self, md, ext: SvgbobExtension) -> None:
        super(SvgbobPreprocessor, self).__init__(md)
        self.ext: SvgbobExtension = ext

    def run(self, lines: typ.List[str]) -> typ.List[str]:
        is_in_fence = False
        out_lines  : typ.List[str] = []
        block_lines: typ.List[str] = []

        default_options: wrapper.Options = {
            'tag_type': self.ext.getConfig('tag_type', 'inline_svg')
        }
        for name in self.ext.config.keys():
            val = self.ext.getConfig(name, "")
            if val != "":
                default_options[name] = val

        for line in lines:
            if is_in_fence:
                block_lines.append(line)
                if not ("```" in line or "~~~" in line):
                    continue

                is_in_fence = False
                block_text  = "\n".join(block_lines)
                del block_lines[:]
                img_tag  = draw_bob(block_text, default_options)
                img_id   = id(img_tag)
                marker   = f"<p id='svgbob{img_id}'>svgbob{img_id}</p>"
                tag_text = f"<p>{img_tag}</p>"
                out_lines.append(marker)
                self.ext.images[marker] = tag_text
            elif self.RE.match(line):
                is_in_fence = True
                block_lines.append(line)
            else:
                out_lines.append(line)

        return out_lines


class SvgbobPostprocessor(Postprocessor):
    def __init__(self, md, ext: SvgbobExtension) -> None:
        super(SvgbobPostprocessor, self).__init__(md)
        self.ext: SvgbobExtension = ext

    def run(self, text: str) -> str:
        for marker, img in self.ext.images.items():
            wrapped_marker = "<p>" + marker + "</p>"
            if wrapped_marker in text:
                text = text.replace(wrapped_marker, img)
            elif marker in text:
                text = text.replace(marker, img)

        return text
