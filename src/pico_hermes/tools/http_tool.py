
import requests

from .registry import registry


def http_get(args):
    url = args.get("url")
    if not url:
        raise ValueError("url is required")
    timeout = float(args.get("timeout", 15))
    r = requests.get(url, timeout=timeout)
    return {"status": r.status_code, "text": r.text[:50000]}


def http_post_json(args):
    url = args.get("url")
    data = args.get("json")
    if not url:
        raise ValueError("url is required")
    timeout = float(args.get("timeout", 15))
    r = requests.post(url, json=data, timeout=timeout)
    return {"status": r.status_code, "text": r.text[:50000]}


def rss_fetch(args):
    url = args.get("url")
    if not url:
        raise ValueError("url is required")
    timeout = float(args.get("timeout", 15))
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    text = r.text

    # very small RSS/Atom parser (title/link/pubDate/updated)
    items = []
    from xml.etree import ElementTree as ET
    root = ET.fromstring(text)

    def _tag(el, name):
        for c in el:
            if c.tag.endswith(name):
                return c.text or ""
        return ""

    # RSS
    for item in root.findall(".//item"):
        items.append({
            "title": _tag(item, "title"),
            "link": _tag(item, "link"),
            "published": _tag(item, "pubDate"),
        })

    # Atom
    if not items:
        for entry in root.findall(".//{*}entry"):
            link = ""
            for l in entry.findall("{*}link"):
                if l.attrib.get("rel", "alternate") == "alternate":
                    link = l.attrib.get("href", "")
            items.append({
                "title": _tag(entry, "title"),
                "link": link,
                "published": _tag(entry, "updated") or _tag(entry, "published"),
            })

    return items[:50]


registry.register(
    name="http_get",
    schema={
        "name": "http_get",
        "description": "HTTP GET (truncated to 50k chars).",
        "parameters": {
            "type": "object",
            "properties": {"url": {"type": "string"}, "timeout": {"type": "number"}},
            "required": ["url"],
        },
    },
    handler=http_get,
)

registry.register(
    name="http_post_json",
    schema={
        "name": "http_post_json",
        "description": "HTTP POST with JSON body (truncated to 50k chars).",
        "parameters": {
            "type": "object",
            "properties": {"url": {"type": "string"}, "json": {"type": "object"}, "timeout": {"type": "number"}},
            "required": ["url"],
        },
    },
    handler=http_post_json,
)

registry.register(
    name="rss_fetch",
    schema={
        "name": "rss_fetch",
        "description": "Fetch RSS/Atom feed and return items.",
        "parameters": {
            "type": "object",
            "properties": {"url": {"type": "string"}, "timeout": {"type": "number"}},
            "required": ["url"],
        },
    },
    handler=rss_fetch,
)
