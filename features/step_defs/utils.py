from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


def try_to_handle_simple_captcha(driver: WebDriver):
    "this method passes a pop-up yandex captcha"
    try:
        driver.find_element(by=By.XPATH, value='//*[@id="js-button"]').click()
        sleep(3)
    except NoSuchElementException:
        pass


def filter_existence_check(driver: WebDriver):
    """
    sometimes the page with filters does not load correctly and reloading does not help,
    you can see example of this occasion in img/img.png,
    so this method checks whether the page has loaded and if not, the test is skipped
    :param driver:
    :return:
    """
    try:
        return driver.find_element(By.XPATH, '/html/body/div[2]/section/div[2]/div/div/div[2]/div[3]/div[9]/div/button').is_displayed()
    except NoSuchElementException:
        return False


def scroll_to_page_bottom(driver: WebDriver):
    len_of_page = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var len_of_page=document.body.scrollHeight;return len_of_page;")
    match = False
    while not match:
        last_count = len_of_page
        sleep(0.5)
        len_of_page = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var len_of_page=document.body.scrollHeight;return len_of_page;")
        if last_count == len_of_page:
            match = True
