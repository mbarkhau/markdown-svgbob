<div align="center">
<p align="center">
  <img alt="logo" src="https://gitlab.com/mbarkhau/markdown-svgbob/-/raw/master/logo.png">
</p>
</div>


# [markdown-svgbob][repo_ref]

This is an extension for [Python Markdown](https://python-markdown.github.io/)
which renders diagrams using [svgbob](https://github.com/ivanceras/svgbob).

You can try it out using the [Svgbob Editor](https://ivanceras.github.io/svgbob-editor/)
or the [AsciiGrid Editor](https://asciigrid.litprog.dev).

Project/Repo:

[![MIT License][license_img]][license_ref]
[![Supported Python Versions][pyversions_img]][pyversions_ref]
[![CalVer v202406.1023][version_img]][version_ref]
[![PyPI Version][pypi_img]][pypi_ref]
[![PyPI Downloads][downloads_img]][downloads_ref]

Code Quality/CI:

[![GitHub CI Status][github_build_img]][github_build_ref]
[![GitLab CI Status][gitlab_build_img]][gitlab_build_ref]
[![Type Checked with mypy][mypy_img]][mypy_ref]
[![Code Coverage][codecov_img]][codecov_ref]
[![Code Style: sjfmt][style_img]][style_ref]


|                 Name                |        role       |  since  | until |
|-------------------------------------|-------------------|---------|-------|
| Manuel Barkhau (mbarkhau@gmail.com) | author/maintainer | 2019-04 | -     |


## Install

```bash
$ pip install markdown-svgbob
```

This package includes the following binaries:

 - `svgbob_0.5.5_x86_64-Darwin`
 - `svgbob_0.5.5_x86_64-Linux`
 - `svgbob_0.5.5_x86_64-Windows.exe`

If you are on another platform, or want to use a more recent version of `svgbob_cli`, you will need to install rust and then svgbob via cargo.

```bash
$ curl https://sh.rustup.rs -sSf | sh   # see https://rustup.rs/
$ cargo install svgbob_cli
```

This extension will always use the installed version of svgbob if it is available.


## Usage

In your markdown text you can define the block:

    ```bob
         .---.
        /-o-/--
     .-/ / /->
    ( *  \/
     '-.  \
        \ /
         '
    ```

The info string `bob` is chosen to match [spongedown](https://github.com/ivanceras/spongedown).


## Development/Testing

```bash
$ git clone https://github.com/mbarkhau/markdown-svgbob
$ cd markdown-svgbob
$ make conda
$ make lint mypy test
```


## MkDocs Integration

In your `mkdocs.yml` add this to markdown_extensions.

```yaml
markdown_extensions:
  - markdown_svgbob:
      tag_type: inline_svg
      bg_color: white
      fg_color: black
      min_char_width: 80
```

Valid options for `tag_type` are `inline_svg` (the default), `img_utf8_svg` and `img_base64_svg`.

The option `min_char_width` allows you to create diagrams of a uniform scale.


[repo_ref]: https://github.com/mbarkhau/markdown-svgbob

[github_build_img]: https://github.com/mbarkhau/markdown-svgbob/workflows/CI/badge.svg
[github_build_ref]: https://github.com/mbarkhau/markdown-svgbob/actions?query=workflow%3ACI

[gitlab_build_img]: https://gitlab.com/mbarkhau/markdown-svgbob/badges/master/pipeline.svg
[gitlab_build_ref]: https://gitlab.com/mbarkhau/markdown-svgbob/pipelines

[codecov_img]: https://gitlab.com/mbarkhau/markdown-svgbob/badges/master/coverage.svg
[codecov_ref]: https://mbarkhau.gitlab.io/markdown-svgbob/cov

[license_img]: https://img.shields.io/badge/License-MIT-blue.svg
[license_ref]: https://gitlab.com/mbarkhau/markdown-svgbob/blob/master/LICENSE

[mypy_img]: https://img.shields.io/badge/mypy-checked-green.svg
[mypy_ref]: https://mbarkhau.gitlab.io/markdown-svgbob/mypycov

[style_img]: https://img.shields.io/badge/code%20style-%20sjfmt-f71.svg
[style_ref]: https://gitlab.com/mbarkhau/straitjacket/

[pypi_img]: https://img.shields.io/badge/PyPI-wheels-green.svg
[pypi_ref]: https://pypi.org/project/markdown-svgbob/#files

[downloads_img]: https://pepy.tech/badge/markdown-svgbob/month
[downloads_ref]: https://pepy.tech/project/markdown-svgbob

[version_img]: https://img.shields.io/static/v1.svg?label=CalVer&message=v202406.1023&color=blue
[version_ref]: https://pypi.org/project/bumpver/

[pyversions_img]: https://img.shields.io/pypi/pyversions/markdown-svgbob.svg
[pyversions_ref]: https://pypi.python.org/pypi/markdown-svgbob

