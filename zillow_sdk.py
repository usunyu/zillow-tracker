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
    "Cookie": "zguid=24|%2454742c34-784c-4577-affc-1142d3ec37ad; _ga=GA1.2.316644807.1695510265; zjs_anonymous_id=%2254742c34-784c-4577-affc-1142d3ec37ad%22; zjs_user_id=null; zg_anonymous_id=%22876ad884-3ce7-400d-91d8-a50ce492a07b%22; _gcl_au=1.1.857535933.1695510265; _pxvid=89f92519-5a65-11ee-b80e-1bfbd30aa557; __pdst=832fc926c5394551b90e92e28f55e973; _pin_unauth=dWlkPU9UZGlaV016WkRVdE1XVmxPQzAwWlRjd0xXRm1Nakl0TWpBNE1XSTFPRGs1WTJJNA; _cs_c=0; _cs_id=233648d7-1680-a2b1-fa09-ee81d75368fa.1695510849.1.1695511483.1695510849.1.1729674849675; _gac_UA-21174015-56=1.1696214508.CjwKCAjwseSoBhBXEiwA9iZtxqLj4d079H4GnZUzx43r9IlJbyF03vkprcpBFDZw1lsqCiqVMZ3pqBoCFyAQAvD_BwE; _gcl_aw=GCL.1696214508.CjwKCAjwseSoBhBXEiwA9iZtxqLj4d079H4GnZUzx43r9IlJbyF03vkprcpBFDZw1lsqCiqVMZ3pqBoCFyAQAvD_BwE; search=6|1701037188829%7Crect%3D37.749364187468444%252C-122.3914230472412%252C37.69444021829437%252C-122.49184495275878%26rid%3D97567%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26sort%3Ddays%26z%3D1%26listPriceActive%3D1%26days%3D30%26type%3Dhouse%252Cmultifamily%26price%3D0-1250000%26mp%3D0-6930%26fs%3D0%26fr%3D0%26mmm%3D0%26rs%3D1%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%0997567%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Atrue%7D%09%09%09%09%09; x-amz-continuous-deployment-state=AYABeAfaO%2FmRbD9ABpU8Hki%2FEdwAPgACAAFEAB1kM2Jsa2Q0azB3azlvai5jbG91ZGZyb250Lm5ldAABRwAVRzA3MjU1NjcyMVRZRFY4RDcyVlpWAAEAAkNEABpDb29raWUAAACAAAAADDgTvuNYIQGbGvF%2FnwAwrPQEKKOkVSvQJ3eyO3FW3e4vcQyqaoVPUkgg87l6o0xzrBkesxfo2jC6gSyUFVM1AgAAAAAMAAQAAAAAAAAAAAAAAAAAAAGqFKHWnOoG7IC56m9h7n7%2F%2F%2F%2F%2FAAAAAQAAAAAAAAAAAAAAAQAAAAz+VVf2wbrEsQ1xpftPG%2FNIf6pRyW4dy+fh+SH2NIf6pRyW4dy+fh+SHw==; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; pxcts=29ce86e7-889b-11ee-b118-4dc8a5926211; _pxff_rf=1; _pxff_fp=1; _pxff_cfp=1; _pxff_bsco=1; zgsession=1|8bc5d985-8423-4167-b1b8-e730f8a29125; _gid=GA1.2.1729537383.1700591107; DoubleClickSession=true; _gat=1; _uetsid=4c058930889b11eeba931d8cef87f630; _uetvid=8ba7eb005a6511eebca6e381cf8ef374; _hp2_id.1215457233=%7B%22userId%22%3A%224023631568943192%22%2C%22pageviewId%22%3A%222162112454410282%22%2C%22sessionId%22%3A%221761690463337622%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _hp2_ses_props.1215457233=%7B%22ts%22%3A1700591107199%2C%22d%22%3A%22www.zillow.com%22%2C%22h%22%3A%22%2F%22%7D; _clck=8pvrzc%7C2%7Cfgw%7C0%7C1361; _clsk=rpblzv%7C1700591108069%7C1%7C0%7Cb.clarity.ms%2Fcollect; _px3=2a2c06735d70bd3281130bbb1754724bb3ef4b19a5f5b1469efc6e485280d48d:Cj1mVuJcnLDRa6UwxUqbPti2vq4iJ6n5V0rrbB0e6G1shPGsK7XAoncbLqa/DgkVWj4IfWWaf2w3NFAbq/p/JQ==:1000:T7VUiX5xRA9fWLnpTZzR4H5p22lJEgsj8y7ayIiS1Yy7D/JO6KG+xRe/QQ//tei3GpvLOJNHudlEWGa+qrcuET3E9kgqYFiUep04mivjkNWy1piqvHYJotbXuAdnfVkFBB4cRKESbi7am3kqL/dL4BTb/vAvcPUxW4TkZlkldJBgZsckCo+n314Ni/JIfdyqHGZMzxGp4FutQ1ixgc0KFEDh2H77BHhqUwH3lg76Vu0=; JSESSIONID=9A876DAAC29D761071FF03717FE4B47B; AWSALB=7U0w7Km1UT23r+05r479rpldTzzUCmjzPYsKBnbIAagr7FnX47hFsuGKn9lnV7DHs926kcOzzpTio23XSvgPTmoLc3NhqXpzCGEKotD2zng5HhKcE5kjkPfnplHE; AWSALBCORS=7U0w7Km1UT23r+05r479rpldTzzUCmjzPYsKBnbIAagr7FnX47hFsuGKn9lnV7DHs926kcOzzpTio23XSvgPTmoLc3NhqXpzCGEKotD2zng5HhKcE5kjkPfnplHE",
    "Sec-Ch-Ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
}

SLEEP_MIN = 30
SLEEP_MAX = 180

session = requests.Session()


def fetch_content(url: str) -> str:
    response = session.get(url, headers=BASE_HEADERS)
    time.sleep(random.randint(SLEEP_MIN, SLEEP_MAX))
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
    time.sleep(random.randint(SLEEP_MIN, SLEEP_MAX))
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
