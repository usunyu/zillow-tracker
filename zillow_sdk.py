import time
import json
import requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup


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


def fetch_home_urls(json_data: dict, debug: bool = False) -> list:
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
    if debug:
        print(f"[result count]: {result_count}")

    # parse list urls
    listing_set = set()
    community_urls = set()
    script_tags = soup.find_all("script", type="application/ld+json")
    for script_tag in script_tags:
        json_content = json.loads(script_tag.string)
        if "url" in json_content:
            home_url = json_content["url"]
            # skip community url
            if "www.zillow.com/community" in home_url:
                if home_url not in community_urls:
                    result_count -= 1
                community_urls.add(home_url)
                if debug:
                    print(f"[found new construction]: {home_url}")
                    print(f"[update result count]: {result_count}")
                continue
            listing_set.add(home_url)

    # links = soup.find_all("a")
    # for link in links:
    #     url = link.get("href")
    #     if url and "homedetails" in url:
    #         print(url)
    #         listing_set.add(url)

    listing_urls = list(listing_set)
    if debug:
        print("[home urls]:")
        for url in listing_urls:
            print(url)

    if result_count != len(listing_urls):
        print("Result count not match with fetched urls!")
        print(f"result_count: {result_count}, fetched: {len(listing_urls)}")
        if debug:
            print(f"[fetch url]:\n{json_data['base_url'] + encoded_query}")
    else:
        if debug:
            print("[fetch home urls]: success")

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
