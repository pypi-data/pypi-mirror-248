Usage
=============

Here is a simple python script to show how to use the package:

.. code-block:: python

    import asyncio
    import os
    from AsyncURLCrawler.parser import Parser
    from AsyncURLCrawler.crawler import Crawler
    import yaml


    async def main():
        parser = Parser(
            delay_start=0.1,
            max_retries=5,
            request_timeout=1,
            user_agent="Mozilla",
        )
        crawler = Crawler(
            seed_urls=["https://pouyae.ir"],
            parser=parser,
            exact=True,
            deep=False,
            delay=0.1,
        )
        result = await crawler.crawl()
        with open(
                os.path.join(output_path, 'result.yaml'), 'w') as file:
            for key in result:
                result[key] = list(result[key])
            yaml.dump(result, file)


    if __name__ == "__main__":
        asyncio.run(main())