from typing import ClassVar

class Config:
    """ """
    headers: ClassVar[dict[str, str]] = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }

    proxy: ClassVar[str] = "socks5://127.0.0.1:10808"

    base_url: ClassVar[str] = "https://jobinja.ir/jobs/category/it-software-web-development-jobs/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85-%D9%88%D8%A8-%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87-%D9%86%D9%88%DB%8C%D8%B3-%D9%86%D8%B1%D9%85-%D8%A7%D9%81%D8%B2%D8%A7%D8%B1?preferred_before=1756724524&sort_by=relevance_desc"

    max_concurrent_requests: ClassVar[int] = 5
    request_timeout: ClassVar[int] = 10
