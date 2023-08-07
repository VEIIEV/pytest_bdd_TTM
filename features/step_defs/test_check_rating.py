from time import sleep

from pytest_bdd import given, then, scenarios
from pytest_bdd import parsers
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from features.step_defs.POM.yandex_page_model import YandexMainPage, YandexCatalogSmartphonePage, YandexFilterPage
from features.step_defs.utils import try_to_handle_simple_captcha, filter_existence_check, scroll_to_page_bottom

scenarios('../check_rating.feature')

PHONE_COUNTER: int = 0

SELECTED_PHONE_TEXT: str


# todo добавить скриншоты
# todo проверить что рейтинг выводится нормально

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
    YandexMainPage.get_catalog_button(driver).click()
    YandexMainPage.get_smartphone_link(driver).click()
    try_to_handle_simple_captcha(driver)
    assert driver.title == "Смартфоны — купить по низкой цене на Яндекс Маркете"


@given('go to "All Filters"')
def test_open_filters(browser):
    driver: WebDriver = browser
    try_to_handle_simple_captcha(driver)
    YandexCatalogSmartphonePage.get_filters(driver).click()
    try_to_handle_simple_captcha(driver)
    assert driver.find_element(by=By.XPATH, value="//a[contains(text(),'Показать')]").is_displayed()


@then(parsers.parse("set the search parameter to {price} rubles"))
def test_set_price_border(browser, price: str):
    driver: WebDriver = browser
    try_to_handle_simple_captcha(driver)
    assert filter_existence_check(driver), 'filter page doesnt work'

    maxprice: WebElement = YandexFilterPage.get_maxprice_from(driver)
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

    diagonal_expander = YandexFilterPage.get_diagonal_expander(driver)
    # todo убрать принты
    if not diagonal_expander.get_attribute('aria-expanded'):
        print(type(diagonal_expander.get_attribute('aria-expanded')))
        print(diagonal_expander.get_attribute('aria-expanded'))
        # если использовать простой diagonal_expander.click() не работает
        driver.execute_script("arguments[0].click();", diagonal_expander)

    min_diagonal = YandexFilterPage.get_min_diagonal_form(driver)
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
    global PHONE_COUNTER, SELECTED_PHONE_TEXT
    driver: WebDriver = browser
    try_to_handle_simple_captcha(driver)
    scroll_to_page_bottom(driver)

    PHONE_COUNTER = len(driver.find_elements(By.XPATH, '//*[@id="searchResults"]/div/div/div/div/div/div')) - 1
    selected_phone = YandexCatalogSmartphonePage.get_selected_phone(driver, PHONE_COUNTER)
    SELECTED_PHONE_TEXT = selected_phone.text


@then(parsers.parse("change sort type on sort by '{sort_type}'"))
def test_change_sort_type(browser, sort_type):
    driver: WebDriver = browser
    try_to_handle_simple_captcha(driver)
    YandexCatalogSmartphonePage.get_sort_button(driver, sort_type).click()


@then("find and click on remembered object")
def test_click_on_remembered_object(browser):
    driver: WebDriver = browser
    try_to_handle_simple_captcha(driver)
    scroll_to_page_bottom(driver)

    try:
        wait = WebDriverWait(driver, timeout=10)
        choosen_phone: WebElement = wait.until(expected_conditions.visibility_of_element_located(
            (By.XPATH, f"//a/span[contains(text(),'{SELECTED_PHONE_TEXT}')]/.."))
        )
    except TimeoutException:
        assert False, "No selected phone on page"
    # если элемент не кликабл, это делает его кликабл
    driver.execute_script("arguments[0].click();", choosen_phone)


@then("display the rating of the selected product")
def test_display_product_rating(browser):
    driver: WebDriver = browser
    try_to_handle_simple_captcha(driver)

    wait = WebDriverWait(driver, timeout=10)
    wait.until(expected_conditions.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])

    rating = wait.until(
        expected_conditions.visibility_of_element_located((
            By.XPATH, '/html/body/div[2]/div[2]/main/div[4]/div/div/div[2]/div/div/div[2]/div[1]/div[1]/span[2]'))
    )
    print(rating.text)
    sleep(10)
