import time

from dcentralab_qa_infra_automation.fixtures.InitGlobalParameters import get_logger
from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

NAMI_SETTINGS_TITLE = (By.XPATH, "//*[contains(@class,'chakra-text) and contains(text(), 'Settings')]")
NAMI_SETTINGS_NETWORK_OPTION = (By.XPATH, "//*[contains(@class,'chakra-button') and contains(text(), 'Network')]")
NAMI_SETTINGS_NETWORK_CONTAINER_TITLE = (
    By.XPATH, "//*[contains(@class, 'chakra-text') and contains(text(), 'Network')]")
NAMI_SETTINGS_NETWORK_SELECT = (By.XPATH, "//select[contains(@class, 'chakra-select')]")


class NamiSettingsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = get_logger(self.__class__.__name__)

    def is_on_settings_window(self):
        """
        check if settings window loaded
        :return: true if on page, otherwise return false
        """
        self.logger.info(f"Verify if {self.__class__.__name__} is loaded")
        url = self.driver.current_url
        if "settings" in url and self.is_element_exist("NAMI_SETTINGS_TITLE", NAMI_SETTINGS_TITLE):
            self.logger.info(f"{self.__class__.__name__} is loaded")
            return True
        else:
            self.logger.info(f"{self.__class__.__name__} is not loaded")
            return False

    def click_on_network(self):
        """
        click on network
        """
        self.click("NAMI_SETTINGS_NETWORK_OPTION", NAMI_SETTINGS_NETWORK_OPTION)

    def is_on_network_window(self):
        """
        check if network page loaded
        :return: true if on page, otherwise return false
        """
        url = self.driver.current_url
        self.logger.info(f"Verify if {self.__class__.__name__} is loaded")
        if "network" in url and self.is_element_exist("NAMI_SETTINGS_NETWORK_CONTAINER_TITLE",
                                                      NAMI_SETTINGS_NETWORK_CONTAINER_TITLE):
            self.logger.info(f"{self.__class__.__name__} is loaded")
            return True
        else:
            self.logger.info(f"{self.__class__.__name__} is not loaded")
            return False

    def click_on_network_select(self):
        """
        click on network select
        """
        self.click("NAMI_SETTINGS_NETWORK_SELECT", NAMI_SETTINGS_NETWORK_SELECT)

    def choose_network(self, network):
        """
        choose network
        """
        time.sleep(2)
        CHOOSE_NETWORK = (By.CSS_SELECTOR, f".chakra-select option[value='{network}']")

        self.click("CHOOSE_NETWORK", CHOOSE_NETWORK)

        # Click on somewhere in the page to close the window if did not close
        action_chains = ActionChains(self.driver)
        action_chains.move_by_offset(200, 300).click().perform()
