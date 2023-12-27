from dcentralab_qa_infra_automation.fixtures.InitGlobalParameters import get_logger
from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
welcome to metamask page

@Author: Efrat Cohen
@Date: 12.2022
"""

"""page locators"""
WELCOME_TO_METAMASK_TITLE = (By.CLASS_NAME, "onboarding-welcome")
METAMASK_MASCOT_LOGO = (By.CLASS_NAME, "onboarding-welcome__mascot")
METAMASK_AGREE_TERMS_CHECKBOX = (By.ID, "onboarding__terms-checkbox")
METAMASK_IMPORT_WALLET_BUTTON = (By.CSS_SELECTOR, "[data-testid='onboarding-import-wallet']")


class WelcomeToMetamaskPage(BasePage):

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
        if (self.is_element_exist_with_custom_timeout("WELCOME_TO_METAMASK_TITLE", WELCOME_TO_METAMASK_TITLE,
                                                      self.timeout + 30) and
                "get started" in self.get_text("WELCOME_TO_METAMASK_TITLE", WELCOME_TO_METAMASK_TITLE) and
                self.is_element_exist("METAMASK_MASCOT_LOGO", METAMASK_MASCOT_LOGO)):

            self.logger.info(f"{self.__class__.__name__} loaded")
            return True
        else:
            self.logger.warning(f"{self.__class__.__name__} not loaded")
            return False

    def click_on_agree_terms(self):
        """
        click on agree terms button
        """
        self.click("METAMASK_AGREE_TERMS_CHECKBOX", METAMASK_AGREE_TERMS_CHECKBOX)

    def is_button_exists(self):
        return self.is_element_exist("METAMASK_IMPORT_WALLET_BUTTON", METAMASK_IMPORT_WALLET_BUTTON)

    def click_on_import_wallet(self):
        """
        click on import wallet button
        """
        self.click("METAMASK_IMPORT_WALLET_BUTTON", METAMASK_IMPORT_WALLET_BUTTON)
