import csv
import math
import os
import sys

from config import headers, proxy
from utils import parse_html

from .client import get_data

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def init_csv(file, rows):
    with open(file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows)
        writer.writeheader()


def write_csv(data, file, rows):
    with open(file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows)
        writer.writerows(data)


def get_pages_number(url):
    response = get_data(url, headers, proxy)
    tree = parse_html(response)
    # Number of all pages
    pages = math.ceil(
        int(
            tree.xpath(
                '//span[contains(@class, "c-jobSearchState__numberOfResultsEcho")]/text()'
            )[0]
            .strip()
            .replace(" ", "")
            .replace(",", "")
            .split("\n")[0]
        )
        / 100
    )

    return pages
