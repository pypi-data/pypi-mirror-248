import pytest
from dcentralab_qa_infra_automation.fixtures.InitGlobalParameters import get_logger
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """
    The BasePage class holds all common functionality across the website.
    So, we can use those function in every page.

    @Author: Efrat Cohen
    @Date: 12.2022
    """

    def __init__(self, driver):
        """ BasePage constructor - This function is called every time a new object of the base class is created"""
        self.driver = driver
        self.timeout = pytest.properties.get("timeout")
        self.logger = get_logger(self.__class__.__name__)

    def get_element(self, element_name, by_locator):
        """
        Get element
        :param element_name: current element name
        :param by_locator: current locator
        :return: element when found, otherwise None
        """
        try:
            self.logger.info(f"Searching for element :: {element_name} :: with locator :: {by_locator}")
            element = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(by_locator))
            if element:
                self.logger.info(f"Element :: {element_name} :: with locator :: {by_locator} :: found.")
                return element
            else:
                self.logger.info(f"Could not found element :: {element_name}.")
        except Exception as error:
            self.logger.error(f"An error occurred.", error)
            return None

    def get_elements(self, element_name, by_locator):
        """
        Get list of elements
        :param element_name: current element name
        :param by_locator: current locator
        :return: element when found, otherwise None
        """
        try:
            self.logger.info(f"Searching for List of elements :: {element_name} :: with locator :: {by_locator}")
            element = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_all_elements_located(by_locator))
            self.logger.info(f"List of elements :: {element_name} :: with locator :: {by_locator} :: found.")
            return element
        except Exception as error:
            self.logger.warning(
                f"Could not found List of elements :: {element_name} :: with locator {by_locator}.\n{error}")
            return None

    def is_element_exist(self, element_name, by_locator):
        """
        check if element exist
        @param: element_name - current element name
        @param: by_locator - current locator
        @return: true if on page, otherwise return false
        """
        try:
            self.logger.info(f"Verify if element :: {element_name} :: exists on the page.")
            element = WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(by_locator))
            if element:
                self.logger.info(f"Element:  {element_name} :: with locator {by_locator} :: exists.")
                return True
            else:
                self.logger.info(f"Element :: {element_name} :: with locator {by_locator} :: not found.")
                return False

        except Exception as error:
            # If element not found
            self.logger.error(f"Element :: {element_name} :: with locator {by_locator} :: not in DOM.\n{error}")
            return False

    def is_element_exist_with_custom_timeout(self, element_name, by_locator, timeout):
        """
        check if element exists
        @param: element_name - current element name
        @param: by_locator - current locator
        @return: true if on page, otherwise return false
        """
        try:
            self.logger.info(
                f"Check if element ::{element_name} :: is exists on the page with custom timeout :: {timeout}")
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(by_locator))
            if element:
                self.logger.info(f"Element :: {element_name} :: with locator :: {by_locator} :: exists.")
                return True
            else:
                self.logger.error(
                    f"Element {element_name} :: with locator {by_locator} :: not found.")
                return False
        except Exception as error:
            # If element not found
            self.logger.error(
                f"Element {element_name} :: with locator {by_locator} :: not in DOM.\n{error}")
            return False

    def is_specific_element_exist(self, element_name, by_locator, index):
        """
        check if specific element of a list exists
        @param: element_name - current element name
        @param: by_locator - current locator
        @param: index - list index to check
        @return: true if on page, otherwise return false
        """
        try:
            self.logger.info(f"Check if element :: {element_name} :: in index :: {index} :: exists on the page")
            element = WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_all_elements_located(by_locator))[
                index]
            if element:
                self.logger.info(
                    f"Element :: {element_name} :: with locator :: {by_locator} :: in index :: {index} :: exists.")
                return True
        except Exception as error:
            # If element not found
            self.logger.error(
                f"Element {element_name} :: with locator :: {by_locator} :: in index :: {index} :: doesn't exist "
                f"or not found.\n{error}")
            return False

    def click(self, element_name, by_locator):
        """
         Performs click on web element whose locator is passed to it
         :param element_name - current element name
         :param by_locator - current locator to click on
        """
        try:
            self.logger.info(f"Clicking on element :: {element_name} :: with locator :: {by_locator}.")
            WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(by_locator)).click()
            self.logger.info(f"Clicked on element :: {element_name} :: with locator {by_locator}")
        except Exception as error:
            self.logger.error(
                f"Could not click on element :: {element_name} :: with locator :: {by_locator}.\n {error}")

    def click_on_specific_item_in_list(self, element_name, by_locator, index):
        """
        Performs click on specific item in web element list whose locator is passed to it
        :param element_name - current element name
        :param by_locator - current locator
        :param index - index to click on
        """
        try:
            self.logger.info(f"Clicking on element :: {element_name} with locator :: {by_locator} :: in index {index}")
            WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_all_elements_located(by_locator))[
                index].click()
            self.logger.info(
                f"Clicked on element :: {element_name} :: with locator :: {by_locator} :: in index {index}")
        except Exception as error:
            self.logger.error(
                f"Could not click on element :: {element_name} :: with locator :: {by_locator} :: in index :: {index}"
                f"\n{error}")

    def enter_text(self, element_name, by_locator, text):
        """
         Performs text entry of the passed in text, in a web element whose locator is passed to it
         :param element_name - current element name
         :param by_locator - current locator
         :param text - test to insert
        """
        try:
            self.logger.info(
                f"Inserting value :: {text} :: into element :: {element_name} :: with locator :: {by_locator}")
            WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(by_locator)).send_keys(
                text)
            self.logger.info(f"{text} :: inserted into element :: {element_name} :: with locator :: {by_locator}")

        except Exception as error:
            self.logger.error(
                f"Could not insert text :: {text} :: into element :: {element_name} :: with locator {by_locator}.\n"
                f"{error}")

    def enter_text_on_specific_list_item(self, element_name, by_locator, index, text):
        """
         Performs text entry of the passed in text, in a web element whose locator is passed to it
         :param element_name - current element name
         :param by_locator - current locator
         :param index - current index
         :param text - test to insert
        """

        try:
            self.logger.info(
                f"Inserting value :: {text} :: into element :: {element_name} :: with locator :: {by_locator} :: "
                f"in index :: {index}")
            WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_all_elements_located(by_locator))[
                index].send_keys(text)
            self.logger.info(
                f"{text} :: inserted into element :: {element_name} :: with locator :: {by_locator} :: "
                f"in index :: {index}")
        except Exception as error:

            self.logger.error(
                f"Could not insert text :: {text} :: into element :: {element_name} :: with locator {by_locator} :: "
                f"in index :: {index}.\n{error}")

    def upload_file(self, element_name, by_locator, file_path):
        """
        Performs choose file in input with type file, in a web element whose locator and file path are passed to it
        :param element_name - current element name
        :param by_locator - current locator to click on
        :param file_path:
        """
        try:

            self.logger.info(
                f"Uploading file: {file_path} into element :: {element_name} :: with locator :: {by_locator}")
            WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(by_locator)).send_keys(
                file_path)
            self.logger.info(f"File with path :: {file_path} :: uploaded into element :: {element_name}")
        except Exception as error:
            self.logger.error(
                f"Could not upload file with path :: {file_path} :: into element :: {element_name} :: "
                f"with locator :: {by_locator}.\n{error}")

    def get_text(self, element_name, by_locator):
        """
        Performs get text of web element whose locator is passed to it
        :param by_locator - current locator
        :param element_name: - current element
        :return current element text
        """
        try:
            self.logger.info(f"Getting the text value for element :: {element_name} :: with locator :: {by_locator}")
            element_text = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(by_locator)).text
            self.logger.info(f"Text value for element :: {element_name} :: is :: {element_text}")
            return element_text
        except Exception as error:
            self.logger.error(
                f"Could not get the text value for element :: {element_name} :: with locator :: {by_locator}.\n"
                f"{error}")
            return None

    def clear_text(self, element_name, by_locator):
        """
        Performs clear value of web element whose locator is passed to it
        :param by_locator - current locator
        :param element_name: - current element
        """
        try:
            self.logger.info(f"Clearing input from element :: {element_name} :: with locator {by_locator}")
            WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(by_locator)).clear()
            self.logger.info(f"Input cleared from element :: {element_name} :: with locator {by_locator}")
        except Exception as error:
            self.logger.error(
                f"Could not clear input for element :: {element_name} :: with locator :: {by_locator}.\n"
                f"{error}")

    def scroll_to_element(self, element_name, by_locator):
        """
        scroll the page to specific element whose locator is passed to it
        :param by_locator - current locator
        :param element_name: - current element
        """
        try:
            self.logger.info(f"Scrolling to element :: {element_name} :: with locator {by_locator}")
            element = WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(by_locator))
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            self.logger.info(f"Scrolled to element :: {element_name} :: with locator {by_locator}")

        except Exception as error:
            self.logger.error(
                f"Could not scroll to element :: {element_name} :: with locator :: {by_locator}.\n{error}")

    def is_button_enable(self, element_name, by_locator):
        """
        Verify is button is enabled in order to click
        :param element_name:
        :param by_locator:
        :return: boolean
        """
        is_enable = False
        try:
            self.logger.info(f"Verifying if element :: {element_name} :: with locator :: {by_locator} :: is enabled")
            element = WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(by_locator))
            if element:
                if element.is_enabled():
                    is_enable = True
                else:
                    is_enable = False
            self.logger.info(f"Element :: {element_name} :: with locator :: {by_locator} :: is enable :: {is_enable}")
            return is_enable

        except Exception as error:
            self.logger.error(
                f"Element :: {element_name} with locator :: {by_locator} not found or not enabled.\n{error}")
            return False

    def get_element_attribute_list(self, element_name, by_locator, attribute):
        """

        :param element_name: current element
        :param by_locator: current locator
        :param attribute: HTML attribute (class,id,...)
        :return:
        """
        try:
            element = self.get_element(element_name, by_locator)
            if element:
                attribute_list = element.get_attribute(attribute)
                if attribute_list:
                    self.logger.info(
                        f"Found List of attributes :: {attribute}: {attribute_list}, for element :: {element_name}")
                    return attribute_list
                else:
                    self.logger.info(
                        f"Attribute List is :: {attribute_list} :: for element :: {element_name} :: with locator :: "
                        f"{by_locator}")
                    return None
            else:
                self.logger.info(f"Could not found element :: {element_name} :: with locator :: {by_locator}")

        except Exception as error:
            self.logger.error(f"An error occurred :: {error}")
            return None
