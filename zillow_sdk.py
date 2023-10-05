import time
import httpx
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup

BASE_URL = "https://www.zillow.com/search/GetSearchPageState.htm?"

# we should use browser-like request headers to prevent being instantly blocked
BASE_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6",
    "Sec-Ch-Ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
}


def fetch_content(url: str) -> str:
    response = requests.get(url, headers=BASE_HEADERS)
    time.sleep(1.0)
    return response.text


def fetch_home_urls(json_data: dict, debug: bool = False) -> list:
    query_json = json_data["search_query"]
    parameters = {
        "searchQueryState": query_json,
        "wants": {"cat1": ["listResults", "mapResults"], "cat2": ["total"]},
        # "requestId": 2,
    }
    fetch_url = BASE_URL + urlencode(parameters)
    response = httpx.get(fetch_url, headers=BASE_HEADERS)
    time.sleep(1.0)
    data = response.json()
    results = data["cat1"]["searchResults"]["mapResults"]
    total_count = data["cat1"]["searchList"]["totalResultCount"]
    total_pages = data["cat1"]["searchList"]["totalPages"]
    if debug:
        print(
            f"[results_count]: {len(results)}, [total_count]: {total_count}, [total_pages]: {total_pages}"
        )
    home_urls = []
    result_count = total_count
    for detail in results:
        home_url = f"https://www.zillow.com{detail['detailUrl']}"
        if "www.zillow.com/community" in home_url:
            result_count -= 1
            if debug:
                print(f"[found community url]: {home_url}")
                print(f"[update result count]: {result_count}")
            continue
        home_urls.append(home_url)
    if debug:
        print("[home urls]:")
        for url in home_urls:
            print(url)
    if result_count != len(home_urls):
        print("Result count not match with fetched urls!")
        print(f"result_count: {result_count}, fetched: {len(home_urls)}")
        if debug:
            print(f"*** [fetch url]: ***\n{fetch_url}")
    else:
        if debug:
            print("[fetch home urls]: success")
    return home_urls


def get_views_count(html_content: str, home_url: str = None) -> int:
    soup = BeautifulSoup(html_content, "lxml")
    dt_tags = soup.select("dl > dt")
    if len(dt_tags) == 3:
        views = dt_tags[1].get_text()
    elif len(dt_tags) == 6:
        views = dt_tags[2].get_text()
    try:
        views_count = int(views.replace(",", ""))
    except:
        views_count = 0
        print(f"Unable to parse the views count from url: {home_url}\n")
        # for dt_tag in dt_tags:
        #     print(dt_tag)
    return views_count


def check_is_auction(html_content: str, home_url: str = None) -> bool:
    soup = BeautifulSoup(html_content, "lxml")
    span_tags = soup.find_all("span")
    is_auction = False
    for span in span_tags:
        if span.text == "Auction":
            is_auction = True
            break
    return is_auction
