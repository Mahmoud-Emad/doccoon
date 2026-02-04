"""
Content sanitization utilities for preventing XSS attacks.
"""

import bleach

# Allowed HTML tags for markdown content
# These are common tags that markdown can generate
ALLOWED_TAGS = [
    "a",
    "abbr",
    "acronym",
    "b",
    "blockquote",
    "br",
    "code",
    "dd",
    "del",
    "div",
    "dl",
    "dt",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "i",
    "img",
    "ins",
    "kbd",
    "li",
    "mark",
    "ol",
    "p",
    "pre",
    "q",
    "s",
    "samp",
    "small",
    "span",
    "strong",
    "sub",
    "sup",
    "table",
    "tbody",
    "td",
    "tfoot",
    "th",
    "thead",
    "tr",
    "u",
    "ul",
    "var",
]

# Allowed attributes for each tag
ALLOWED_ATTRIBUTES = {
    "*": ["class", "id"],
    "a": ["href", "title", "target", "rel"],
    "abbr": ["title"],
    "acronym": ["title"],
    "img": ["src", "alt", "title", "width", "height"],
    "td": ["colspan", "rowspan", "align"],
    "th": ["colspan", "rowspan", "align", "scope"],
    "table": ["border", "cellpadding", "cellspacing"],
}

# Allowed URL protocols
ALLOWED_PROTOCOLS = ["http", "https", "mailto", "tel"]


def sanitize_html(content: str) -> str:
    """
    Sanitize HTML content to prevent XSS attacks.

    This is used for content that may contain HTML (e.g., rendered markdown).
    """
    if not content:
        return content

    return bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )


def sanitize_markdown(content: str) -> str:
    """
    Sanitize markdown content.

    For markdown, we primarily need to:
    1. Remove any raw HTML script tags or event handlers
    2. Sanitize any embedded HTML

    Since markdown is stored as plain text and rendered on the frontend,
    the main risk is embedded HTML within markdown.
    """
    if not content:
        return content

    # For markdown content, we allow the raw markdown syntax
    # but sanitize any embedded HTML to prevent XSS
    # bleach.clean will strip dangerous tags while preserving safe content
    return bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )


def sanitize_plain_text(content: str) -> str:
    """
    Sanitize plain text by stripping all HTML tags.

    Use this for content that should never contain HTML.
    """
    if not content:
        return content

    return bleach.clean(content, tags=[], strip=True)
