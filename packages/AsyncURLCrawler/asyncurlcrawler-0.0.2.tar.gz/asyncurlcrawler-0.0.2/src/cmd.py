import argparse
import asyncio
import os
from config import load_config
from typing import List
from AsyncURLCrawler.parser import Parser
from AsyncURLCrawler.crawler import Crawler
import yaml


def parse_args() -> [List[str], bool, bool, float]:
    parser = argparse.ArgumentParser(
      description='URLCrawler'
    )
    parser.add_argument('--url', nargs='+', type=str,
                        help='Pass at least one URL to crawl.')
    parser.add_argument('--exact', action='store_true',
                        help='If set then crawls the exact subdomain/domain.')
    parser.add_argument('--deep', action='store_true',
                        help='If set then crawls all the visited urls.'
                             'The default value is false.')
    parser.add_argument('--delay', type=float, default=0,
                        help='Delay between HTTP requests.')
    parser.add_argument('--output', type=str,
                        help='Outputfile path.')
    args = parser.parse_args()
    if args.url:
        urls = args.url
    else:
        raise Exception("At least one URL is required to crawl.")
    deep = False
    if args.deep:
        deep = True
    exact = False
    if args.exact:
        exact = True
    output = args.output
    if not args.output:
        output = os.getcwd()
    return urls, exact, deep, args.delay, output


async def main():
    urls, exact, deep, delay, output_path = parse_args()
    config = load_config()
    parser = Parser(
        delay_start=config.parser.delay_start,
        max_retries=config.parser.max_retries,
        request_timeout=config.parser.request_timeout,
        user_agent=config.parser.user_agent,
    )
    crawler = Crawler(
        seed_urls=urls,
        parser=parser,
        exact=exact,
        deep=deep,
        delay=delay,
    )
    result = await crawler.crawl()
    with open(
            os.path.join(output_path, 'result.yaml'), 'w') as file:
        for key in result:
            result[key] = list(result[key])
        yaml.dump(result, file)


if __name__ == "__main__":
    asyncio.run(main())
