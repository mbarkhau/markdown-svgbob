# `pylint-ignore`

**WARNING: This file is programatically generated.**

This file is parsed by `pylint-ignore` to determine which `pylint`
messages should be ignored.

- Do not edit this file manually.
- To update, use `pylint-ignore --update-ignorefile`

The recommended approach to using `pylint-ignore` is:

1. If a message refers to a valid issue, update your code rather than
   ignoring the message.
2. If a message should *always* be ignored (globally), then to do so
   via the usual `pylintrc` or `setup.cfg` files rather than this
   `pylint-ignore.md` file.
3. If a message is a false positive, add a comment of this form to your code:
   `# pylint:disable=<symbol> ; explain why this is a false positive`


## File src/markdown_svgbob/wrapper.py - Line 119 - R0914 (too-many-locals)

- `message: Too many local variables (23/20)`
- `author : Manuel Barkhau <mbarkhau@gmail.com>`
- `date   : 2020-07-21T20:57:45`

```
  117:
  118:
> 119: def text2svg(image_text: str, options: Options = None) -> bytes:
  120:     binpath   = get_bin_path()
  121:     cmd_parts = [str(binpath)]
```

