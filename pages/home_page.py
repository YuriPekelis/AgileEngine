from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.career_page import CareerPage


class HomePageLocator:
    PAGE_URL = 'https://agileengine.com/'
    CAREER_BTN = (By.CSS_SELECTOR, '#nav-menu-item-11631 .menu-link')


class HomePage(BasePage):

    def open_page(self):
        self.open_url(HomePageLocator.PAGE_URL)
        return self

    def go_to_career(self):
        self.click_element(HomePageLocator.CAREER_BTN)
        return CareerPage(self.driver)
