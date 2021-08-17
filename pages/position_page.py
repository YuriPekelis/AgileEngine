from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class PositionPageLocator:
    APPLY_BTN = (By.CSS_SELECTOR, '[class="sidebar-main"] #single-job-apply-btn')
    APPLY_SIDEBAR = (By.CSS_SELECTOR, '#single-job-apply.single-job-active')
    APPLY_SIDEBAR_FIRST_NAME_FLD = (By.CSS_SELECTOR, 'input[aria-label="First Name"]')
    APPLY_SIDEBAR_LAST_NAME_FLD = (By.CSS_SELECTOR, 'input[aria-label="Last Name"]')
    APPLY_SIDEBAR_EMAIL_FLD = (By.CSS_SELECTOR, 'input[aria-label="Email"]')
    APPLY_SIDEBAR_PHONE_FLD = (By.CSS_SELECTOR, 'input[aria-label="Phone"]')
    APPLY_SIDEBAR_LINKEDIN_FLD = (By.CSS_SELECTOR, 'input[aria-label="LinkedIn URL"]')
    APPLY_SIDEBAR_BROWSE_BTN = (By.CSS_SELECTOR, '#theFile_link\(Attach\ resume\)')
    APPLY_SIDEBAR_POLICY_CHKBOX = (By.CSS_SELECTOR, '#policy')
    APPLY_SIDEBAR_SUBMIT_BTN = (By.CSS_SELECTOR, '.blubtn[type="submit"]')


class PositionPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.apply_side_bar = None

    def open_apply_sidebar(self):
        self.click_element(PositionPageLocator.APPLY_BTN)
        self.apply_side_bar = ApplySidebar(self.driver)
        return self

    def get_apply_position_flds_visibility(self):
        return self.apply_side_bar.get_elements_presence()


class ApplySidebar(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.form = self.find_element(PositionPageLocator.APPLY_SIDEBAR)

    def get_elements_presence(self):
        form_elements_locator_names = ['APPLY_SIDEBAR_FIRST_NAME_FLD', 'APPLY_SIDEBAR_LAST_NAME_FLD',
                                       'APPLY_SIDEBAR_EMAIL_FLD', 'APPLY_SIDEBAR_PHONE_FLD',
                                       'APPLY_SIDEBAR_LINKEDIN_FLD', 'APPLY_SIDEBAR_BROWSE_BTN']
        presence_state = {}
        for element_name in form_elements_locator_names:
            is_element_present = bool(self.find_element(getattr(PositionPageLocator, element_name),
                                                        wait_time=2, skip_exception=True))
            presence_state[element_name] = is_element_present
        return presence_state
