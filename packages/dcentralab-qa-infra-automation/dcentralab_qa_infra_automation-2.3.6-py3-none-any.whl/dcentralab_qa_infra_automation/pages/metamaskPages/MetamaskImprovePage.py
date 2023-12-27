from dcentralab_qa_infra_automation.fixtures.InitGlobalParameters import get_logger
from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
improve metamask page

@Author: Efrat Cohen
@Date: 12.2022
"""

"""page locators"""
METAMASK_IMPROVE_CONTAINER = (By.CSS_SELECTOR, "[data-testid='onboarding-metametrics']")
METAMASK_I_AGREE_BUTTON = (By.CSS_SELECTOR, "[data-testid='metametrics-i-agree']")


class MetamaskImprovePage(BasePage):

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
        if self.is_element_exist("METAMASK_IMPROVE_CONTAINER", METAMASK_IMPROVE_CONTAINER):
            self.logger.info(f"Verify if {self.__class__.__name__} is loaded")
            return True
        else:
            self.logger.warning(f"{self.__class__.__name__} is not loaded")
            return False

    def click_on_i_agree_button(self):
        """
        click on i agree button
        """
        self.click("METAMASK_I_AGREE_BUTTON", METAMASK_I_AGREE_BUTTON)
