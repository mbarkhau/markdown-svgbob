# Changelog for https://gitlab.com/mbarkhau/markdown-svgbob

## v202103.1015

 - Fix related to [#14](https://gitlab.com/mbarkhau/markdown-katex/-/issues/14): Since `Markdown>=3.3` support for [Markdown in HTML][md_in_html] was broken.

[md_in_html]: https://python-markdown.github.io/extensions/md_in_html/


## v202006.0015

 - Fix: `bg_color` not updated in some cases


## v202001.0013-beta

 - Fix #2: Ignore trailing whitespace after closing fence.


## v202001.0012-beta

 - Add: `min_char_width` option. Allows diagrams in a document to have a uniform scale.


## v202001.0011-beta

 - Fix: Bad image substitution when markdown has multiple diagrams


## v202001.0009-beta

 - Fix: Bad parsing of fences


## v201907.0008-beta

 - Fix: use PEP 508 environment marker to not always install the `typing` package. Fixes gitlab#1


## v201905.0007-beta

 - Add: `bg_color` and `fg_color` options


## v201905.0006-beta

 - Fix: better error reporting
 - Fix: cleanup temp dir


## v201904.0004-beta

 - Initial release
