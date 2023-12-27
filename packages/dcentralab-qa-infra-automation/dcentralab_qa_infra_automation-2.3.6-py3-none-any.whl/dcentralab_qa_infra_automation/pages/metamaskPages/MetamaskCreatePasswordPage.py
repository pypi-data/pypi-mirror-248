import pytest
from dcentralab_qa_infra_automation.fixtures.InitGlobalParameters import get_logger
from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
create password page

@Author: Efrat Cohen
@Date: 07.2023
"""

"""page locators"""
METAMASK_CREATE_PASSWORD_CONTAINER = (By.CLASS_NAME, "create-password__wrapper")
METAMASK_NEW_PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-testid='create-password-new']")
METAMASK_CONFIRM_PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-testid='create-password-confirm']")
METAMASK_UNDERSTAND_CHECKBOX = (By.CSS_SELECTOR, "[data-testid='create-password-terms']")
METAMASK_IMPORT_WALLET_BTN = (By.CLASS_NAME, "create-password__form--submit-button")


class MetamaskCreatePasswordPage(BasePage):

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
        if self.is_element_exist("METAMASK_CREATE_PASSWORD_CONTAINER", METAMASK_CREATE_PASSWORD_CONTAINER):
            self.logger.info(f"{self.__class__.__name__} is loaded")
            return True
        else:
            self.logger.warning(f"{self.__class__.__name__} is not loaded")
            return False

    def insert_password(self):
        """
        insert password
        """
        self.enter_text("METAMASK_NEW_PASSWORD_INPUT", METAMASK_NEW_PASSWORD_INPUT,
                        pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("password"))

    def insert_confirm_password(self):
        """
        insert confirm password
        """
        self.enter_text("METAMASK_CONFIRM_PASSWORD_INPUT", METAMASK_CONFIRM_PASSWORD_INPUT,
                        pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("password"))

    def click_on_understand_metamask_checkbox(self):
        """
        click on understand metamask checkbox
        """
        self.click("METAMASK_UNDERSTAND_CHECKBOX", METAMASK_UNDERSTAND_CHECKBOX)

    def click_on_import_wallet(self):
        """
        click on import wallet
        """
        self.click("METAMASK_IMPORT_WALLET_BTN", METAMASK_IMPORT_WALLET_BTN)
