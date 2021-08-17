import time
from typing import Union, Tuple, List

from multipledispatch import dispatch
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """
    Class with all common methods for all pages
    """

    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url: str):
        """
        Opens url in browser
        :param url: url which will be opened
        """
        self.driver.get(url)
    # -----------------------------------------------------------------

    @dispatch(WebElement)
    def find_element(self, element: WebElement) -> WebElement:
        """
        Returns the same element. Added to have possibility to use method universally for finding element
        :param element: already found Webelement
        :return: already found Webelement
        """
        return element
    # -----------------------------------------------------------------

    @dispatch(tuple)
    def find_element(self, element_locator: Tuple[By, str], wait_time=10, skip_exception=False) -> \
            Union[WebElement, None]:
        """
        Finds element on the page
        :param element_locator: (By.___, value) Locator with type of search from By class and value for this class
        :param wait_time: max time for element wait
        :param skip_exception: in case of element absence if True - returns None, if False - raise exception
        :return: Element or None
        :raise: TimeoutException in case of absence and skip_exception - False
        """
        try:
            return WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located(element_locator),
                                                               message=f"Can't find element with {element_locator}")
        except TimeoutException as err:
            if not skip_exception:
                print(f"Element was not found in {wait_time} seconds")
                raise err
            return None
    # -----------------------------------------------------------------

    @dispatch(list[WebElement])
    def find_elements(self, elements: List[WebElement]) -> List[WebElement]:
        """
        Returns the same list of elements. Added to have possibility to use method universally for finding element
        :param element: already found list of Webelements
        :return: already found list of Webelements
        """
        return elements
    # -----------------------------------------------------------------

    @dispatch(tuple)
    def find_elements(self, elements_locator: Tuple[By, str], wait_time=10, skip_exception=False) -> List[WebElement]:
        """
        Finds elements on the page
        :param elements_locator: (By.___, value) Locator with type of search from By class and value for this class
        :param wait_time: max time for element wait
        :param skip_exception: in case of elements absence if True - returns [], if False - raise exception
        :return: list of Elements
        :raise: TimeoutException in case of absence and skip_exception - False
        """
        try:
            return WebDriverWait(self.driver, wait_time).until(EC.presence_of_all_elements_located(elements_locator),
                                                               message=f"Can't find elements with {elements_locator}")
        except TimeoutException as err:
            if not skip_exception:
                print(f"Elements was not found in {wait_time} seconds")
                raise err
            return []
    # -----------------------------------------------------------------

    def click_element(self, element: Union[WebElement, Tuple[By, str]]):
        """
        Click element on the page
        :param element: already found element or locator for searching
        """
        element = self.find_element(element)
        element.click()
    # -----------------------------------------------------------------

    def input_text(self, element: Union[WebElement, Tuple[By, str]], text: str):
        """
        Click element on the page
        :param element: already found element or locator for searching
        :param text: string which will be entered
        """
        element = self.find_element(element)
        element.send_keys(text)
    # -----------------------------------------------------------------

    def get_element_text(self, element: Union[WebElement, Tuple[By, str]]) -> str:
        """
        Returns innerText of the element
        :param element: already found element or locator for searching
        :return: innerText of the element
        """
        element = self.find_element(element)
        return element.get_attribute('innerText')
    # -----------------------------------------------------------------

    def get_elements_text(self, elements: Union[List[WebElement], Tuple[By, str]]) -> List[str]:
        """
        Returns innerText of the all found elements
        :param elements: already found elements or locator for searching
        :return: innerText of the elements
        """
        elements = self.find_elements(elements)
        return [element.get_attribute('innerText') for element in elements]
    # -----------------------------------------------------------------

    def find_element_inside_element(self, parent_element: Union[WebElement, Tuple[By, str]],
                                    child_element_locator: Tuple[By, str], wait_time=10,
                                    skip_exception=False) -> Union[WebElement, None]:
        """
        Searches for element inside element
        :param parent_element: already found parent element or locator for searching it
        :param child_element_locator: (By.___, value) Locator with type of search from By class and value for this class
        :param wait_time: max time for element wait
        :param skip_exception: in case of element absence if True - returns None, if False - raise exception
        :return: Element or None
        :raise: TimeoutException in case of absence and skip_exception - False
        """
        parent_element = self.find_element(parent_element)
        for i in range(wait_time):
            by_type, value = child_element_locator
            if by_type == By.CSS_SELECTOR:
                child = parent_element.find_element_by_css_selector(value)
            elif by_type == By.XPATH:
                child = parent_element.find_element_by_xpath(value)
            else:
                child = parent_element.find_element(child_element_locator)
            if child:
                return child
            time.sleep(1)
        else:
            if not skip_exception:
                raise TimeoutException(f'Element was not found in {wait_time} seconds')
            return None
    # -----------------------------------------------------------------

    def find_elements_inside_element(self, parent_element: Union[WebElement, Tuple[By, str]],
                                     children_element_locator: Tuple[By, str], wait_time=10,
                                     skip_exception=False) -> List[WebElement]:
        """
        Searches for elements inside element
        :param parent_element: already found parent element or locator for searching it
        :param children_element_locator: (By.___, value) Locator with type of search from By class and value for
                this class
        :param wait_time: max time for element wait
        :param skip_exception: in case of elements absence if True - returns [], if False - raise exception
        :return: list of found Webelements
        :raise: TimeoutException in case of absence and skip_exception - False
        """
        parent_element = self.find_element(parent_element)
        for i in range(wait_time):
            by_type, value = children_element_locator
            if by_type == By.CSS_SELECTOR:
                children = parent_element.find_elements_by_css_selector(value)
            elif by_type == By.XPATH:
                children = parent_element.find_elements_by_xpath(value)
            else:
                children = parent_element.find_elements(children_element_locator)
            if len(children):
                return children
            time.sleep(1)
        else:
            if not skip_exception:
                raise TimeoutException(f'Elements was not found in {wait_time} seconds')
            return []
# -----------------------------------------------------------------

    def switch_to_the_tab(self, tab_number=-1):
        """
        Switch to the tab in browser by number
        :param tab_number: number of tab in order, default - the last one
        """
        self.driver.switch_to.window(self.driver.window_handles[tab_number])

