
from typing import Dict

def generate_tag(tag_name: str, attrs: Dict[str, str], content: str = None) -> str:
    """Generates a generic HTML tag with optional attributes and content.

    Args:
        tag_name: The name of the tag to generate.
        attrs: A dictionary of attributes for the tag.
        content: Optional content to place within the tag.

    Returns:
        The generated HTML tag as a string.
    """

    attrs_str = " ".join(f'{key}="{value}"' for key, value in attrs.items())
    return f"<{tag_name} {attrs_str}>{content or ''}</{tag_name}>"

def script(src: str, attrs: Dict[str, str] = {}) -> str:
    """Generates an HTML script tag."""
    return generate_tag("script", attrs, content=f' src="{src}"')  # Place src as content for correct placement

def stylesheet(href: str) -> str:
    """Generates an HTML stylesheet link tag."""
    return generate_tag("link", {"rel": "stylesheet", "href": href})

def stylesheet_preload(href: str) -> str:
    """Generates an HTML link tag for preloading a stylesheet."""
    return generate_tag("link", {"rel": "preload", "href": href, "as": "style"})

def preload(href: str, attrs: Dict[str, str]) -> str:
    """Generates a generic HTML preload link tag."""
    return generate_tag("link", {"href": href}, **attrs)  # Unpack additional attributes
