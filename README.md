# [markdown-svgbob][repo_ref]

This is an extension for [Python Markdown](https://python-markdown.github.io/)
which renders diagrams using [svgbob](https://github.com/ivanceras/svgbob).

Project/Repo:

[![MIT License][license_img]][license_ref]
[![Supported Python Versions][pyversions_img]][pyversions_ref]
[![PyCalVer v201904.0001-alpha][version_img]][version_ref]
[![PyPI Version][pypi_img]][pypi_ref]
[![PyPI Downloads][downloads_img]][downloads_ref]

Code Quality/CI:

[![Build Status][build_img]][build_ref]
[![Type Checked with mypy][mypy_img]][mypy_ref]
[![Code Coverage][codecov_img]][codecov_ref]
[![Code Style: sjfmt][style_img]][style_ref]


|                 Name                |        role       |  since  | until |
|-------------------------------------|-------------------|---------|-------|
| Manuel Barkhau (mbarkhau@gmail.com) | author/maintainer | 2019-04 | -     |


## Install

```bash
$ pip install markdown-svgbob
$ pip install Pillow    # only for any format other than svg
```

The library currently only has built-in support for `x86_64-Linux`. If
you are on another platform, you will need to install rust and then svgbob via cargo. 

```bash
$ curl https://sh.rustup.rs -sSf | sh   # see https://rustup.rs/
$ cargo install svgbob_cli
```

## Use

In your markdown text you can define the block:

    ```svgbob
    ```

[repo_ref]: https://gitlab.com/mbarkhau/markdown-svgbob

[build_img]: https://gitlab.com/mbarkhau/markdown-svgbob/badges/master/pipeline.svg
[build_ref]: https://gitlab.com/mbarkhau/markdown-svgbob/pipelines

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

[version_img]: https://img.shields.io/static/v1.svg?label=PyCalVer&message=v201904.0001-alpha&color=blue
[version_ref]: https://pypi.org/project/pycalver/

[pyversions_img]: https://img.shields.io/pypi/pyversions/markdown-svgbob.svg
[pyversions_ref]: https://pypi.python.org/pypi/markdown-svgbob

