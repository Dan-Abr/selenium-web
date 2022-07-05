# third-party
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Django
from django.contrib.auth.models import User

# local Django
from .models import E2ETestResultsModel


def crawl_website(user_pk, url, find_element_class):
    # The user who requested the task
    user = User.objects.get(pk=user_pk)

    options = webdriver.ChromeOptions()
    options.add_argument(' - incognito ')

    browser = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)

    browser.get(url)

    timeout = 10
    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, find_element_class),
            )
        )

        elements = browser.find_elements_by_xpath(find_element_class)

        # Store crawled data in the database
        E2ETestResultsModel.objects.create(
            url=url,
            page_title="title",
            status="Success",
            # e2e_test_params = e2e_test_params_model_obj,
            user=user,
        )

    except TimeoutException:
        print("waiting to load")
        browser.quit()

        E2ETestResultsModel.objects.create(
            url=url,
            page_title="title",
            status="Failed",
            # e2e_test_params = e2e_test_params_model_obj,
            user=user,
        )

