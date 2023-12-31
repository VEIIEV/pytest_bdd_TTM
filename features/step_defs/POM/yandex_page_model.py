# selenium 4

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class YandexMainPage:
    # catalog_button: WebElement
    # smartphone_link: WebElement
    #
    # def __init__(self, driver: WebDriver):
    #     if driver.title == 'Интернет-магазин Яндекс Маркет — покупки с быстрой доставкой':
    #         self.catalog_button = driver.find_element(By.XPATH,
    #                                                   '/html/body/div[2]/header/div[1]/div/div/noindex[1]/div/div/button')
    #         self.smartphone_link = driver.find_element(By.XPATH, "//a[contains(text(),'Смартфоны')]")
    #     super().__init__()

    @classmethod
    def get_catalog_button(cls, driver: WebDriver) -> WebElement:
        return driver.find_element(By.XPATH, '/html/body/div[2]/header/div[1]/div/div/noindex[1]/div/div/button')

    @classmethod
    def get_smartphone_link(cls, driver: WebDriver) -> WebElement:
        return driver.find_element(By.XPATH, "//a[contains(text(),'Смартфоны')]")


class YandexFilterPage:
    @classmethod
    def get_maxprice_from(cls, driver: WebDriver) -> WebElement:
        return driver.find_element(by=By.XPATH, value='//div[2]/input')

    @classmethod
    def get_diagonal_expander(cls, driver: WebDriver) -> WebElement:
        wait = WebDriverWait(driver, timeout=5)
        return wait.until(
            expected_conditions.visibility_of_element_located((
                By.XPATH, '/html/body/div[2]/section/div[2]/div/div/div[2]/div[1]/div[20]/div/button'))
        )

    @classmethod
    def get_min_diagonal_form(cls, driver: WebDriver) -> WebElement:
        wait = WebDriverWait(driver, timeout=5)
        return wait.until(
            expected_conditions.element_to_be_clickable((
                By.XPATH, '//*[@id="14805766"]/div/div[1]/input'))
        )


class YandexCatalogSmartphonePage:

    @classmethod
    def get_selected_phone(cls, driver: WebDriver, number) -> WebElement:
        wait = WebDriverWait(driver, timeout=5)
        return wait.until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, f'//*[@id="searchResults"]/div/div/div/div/div/div[{number + 1}]//article/div[1]/h3/a'))
        )

    @classmethod
    def get_filters(cls, driver: WebDriver) -> WebElement:
        return driver.find_element(by=By.XPATH,
                                   value="//aside[@id='searchFilters']/div/div[4]/div/div/div/div/a/button/span/span")

    @classmethod
    def get_sort_button(cls, driver: WebDriver, sort_type):
        """"""
        return driver.find_element(By.XPATH, f"//noindex/div/button[contains(text(),'{sort_type}')]")
