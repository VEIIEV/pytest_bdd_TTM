import pytest
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver


@pytest.fixture()
def browser():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(3)
    driver.set_script_timeout(3)
    driver.maximize_window()
    yield driver
    driver.close()
