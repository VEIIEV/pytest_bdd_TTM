import pytest
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import logging


@pytest.fixture()
def browser():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    driver.set_script_timeout(10)
    driver.maximize_window()
    yield driver
    driver.close()


# def pytest_logger_config(logger_config):
#     logger_config.add_loggers([''], stdout_level='INFO')
#     logger_config.set_log_option_default('')
#     logger_config.log_cli = True
#     logger_config.log_cli_level = 'INFO'
#     logger_config.log_cli_format = '%(asctime)s [%(levelname)s] %(message)s'
#     logger_config.log_cli_date_format = '%Y-%m-%d %H:%M:%S'
#
#     logger_config.log_file = 'pytest.log'
#     logger_config.log_file_level = 'INFO'
#     logger_config.log_file_format = '%(asctime)s [%(levelname)s] %(message)s'
#     logger_config.log_file_date_format = '%Y-%m-%d %H:%M:%S'
