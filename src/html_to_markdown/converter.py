"""HTML to Markdown conversion."""

from bs4 import BeautifulSoup, NavigableString


def _strip_non_content(soup: BeautifulSoup) -> None:
    """Remove tags whose text should not appear in Markdown (CSS, JS, metadata)."""
    for tag in soup.find_all(["script", "style", "noscript", "template"]):
        tag.decompose()
    div = soup.div
    if div is not None:
        for head in soup.find_all("head"):
            for title in reversed(head.find_all("title")):
                div.insert(0, title.extract())
    for tag in soup.find_all("head"):
        tag.decompose()
    for tag in soup.find_all(["meta", "link", "base"]):
        tag.decompose()


def html_to_markdown(html: str) -> str:
    """Convert HTML string to markdown. Accepts HTML string, returns markdown string.

    Drops non-content markup (e.g. ``<style>``, ``<script>``, ``<head>``, ``<meta>``)
    before conversion so CSS and metadata do not appear in the output.
    ``<title>`` (including from ``<head>``) is emitted as a level-1 heading.
    """
    soup = BeautifulSoup(f"<div>{html}</div>", "html.parser")
    _strip_non_content(soup)
    div = soup.div
    return "".join(_convert_node(child) for child in div.children).strip()


def _convert_node(node) -> str:
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
    children = "".join(_convert_node(child) for child in child_nodes)

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
    if tag_name == "title":
        text = children.strip()
        return f"# {text}\n\n" if text else ""
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
            items.append(f"{marker} {_convert_node(li).strip()}\n")
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
