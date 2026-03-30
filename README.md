# vesicle-html-to-markdown

Small Python library that turns HTML strings into Markdown.

## Requirements

- Python 3.9+
- [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/) (see [`pyproject.toml`](pyproject.toml))
- **lxml** is installed by default; parsing defaults to the standard-library ``html.parser``. Pass ``parser="lxml"`` if you want the lxml backend instead.

## Installation

From the repository root (with a virtual environment activated):

```bash
pip install .
```

For an editable install while developing:

```bash
pip install -e .
```

The importable package name is `html_to_markdown` (the PyPI-style distribution name is `vesicle-html-to-markdown`).

## Usage

```python
from html_to_markdown import html_to_markdown

md = html_to_markdown("<p>Hello, <strong>world</strong>.</p>")
print(md)

# Optional: use lxml as the Beautiful Soup backend
md = html_to_markdown("<p>Hello</p>", parser="lxml")
```

Input is parsed **as-is** with Beautiful Soup (no synthetic wrapper). The default is ``parser="html.parser"``; pass ``parser="lxml"`` to use lxml instead. Tree shape and whitespace can differ slightly between parsers. Conversion walks **`body`** when it exists; otherwise **`html`** children, otherwise top-level soup nodes (skipping doctypes). That covers full documents and typical fragments the parser normalizes under `html` / `body`.

### Composable conversion (low-level API)

You can mirror ``html_to_markdown`` with the same building blocks the library uses internally:

```python
from bs4 import BeautifulSoup

from html_to_markdown import (
    HtmlParser,
    conversion_children,
    convert_node,
    strip_non_content,
)

html = "<p>Hello, <strong>world</strong>.</p>"
parser: HtmlParser = "html.parser"
soup = BeautifulSoup(html, parser)
strip_non_content(soup)
md = "".join(convert_node(child) for child in conversion_children(soup)).strip()
```

- ``strip_non_content`` mutates the soup in place (remove scripts, styles, head, etc.).
- ``conversion_children`` takes a **``BeautifulSoup``** instance only (not an arbitrary element tag as root).
- ``convert_node`` accepts Beautiful Soup **tree nodes** (strings or tags), including a tag root if you want one subtree as markdown.
- ``HtmlParser`` is exported for type hints on ``parser`` when calling ``BeautifulSoup(..., parser=...)``.

### Stripped markup

Before conversion, non-visible or non-body markup is removed so it does not leak into Markdown (for example CSS in `<style>` or metadata in `<head>`):

- **Removed:** `script`, `style`, `noscript`, `template`, `head`, `meta`, `link`, `base`, and `title`.

## Supported elements

Rough mapping from HTML to Markdown:

| HTML | Markdown |
|------|----------|
| `h1`–`h6` | ATX headings (`#` … `######`) |
| `p` | Paragraphs (blank line after) |
| `strong`, `b` | `**bold**` |
| `em`, `i` | `*italic*` |
| `code` | Inline `` `code` `` |
| `pre` (+ optional `code.language-*`) | Fenced code blocks |
| `ul` / `ol` | `-` / numbered list items |
| `blockquote` | `>` lines |
| `a` | `[text](href)` |
| `img` | `![alt](src)` |
| `br` | Newline |

Other tags have their children emitted without a specific wrapper when possible.

## Testing

```bash
pip install -e ".[dev]"
pytest
```

## Building

This project uses [Hatchling](https://hatch.pypa.io/latest/) as the build backend. To produce a wheel:

```bash
pip install build
python -m build --wheel
```

## License

[MIT](LICENSE).
