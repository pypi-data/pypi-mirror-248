from dcentralab_qa_infra_automation.fixtures.InitGlobalParameters import get_logger
from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
successfully created wallet page

@Author: Efrat Cohen
@Date: 06.2023
"""

"""page locators"""
NAMI_SUCCESSFUL_PLANET_ICON = (By.ID, "kawaii-planet")
NAMI_SUCCESSFUL_CONTAINER_CLOSE_BUTTON = (
By.XPATH, "//button[contains(@class,'chakra-button') and contains(text(), 'Close')]")


class NamiSuccessfullyCreatedWalletPage(BasePage):

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

        if self.is_element_exist("NAMI_SUCCESSFUL_PLANET_ICON", NAMI_SUCCESSFUL_PLANET_ICON):
            self.logger.info(f"{self.__class__.__name__} is loaded")
            return True
        else:

            self.logger.warning(f"{self.__class__.__name__} is not loaded")
            return False

    def click_on_close_button(self):
        """
        click on close button
        """
        self.click("NAMI_SUCCESSFUL_CONTAINER_CLOSE_BUTTON", NAMI_SUCCESSFUL_CONTAINER_CLOSE_BUTTON)
