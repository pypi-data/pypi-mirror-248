################################################################################
# flexiWAN SD-WAN software - flexiEdge, flexiManage.
# For more information go to https://flexiwan.com
#
# Copyright (C) 2020  flexiWAN Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
################################################################################

################################################################################
# This file is a part of pytest framework. Its name and location are predefined.
# It implements pytest hooks that are used at various stages of test execution,
# e.g. on pytest bootup, on invocation of specific test, on exit of specific
# test, etc.
################################################################################

import json
import logging
import os
import pytest
import sys
import traceback
from common import fwahost
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from common import fwaconfig
from pageObjects import fwaloginPage
from pageObjects import fwapathLabelPage

def pytest_addoption(parser):
    parser.addoption(
        "--setup_json_file", action="store", help="JSON file with configuration of testbed"
    )
    parser.addoption(
        "--log_folder", action="store", help="path where to store test results"
    )
    parser.addoption(
        "--clean", action="store", help="Flag for cleaning devices"
    )
    parser.addoption(
        "--test_version", action="store", help="Flag for test release"
    )
    parser.addoption(
        "--previous_version", action="store", help="Flag for previous release"
    )

def pytest_configure(config):
    ''''pytest_configure' is predefined hook of the pytest framework.
    It is invoked once for all tests found in the folder were the conftest.py
    file is located and its subfolers. So it includes global stuff, like logger.
        To configure test specific stuff use the 'test_config' fixture.
    '''
    # Configure logger which is global for all tests.
    # Test specific log file is configured from within per test hook - test_config.
    root = logging.getLogger()
    root.setLevel(level=logging.DEBUG)
    
    # Create and save the formatter object to be used from per test hooks.
    # Note the 'pytest.log_formatter' field is not predefined. It is created
    # by the pytest framework in run time by assignment statement.
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s: %(message)s')
    pytest.log_formatter = formatter

    # Load setup JSON if provided and save it into pytest to be used later.
    # Note the 'pytest.setup' field is not predefined. It is created
    # by the pytest framework in run time by assignment statement.
    pytest.setup = {}
    filename = config.getoption('--setup_json_file')
    if not filename:
        automation_root = os.path.dirname(os.path.realpath(__file__).replace('\\','/'))
        filename = os.path.join(automation_root, 'config' , 'local.json')
        print("file name found local.json")
        if not os.path.exists(filename):
            filename = os.path.join(automation_root, 'config' , 'cicd.json')
    if filename:
        with open(filename, 'r') as f:
            pytest.setup = json.loads(f.read())

    # Update python search pathes with automation tree, so python could find fwa* modules
    #automation_root = os.path.dirname(os.path.realpath(__file__).replace('\\','/'))
    #sys.path.append(os.path.join(automation_root, 'common'))
    #sys.path.append(os.path.join(automation_root, 'scale'))

@pytest.fixture(scope='session')
def test_config(request):
    '''pytest.fixture is a feature of pytest framework.
    It enables user to feed tests located in the same folder and its subfolders,
    where the conftest.py is located with global data and functions.
    We use 'test_config' fixture to parse configuration on pytest invocation.
    Than pytest will provide this configuration to every test object that
    registered for this fixture. To register for fixture just use it's name
    as argument for method, e.g. 'def function_that_uses_fixtire(test_config):'.
    Note 'test_config' name is not predefined in pytest, it is our choice.
    '''
    #current_test_name = request.module.__name__
    current_test_name = "scale"

    # Load folder for logs
    log_folder = request.config.getoption('--log_folder')
    if not log_folder:
        log_folder = './results'
    log_folder = os.path.join(log_folder, current_test_name)
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Create logger with log file, which is specific for the current test
    fh = logging.FileHandler(os.path.join(log_folder, current_test_name+'.log'))
    fh.setFormatter(pytest.log_formatter)
    log = logging.getLogger()
    for handler in log.handlers[:]:  # remove all old handlers
        log.removeHandler(handler)
    log.addHandler(fh)

    # Log the configuration generated for the current test
    config = {
        'setup'      : pytest.setup,
        'log_folder' : log_folder
    }
    separator = '====== %s configuration =====' % current_test_name
    logging.info(separator)
    logging.info(json.dumps(config, sort_keys=True, indent=4))
    logging.info('=' * len(separator))

    return config

