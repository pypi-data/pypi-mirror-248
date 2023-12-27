from dcentralab_qa_infra_automation.fixtures.InitGlobalParameters import get_logger
from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
Nami base page

@Author: Efrat Cohen
@Date: 06.2023
"""

"""page locators"""
NAMI_WALLET_BASE_PAGE_MENU_BUTTON = (By.ID, "menu-button-8")
NAMI_WALLET_MENU_SETTINGS_OPTION = (By.ID, "menu-list-8-menuitem-12")


class NamiBasePage(BasePage):

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
        if "wallet" in url and self.is_element_exist("MENU_BUTTON", NAMI_WALLET_BASE_PAGE_MENU_BUTTON):
            self.logger.info(f"{self.__class__.__name__} is loaded")
            return True
        else:
            self.logger.waring(f"{self.__class__.__name__} is not loaded")
            return False

    def click_on_menu(self):
        """
        click on menu button
        """
        self.click("NAMI_WALLET_BASE_PAGE_MENU_BUTTON", NAMI_WALLET_BASE_PAGE_MENU_BUTTON)

    def click_on_setting(self):
        """
        click on settings
        """
        if self.is_element_exist("NAMI_WALLET_MENU_SETTINGS_OPTION", NAMI_WALLET_MENU_SETTINGS_OPTION):
            self.click("NAMI_WALLET_MENU_SETTINGS_OPTION", NAMI_WALLET_MENU_SETTINGS_OPTION)
