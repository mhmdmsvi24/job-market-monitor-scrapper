from lxml import html as lxml_html

def parse_html(data):
    return lxml_html.fromstring(data)

def extract_jobs_data(container):
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