@pytest.fixture
def clean_setup(request):
    '''It is used to clean the setup after the test has ran.
    Giving True will clean the setup and False will leave it as it is
    '''
    clean_ = request.config.getoption('--clean')
    if clean_ == 'True':
        return True
    else :
        return False

@pytest.fixture
def version(request):
    version_t = request.config.getoption('--test_version')
    version_p = request.config.getoption('--previous_version')
    return version_t, version_p

@pytest.fixture
def report_result(request):
    '''Wrapper above report_property builtin fixture.
    It is used to add helper results into report file.
    The record_property fixture code was used as a reference:
    https://docs.pytest.org/en/latest/_modules/_pytest/junitxml.html
    '''
    def _append_property(result):
        caller_name = traceback.extract_stack(limit=2)[0].name
        result_str  = "success" if result else "FAILURE"
        request.node.user_properties.append((caller_name, result_str))
        return result
    return _append_property

# @pytest.fixture
# def netplan_backup(test_config):
#     '''It will take a backup of netplan file and return backup file in tearDown
#     '''
#     logging.info('taking backup of original netplan file')
#     device = fwahost.Host(
#             test_config["setup"]["branches"][0]["device"]["host"])
#     _, netplan_files = device.sftp_cmd(path='/etc/netplan/')
#     for nf in netplan_files:
#         device.exec_cmd(f"sudo cp /etc/netplan/{nf} /etc/netplan/{nf}.backup")
#     yield netplan_files
#     logging.info('reverting original netplan file after test')
#     device = fwahost.Host(
#             test_config["setup"]["branches"][0]["device"]["host"])
#     for nf in netplan_files:
#         res,_,out,err = device.exec_cmd(f"sudo mv /etc/netplan/{nf}.backup /etc/netplan/{nf}")
#         if not res:
#             logging.debug(f'stdout{out}, error:{err}')
#     device.exec_cmd("sudo netplan apply")

# @pytest.fixture(params=['CHROME'])
# def init_driver(request, test_config):
#     logging.info(f'Opening {request.param} browser')
#     if request.param == 'CHROME':
#         options = Options()
#         options.binary_location = fwaconfig.CHROME_PATH
#         options.add_argument("--no-sandbox")
#         options.add_argument("--headless")
#         options.add_argument('--incognito')
#         options.add_argument(f"--window-size={fwaconfig.WINDOW_SIZE}")
#         desired_capabilities = DesiredCapabilities.CHROME
#         desired_capabilities = options.to_capabilities()
#         web_driver = webdriver.Chrome(
#             executable_path = fwaconfig.CHROMEDRIVER_PATH,
#             options=options)
#     if request.param == 'FIREFOX':
#         firefox_options = webdriver.FirefoxOptions()
#         firefox_options.add_argument('-headless')
#         firefox_options.add_argument(f"--window-size={fwaconfig.WINDOW_SIZE}")
#         web_driver = webdriver.Firefox(
#             executable_path = fwaconfig.GECKODRIVER_PATH,
#             firefox_options=firefox_options)
#     url = test_config['setup']['server']['url']
#     web_driver.delete_all_cookies()
#     web_driver.get(url)
#     current_url = web_driver.current_url
#     if not current_url == url+ '/login':
#         logging.error('Browser failed to load url')
#         return False
#     logging.info(f'Browser Started {current_url} successfully')
#     yield web_driver
#     web_driver.close()
#     logging.info('Browser closed successfully')

# @pytest.fixture
# def login_fleximanage_set_account(request, test_config, init_driver):
#     login = fwaloginPage.LoginPage(init_driver)
#     logging.info('login to fleximanage')
#     user_config = test_config['setup']['users']['predefined_account']
#     username = user_config['user_name']
#     password = user_config['password']
#     account_name = user_config['account_name']
#     res = login.login_new(username, password)
#     if res:
#         res = login.set_account(
#             account_name, username, password)
#     return res

# @pytest.fixture
# def add_pathlabel(init_driver):
#     path_page = fwapathLabelPage.PathLabelPage(init_driver)
#     logging.info('navigate to path label page')
#     for path_label in fwaconfig.multi_pathlabel_config:
#         res = path_page.create_path_label(path_label)
#         if not res:
#             logging.error('failed to create path label')
#             return False
#         continue
#     return True
