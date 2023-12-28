from httpx import Response, AsyncClient, ConnectTimeout
import asyncio
from typing import List
from bs4 import BeautifulSoup
from AsyncURLCrawler.url_utils import normalize_url, validate_url


class Parser:
    """
    This module retrieve a URL, parses its HTML content, and extract URLs from <a> tags.
    If HTTP request fails, the subsequent request is not sent immediately;
    instead, it waits for a specified duration and then retries.
    The delay between consecutive unsuccessful requests increases exponentially with each attempt.
    Additionally, there is a predefined limit on the number of retries.
    This retry approach is known as exponential backoff.

    :param delay_start: Indicates the initial value of delay in exponential backoff strategy. The default value is 0.1 seconds.
    :param max_retries: Maximum number of retries. The default value is 5.
    :param request_timeout: HTTP request timeout in seconds. The default value is 1 seconds.
    :param user_agent: User Agent in HTTP request header. The default value is Mozilla/5.0.
    """
    def __init__(self, delay_start: float = 0.1, max_retries: int = 5,
                 request_timeout: float = 1, user_agent: str = 'Mozilla/5.0'):
        self._delay_start = delay_start
        self._current_delay = delay_start
        self._max_retries = max_retries
        self._request_timeout = request_timeout
        self._current_retry = 0
        self._user_agent = user_agent

    def reset(self):
        """
        Resets exponential backoff internal state for each URL.
        It is necessary to call this method before fetching a new URL.
        """
        self._current_retry = 0
        self._current_delay = self._delay_start

    async def _fetch_page(self, url: str) -> [Response, None]:
        """
        This method fetches a URL, sets user agent header and timeout for each HTTP request.
        The request is executed asynchronously.
        """
        # TODO Check file format before fetching! ignore jpg, pdf, ...
        async with AsyncClient() as client:
            try:
                response = await client.get(
                    url,
                    timeout=self._request_timeout,
                    headers={"User-Agent": self._user_agent},
                )
            except ConnectTimeout:
                return None
            return response

    def _extract_urls(self, response: str, base_url: str) -> List[str]:
        """
        Extracts URLs from <a> tag.
        Checks if a URL is valid and returns list of absolute URLs.
        Relative URLs are converted to absolute URLs by having base_url.
        """
        soup = BeautifulSoup(response, 'html.parser')
        urls = list()
        for link in soup.find_all('a', href=True):
            n_link = normalize_url(link.get('href'), base_url)
            if validate_url(n_link):
                urls.append(n_link)
        return urls

    async def probe(self, url: str) -> List[str]:
        """
        Probe fetches a URL by calling `_fetch_page()` and passes the content to `_extract_urls().`
        Exponential backoff strategy is handled in this method.
        If the status code in response is not 2xx or the request is timed-out it is considered failed request.
        """
        # TODO Check response size!
        response = await self._fetch_page(url)
        status_code = None
        if response:
            status_code = response.status_code
        while status_code is None or status_code == 429 or status_code >= 500:
            if self._current_retry == self._max_retries:
                break
            await asyncio.sleep(self._current_delay)
            self._current_delay *= pow(2, self._current_retry)
            self._current_retry += 1
            response = await self._fetch_page(url)
            if response:
                status_code = response.status_code
        if status_code != 200:
            return []
        urls = self._extract_urls(response.text, url)
        return urls
