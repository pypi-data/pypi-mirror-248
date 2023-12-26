from dcentralab_qa_infra_automation.fixtures.InitGlobalParameters import get_logger
from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
welcome page

@Author: Efrat Cohen
@Date: 06.2023
"""

"""page locators"""
NAMI_WELCOME_TITLE = (By.XPATH, "//*[contains(@class, 'chakra-text css-1mmhjtn')]")
NAMI_IMPORT_WALLET_BTN = (By.XPATH, "//button[contains(text(),'Import')]")
NAMI_IMPORT_A_WALLET_POPUP_TITLE = (By.ID, "chakra-modal--header-12")
NAMI_CHOOSE_SEED_PHRASE_SELECT = (By.CSS_SELECTOR, "select.chakra-select")
NAMI_ACCEPT_TERMS_BTN = (By.CLASS_NAME, "chakra-checkbox__control")
NAMI_CONTINUE_BUTTON = (
    By.XPATH, "//footer[contains(@class,'chakra-modal__footer')]//button[contains(text(), 'Continue')]")


class NamiWelcomePage(BasePage):

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
        if "welcome" in url and self.is_element_exist("NAMI_WELCOME_TITLE", NAMI_WELCOME_TITLE):
            self.logger.info(f"{self.__class__.__name__} is loaded")
            return True
        else:
            self.logger.info(f"{self.__class__.__name__} is not loaded")
            return False

    def click_on_import_wallet(self):
        """
        click on import wallet button
        """
        if self.is_element_exist("NAMI_IMPORT_WALLET_BTN",NAMI_IMPORT_WALLET_BTN):
            self.click("NAMI_IMPORT_WALLET_BTN", NAMI_IMPORT_WALLET_BTN)

    def is_import_a_wallet_popup_loaded(self):
        """
        check is import a wallet popup loaded
        """
        if self.is_element_exist("NAMI_IMPORT_A_WALLET_POPUP_TITLE", NAMI_IMPORT_A_WALLET_POPUP_TITLE):
            return True
        else:
            return False

    def click_on_choose_seed_phrase_length(self):
        """
        click on choose seed phrase length
        """
        if self.is_element_exist("NAMI_CHOOSE_SEED_PHRASE_SELECT",NAMI_CHOOSE_SEED_PHRASE_SELECT):
            self.click("NAMI_CHOOSE_SEED_PHRASE_SELECT", NAMI_CHOOSE_SEED_PHRASE_SELECT)

    def choose_word_seed_phrase(self,seed_phrase_length):
        """
        choose word seed phrase
        """
        NAMI_WORD_SEED_PHRASE_OPTION = (By.CSS_SELECTOR, f"select.chakra-select option[value='{seed_phrase_length}']")

        self.click("WORD_SEED_PHRASE_OPTION", NAMI_WORD_SEED_PHRASE_OPTION)

    def click_on_accept_terms_button(self):
        """
        click on accept terms button
        """
        self.click("ACCEPT_TERMS_BTN", NAMI_ACCEPT_TERMS_BTN)

    def click_on_continue_button(self):
        """
        click on continue button
        """
        self.click("CONTINUE_BUTTON", NAMI_CONTINUE_BUTTON)
