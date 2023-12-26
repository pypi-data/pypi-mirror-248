import json
import logging.config

import json5
import pytest
import yaml

"""
Init global parameters fixture function to load all the project necessary global parameters 
before all the tests running.

@Author: Efrat Cohen
@Date: 11.2022
"""


def before_all():
    """
    Loads project global parameters and store them as pytest global variable, so the parameters will be accessible
    everywhere
    """

    # Init Json properties
    # Opening JSON file
    f = open(pytest.user_dir + '/app-config.json')
    # Returns JSON object as a dictionary
    data = json.load(f)
    # Store the properties in pytest global variables
    pytest.properties = data
    # Closing file
    f.close()

    # Init Tokens JSON data only in TokensFarm or chainport project
    if "tokensfarm" in pytest.user_dir or "chainport" in pytest.user_dir:
        # Opening token JSON file
        f = open(pytest.user_dir + '/testsData/tokens.json')
        # Returns JSON object as a dictionary
        tokens = json.load(f)
        # Store the data in pytest global variables
        pytest.tokens = tokens
        # Closing file
        f.close()

    # Init farms file only in tokensfarm project
    if "tokensfarm" in pytest.user_dir:
        # Init farms JSON data
        # Opening farms JSON file
        f = open(pytest.user_dir + '/testsData/farms.json')
        # Returns JSON object as a dictionary
        farms_data = json.load(f)
        # Store the data in pytest global variables
        pytest.farms_data = farms_data
        # Closing file
        f.close()

    # Init wallets JSON data
    # Opening wallets JSON file
    f = open(pytest.user_dir + '/testsData/wallets.json')
    # Returns JSON object as a dictionary
    wallets_data = json.load(f)
    # Store the data in pytest global variables
    pytest.wallets_data = wallets_data
    # Closing file
    f.close()

    # Initialize the logger instance
    with open(pytest.user_dir + '/tests/logging.yaml', 'rt') as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


def get_logger(class_name):
    """
    get logger instance
    :param class_name: current class name
    :return: logger - new current class logger instance
    """
    # Get the logger related to the calling class
    logger = logging.getLogger(class_name)
    return logger

    # Get an instance of the logger and use it to write a log
    # Store the logger in pytest global variables


pytest.logger = logging.getLogger(__name__)
