from dcentralab_qa_infra_automation.fixtures.InitGlobalParameters import get_logger
from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
Set a spending cap for your page

@Author: Efrat Cohen
@Date: 09.2023
"""

"""page locators"""
METAMASK_TOKEN_APPROVAL_CONTAINER = (By.CLASS_NAME, "token-allowance-container")
METAMASK_TOKEN_APPROVAL_SPENDING_CAP_CONTAINER = (By.CLASS_NAME, "custom-spending-cap")
METAMASK_TOKEN_APPROVAL_SPENDING_CAP_INPUT = (By.CSS_SELECTOR, "[data-testid='custom-spending-cap-input']")
METAMASK_TOKEN_APPROVAL_SPENDING_CAP_MAX_BTN = (By.CLASS_NAME, "custom-spending-cap__max")
METAMASK_TOKEN_APPROVAL_SPENDING_CAP_NEXT_BTN = (By.CSS_SELECTOR, "[data-testid='page-container-footer-next']")
METAMASK_TOKEN_APPROVAL_SPENDING_CAP_REVIEW = (By.CSS_SELECTOR, "[data-testid='page-container-footer-next']")


class MetamaskSetSpendingCapPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)
        self.logger = get_logger(self.__class__.__name__)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        url = self.driver.current_url
        self.logger.info(f"Verify if {self.__class__.__name__} is loaded")
        if ("approve" in url and self.is_element_exist("METAMASK_TOKEN_APPROVAL_CONTAINER",
                                                       METAMASK_TOKEN_APPROVAL_CONTAINER) and
                self.is_element_exist("METAMASK_TOKEN_APPROVAL_SPENDING_CAP_CONTAINER",
                                      METAMASK_TOKEN_APPROVAL_SPENDING_CAP_CONTAINER) and
                self.is_element_exist("METAMASK_TOKEN_APPROVAL_SPENDING_CAP_INPUT",
                                      METAMASK_TOKEN_APPROVAL_SPENDING_CAP_INPUT) and
                self.is_element_exist("METAMASK_TOKEN_APPROVAL_SPENDING_CAP_MAX_BTN",
                                      METAMASK_TOKEN_APPROVAL_SPENDING_CAP_MAX_BTN)):
            self.logger.info(f"{self.__class__.__name__} is loaded")
            return True
        else:
            self.logger.warning(f"{self.__class__.__name__} is not loaded")
            return False

    def click_max_button(self):
        """
        choose max custom spending cap
        """
        self.click("METAMASK_TOKEN_APPROVAL_SPENDING_CAP_MAX_BTN", METAMASK_TOKEN_APPROVAL_SPENDING_CAP_MAX_BTN)

    def click_next_button(self):
        """
        click on next button
        """
        if "next" in self.get_text("METAMASK_TOKEN_APPROVAL_SPENDING_CAP_NEXT_BTN",
                                   METAMASK_TOKEN_APPROVAL_SPENDING_CAP_NEXT_BTN).lower():
            self.click("METAMASK_TOKEN_APPROVAL_SPENDING_CAP_NEXT_BTN", METAMASK_TOKEN_APPROVAL_SPENDING_CAP_NEXT_BTN)

    def click_approve_button(self):
        """
        click on approve button
        """
        if "approve" in self.get_text("METAMASK_TOKEN_APPROVAL_SPENDING_CAP_NEXT_BTN",
                                      METAMASK_TOKEN_APPROVAL_SPENDING_CAP_NEXT_BTN):
            self.click("METAMASK_TOKEN_APPROVAL_SPENDING_CAP_NEXT_BTN", METAMASK_TOKEN_APPROVAL_SPENDING_CAP_NEXT_BTN)
