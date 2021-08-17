import random
import time

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.position_page import PositionPage


class OpenPositionsPageLocator:
    FILTER_BTN = (By.CSS_SELECTOR, '#show-filters-btn')
    FILTER_CATEGORIES_SHOWN_DRP_DWN = (By.CSS_SELECTOR, '.awsm-filter-item.filter-active')
    FILTER_CATEGORIES_UNHOLD_BTN = (By.CSS_SELECTOR, '.awsm-selectric-arrow-drop')
    FILTER_CATEGORIES_OPTIONS = (By.CSS_SELECTOR, '.awsm-selectric-scroll li')
    POSITION_SHOW_BTN = (By.CSS_SELECTOR, '.awsm-job-more')
    POSITION_TITLE = (By.CSS_SELECTOR, '.awsm-job-item .awsm-job-post-title')
    SEARCH_BTN = (By.CSS_SELECTOR, '#homepage-search-btn')

    LOCATION_TEXT = 'location'


class OpenPositionsPage(BasePage):

    def filter_found_positions(self, filters):
        if not self.find_element(OpenPositionsPageLocator.FILTER_CATEGORIES_SHOWN_DRP_DWN, skip_exception=True):
            self.click_element(OpenPositionsPageLocator.FILTER_BTN)
        self._choose_filters(filters)
        time.sleep(2)  # instead of this it is better to find some condition, but I haven't found what could be changed
        return self

    def _choose_filters(self, filters):
        category_drp_dwns = self.find_elements(OpenPositionsPageLocator.FILTER_CATEGORIES_SHOWN_DRP_DWN)
        for category_name, choosing_value in filters.items():
            found_filters = [elem for elem in category_drp_dwns if category_name in self.get_element_text(elem)]
            if len(found_filters) != 1:
                raise Exception(f"Has to be found 1 dropdown with {category_name} bit found {len(found_filters)}")
            unhold_btn = self.find_element_inside_element(found_filters[0],
                                                          OpenPositionsPageLocator.FILTER_CATEGORIES_UNHOLD_BTN)
            self.click_element(unhold_btn)
            options = self.find_elements_inside_element(found_filters[0],
                                                        OpenPositionsPageLocator.FILTER_CATEGORIES_OPTIONS)
            found_options = [option for option in options if choosing_value in self.get_element_text(option)]
            if len(found_options) != 1:
                raise Exception(f"Has to be found 1 option with value {choosing_value} for filter {category_name}, "
                                f"but found {len(found_options)}")
            self.click_element(found_options[0])

    def get_all_positions_title(self):
        return self.get_elements_text(OpenPositionsPageLocator.POSITION_TITLE)

    def choose_random_position(self):
        positions_show_btns = self.find_elements(OpenPositionsPageLocator.POSITION_SHOW_BTN)
        idx = random.choice(range(len(positions_show_btns)))
        print(f"Chosen position with number {idx}")
        self.click_element(positions_show_btns[idx])
        return PositionPage(self.driver)
