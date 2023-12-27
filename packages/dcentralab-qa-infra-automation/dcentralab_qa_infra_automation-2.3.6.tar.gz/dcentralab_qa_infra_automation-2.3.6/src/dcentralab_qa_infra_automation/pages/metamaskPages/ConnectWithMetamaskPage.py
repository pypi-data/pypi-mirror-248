
import pytest
from dcentralab_qa_infra_automation.fixtures.InitGlobalParameters import get_logger
from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
connect with metamask page

@Author: Efrat Cohen
@Date: 12.2022
"""

"""page locators"""
METAMASK_CONNECT_WALLET_PERMISSIONS_CONTAINER = (By.CLASS_NAME, "permissions-connect")
METAMASK_CONNECT_WALLET_PERMISSIONS_CONTAINER_TITLE = (By.CLASS_NAME, "permissions-connect-header__title")
METAMASK_CONNECT_WALLET_PERMISSIONS_CONTAINER_NEXT_BUTTON = (
    By.XPATH, "//button[contains(@class,'btn-primary') and contains(text(),'Next')]")
METAMASK_CONNECT_WALLET_PERMISSIONS_CONTAINER_CONNECT_BUTTON = (
    By.CSS_SELECTOR, "[data-testid='page-container-footer-next']")
CONNECT_WITH_METAMASK_EXTENSION_BUTTON = (By.XPATH, "//*[contains(text(),'Connect With MetaMask Extension')]")


class ConnectWithMetamaskPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)
        self.logger = get_logger(self.__class__.__name__)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        self.logger.info(f"Verify if {self.__class__.__name__} is loaded ")
        url = self.driver.current_url
        if ("connect" in url and self.is_element_exist("CONNECT_WALLET_PERMISSIONS_CONTAINER",
                                                       METAMASK_CONNECT_WALLET_PERMISSIONS_CONTAINER) and
                "MetaMask" in self.get_text("CONTAINER_TITLE", METAMASK_CONNECT_WALLET_PERMISSIONS_CONTAINER_TITLE)):
            self.logger.info(f"{self.__class__.__name__} is loaded")
            return True
        else:
            self.logger.warning(f"{self.__class__.__name__} is not loaded.")
            return False

    def click_on_connect_with_metamask_extension_button(self):
        """
        click on connect with metamask extension popup button
        """
        # If the popup exists
        if self.is_element_exist_with_custom_timeout("CONNECT_WITH_METAMASK_EXTENSION_BUTTON",
                                                     CONNECT_WITH_METAMASK_EXTENSION_BUTTON,
                                                     pytest.properties.get("timeout") / 10):
            # Click on the button
            self.click("CONNECT_WITH_METAMASK_EXTENSION_BUTTON", CONNECT_WITH_METAMASK_EXTENSION_BUTTON)

    def click_on_next_button(self):
        """
        click on next button
        """
        # If the popup exists
        if self.is_element_exist_with_custom_timeout("METAMASK_CONNECT_WALLET_PERMISSIONS_CONTAINER_NEXT_BUTTON",
                                                     METAMASK_CONNECT_WALLET_PERMISSIONS_CONTAINER_NEXT_BUTTON,
                                                     self.timeout / 10):
            self.click("METAMASK_CONNECT_WALLET_PERMISSIONS_CONTAINER_NEXT_BUTTON",
                       METAMASK_CONNECT_WALLET_PERMISSIONS_CONTAINER_NEXT_BUTTON)

    def click_on_connect_button(self):
        """
        click on connect button
        """
        url = self.driver.current_url
        if ("confirm-permissions" in url and "Connect" in
                self.get_text("METAMASK_CONNECT_WALLET_PERMISSIONS_CONTAINER_CONNECT_BUTTON)",
                              METAMASK_CONNECT_WALLET_PERMISSIONS_CONTAINER_CONNECT_BUTTON)):
            self.click("METAMASK_CONNECT_WALLET_PERMISSIONS_CONTAINER_CONNECT_BUTTON",
                       METAMASK_CONNECT_WALLET_PERMISSIONS_CONTAINER_CONNECT_BUTTON)
