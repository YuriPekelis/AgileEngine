import pytest
from selenium import webdriver

# Path to the ChromeDriver has to be added here
CHROME_DRIVER_PATH = ''


@pytest.fixture(scope='module')
def browser():
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    yield driver
    driver.quit()
