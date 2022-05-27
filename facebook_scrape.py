from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

path = 'C:/Users/deauy/Documents/perky/chromedriver.exe'
options = webdriver.ChromeOptions()
service = Service(path)
options.add_argument("window-size=1200x600")
driver = webdriver.Chrome(service=service, options = options)

driver.get("https://www.facebook.com")
driver.maximize_window()
driver.implicitly_wait(20)

try:
    accept_cookie = driver.find_element(By.CSS_SELECTOR, 'button[data-cookiebanner="accept_only_essential_button"]')
    accept_cookie.click()
except NoSuchElementException:
    print('there are no coookies to accept')

email = input('email: ')
password = input('password: ')

sleep(1.5)
username = driver.find_element(By.ID, 'email')
username.send_keys(email)


password = driver.find_element(By.ID, 'pass')
password.send_keys(password+Keys.ENTER)

sleep(1.5)

market = driver.find_element(By.CSS_SELECTOR, 'a[href="/marketplace/?ref=app_tab"]')
market.click()

sleep(2.5)
search = driver.find_element(By.CSS_SELECTOR, 'label input[placeholder="Search Marketplace"]')
search.send_keys('iphone'+Keys.ENTER)

sleep(5)

ScrollNumber = 50
for i in range(1,ScrollNumber):
    driver.execute_script("window.scrollTo(1,50000)")
    sleep(5)

from bs4 import BeautifulSoup as BS
import pandas as pd

soup = BS(driver.page_source, 'lxml')

driver.quit()

#with open('fb_source.txt', 'wb') as file:
    #file.write(soup.encode('utf-8'))

products = soup.find_all('div', {'class':"b3onmgus ph5uu5jm g5gj957u buofh1pr cbu4d94t rj1gh0hx j83agx80 rq0escxv fnqts5cd fo9g3nie n1dktuyu e5nlhep0 ecm0bbzt"})

link = [item.find('a', {'role':'link'}).get('href') if item.find('a', {'role':'link'}) != None else 'Nan' for item in products]

location = [item.find('div', {'class':'a8nywdso e5nlhep0 rz4wbd8a ecm0bbzt'}).string if item.find('div', {'class':'a8nywdso e5nlhep0 rz4wbd8a ecm0bbzt'}) != None else 'NaN' for item in products]

price = [item.find('span', {'class':'j83agx80'}).string if item.find('span', {'class':'j83agx80'}) != None else 'NaN' for item in products]

device_model = [item.find('div', {'class':'a8nywdso e5nlhep0 rz4wbd8a linoseic'}).string if item.find('div', {'class':'a8nywdso e5nlhep0 rz4wbd8a linoseic'}) != None else 'NaN' for item in products]

import pandas as pd

df = pd.DataFrame({'link':link[:-8], 'location':location[:-8], 'price':price[:-8], 'device_model':device_model[:-8]})

df

df.to_csv('iphone_for_sale.csv')
