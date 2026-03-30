"""Baseline tests for current html_to_markdown behavior (pre parse-as-is refactor)."""

from __future__ import annotations

import pytest

from html_to_markdown import html_to_markdown


def test_paragraph_and_inline_strong() -> None:
    # Whitespace-only text nodes are dropped; trailing newlines removed by final .strip().
    assert html_to_markdown("<p>Hello, <strong>world</strong>.</p>") == "Hello,**world**."


def test_two_paragraphs() -> None:
    out = html_to_markdown("<p>First</p><p>Second</p>")
    assert out == "First\n\nSecond"


def test_empty_input() -> None:
    assert html_to_markdown("") == ""


def test_plain_text_fragment() -> None:
    assert html_to_markdown("Hello") == "Hello"


def test_head_and_style_stripped() -> None:
    html = (
        "<html><head>"
        '<title>My Page</title>'
        "<style>body { color: red; } @media (max-width: 600px) { .x { display: none; } }</style>"
        "</head><body><p>Body text</p></body></html>"
    )
    out = html_to_markdown(html)
    assert out == "Body text"
    assert "My Page" not in out
    assert "@media" not in out
    assert "color: red" not in out


def test_script_tag_removed() -> None:
    out = html_to_markdown("<p>Hi</p><script>alert(1)</script><p>Bye</p>")
    assert "alert" not in out
    assert "Hi" in out and "Bye" in out


def test_unordered_list() -> None:
    out = html_to_markdown("<ul><li>a</li><li>b</li></ul>")
    assert out == "- a\n- b"


def test_link() -> None:
    assert (
        html_to_markdown('<a href="https://example.com">x</a>')
        == "[x](https://example.com)"
    )


def test_image() -> None:
    out = html_to_markdown('<img src="u.png" alt="A">')
    assert out == "![A](u.png)"


def test_pre_with_language() -> None:
    out = html_to_markdown(
        '<pre><code class="language-py">x = 1\n</code></pre>'
    )
    assert "```py\n" in out
    assert "x = 1" in out


def test_h2_heading() -> None:
    assert html_to_markdown("<h2>Sub</h2>") == "## Sub"


@pytest.mark.parametrize("parser", ("lxml", "html.parser"))
def test_parser_switch_paragraph_and_strong(parser: str) -> None:
    assert (
        html_to_markdown(
            "<p>Hello, <strong>world</strong>.</p>",
            parser=parser,
        )
        == "Hello,**world**."
    )


def test_invalid_parser_raises() -> None:
    with pytest.raises(ValueError, match="parser must be"):
        html_to_markdown("<p>x</p>", parser="xml")  # type: ignore[arg-type]


