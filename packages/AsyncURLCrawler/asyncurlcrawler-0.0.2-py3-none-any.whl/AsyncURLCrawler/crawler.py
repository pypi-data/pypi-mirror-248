from typing import List, Dict
from AsyncURLCrawler.url_utils import (
    validate_urls,
    have_exact_subdomain,
    have_exact_domain,
)
from collections import deque
from AsyncURLCrawler.parser import Parser
import asyncio


class Crawler:
    """
    This module extracts URLs from the targets by using Breadth First Search algorithm.

    :param seed_urls: List of target URLs to crawl. Valid URL pattern is: https://pouyae.ir
    :param parser: An instance of Parser class. Parser object fetches the URL and returns extracted URLs.
    :param deep: If set, crawls all visited URLs, although this is not recommended due to its resource-intensive nature. Alternatively, it crawls URLs that share the same base domain as the seed URL.
    :param exact: If set, crawls URLs that share the exact subdomain as the seed URL. If deep is set, exact is ignored.
    :param delay: The delay between each URL crawl. It is used to adjust request per seconds and avoid denial of service on seed URLs.
    """
    def __init__(self, seed_urls: List[str],
                 parser: Parser,
                 deep: bool = False,
                 exact: bool = True,
                 delay: float = 0):
        self._set_seed_urls(seed_urls)
        self._parser = parser
        self._deep = deep
        self._exact = exact
        self._delay = delay

    def _set_seed_urls(self, seed_urls: List[str]) -> None:
        validate_urls(seed_urls)
        self._seed_urls = seed_urls
        self._visited_urls = dict.fromkeys(seed_urls, set())

    def _update_queue(self, extracted_url: str, root_url: str) -> None:
        if self._deep:
            self._queue.append(extracted_url)
        else:
            if self._exact:
                if have_exact_domain(extracted_url, root_url):
                    self._queue.append(extracted_url)
            else:
                if have_exact_subdomain(extracted_url, root_url):
                    self._queue.append(extracted_url)

    def _reset_queue(self) -> None:
        self._queue = deque()

    async def crawl(self) -> Dict:
        """Crawls all seed URLs one by one based on BFS algorithm.
        Returns visited URLs in a python dictionary.
        Each key is seed URL and value is list of visited URLs for that key."""
        for root_url in self._seed_urls:
            self._reset_queue()
            self._queue.append(root_url)
            while self._queue:
                current_url = self._queue.popleft()
                self._parser.reset()
                extracted_urls = await self._parser.probe(current_url)
                for extracted_url in extracted_urls:
                    if extracted_url not in self._visited_urls[root_url]:
                        self._visited_urls[root_url].add(extracted_url)
                        self._update_queue(extracted_url, root_url)
                await asyncio.sleep(self._delay)
        return self._visited_urls

    async def yielded_crawl(self):
        """
        Crawls all seed URLs one by one based on BFS algorithm.
        Yields each visited URL. To get list of visited URLs use `get_visited_urls()`.
        """
        for root_url in self._seed_urls:
            self._reset_queue()
            self._queue.append(root_url)
            while self._queue:
                current_url = self._queue.popleft()
                self._parser.reset()
                extracted_urls = await self._parser.probe(current_url)
                for extracted_url in extracted_urls:
                    if extracted_url not in self._visited_urls[root_url]:
                        self._visited_urls[root_url].add(extracted_url)
                        self._update_queue(extracted_url, root_url)
                        yield extracted_url
                await asyncio.sleep(self._delay)
        return

    def get_visited_urls(self) -> Dict:
        """Returns visited URLs in a python dictionary.
        Each key is seed URL and value is list of visited URLs for that key."""
        return self._visited_urls
