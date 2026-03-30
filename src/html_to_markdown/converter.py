"""HTML to Markdown conversion."""

from typing import Literal

from bs4 import BeautifulSoup, NavigableString
from bs4.element import Doctype, PageElement

HtmlParser = Literal["lxml", "html.parser"]


def strip_non_content(soup: BeautifulSoup) -> None:
    """Remove tags whose text should not appear in Markdown (CSS, JS, metadata).

    Mutates ``soup`` in place. Call before :func:`conversion_children` when
    mirroring :func:`html_to_markdown`.
    """
    for tag in soup.find_all(["script", "style", "noscript", "template"]):
        tag.decompose()
    for tag in soup.find_all("head"):
        tag.decompose()
    for tag in soup.find_all(["meta", "link", "base"]):
        tag.decompose()
    for tag in soup.find_all("title"):
        tag.decompose()


def conversion_children(soup: BeautifulSoup) -> list[PageElement]:
    """Top-level tree nodes to convert for a parsed document (public building block).

    Returns ``body``'s children if ``body`` exists, else ``html``'s children,
    else top-level soup roots (skipping doctypes). Only accepts a
    :class:`~bs4.BeautifulSoup` instance, not an element tag as root.
    """
    body = soup.body
    if body is not None:
        return list(body.children)
    html_el = soup.html
    if html_el is not None:
        return list(html_el.children)
    return [
        c
        for c in soup.children
        if not isinstance(c, Doctype)
    ]


def html_to_markdown(html: str, *, parser: HtmlParser = "html.parser") -> str:
    """Convert HTML string to markdown. Accepts HTML string, returns markdown string.

    Parses the string as a document or fragment (no synthetic wrapper) using
    Beautiful Soup with ``parser`` (default ``\"html.parser\"``; or ``\"lxml\"``). Drops
    non-content markup (e.g. ``<style>``, ``<script>``, ``<head>``, ``<meta>``)
    before walking ``body`` (or fallback roots).
    """
    if parser not in ("lxml", "html.parser"):
        raise ValueError(
            f"parser must be 'lxml' or 'html.parser', got {parser!r}"
        )
    soup = BeautifulSoup(html, parser)
    strip_non_content(soup)
    body_md = "".join(convert_node(child) for child in conversion_children(soup))
    return body_md.strip()


def convert_node(node: PageElement) -> str:
    """Convert a single Beautiful Soup tree node to markdown (public building block).

    Handles :class:`~bs4.element.NavigableString` and tags; unknown or empty
    nodes yield ``\"\"``. For a subtree, pass the root tag from the parsed tree.
    """
    if isinstance(node, NavigableString):
        text = str(node).strip()
        return text or ""

    if not hasattr(node, "name") or node.name is None:
        return ""

    tag_name = node.name.lower()

    # Filter whitespace-only text nodes (indentation from HTML)
    child_nodes = [
        child
        for child in node.children
        if not isinstance(child, NavigableString) or str(child).strip() != ""
    ]
    children = "".join(convert_node(child) for child in child_nodes)

    if tag_name == "h1":
        return f"# {children}\n\n"
    if tag_name == "h2":
        return f"## {children}\n\n"
    if tag_name == "h3":
        return f"### {children}\n\n"
    if tag_name == "h4":
        return f"#### {children}\n\n"
    if tag_name == "h5":
        return f"##### {children}\n\n"
    if tag_name == "h6":
        return f"###### {children}\n\n"
    if tag_name == "p":
        return f"{children}\n\n"
    if tag_name in ("strong", "b"):
        return f"**{children}**"
    if tag_name in ("em", "i"):
        return f"*{children}*"
    if tag_name == "code":
        return f"`{children}`"
    if tag_name == "pre":
        code = node.find("code")
        lang = ""
        if code and code.get("class"):
            for cls in code["class"]:
                if cls.startswith("language-"):
                    lang = cls.replace("language-", "")
                    break
        return f"\n```{lang}\n{code.get_text() if code else children}\n```\n\n"
    if tag_name in ("ul", "ol"):
        items = []
        for idx, li in enumerate(node.find_all("li", recursive=False)):
            marker = f"{idx + 1}." if tag_name == "ol" else "-"
            items.append(f"{marker} {convert_node(li).strip()}\n")
        return "\n" + "".join(items) + "\n"
    if tag_name == "li":
        return children.strip()
    if tag_name == "blockquote":
        return f"> {children.strip()}\n\n"
    if tag_name == "a":
        href = node.get("href", "") or ""
        return f"[{children}]({href})"
    if tag_name == "img":
        src = node.get("src", "") or ""
        alt = node.get("alt", "") or ""
        return f"![{alt}]({src})\n\n"
    if tag_name == "br":
        return "\n"

    return children
