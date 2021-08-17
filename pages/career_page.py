from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.open_positions_page import OpenPositionsPage


class CareerPageLocator:
    SEARCH_INPUT_FLD = (By.CSS_SELECTOR, '#home-search-input')
    SEARCH_BTN = (By.CSS_SELECTOR, '#homepage-search-btn')


class CareerPage(BasePage):

    def search_career(self, position_type):
        self.input_text(CareerPageLocator.SEARCH_INPUT_FLD, position_type)
        self.click_element(CareerPageLocator.SEARCH_BTN)
        self.switch_to_the_tab()
        return OpenPositionsPage(self.driver)
