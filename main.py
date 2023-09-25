import time
import json
import requests
from urllib.parse import quote_plus
from tqdm import tqdm
from bs4 import BeautifulSoup
from tracking_areas import TRACKING_AREAS

TRACKING_AREA_LIST = ["bay_area"]


def fetch_content(url: str) -> str:
    headers = {
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
    response = requests.get(url, headers=headers)
    time.sleep(1.0)
    return response.text


def fetch_home_urls(json_data: dict) -> list[str]:
    query_json = json_data["search_query"]
    query_string = json.dumps(query_json)
    encoded_query = quote_plus(query_string)
    url = json_data["base_url"] + encoded_query
    html_content = fetch_content(url)
    soup = BeautifulSoup(html_content, "lxml")

    # parse result count
    count_span = soup.find("span", class_="result-count")
    result_count = 0
    if count_span:
        count_content = count_span.get_text()
        result_count = int(count_content.split(" ")[0])

    # parse list urls
    listing_set = set()
    script_tags = soup.find_all("script", type="application/ld+json")
    for script_tag in script_tags:
        json_content = json.loads(script_tag.string)
        if "url" in json_content:
            listing_set.add(json_content["url"])
    listing_urls = list(listing_set)

    if result_count != len(listing_urls):
        print("Result count not match with fetched urls!")
    return listing_urls


def fetch_views_count(home_url: str) -> int:
    html_content = fetch_content(home_url)
    soup = BeautifulSoup(html_content, "lxml")
    dt_tags = soup.select("dl > dt")
    views = dt_tags[2].get_text()
    views_count = int(views.replace(",", ""))
    return views_count


def main():
    home_urls = []
    for tracking_area in TRACKING_AREA_LIST:
        tracking_json = TRACKING_AREAS[tracking_area]
        print(f"Fetching {tracking_json['title']} listing urls...")
        for json_data in tqdm(tracking_json["listing"]):
            listing_urls = fetch_home_urls(json_data)
            home_urls += listing_urls
    print(f"Fetched total listing urls: {len(home_urls)}")

    total_views = 0
    for home_url in tqdm(home_urls):
        views_count = fetch_views_count(home_url)
        total_views += views_count
    print(f"Total views count: {total_views}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass