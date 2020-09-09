import time
import folium

from selenium import webdriver


WAITING_TIME = 1


def get_driver():
    """
    Get chrome driver

    Returns:
        browser object
    """

    # setup config
    option = webdriver.ChromeOptions()
    option.add_argument("--no-sandbox")
    option.add_argument("--headless")
    option.add_argument("--incognito")
    option.add_argument("--start-maximized")
    option.add_argument("--window-size=1920,1080")

    # load browser
    browser = webdriver.Remote("127.0.0.1:4444", option.to_capabilities())
    return browser


def save_map(m, name, driver):
    """
    Capture map

    Args:
        m: folium map object
        name: output name
        driver: selenium driver
    """

    m.save("./data/map.html")
    driver.get(f"file:///usr/src/app/data/map.html")
    time.sleep(WAITING_TIME)
    driver.save_screenshot(name)


def get_all_image(req):
    """
    Get all image

    Args:
        req: dictionary
    """
    zoom, lat1, long1, lat2, long2 = req['zoom'], req['lat1'], req['long1'], req['lat2'], req['long2']

    driver = get_driver()

    m = folium.Map(
        location=[(lat1 + lat2) / 2, (long1 + long2) / 2],
        zoom_start=zoom,
    )

    save_map(m, "./data/background-route.png", driver)

    folium.Circle((lat1, long1), 1).add_to(m)
    folium.Circle((lat2, long2), 1).add_to(m)

    save_map(m, "./data/target-route.png", driver)

