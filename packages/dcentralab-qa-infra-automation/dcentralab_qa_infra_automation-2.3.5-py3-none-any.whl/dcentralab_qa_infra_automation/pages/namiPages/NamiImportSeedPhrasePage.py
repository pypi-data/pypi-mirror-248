from dcentralab_qa_infra_automation.fixtures.InitGlobalParameters import get_logger
from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
import seed phrase page

@Author: Efrat Cohen
@Date: 06.2023
"""

"""page locators"""
NAMI_IMPORT_WALLET_CONTAINER_TITLE = (
    By.XPATH, "//*[contains(@class,'chakra-text css-yefpd7') and contains(text(),'Import')]")
NAMI_SEED_PHRASE_INPUTS = (By.CLASS_NAME, "chakra-input")
NAMI_IMPORT_WALLET_NEXT_BUTTON = (By.XPATH, "//button[contains(@class,'chakra-button') and contains(text(),'Next')]")


class NamiImportSeedPhrasePage(BasePage):

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
        if "import" in url and self.is_element_exist("NAMI_IMPORT_WALLET_CONTAINER_TITLE",
                                                     NAMI_IMPORT_WALLET_CONTAINER_TITLE):
            self.logger.info(f"{self.__class__.__name__} is loaded")
            return True
        else:
            self.logger.warning(f"{self.__class__.__name__} is not loaded")
            return False

    def insert_word_seed_phrase(self, seed_phrase_list):
        """
        :param seed_phrase_list: list of words to import wallet
        :return:
        """
        for index in range(0, len(seed_phrase_list)):
            word = seed_phrase_list.get(f"seed_phrase_{index + 1}")
            self.enter_text_on_specific_list_item(f"SEED_PHRASE_WORDS_{index + 1}", NAMI_SEED_PHRASE_INPUTS, index,
                                                  word)

    def click_on_next_button(self):
        """
        click on next button
        """
        self.click("NAMI_IMPORT_WALLET_NEXT_BUTTON", NAMI_IMPORT_WALLET_NEXT_BUTTON)
