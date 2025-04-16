from Race.models import *
import requests
from bs4 import BeautifulSoup as bs
import os

BASE_URL = "https://www.formula1.com/en/drivers"
banned_url = "/en/latest/tags/"

def fill_driver_image(year):
    drivers = SeasonDriver.objects.filter(year=year).select_related('driver')

    os.makedirs(f"static/driver_img", exist_ok=True)

    for d in drivers:
        name_list = [d.driver.first_name, d.driver.last_name]
        url_name = "-".join(name_list).lower()
        driver_name = " ".join(name_list).lower()
        url = f"{BASE_URL}/{url_name}"

        # <img alt="Liam Lawson" src="https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/fom-website/drivers/2025Drivers/lawson-racing-bulls" 
        # class="f1-c-image aspect-square laptop:aspect-4/3 desktop:aspect-16/10 w-full overflow-hidden object-cover object-top">
        res = requests.get(url)
        if res.status_code != 200:
            print(f"{d.driver.full_name} image not found")
            print(d.driver_id)
            continue
        soup = bs(res.content, "html.parser")
        images = soup.find_all('img')
        driver_image = None
        for img in images:
            alt = img.get('alt','').lower()
            if driver_name in alt:
                driver_image = img.get('src', '')
                break

        img_src = requests.get(driver_image).content
        with open(f"static/driver_img/{d.driver_id}.avif", "wb") as f:
            f.write(img_src)
        


