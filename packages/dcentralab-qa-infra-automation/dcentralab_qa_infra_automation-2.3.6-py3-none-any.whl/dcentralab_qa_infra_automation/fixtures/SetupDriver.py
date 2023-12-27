import pytest
from dcentralab_qa_infra_automation.drivers import ChromeDriver, BraveDriver
from dcentralab_qa_infra_automation.fixtures.InitGlobalParameters import get_logger
from dcentralab_qa_infra_automation.infra.CustomEventListener import CustomEventListener
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

"""
setup and cleanup fixtures functions to init and close the driver. 
before the tests - init the driver, after the tests - close driver.

@Author: Efrat Cohen
@Date: 10.2022
"""

logger = get_logger("SetUpDriver")


def before_test(request):
    logger.info("Test: " + request.node.nodeid + " is started ")

    # Init driver based on injected driver type
    if pytest.data_driven.get("browser") == "chrome":
        logger.info("chrome driver type injected, initialize chrome browser")
        driver = ChromeDriver.initChromeDriver()
    elif pytest.data_driven.get("browser") == "brave":
        logger.info("brave browser type injected, initialize brave browser")
        driver = BraveDriver.initBraveDriver()

    # If no driver type injected - chrome is the default
    else:
        logger.info("no browser type injected, initialize default chrome browser")
        driver = ChromeDriver.initChromeDriver()

    # Add event listener
    event_listener = CustomEventListener()
    event_firing_driver = EventFiringWebDriver(driver, event_listener)

    logger.info("driver :" + event_firing_driver.name + " had installed successfully")
    driver.maximize_window()
    logger.info("window had maximize")

    # Store driver in cls object
    request.cls.driver = driver
    pytest.driver = driver


# Use in cleanup fixture
def after_test(request):
    logger.info("close " + request.cls.driver.name + "driver")
    request.cls.driver.quit()
    logger.info("Test " + request.node.nodeid + " is Finished")
