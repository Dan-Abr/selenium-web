# standard-library
import time

# third-party
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Django
from django.contrib.auth.models import User

# local Django
from .models import E2ETestResultsModel


def crawl_website(user_pk, url, tasks):
    # The user who requested the task
    user = User.objects.get(pk=user_pk)

    # User settings
    user_options = webdriver.ChromeOptions()
    user_options.add_argument(' - incognito ')

    # System Settings
    driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=user_options)
    
    # Open URL
    timeout = 30
    error_list = []
    try:
        driver.get(url)
        driver.set_page_load_timeout(timeout)
    except TimeoutException:
        error_list.append("Timeout.")

    # Perform crawling tasks (wait, click)
    error_list = perform_actions(driver, tasks, timeout, error_list)
    # Quit
    driver.quit()

    # Summarize results
    post_results_to_db(user, url, error_list)


def perform_actions(driver, tasks, timeout, error_list):
    # Perform crawling tasks (wait, click)
    for task in tasks:
        # Each task has only one dict inside
        task = list(task.items())[0]
        # Python supports match-case from v3.1, however
        # Microsoft VSCode isn't supporting its syntax yet.
        # Source: https://github.com/microsoft/vscode-python/issues/17745
        if(task[0] == '1'):
            # Wait
            try:
                time.sleep(task[1])
            except TimeoutException:
                error_list.append("Timeout.")
                # driver.quit()
            except Exception as e:
                error_list.append(str(e))
        elif(task[0] == '2'):
            # Click
            try:
                driver.find_element_by_xpath(task[1]).click()
            except TimeoutException as e:
                error_list.append("Timeout.")
                # driver.quit()
            except Exception as e:
                error_list.append(str(e))
    return error_list


def post_results_to_db(user, url, error_list):
    if len(error_list) == 0:
        E2ETestResultsModel.objects.create(
            url=url,
            page_title="title",
            status="Success",
            # e2e_test_params = test_id,
            user=user,
        )
    else:
        E2ETestResultsModel.objects.create(
            url=url,
            page_title="title",
            status="Failed",
            failed_details="".join(str(error) for error in error_list),
            # failed_details="Failed",
            # e2e_test_params = test_id,
            user=user,
        )


