import zillow_sdk
from tracking_areas import TRACKING_AREAS

if __name__ == "__main__":
    tracking_json = TRACKING_AREAS["irvine"]
    home_urls = []
    print(f"Fetching {tracking_json['title']} listing urls...")
    for json_data in tracking_json["listing"]:
        print(f"[zip code]: {json_data['zip_code']}")
        listing_urls = zillow_sdk.fetch_home_urls(json_data, debug=True)
        home_urls += listing_urls
        print()
    print(f"Fetched total listing urls: {len(home_urls)}\n")
