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
    write_csv,
)

async def fetch_page(page: int) -> list[dict[str, str]]:
    url = Config.base_url + f"&page={page}"
    print(f"Scraping Page {page} ---- URL: {url}")
    await asyncio.sleep(random.uniform(0.5, 1))

    response = await get_data(url, Config.headers, Config.proxy, timeout=Config.request_timeout)
    if not response:
        return []

    tree = parse_html(response.text)
    main = tree.xpath(
        '//ul[@class="o-listView__list c-jobListView__list"]/li[contains(@class, "o-listView__item__application")]'
    )
    return extract_jobs_data(main)

async def write_batches(all_results: list[list[dict[str, str]]], csv_files: list[Path]):
    locks = {str(f): asyncio.Lock() for f in csv_files}

    tasks = []
    for i, jobs in enumerate(all_results):
        if not jobs:
            continue

        file_index = i // 10   # or round-robin: i % len(csv_files)
        file_path = csv_files[file_index]
        lock = locks[str(file_path)]
        tasks.append(write_csv(jobs, file_path, ["title", "company", "location", "contract"], lock))

    await asyncio.gather(*tasks)

async def main() -> None:
    pages = 5
    path = Path(__file__).parent / "data"
    create_dir(path)

    num_files = math.ceil(pages / 10)
    base_name = "jobs"
    csv_result: list[str] = create_csv(
        base_name, num_files, ["title", "company", "location", "contract"], path
    )
    csv_files = [path / f for f in csv_result]

    print(f"-----Successfully created {len(csv_files)} files for {pages} pages")

    # 1. Fetch all jobs
    all_results = await asyncio.gather(*(fetch_page(i + 1) for i in range(pages)))

    # 2. Write them to CSVs
    await write_batches(all_results, csv_files)


if __name__ == "__main__":
    tracemalloc.start()
    start = time.time()
    asyncio.run(main())
    end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Scraping finished in {end - start:.2f} seconds")
    print(f"Current memory usage: {current / 1024 / 1024:.2f} MB")
    print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")
