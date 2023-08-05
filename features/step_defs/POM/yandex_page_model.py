# selenium 4
from time import sleep

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# todo: сделать POM который имеет в переменных: основные кнопки, filter = который хранит кнопки фильтра
# todo: вынести в  фикстуру подключение драйвера и заход на главную страницу

class YandexMarketPage:
    pass