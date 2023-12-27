from dcentralab_qa_infra_automation.fixtures.InitGlobalParameters import get_logger
from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
create account page

@Author: Efrat Cohen
@Date: 06.2023
"""

"""page locators"""
NAMI_CREATE_WALLET_ACCOUNT_TITLE = (
    By.XPATH, "//*[contains(@class,'chakra-text') and contains(text(), 'Create Account')]")
NAMI_CREATE_WALLET_ACCOUNT_NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Enter account name']")
NAMI_CREATE_WALLET_ACCOUNT_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[placeholder='Enter password']")
NAMI_CREATE_WALLET_ACCOUNT_CONFIRM_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[placeholder='Confirm password']")
NAMI_CREATE_WALLET_ACCOUNT_CREATE_BUTTON = (
    By.XPATH, "//button[contains(@class,'chakra-button') and contains(text(), 'Create')]")


class NamiCreateAccountPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)
        self.logger = get_logger(self.__class__.__name__)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        self.logger.info(f"Verify if {self.__class__.__name__} is loaded")
        url = self.driver.current_url
        if "account" in url and self.is_element_exist("NAMI_CREATE_WALLET_ACCOUNT_TITLE",
                                                      NAMI_CREATE_WALLET_ACCOUNT_TITLE):
            self.logger.info(f"{self.__class__.__name__} is loaded")
            return True
        else:
            self.logger.warning(f"{self.__class__.__name__} is not loaded")
            return False

    def insert_account_name(self, account_name):
        """
        insert account name
        """
        self.enter_text("NAMI_CREATE_WALLET_ACCOUNT_NAME_INPUT", NAMI_CREATE_WALLET_ACCOUNT_NAME_INPUT, account_name)

    def insert_password(self, password):
        """
        insert password
        """
        self.enter_text("NAMI_CREATE_WALLET_ACCOUNT_PASSWORD_INPUT", NAMI_CREATE_WALLET_ACCOUNT_PASSWORD_INPUT,
                        password)

    def insert_confirm_password(self, password):
        """
        insert confirm password
        """
        self.enter_text("NAMI_CREATE_WALLET_ACCOUNT_CONFIRM_PASSWORD_INPUT",
                        NAMI_CREATE_WALLET_ACCOUNT_CONFIRM_PASSWORD_INPUT, password)

    def click_on_create_button(self):
        """
        click on create button
        """
        self.click("NAMI_CREATE_WALLET_ACCOUNT_CREATE_BUTTON", NAMI_CREATE_WALLET_ACCOUNT_CREATE_BUTTON)
