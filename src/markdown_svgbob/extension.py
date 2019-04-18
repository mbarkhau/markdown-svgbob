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


def svg2img_uri(svg_data: bytes, encoding: str = 'base64') -> str:
    if encoding == 'base64':
        img_b64_data: bytes = base64.standard_b64encode(svg_data)
        img_text = img_b64_data.decode('ascii')
    elif encoding == 'utf-8':
        img_text = svg_data.decode("utf-8")
        img_text = quote(img_text.replace("\n", ""))
    else:
        err_msg = f"Invalid encoding='{encoding}'"
        raise NotImplementedError(err_msg)

    return f"data:image/svg+xml;{encoding},{img_text}"


def draw_svgbob(block_text: str, default_options: wrapper.Options = None) -> str:
    if block_text.startswith("```svgbob"):
        block_text = block_text[len("```svgbob") :]
    if block_text.endswith("```"):
        block_text = block_text[: -len("```")]

    header, rest = block_text.split("\n", 1)

    options: wrapper.Options = {}

    if default_options:
        options.update(default_options)

    if "{" in header and "}" in header:
        options.update(json.loads(header))
        block_text = rest

    data_uri_encoding = typ.cast(str, options.pop('data_uri_encoding', "base64"))

    svg_data = wrapper.text2svg(block_text, options)

    return svg2img_uri(svg_data, encoding=data_uri_encoding)


class SvgbobExtension(Extension):
    def __init__(self, **kwargs) -> None:
        self.config = {'format': ['svg', "Format to use (svg/png)"]}
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

    RE = re.compile(r"^```svgbob")

    def __init__(self, md, ext: SvgbobExtension) -> None:
        super(SvgbobPreprocessor, self).__init__(md)
        self.ext: SvgbobExtension = ext

    def run(self, lines: typ.List[str]) -> typ.List[str]:
        is_in_fence = False
        out_lines  : typ.List[str] = []
        block_lines: typ.List[str] = []

        default_options: wrapper.Options = {
            # output_fmt: str = self.ext.getConfig('format', 'svg')
        }

        for line in lines:
            if is_in_fence:
                block_lines.append(line)
                if "```" not in line:
                    continue

                is_in_fence = False
                block_text  = "\n".join(block_lines)
                del block_lines[:]
                img_uri    = draw_svgbob(block_text, default_options)
                img_uri_id = id(img_uri)
                marker     = f"<p id='svgbob{img_uri_id}'>svgbob{img_uri_id}</p>"
                tag_text   = f"<p><img src='{img_uri}' /></p>"
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
