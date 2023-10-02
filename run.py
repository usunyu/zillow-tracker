import time
import schedule
from tqdm import tqdm
from firebase import services as fb
from tracking_areas import TRACKING_AREAS
import zillow_sdk

TRACKING_AREA_LIST = [
    "bay_area",
    # "irvine",
]


def fetch_new_listings_views_job():
    # go through each tracking area
    for tracking_area in TRACKING_AREA_LIST:
        home_urls = []
        tracking_json = TRACKING_AREAS[tracking_area]
        print(f"Fetching {tracking_json['title']} listing urls...")
        for json_data in tqdm(tracking_json["listing"]):
            listing_urls = zillow_sdk.fetch_home_urls(json_data)
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
                views_count = zillow_sdk.fetch_views_count(home_url)
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
    fetch_new_listings_views_job()
    # try:
    #     schedule.every(30).minutes.do(fetch_new_listings_views_job)

    #     while True:
    #         schedule.run_pending()
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     pass
