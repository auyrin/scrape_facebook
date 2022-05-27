from requests_html import AsyncHTMLSession as AHS
from time import sleep

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.amazon.com/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}
url = 'https://www.amazon.com/s?k=dynamic+microphone'

def slice(text):
    slice_loc = text.find('\n')
    return text[:slice_loc]

def strip_(item):
    slice_loc = item.find('$')
    return item[slice_loc:slice_loc*2]

pages = 7

s = AHS()
links = []
ratings = []
price = []
device_name = []
for num in range(1, pages+1):
    full_url = url+f'&page={num}'
    r = await s.get(full_url, headers = headers)
    sleep(5)

    try:
        await r.html.arender()
    except:
        print('run render outside a loop next time')
    sleep(5)

    products = r.html.find('div.s-main-slot.s-result-list.s-search-results.sg-row div.sg-col-4-of-12 div.a-section.a-spacing-base')

    device_model_text = [item.xpath('//h2/a/span')[0].text for item in products ]
    device_name.extend([slice(item) for item in device_model_text])

    price_text = [item.xpath('//div/a/span/span')[0].text for item in products ]
    price.extend([strip_(slice(item).lstrip('$')) for item in price_text])

    ratings_text = [item.xpath('//div/span/span/a/i/span')[0].text for item in products ]
    ratings.extend([slice(item) for item in ratings_text])

    node_link = [item.xpath('//h2/a/@href')[0] for item in products ]
    links.extend(['https://www.amazon.com'+item for item in node_link])

    sleep(5)

s.close()

import pandas as pd

df = pd.DataFrame({'product_link': links, 'device_decription': device_name, 'price': price, 'ratings': ratings})

df.to_csv('dynamic_mics_amazon.csv')
