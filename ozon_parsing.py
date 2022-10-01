import json
import time

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

list_of_os = []


def search(obj):
    if isinstance(obj, list):
        for list_item in obj:
            try_eval(list_item)
    elif isinstance(obj, dict):
        for dict_value in obj.values():
            try_eval(dict_value)
    elif isinstance(obj, str):
        if 'Android ' in obj or 'iOS ' in obj:
            list_of_os.append(obj)


def try_eval(obj):
    try:
        convert = eval(obj)
    except Exception as e:
        search(obj)
    else:
        search(convert)


def get_html(link, wait_time):
    print(link)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--enable-javascript')
    options.add_argument(
        "--user-agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0'")
    driver = webdriver.Chrome(service=Service('/Users/foxmac/Desktop/chromedriver'), options=options)
    driver.get(link)
    time.sleep(wait_time)
    full_html = driver.page_source
    driver.close()
    soup = bs(full_html, 'html.parser')
    return soup


page_counter = 1
while len(list_of_os) <= 100:
    soup = get_html(f'https://www.ozon.ru/category/smartfony-15502/?page={page_counter}&sorting=rating',
                    12)
    div = soup.find('div', attrs={"data-widget": "megaPaginator"})
    links = set()
    for a in div.find_all('a', href=True):
        if '/product/smartfon' in a['href'] and 'comments' not in a['href']:
            links.add(a['href'])

    for link in list(links):
        api_link = f'https://www.ozon.ru/api/composer-api.bx/page/json/v2?url=' \
                   f'{link}%26layout_container%3DpdpPage2column%26layout_page_index%3D2%26sh%3DS1Doouzrjw'
        soup = get_html(api_link, 4)
        json_data = soup.find('pre').string
        array_from_api = json.loads(json_data)
        try_eval(array_from_api)
        print(list_of_os)
    page_counter += 1

res = sorted(list(list_of_os), reverse=True)
print(res)
