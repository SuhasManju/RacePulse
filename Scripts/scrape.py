from Race.models import *
import requests
from bs4 import BeautifulSoup as bs
import os

banned_url = "/en/latest/tags/"

def fill_driver_image(year):
    BASE_URL = "https://www.formula1.com/en/drivers"
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


def fill_circuit_image(year):
    BASE_URL = "https://www.formula1.com/en/racing/2025/{circuit_id}/circuit"
    races = Race.objects.filter(year=year).select_related("circuit", "circuit__country")

    os.makedirs(f"static/circuit_img", exist_ok=True)


    # <img alt="Australia_Circuit.png" src="https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_771/content/dam/fom-website/2018-redesign-assets/Circuit maps 16x9/Australia_Circuit">


    for race in races:
        c_name =race.circuit_id
        url = BASE_URL.format(circuit_id=race.circuit_id)

        res = requests.get(url)

        if res.status_code != 200:
            c_name = race.circuit.country.name.lower()
            url = BASE_URL.format(circuit_id=race.circuit.country.name.lower())
            res = requests.get(url)

        print(url)

        if res.status_code != 200:
            print(f"{race.official_name} {race.circuit.country.name} image not found")
            print(race.circuit.country.pk)
            print()
            continue

        print(race.official_name, "Successs")

        soup = bs(res.content, "html.parser")
        images = soup.find_all('img')
        circuit_image = None
        for img in images:
            alt = img.get('alt','').lower()
            if f"{c_name}_circuit.png" in alt:
                circuit_image = img.get('src', '')
                break

        if not circuit_image:
            print(f"{race.official_name} {race.circuit.country.name} image not found")
            print(race.circuit.country.pk)
            print()
            continue
        

        img_source = requests.get(circuit_image).content
        with open(f"static/circuit_img/{race.circuit.pk}.avif", "wb") as f:
            f.write(img_source)


def fill_team_image(year):
    BASE_URL = "https://media.formula1.com/image/upload/f_auto,c_limit,q_75,w_1320/content/dam/fom-website/2018-redesign-assets/team logos/"

    teams = SeasonConstructor.objects.filter(
        year=year).select_related("constructor")

    os.makedirs(f"static/team_img", exist_ok=True)

    for t in teams:
        name = t.constructor.name.lower().split(" ")
        name = " ".join(name)
        url = BASE_URL + f"{name}"
        res = requests.get(url)
        print(url)

        if res.status_code != 200:
            print(f"Image not found for: {name}")
            continue

        with open(f"static/team_img/{t.constructor.pk}.avif", "wb") as f:
            f.write(res.content)
