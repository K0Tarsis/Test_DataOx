import time
import peewee

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pygsheet import *
from datetime import datetime
from models import *


service = Service('chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")
driver = webdriver.Chrome(service=service, options=options)


def main():

    try:
        url = "https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273"
        driver.get(url)

        while True:
            time.sleep(3)

            container = driver.find_elements(By.CLASS_NAME, "container-results")[1]
            items = container.find_elements(By.CLASS_NAME, 'clearfix')

            for item in items:

                try:
                    pict_url = item.find_element(By.CLASS_NAME, "image").find_element(By.TAG_NAME, "img").get_attribute('data-src')
                    if pict_url is None:
                        pict_url = 'Dont Have Pict'
                except Exception:
                    pict_url = 'Dont Have Pict'

                title = item.find_element(By.CLASS_NAME, 'title').text.strip()
                dt_str = item.find_element(By.CLASS_NAME, 'location').find_elements(By.TAG_NAME, 'span')[-1].text

                try:
                    date = datetime.strptime(dt_str, '%d/%m/%Y').strftime('%d-%m-%Y')
                except Exception:
                    date = datetime.now().strftime('%d-%m-%Y')

                city = item.find_element(By.CLASS_NAME, 'location').find_element(By.TAG_NAME, 'span').text.strip()
                try:
                    beds = int(item.find_element(By.CLASS_NAME, 'bedrooms').text.split(' ')[-1])
                except Exception:
                    beds = 1
                description = item.find_element(By.CLASS_NAME, 'description').text.strip()
                price_all = item.find_element(By.CLASS_NAME, 'price').text.replace(",", "")

                try:
                    price = round(float(price_all[1:]), 2)
                    currency = price_all[0]

                except Exception:
                    price = 0
                    currency = '0'

                row = Apartment(title=title, pict_url=pict_url,
                                city=city, beds=beds, description=description,
                                price=price, currency=currency, date=date)
                row.save()

                write_google_sheet([title, pict_url, city, beds, description, price, currency, date])

                # print(f"URL: {pict_url} \nTitle: {title} \nDate: {date} "
                #       f"\nCity: {city} \nBeds: {beds} \nDesc: {description} \nPrice: {price}")

            try:
                driver.get(driver.find_element(By.LINK_TEXT, 'Next >').get_attribute('href'))
                print('NEXT')

            except NoSuchElementException:
                print('End of pagin')

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":

    try:
        dbhandle.connect()
        Apartment.create_table()

    except peewee.InternalError as px:
        print(str(px))

    main()

    sh.share('kostiantyn.hovorukha@gmail.com', role='writer')
