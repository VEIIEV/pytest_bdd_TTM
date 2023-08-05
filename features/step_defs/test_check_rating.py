import time
from time import sleep
from pytest_bdd import parsers
import pytest
from pytest_bdd import scenario, given, when, then, scenarios
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from features.step_defs.utils import *

scenarios('../check_rating.feature')

PHONE_COUNTER: int = 0

CHOOSEN_PHONE_LINK: str


@given("Open market.yandex.ru")
def test_open_main_page(browser):
    driver: WebDriver = browser
    try_to_handle_simple_captcha(driver)
    driver.get('https://market.yandex.ru')
    try_to_handle_simple_captcha(driver)
    assert driver.title == 'Интернет-магазин Яндекс Маркет — покупки с быстрой доставкой'


@given('in the "Catalog → Electronics" section, select "Smartphones"')
def test_open_smartphone_section(browser):
    driver: WebDriver = browser
    try_to_handle_simple_captcha(driver)
    catalog_buttom = driver.find_element(by=By.XPATH,
                                         value='/html/body/div[2]/header/div[1]/div/div/noindex[1]/div/div/button')
    catalog_buttom.click()
    smartphone_link: WebElement = driver.find_element(by=By.XPATH, value="//a[contains(text(),'Смартфоны')]")
    smartphone_link.click()
    try_to_handle_simple_captcha(driver)
    assert driver.title == "Смартфоны — купить по низкой цене на Яндекс Маркете"


@given('go to "All Filters"')
def test_open_filters(browser):
    driver: WebDriver = browser
    try_to_handle_simple_captcha(driver)
    filters: WebElement = driver.find_element(by=By.XPATH,
                                              value="//aside[@id='searchFilters']/div/div[4]/div/div/div/div/a/button/span/span")
    filters.click()
    try_to_handle_simple_captcha(driver)
    assert driver.find_element(by=By.XPATH, value="//a[contains(text(),'Показать')]").is_displayed()


@then(parsers.parse("set the search parameter to {price} rubles"))
def test_set_price_border(browser, price: str):
    driver: WebDriver = browser
    try_to_handle_simple_captcha(driver)
    assert filter_existence_check(driver), 'filter page doesnt work'

    maxprice: WebElement = driver.find_element(by=By.XPATH, value='//div[2]/input')
    maxprice.click()
    maxprice.clear()
    maxprice.send_keys(price)
    maxprice.send_keys(Keys.ENTER)
    try_to_handle_simple_captcha(driver)
    assert maxprice.get_attribute('value') == price


@then(parsers.parse("the diagonal of the screen from {diagonal} inches"))
def test_set_diagonal(browser, diagonal):
    driver: WebDriver = browser
    try_to_handle_simple_captcha(driver)
    assert filter_existence_check(driver), 'filter page doesnt work'

    diagonal_expander = driver.find_element(
        By.XPATH, '/html/body/div[2]/section/div[2]/div/div/div[2]/div[1]/div[20]/div/button')
    if not diagonal_expander.get_attribute('aria-expanded'):
        diagonal_expander.click()

    wait = WebDriverWait(driver, timeout=5)
    min_diagonal = wait.until(
        expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="14805766"]/div/div[1]/input'))
    )
    min_diagonal.click()
    min_diagonal.clear()
    min_diagonal.send_keys(diagonal)
    min_diagonal.send_keys(Keys.ENTER)
    try_to_handle_simple_captcha(driver)
    assert min_diagonal.get_attribute('value') == diagonal


@then(parsers.parse("at least {amount} of any manufacturers"))
def test_set_manufacturers(browser, amount):
    driver: WebDriver = browser
    amount = int(amount)
    try_to_handle_simple_captcha(driver)
    assert filter_existence_check(driver), 'filter page doesnt work'

    if filter_existence_check(driver):
        wait = WebDriverWait(driver, timeout=5)
        checkbox_list: list[WebElement] = wait.until(
            expected_conditions.visibility_of_all_elements_located((By.XPATH, '//*[@id="7893318"]//input'))
        )
        for box in checkbox_list[0:amount]:
            box.click()
        sleep(5)


@then('click button "Show"')
def test_apply_selected_filters(browser):
    driver: WebDriver = browser
    try_to_handle_simple_captcha(driver)
    show_button = driver.find_element(by=By.XPATH, value="//a[contains(text(),'Показать')]")
    show_button.click()


@then("count smartphone on first page and remember last one from the list")
def test_count_smartphone(browser):
    global PHONE_COUNTER, CHOOSEN_PHONE_LINK
    driver: WebDriver = browser
    try_to_handle_simple_captcha(driver)
    scroll_to_page_bottom(driver)

    PHONE_COUNTER = len(driver.find_elements(By.XPATH, '//*[@id="searchResults"]/div/div/div/div/div/div')) - 1
    wait = WebDriverWait(driver, timeout=5)
    choosen_phone: WebElement = wait.until(expected_conditions.element_to_be_clickable(
        (By.XPATH, f'//*[@id="searchResults"]/div/div/div/div/div/div[{PHONE_COUNTER + 1}]//article/div[1]/h3/a'
         ))
    )
    CHOOSEN_PHONE_LINK = choosen_phone.get_attribute("href")


@then(parsers.parse("change sort type on sort by '{sort_type}'"))
def test_change_sort_type(browser, sort_type):
    driver: WebDriver = browser
    try_to_handle_simple_captcha(driver)
    driver.find_element(By.XPATH, f"//noindex/div/button[contains(text(),'{sort_type}')]").click()


@then("find and click on remembered object")
def test_click_on_remembered_object(browser):
    driver: WebDriver = browser
    try_to_handle_simple_captcha(driver)
    scroll_to_page_bottom(driver)

    try:
        wait = WebDriverWait(driver, timeout=5)
        choosen_phone: WebElement = wait.until(expected_conditions.element_to_be_clickable(
            (By.XPATH, f'//a[@href="{CHOOSEN_PHONE_LINK}"]'))
        )
    except TimeoutException:
        assert False, "No selected phone on page"
    # если элемент не кликабл, это делает его кликабл
    driver.execute_script("arguments[0].click();", choosen_phone)
    sleep(10)


@given("display the rating of the selected product")
def test_display_product_rating(browser):
    driver: WebDriver = browser
    try_to_handle_simple_captcha(driver)
    rating = driver.find_element(By.XPATH,
                                 '/html/body/div[2]/div[2]/main/div[4]/div/div/div[2]/div/div/div[2]/div[1]/div[1]/span[2]')
    print(rating.text)
