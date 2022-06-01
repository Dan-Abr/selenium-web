# import requests (uninstalled)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from .models import DOMElement

def crawl_website(url, find_element_class):
    options = webdriver.ChromeOptions()
    options.add_argument(" - incognito ")

    browser = webdriver.Chrome(executable_path="./chromedriver", chrome_options=options)

    browser.get(url)

    timeout = 10
    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, find_element_class),
            )
        )
    except TimeoutException:
        print("waiting to load")
        browser.quit()

    elements = browser.find_elements_by_xpath(find_element_class)
    print(elements)

    # Store crawled data in the database
    # DOMElement.objects.create(
    #     source=url,
    #     link=url,
    #     title="title",
    # )