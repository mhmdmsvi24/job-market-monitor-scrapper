from config import base_url, headers, proxy
from lxml import html
from utils import (
    extract_jobs_data,
    get_data,
    get_pages_number,
    init_csv,
    parse_html,
    write_csv,
)


def main():
    # initialize a csv file as a database
    init_csv("jobs.csv", ["title", "company", "location", "contract"])

    # pages = get_pages_number(base_url)

    for page in range(10):
        url = base_url + f"&page={page + 1}"
        print(f"Scrapping Page {page}")
        response = get_data(url, headers, proxy)

        if response:
            tree = parse_html(response.text)

            # List of job listings on each page (20)
            main = tree.xpath(
                '//ul[@class="o-listView__list c-jobListView__list"]/li[contains(@class, "o-listView__item__application")]'
            )

            jobs = extract_jobs_data(main)
            write_csv(jobs, "jobs.csv", ["title", "company", "location", "contract"])


if __name__ == "__main__":
    main()
