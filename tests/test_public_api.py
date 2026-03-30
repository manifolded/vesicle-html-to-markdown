"""Public re-exports and low-level pipeline parity with html_to_markdown."""

from __future__ import annotations

from typing import get_args

from bs4 import BeautifulSoup

from html_to_markdown import (
    HtmlParser,
    conversion_children,
    convert_node,
    html_to_markdown,
    strip_non_content,
)


def test_public_api_imports() -> None:
    assert callable(strip_non_content)
    assert callable(conversion_children)
    assert callable(convert_node)
    assert set(get_args(HtmlParser)) == {"html.parser", "lxml"}


def test_low_level_pipeline_matches_html_to_markdown() -> None:
    html = "<p>Hello, <strong>world</strong>.</p>"
    parser: HtmlParser = "html.parser"
    soup = BeautifulSoup(html, parser)
    strip_non_content(soup)
    md = "".join(convert_node(c) for c in conversion_children(soup)).strip()
    assert md == html_to_markdown(html, parser=parser)
