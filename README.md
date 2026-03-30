# vesicle-html-to-markdown

Small Python library that turns HTML strings into Markdown.

## Requirements

- Python 3.9+
- [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/) with the **lxml** parser (see [`pyproject.toml`](pyproject.toml))

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

Input is parsed **as-is** with Beautiful Soup using the **lxml** parser (no synthetic wrapper). Conversion walks **`body`** when it exists; otherwise **`html`** children, otherwise top-level soup nodes (skipping doctypes). That covers full documents and typical fragments the parser normalizes under `html` / `body`.

### Stripped markup

Before conversion, non-visible or non-body markup is removed so it does not leak into Markdown (for example CSS in `<style>` or metadata in `<head>`):

- **Removed:** `script`, `style`, `noscript`, `template`, `head`, `meta`, `link`, `base`, and any remaining `title` tags after the document title is handled.
- **Document title:** The **first** `<title>` inside `<head>` may be prepended as `# …` plus a blank line when its content is **plain text only** (no nested elements) and non-empty after whitespace normalization. Otherwise no title line is added.

## Supported elements

Rough mapping from HTML to Markdown:

| HTML | Markdown |
|------|----------|
| `h1`–`h6` | ATX headings (`#` … `######`) |
| `title` | Not emitted as a tag; first `<title>` in `<head>` may become a leading `# …` line (plain text only) |
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
