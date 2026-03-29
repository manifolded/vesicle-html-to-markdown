# vesicle-html-to-markdown

Small Python library that turns HTML strings into Markdown.

## Requirements

- Python 3.9+
- [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/) (declared in `pyproject.toml`)

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
```

Input is parsed as an HTML fragment: it is wrapped for parsing, then the outer wrapper is not part of the logical document you pass in—only your markup is converted.

### Stripped markup

Before conversion, non-visible or non-body markup is removed so it does not leak into Markdown (for example CSS in `<style>` or metadata in `<head>`):

- **Removed:** `script`, `style`, `noscript`, `template`, `head` (after titles are handled), `meta`, `link`, `base`
- **Preserved:** `<title>` text from `<head>` is moved to the start of the fragment and emitted as a level-1 heading (`# …`), same as a document title in Markdown.

## Supported elements

Rough mapping from HTML to Markdown:

| HTML | Markdown |
|------|----------|
| `h1`–`h6` | ATX headings (`#` … `######`) |
| `title` | Level-1 heading (`#` …); titles from `<head>` appear first |
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
