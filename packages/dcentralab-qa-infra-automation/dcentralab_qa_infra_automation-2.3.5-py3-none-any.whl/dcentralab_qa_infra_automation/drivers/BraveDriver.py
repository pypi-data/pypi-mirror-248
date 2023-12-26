import pytest
from dcentralab_qa_infra_automation.drivers.HelperFunctions import addExtensionToChrome
from dcentralab_qa_infra_automation.fixtures.InitGlobalParameters import get_logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as BraveService
from webdriver_manager.chrome import ChromeDriverManager

"""
init brave browser driver

@Author: Efrat Cohen
@Date: 12.2022
"""

logger = get_logger("BraveDriver")


def getBraveBinaryLocation(os):
    """
    add brave to chrome based on OS type
    :return: binary_location
    """
    # On windowsOS - use windows brave path
    if os == "windows":
        binary_location = pytest.properties.get("brave.windows.path")
    # use mac brave path
    else:
        binary_location = pytest.properties.get("brave.mac.path")
    return binary_location


def initBraveDriver():
    """
    init brave driver, using ChromeDriverManager for chromeDriver installation
    :return: driver - driver instance
    """
    options = webdriver.ChromeOptions()
    options.binary_location = getBraveBinaryLocation(pytest.data_driven.get("os"))
    brave_service = BraveService(executable_path=ChromeDriverManager().install())

    if pytest.data_driven.get("headless") == "yes":
        logger.info("Add headless to chrome options")
        options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    logger.info("Start the chrome driver with options")
    driver = webdriver.Chrome(service=brave_service, options=options)

    return driver


def initBraveDriverWithExtension():
    """
    init brave driver with CRX extension, using ChromeDriverManager for chromeDriver installation
    :return: driver - driver instance
    """
    options = webdriver.ChromeOptions()
    options.binary_location = getBraveBinaryLocation(pytest.data_driven.get("os"))
    options.add_extension(addExtensionToChrome())
    brave_service = BraveService(executable_path=ChromeDriverManager().install())

    if pytest.data_driven.get("headless") == "yes":
        logger.info("Add headless to chrome options")
        options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    logger.info("Start the chrome driver with options")
    driver = webdriver.Chrome(service=brave_service, options=options)
    return driver
