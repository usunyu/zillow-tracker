import time
import json
import requests
import schedule
from urllib.parse import quote_plus
from tqdm import tqdm
from bs4 import BeautifulSoup
from firebase import services as fb
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


def fetch_new_listings_views_job():
    # go through each tracking area
    for tracking_area in TRACKING_AREA_LIST:
        home_urls = []
        tracking_json = TRACKING_AREAS[tracking_area]
        print(f"Fetching {tracking_json['title']} listing urls...")
        for json_data in tqdm(tracking_json["listing"]):
            listing_urls = fetch_home_urls(json_data)
            home_urls += listing_urls
        print(f"Fetched total listing urls: {len(home_urls)}\n")

        total_views = 0
        fetch_views_failed = False
        # for home_url in tqdm(home_urls):
        for home_url in home_urls:
            views_count = 0
            retry_count = 0
            # retry 3
            while views_count == 0 and retry_count < 3:
                views_count = fetch_views_count(home_url)
                retry_count += 1
            if views_count == 0:
                fetch_views_failed = True
                break
            total_views += views_count
            print(f"{home_url}, views: {views_count}\n")
        print(f"Total views count: {total_views}\n")

        if not fetch_views_failed:
            upload_data = {
                "new_listings_count": len(home_urls),
                "total_views_count": total_views,
            }
            print(f"Upload data to firebase: {upload_data}\n")
            # upload to firebase
            fb.save_new_listings_and_views_count(
                tracking_area,
                {
                    "new_listings_count": len(home_urls),
                    "total_views_count": total_views,
                },
            )
        else:
            print(f"Skip upload data to firebase...\n")


if __name__ == "__main__":
    try:
        schedule.every(30).minutes.do(fetch_new_listings_views_job)

        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        pass
