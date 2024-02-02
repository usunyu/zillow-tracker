import time
import random
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from utils import print_msg

BASE_URL = "https://www.zillow.com/search/GetSearchPageState.htm?"

# we should use browser-like request headers to prevent being instantly blocked
BASE_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6",
    "Cache-Control": "max-age=0",
    # "Cookie": "zguid=24|%24c3094722-1da0-46c3-bf20-ffad0c45e5fa; _ga=GA1.2.1085683231.1704505862; zjs_anonymous_id=%22c3094722-1da0-46c3-bf20-ffad0c45e5fa%22; zjs_user_id=null; zg_anonymous_id=%2219a51140-7c20-4bf1-9034-c019f84ddfc9%22; _pxvid=0bedea74-ac36-11ee-a0cb-6a469e1e9ec1; _gcl_au=1.1.278652768.1704505862; __pdst=a043be2f81a141eb9cdec93e3ec6abc3; _pin_unauth=dWlkPU9UZGlaV016WkRVdE1XVmxPQzAwWlRjd0xXRm1Nakl0TWpBNE1XSTFPRGs1WTJJNA; optimizelyEndUserId=oeu1706162194765r0.10879172202088117; zgcus_aeut=AEUUT_7f0edf7a-bb46-11ee-b246-ea0cdbc9a38f; zgcus_aeuut=AEUUT_7f0edf7a-bb46-11ee-b246-ea0cdbc9a38f; _gid=GA1.2.2000045317.1706162195; _clck=efzz4z%7C2%7Cfip%7C0%7C1466; zgsession=1|864606ed-4984-4b99-8991-05adac016887; DoubleClickSession=true; pxcts=cdadfaa9-bb94-11ee-80a3-5dcf5476fede; _hp2_ses_props.1215457233=%7B%22ts%22%3A1706195827830%2C%22d%22%3A%22www.zillow.com%22%2C%22h%22%3A%22%2F%22%7D; JSESSIONID=F90973DF9BD6BA67BFBD5CAD07A13ECB; search=6|1708787844964%7Crect%3D37.57767011909112%2C-122.23572108666991%2C37.530719340704096%2C-122.40360591333007%26rid%3D13699%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26listPriceActive%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%26student-housing%3D0%26income-restricted-housing%3D0%26military-housing%3D0%26disabled-housing%3D0%26senior-housing%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%0913699%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Atrue%7D%09%09%09%09%09; x-amz-continuous-deployment-state=AYABeBNTQN5RBS1SfpOH9AO6%2FTkAPgACAAFEAB1kM2Jsa2Q0azB3azlvai5jbG91ZGZyb250Lm5ldAABRwAVRzA3MjU1NjcyMVRZRFY4RDcyVlpWAAEAAkNEABpDb29raWUAAACAAAAADBq3OBNCb8W+S8VfvQAwkT1D5OgyXtn2elVInW%2FFS7MyDBcENrMGt8dtqms01v3Zjg7pH0+1H5rg6EJXi2I+AgAAAAAMAAQAAAAAAAAAAAAAAAAAAGmXaxXs%2FPiZumVmOGgmnwj%2F%2F%2F%2F%2FAAAAAQAAAAAAAAAAAAAAAQAAAAw5RSEYGYYhn0l7yeUKHx7H9umaAavKfp4Ug+QR9umaAavKfp4Ug+QR9umaAavKfp4Ug+QR9umaAavKfp4Ug+QR; _hp2_id.1215457233=%7B%22userId%22%3A%221554419120361057%22%2C%22pageviewId%22%3A%22190210636107196%22%2C%22sessionId%22%3A%228225247830439819%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _uetsid=7fff7110bb4611eea715ffbf54c1e512; _uetvid=8ba7eb005a6511eebca6e381cf8ef374; AWSALB=PuxF2Cfs+kBFpp2Az1zItKQwbvo65KbHQji33rkjP8nmOpfKqMX67oIyuWsjpWVfoAJdn4mm1PUStwrQmg08zSQMlm75E+BQD8/6MYuiw2w1ttpZYcFr67Q81+xa; AWSALBCORS=PuxF2Cfs+kBFpp2Az1zItKQwbvo65KbHQji33rkjP8nmOpfKqMX67oIyuWsjpWVfoAJdn4mm1PUStwrQmg08zSQMlm75E+BQD8/6MYuiw2w1ttpZYcFr67Q81+xa; _clsk=19g93ha%7C1706196238901%7C5%7C0%7Cl.clarity.ms%2Fcollect; _px3=4a1da84f9df303439db6a57e67b12cd3dcc432ab1b89713a9d8c8c2822e0335a:iz7EaR9HOviKZzILGtvgK9zo8cezD0AxyRv179u/QPWVKsJs4ndWQuZFok1ffEH+AQgAv+TYxqvqIme398FdPg==:1000:PKaHV9zEf7WWybooXrGDlOiVGyg+Ctefyh72bTICmlSfCQL+AG+IbckDIbzbTH9+xB50NTwSZf6hzo9Ga5En61dZprKXjFgtspTVyGdHtgEfK0gUZHqmFQruTxguuOQRdS3CO4tTz98136wSHPWsOvcUZCkfDgEc3V8F9FV2bpP3TCGLtIm5YRvvWvt8KkDZA3ix+BJWc+6AXt6li6eW06AzeHqITEXi12uM8RTPzq0=",
    "Sec-Ch-Ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

SLEEP_MIN = 30
SLEEP_MAX = 180

session = requests.Session()


def random_sleep():
    seconds = random.randint(SLEEP_MIN, SLEEP_MAX)
    print_msg(f"😴 sleep {seconds} seconds...")
    time.sleep(seconds)


def fetch_content(url: str) -> str:
    response = session.get(url, headers=BASE_HEADERS)
    random_sleep()
    return response.text


def fetch_home_urls(json_data: dict, debug: bool = False) -> list:
    query_json = json_data["search_query"]
    parameters = {
        "searchQueryState": query_json,
        "wants": {"cat1": ["listResults", "mapResults"], "cat2": ["total"]},
        # "requestId": 2,
    }
    fetch_url = BASE_URL + urlencode(parameters)
    response = session.get(fetch_url, headers=BASE_HEADERS)
    random_sleep()
    data = response.json()
    results = data["cat1"]["searchResults"]["mapResults"]
    total_count = data["cat1"]["searchList"]["totalResultCount"]
    total_pages = data["cat1"]["searchList"]["totalPages"]
    if debug:
        print_msg(
            f"[results_count]: {len(results)}, [total_count]: {total_count}, [total_pages]: {total_pages}"
        )
    home_urls = []
    result_count = total_count
    for detail in results:
        home_url = f"https://www.zillow.com{detail['detailUrl']}"
        if "www.zillow.com/community" in home_url:
            result_count -= 1
            if debug:
                print_msg(f"[found community url]: {home_url}")
                print_msg(f"[update result count]: {result_count}")
            continue
        home_urls.append(home_url)
    if debug:
        print_msg("[home urls]:")
        for url in home_urls:
            print_msg(url)
    if result_count != len(home_urls):
        print_msg("Result count not match with fetched urls!")
        print_msg(
            f"result_count: {result_count}, fetched: {len(home_urls)}\n{fetch_url}"
        )
    else:
        if debug:
            print_msg("[fetch home urls]: success")
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
        print_msg(f"Unable to parse the views count from url: {home_url}\n")
        # for dt_tag in dt_tags:
        #     print_msg(dt_tag)
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
