# selenium 4
from time import sleep

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# todo: сделать POM который имеет в переменных: основные кнопки, filter = который хранит кнопки фильтра
# todo: вынести в  фикстуру подключение драйвера и заход на главную страницу

class YandexMainPage:

    @classmethod
    def get_catalog_button(cls, driver: WebDriver):
        return driver.find_element(By.XPATH, '/html/body/div[2]/header/div[1]/div/div/noindex[1]/div/div/button')

    @classmethod
    def get_smartphone_link(cls, driver: WebDriver):
        return driver.find_element(By.XPATH, "//a[contains(text(),'Смартфоны')]")


class YandexFilterPage:
    @classmethod
    def do_something(cls, driver: WebDriver):
        return


class YandexCatalogSmartphone:
    pass