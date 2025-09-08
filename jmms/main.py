import asyncio
import random
import time
import tracemalloc
from pathlib import Path
import math

from config import Config
from utils import (
    extract_jobs_data,
    get_data,
    get_pages_number,
    create_csv,
    create_dir,
    parse_html,
    write_csv_async,
)

async def main():
    pages = 30
    # pages = get_pages_number(Config.base_url)
    path = Path(__file__).parent / "data"
    create_dir(path)

    num_files = math.ceil(pages / 10)
    base_name = "jobs"

    csv_result = create_csv(base_name, num_files, ["title", "company", "location", "contract"], path)

    print(f"-----Successfully created {len(csv_result)} files for {pages} pages")

    async def fetch_page(page, filename, lock):
        semaphore = asyncio.Semaphore(Config.max_cuncurrent_requests)
        async with semaphore:
            url = Config.base_url + f"&page={page}"
            print(f"Scraping Page {page} ---- URL: {url}")
            await asyncio.sleep(random.uniform(0.5, 1))
            response = await get_data(url, Config.headers, Config.proxy, timeout=Config.request_timeout)

            if response:
                tree = parse_html(response.text)
                main = tree.xpath(
                    '//ul[@class="o-listView__list c-jobListView__list"]/li[contains(@class, "o-listView__item__application")]'
                )
                jobs = extract_jobs_data(main)

                await write_csv_async(jobs, filename, ["title", "company", "location", "contract"], lock)

                return jobs

        # Create locks keyed by full path string for each file


    tasks = []
    locks = {str(path / f): asyncio.Lock() for f in csv_result}

    for i in range(pages):
        file_index = i // 10
        file_name = csv_result[file_index]
        file_path = path / file_name
        lock = locks[str(file_path)]
        tasks.append(fetch_page(i + 1, file_path, lock))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    tracemalloc.start()
    start = time.time()
    asyncio.run(main())
    end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Scraping finished in {end - start:.2f} seconds")
    print(f"Current memory usage: {current / 1024 / 1024:.2f} MB")
    print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")
