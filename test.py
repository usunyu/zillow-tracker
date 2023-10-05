import zillow_sdk
from bs4 import BeautifulSoup
from tracking_areas import TRACKING_AREAS


def test_home_urls_count():
    tracking_json = TRACKING_AREAS["bay_area"]
    home_urls = []
    print(f"Fetching {tracking_json['title']} listing urls...")
    for json_data in tracking_json["listing"]:
        zip_code = json_data["zip_code"]
        if zip_code != 94134:
            continue
        print(f"[zip code]: {zip_code}")
        listing_urls = zillow_sdk.fetch_home_urls(json_data, debug=True)
        home_urls += listing_urls
        print()
    print(f"Fetched total listing urls: {len(home_urls)}\n")


def test_auction_listing():
    # url = "https://www.zillow.com/homedetails/448-Wilde-Ave-San-Francisco-CA-94134/15172934_zpid/"
    url = "https://www.zillow.com/homedetails/339-Sweeny-St-San-Francisco-CA-94134/15165670_zpid/"
    html_content = zillow_sdk.fetch_content(url)
    soup = BeautifulSoup(html_content, "lxml")
    span_tags = soup.find_all("span")
    is_auction = False
    for span in span_tags:
        if span.text == "Auction":
            is_auction = True
        # print(span.text)
    if is_auction:
        print("Is Auction")
    else:
        print("Not Auction")


if __name__ == "__main__":
    # test_home_urls_count()
    test_auction_listing()
