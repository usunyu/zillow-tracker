import time
import random
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup

BASE_URL = "https://www.zillow.com/search/GetSearchPageState.htm?"

# we should use browser-like request headers to prevent being instantly blocked
BASE_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6",
    "Cache-Control": "max-age=0",
    "Cookie": "x-amz-continuous-deployment-state=AYABeNzKKtSNVqJS6sPG2aelgzEAPgACAAFEAB1kM2Jsa2Q0azB3azlvai5jbG91ZGZyb250Lm5ldAABRwAVRzA3MjU1NjcyMVRZRFY4RDcyVlpWAAEAAkNEABpDb29raWUAAACAAAAADKlNlg9f8+76iLZ0kQAwGsQWxO5J9ywFefoq7j%2FPmSgKSlDyjJpPL2SDnqMXjPgt2ixmXD2Jy%2FIqZinazcVvAgAAAAAMAAQAAAAAAAAAAAAAAAAAAK8e2GniAIJHvg34VdOGv0r%2F%2F%2F%2F%2FAAAAAQAAAAAAAAAAAAAAAQAAAAxWoj3fteNztUfm3kJpLaOPd+W9d8+pEyxsBb6NW9d8+pEyxsBb6A==; zguid=24|%2454742c34-784c-4577-affc-1142d3ec37ad; _ga=GA1.2.316644807.1695510265; zjs_anonymous_id=%2254742c34-784c-4577-affc-1142d3ec37ad%22; zjs_user_id=null; zg_anonymous_id=%22876ad884-3ce7-400d-91d8-a50ce492a07b%22; _gcl_au=1.1.857535933.1695510265; _pxvid=89f92519-5a65-11ee-b80e-1bfbd30aa557; __pdst=832fc926c5394551b90e92e28f55e973; _pin_unauth=dWlkPU9UZGlaV016WkRVdE1XVmxPQzAwWlRjd0xXRm1Nakl0TWpBNE1XSTFPRGs1WTJJNA; _cs_c=0; _cs_id=233648d7-1680-a2b1-fa09-ee81d75368fa.1695510849.1.1695511483.1695510849.1.1729674849675; _gac_UA-21174015-56=1.1696214508.CjwKCAjwseSoBhBXEiwA9iZtxqLj4d079H4GnZUzx43r9IlJbyF03vkprcpBFDZw1lsqCiqVMZ3pqBoCFyAQAvD_BwE; _gcl_aw=GCL.1696214508.CjwKCAjwseSoBhBXEiwA9iZtxqLj4d079H4GnZUzx43r9IlJbyF03vkprcpBFDZw1lsqCiqVMZ3pqBoCFyAQAvD_BwE; _gid=GA1.2.1133447200.1696992840; _clck=8pvrzc|2|ffr|0|1361; JSESSIONID=92E267AC78A28AC92331164A7C6B23FE; zgsession=1|95c167db-5d48-4acc-b6b4-118719548cc5; pxcts=46c7ae67-6857-11ee-8c3a-43c02e24d7fe; DoubleClickSession=true; search=6|1699636692461%7Crect%3D37.76779728453276%252C-122.39190101623535%252C37.710782078079546%252C-122.59274482727051%26rid%3D20330%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26sort%3Ddays%26z%3D1%26listPriceActive%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%0997586%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Atrue%7D%09%09%09%09%09; x-amz-continuous-deployment-state=AYABeDBIpGfzQLwqFRt8wXNQ4AUAPgACAAFEAB1kM2Jsa2Q0azB3azlvai5jbG91ZGZyb250Lm5ldAABRwAVRzA3MjU1NjcyMVRZRFY4RDcyVlpWAAEAAkNEABpDb29raWUAAACAAAAADMZp5NLtkAbk9brT7AAwIIZ+po2PTI3MH4h9g9yeF0Kr9ufigoActvbjQ4gToPyCjEdYDax1IU38VUNLY4LOAgAAAAAMAAQAAAAAAAAAAAAAAAAAACD%2FJdCTcHwuefCkUCWLnkL%2F%2F%2F%2F%2FAAAAAQAAAAAAAAAAAAAAAQAAAAyZ9C3wXD5885%2F1dIZkGHEnE2+7Hl1BHS93FVTc+7Hl1BHS93FVTQ==; _gat=1; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; _pxff_cfp=1; _pxff_bsco=1; _hp2_ses_props.1215457233=%7B%22ts%22%3A1697044872991%2C%22d%22%3A%22www.zillow.com%22%2C%22h%22%3A%22%2F%22%7D; _hp2_id.1215457233=%7B%22userId%22%3A%224023631568943192%22%2C%22pageviewId%22%3A%225641240171515229%22%2C%22sessionId%22%3A%221777427097607832%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _uetsid=6f4f9f5067e111eeba751fcd3ecdc8d1; _uetvid=8ba7eb005a6511eebca6e381cf8ef374; _clsk=odd27m|1697044884090|7|0|u.clarity.ms/collect; _px3=c0933b031c21b5a2a88e57ffe3cd25b1eb46462a68a9574708dfc7ea5b7345ff:iOT0T8rt/96oH0K+IyETMHYo37ZcMZxKZ2WhAtORaTDq32TNvuQ0iXkWi41OO+WpQ54M3Lx9CDlnXimOITcDCg==:1000:syBk5Vz+43Iy5pcFt/Y65bAEl3qsELoioVcph5wBN6k/w2/JEWpgMjK/U+quAp1Prg3Tx4f/9y/ULD19KhcS8YqxldrXThoDHeR74hrN05LdLxIHa/5N//Hz/sFn49NXo3UEhm5uAKYn5kdMopMUw0r0C6uIKAuQGNQWWNaxJs3hP+rXvdG09Pxpb49BD2J2zobo8ZBDIu5NmTH1wRmTOtljusKu6P5bT+k6oedEDf0=; AWSALB=DhHCICTOX17BKTow+szmlP8AJS+yDmzmrwiJvWMtHTEA00ERpvbiXWsZq1w3Ko7ux0PHqusEhL8gmX1bMT53/R0MJfL4sdDAprW4si0g75C95T/HVmSVjAhQSzYy; AWSALBCORS=DhHCICTOX17BKTow+szmlP8AJS+yDmzmrwiJvWMtHTEA00ERpvbiXWsZq1w3Ko7ux0PHqusEhL8gmX1bMT53/R0MJfL4sdDAprW4si0g75C95T/HVmSVjAhQSzYy",
    "Sec-Ch-Ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
}

session = requests.Session()


def fetch_content(url: str) -> str:
    response = session.get(url, headers=BASE_HEADERS)
    time.sleep(random.randint(1, 15))
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
    time.sleep(random.randint(1, 15))
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
        print(f"result_count: {result_count}, fetched: {len(home_urls)}\n{fetch_url}")
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
