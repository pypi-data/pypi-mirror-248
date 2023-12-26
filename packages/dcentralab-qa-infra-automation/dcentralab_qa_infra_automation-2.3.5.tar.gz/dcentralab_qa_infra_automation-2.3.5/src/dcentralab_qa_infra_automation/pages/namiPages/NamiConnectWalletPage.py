import pytest
from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
connect wallet popup

@Author: Efrat Cohen
@Date: 06.2023
"""

"""page locators"""
ACCEPT_BTN = (By.XPATH, "//button[contains(@class,'chakra-button') and contains(text(), 'Access')]")


class NamiConnectWalletPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        NAMI_CONNECT_WALLET_POPUP_WALLET_NAME = (By.XPATH,
                                                 f"//div[contains(@class, 'chakra-text') and "
                                                 f"contains(text(),"
                                                 f"'{pytest.wallets_data.get('cardano').get('account_name')}')]")
        NAMI_CONNECT_WALLET_POPUP_URL = (By.XPATH, f"//div[contains(@class,'chakra-text') and "
                                                   f"contains(text(),'{pytest.properties.get('site.chainport.url')}')]")

        if (self.is_element_exist("NAMI_CONNECT_WALLET_POPUP_WALLET_NAME",
                                  NAMI_CONNECT_WALLET_POPUP_WALLET_NAME) and self.is_element_exist(
                "NAMI_CONNECT_WALLET_POPUP_URL", NAMI_CONNECT_WALLET_POPUP_URL) and
                self.is_element_exist("ACCEPT_BTN", ACCEPT_BTN)):
            return True
        else:
            return False

    def click_on_accept_button(self):
        """
        click on accept button
        """
        self.click("ACCEPT_BTN", ACCEPT_BTN)
