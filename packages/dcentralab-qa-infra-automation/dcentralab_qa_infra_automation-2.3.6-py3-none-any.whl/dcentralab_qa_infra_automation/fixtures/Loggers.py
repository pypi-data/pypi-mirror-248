from dcentralab_qa_infra_automation.fixtures.InitGlobalParameters import get_logger

"""
init_logger and loggers fixtures functions. before all the tests running - create logger instance as pytest global 
variable, so it will be accessible everywhere.
before and after each test run - log the test name and status

@Author: Efrat Cohen
@Date: 11.2022
"""

logger = get_logger("Loggers")


def before_test(request):
    """
    When test starts - print current test name in the log file
    :param request: the requesting test context
    """
    logger.info("TEST STARTS, test name: " + request.node.nodeid)


def after_test(request):
    """
    When test finish - print current test name and status in log file
    :param request: the requesting test context
    """
    if request.session.testsfailed:
        # When test failed
        for item in request.session.items:
            error_message = item.rep_call.longreprtext if item.rep_call.longreprtext else ""
            status = "TEST FAILED"
            message = f"{status}, test name: {request.node.nodeid}. Error message is: {error_message}"
            logger.error(message)
    else:
        # When test passed
        logger.info(f"TEST PASSES, test name: {request.node.nodeid}")
