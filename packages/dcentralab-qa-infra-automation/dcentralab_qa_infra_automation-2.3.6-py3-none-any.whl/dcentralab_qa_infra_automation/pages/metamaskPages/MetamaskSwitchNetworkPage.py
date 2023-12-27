from dcentralab_qa_infra_automation.fixtures.InitGlobalParameters import get_logger
from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
allow the site to switch the network page

@Author: Efrat Cohen
@Date: 12.2022
"""

"""page locators"""
METAMASK_SWITCH_NETWORK_CONTAINER_CONTENT = (By.CLASS_NAME, "confirmation-page__content")
METAMASK_SWITCH_NETWORK_CONTAINER_TITLE = (By.CSS_SELECTOR, ".confirmation-page__content h3")
METAMASK_SWITCH_NETWORK_CONTAINER_SWITCH_BUTTON = (
    By.CSS_SELECTOR, ".confirmation-footer__actions .btn-primary")


class MetamaskSwitchNetworkPage(BasePage):

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
        if ("confirmation" in url and
                self.is_element_exist("METAMASK_SWITCH_NETWORK_CONTAINER_CONTENT",
                                      METAMASK_SWITCH_NETWORK_CONTAINER_CONTENT) and
                "switch" in self.get_text("METAMASK_SWITCH_NETWORK_CONTAINER_TITLE",
                                          METAMASK_SWITCH_NETWORK_CONTAINER_TITLE)):
            self.logger.info(f"{self.__class__.__name__} is loaded")
            return True
        else:
            self.logger.warning(f"{self.__class__.__name__} is not loaded")
            return False

    def click_on_switch_network_button(self):
        """
        click on switch network button
        """
        if "switch" in self.get_text("METAMASK_SWITCH_NETWORK_CONTAINER_SWITCH_BUTTON",
                                     METAMASK_SWITCH_NETWORK_CONTAINER_SWITCH_BUTTON).lower():
            self.click("METAMASK_SWITCH_NETWORK_CONTAINER_SWITCH_BUTTON",
                       METAMASK_SWITCH_NETWORK_CONTAINER_SWITCH_BUTTON)
