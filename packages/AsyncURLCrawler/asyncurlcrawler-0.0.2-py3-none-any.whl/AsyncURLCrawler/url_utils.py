import re
from typing import List
import tldextract
from urllib.parse import urlsplit, urljoin

URL_REGEX = re.compile(
    r'^(https?):\/\/'       # Protocol (http, https)
    r'([a-zA-Z0-9._-]+)'    # Domain (may include subdomains)
    r'(\.[a-zA-Z]{2,})'     # Top-level domain (at least 2 characters)
    r'([\/\w._%-]*)*\/?'    # Path (optional)
    r'(\?\S*)?$'            # QueryParam (optional)
)


class InvalidURL(Exception):
    """InvalidURL exception. Valid URL pattern is: https://pouyae.ir"""
    def __init__(self, url):
        self.message = f"{url} is invalid URL! Valid pattern is: http(s)://..."
        super().__init__(self.message)


def validate_urls(urls: List[str]) -> None:
    """Checks pattern for each URL."""
    for url in urls:
        matched = URL_REGEX.match(url)
        if not matched:
            raise InvalidURL(url)


def validate_url(url: str) -> bool:
    """Checks pattern for a URL."""
    matched = URL_REGEX.match(url)
    if matched:
        return True
    else:
        return False


def normalize_url(url: str, base_url: str) -> str:
    """Converts relative URL to absolute URL."""
    url = url.strip()
    split_url = urlsplit(url)
    if not split_url.scheme and not split_url.netloc:
        # URL is relative
        return urljoin(base_url, url)
    return url


def have_exact_subdomain(url1: str, url2: str) -> bool:
    """Checks if two URLs have the same subdomain."""
    extract_url1 = tldextract.extract(url1)
    extract_url2 = tldextract.extract(url2)
    return extract_url1.domain == extract_url2.domain and\
        extract_url1.suffix == extract_url2.suffix


def have_exact_domain(url1: str, url2: str) -> bool:
    """Checks if two URLs have the same domain."""
    split_url1 = urlsplit(url1)
    split_url2 = urlsplit(url2)
    return split_url1.netloc == split_url2.netloc
