from lxml import html as lxml_html
from lxml.etree import Element
import math

from config import Config

from .client import get_data

def parse_html(data: str) -> Element:
    """

    Args:
      data:

    Returns:

    """
    return lxml_html.fromstring(data)

def extract_jobs_data(container: list[Element]) -> list[dict[str, str]]:
    """

    Args:
      container:

    Returns:

    """
    jobs = []
    for job in container:
        # the job title and demand
        title = job.xpath('.//h2/a[@class="c-jobListView__titleLink"]/text()')
        title = title[0].strip().replace("\u200c", "")

        # The list that contains company, location and contract
        job_data = job.xpath(".//ul/li")

        company = job_data[0].text_content().strip()
        location = job_data[1].text_content().strip()
        contract = (
            job_data[2]
            .text_content()
            .strip()
            .replace(" ", "")
            .replace("\u200c", "")
            .replace("\n", " ")
            .replace("(برای مشاهدهحقوقواردشوید)", "")
        )

        jobs.append(
            {
                "title": title,
                "company": company,
                "location": location,
                "contract": contract,
            }
        )

    return jobs

async def get_pages_number(url: str) -> int:
    response = await get_data(url, Config.headers, Config.proxy)
    tree = parse_html(response.text)
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
