import time
import click
import schedule
from tqdm import tqdm
from firebase import services as fb
from tracking_areas import TRACKING_AREAS
import zillow_sdk

TRACKING_AREA_LIST = [
    "bay_area",
    "irvine",
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
        print(f"Fetched total listing urls: {len(home_urls)}")

        total_views = 0
        fetch_views_failed = False
        print(f"Fetching {tracking_json['title']} views count...")
        auction_urls = []
        for home_url in tqdm(home_urls):
            html_content = zillow_sdk.fetch_content(home_url)
            # check is auction
            is_auction = zillow_sdk.check_is_auction(html_content)
            # skip auction
            if is_auction:
                auction_urls.append(home_url)
                continue

            views_count = zillow_sdk.get_views_count(html_content, home_url)
            if views_count == 0:
                fetch_views_failed = True
                break
            total_views += views_count
            # print(f"{home_url}, views: {views_count}")
        print(f"Total views count: {total_views}")

        listings_count = len(home_urls) - len(auction_urls)
        print(
            f"Filtered total listings count: {listings_count}, auction count: {len(auction_urls)}"
        )
        if not fetch_views_failed:
            upload_data = {
                "new_listings_count": listings_count,
                "total_views_count": total_views,
            }
            print(f"Upload data to firebase [{tracking_area}]: {upload_data}")
            # upload to firebase
            fb.save_new_listings_and_views_count(tracking_area, upload_data)
        else:
            print(f"Skip upload data to firebase...")


@click.command()
@click.option("--mode", type=click.Choice(["schedule", "onetime"]), prompt=True)
def run(mode):
    if mode == "onetime":
        fetch_new_listings_views_job()
    elif mode == "schedule":
        # simulator a human schedule
        schedule.every().day.at("8:30").do(fetch_new_listings_views_job)
        schedule.every().day.at("12:15").do(fetch_new_listings_views_job)
        schedule.every().day.at("18:30").do(fetch_new_listings_views_job)
        schedule.every().day.at("22:15").do(fetch_new_listings_views_job)

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        pass
