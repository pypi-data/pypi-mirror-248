# -*- coding: utf-8 -*-
# pylin:disable=W0612
import re
import os
import time
import json
import shutil
import subprocess

from logger import LOGGER
import core.base_globals as GLOBALS

LOG = LOGGER.log


class Base(object):
    """ Base Test Framework Class.

    This class is the base/super/parent harness for this framework. It is the mother ship
    and is what essentially drives this whole framework. Any new test harness must inherit from
    this class to make avail of all it's features.

    Using the pytest request object the test configuration for the test run is defined. It is this
    class that sets it's various attributes. These are generic attributes that are necessary for
    all tests.

    Attributes of the System Under Test (SUT) (these are defined once per session):
        (1) cluster config -  host, username and password
        (2) grapevine config- host, username, password and port
        (3) log config- level

    Attributes of the Test Method/Case (these are defined once per test method/case):
        (1) test - name, class name, module name, test id
        (2) testdata - test case testdata dir, test class testdata dir, test module testdata dir
        (3) knowngoods - test knowngood file, test case knowngood dir, test class knowngood dir,
                         test module knowngood dir
        (4) output - test output file, test case output dir, test class output dir,
                     test module output dir

    Other attributes of the test instance:
        (1) logger - Logging class instance
        (2) asserts - Asserts class instance
    """
    # pylint: disable=R0904

    __CONFIG = None

    @property
    def config(self):
        return Base.__CONFIG

    __ALL_SUT_CONFIG = None

    @property
    def all_sut_config(self):
        return Base.__ALL_SUT_CONFIG

    __DEVELOPMENT_CONFIG = None

    @property
    def development_config(self):
        return Base.__DEVELOPMENT_CONFIG

    __LOGGING_CONFIG = None

    @property
    def logging_config(self):
        return Base.__LOGGING_CONFIG

    @property
    def driver_config(self):
        return Base.__DRIVER_CONFIG

    __INTERPOLATORS = dict()

    @property
    def interpolators(self):
        return Base.__INTERPOLATORS

    @interpolators.setter
    def interpolators(self, value):
        if isinstance(value, dict):
            Base.__INTERPOLATORS.update(value)
        else:
            self.log.critical("Interpolate value is - '{}'. Expects a valid python dictionary"
                              .format(value))

    __SUPERSEDES = None

    @property
    def supersedes(self):
        return Base.__SUPERSEDES

    @supersedes.setter
    def supersedes(self, value):
        if isinstance(value, dict):
            if ("pattern" in value and "value" in value and "name" in value and
                    "description" in value):
                Base.__SUPERSEDES.append(value)
            else:
                self.log.critical("Supersede expects keys: pattern, value, name, description")
        else:
            self.log.critical("Supersede value is - '{}'. Expects a valid python dictionary"
                              .format(value))

    __SUT = None

    @property
    def sut(self):
        return Base.__SUT

    __TEST = None

    @property
    def test(self):
        return Base.__TEST

    __REQUEST = None

    @property
    def request(self):
        return Base.__REQUEST

    # __TEST_ID = None

    # @property
    # def test_id(self):
    #     return Base.__TEST_ID

    # __TEST_COMPONENT = None

    # @property
    # def test_component(self):
    #     return Base.__TEST_COMPONENT

    # __TEST_DIR = None

    # @property
    # def test_dir(self):
    #     return Base.__TEST_DIR

    # __TEST_MODULE_NAME = None

    # @property
    # def test_module_name(self):
    #     return Base.__TEST_MODULE_NAME

    # __TEST_CLASS_NAME = None

    # @property
    # def test_class_name(self):
    #     return Base.__TEST_CLASS_NAME

    # __TEST_CASE_NAME = None

    @property
    def test_case_name(self):
        return Base.__TEST_CASE_NAME

    __TESTDATA_DIR = 'testdata'

    @property
    def testdata_dir(self):
        return Base.__TESTDATA_DIR

    __TEST_TD_DIR = None

    @property
    def test_td_dir(self):
        return Base.__TEST_TD_DIR

    __TEST_MODULE_TD_DIR = None

    @property
    def test_module_td_dir(self):
        return Base.__TEST_MODULE_TD_DIR

    __TEST_CLASS_TD_DIR = None

    @property
    def test_class_td_dir(self):
        return Base.__TEST_CLASS_TD_DIR

    __TEST_CASE_TD_DIR = None

    @property
    def test_case_td_dir(self):
        return Base.__TEST_CASE_TD_DIR

    # __KNOWNGOOD_DIR = 'knowngood'

    # @property
    # def knowngood_dir(self):
    #     return Base.__KNOWNGOOD_DIR

    # __TEST_KG_DIR = None

    # @property
    # def test_kg_dir(self):
    #     return Base.__TEST_KG_DIR

    # __TEST_MODULE_KG_DIR = None

    # @property
    # def test_module_kg_dir(self):
    #     return Base.__TEST_MODULE_KG_DIR

    # __TEST_CLASS_KG_DIR = None

    # @property
    # def test_class_kg_dir(self):
    #     return Base.__TEST_CLASS_KG_DIR

    # __TEST_CASE_KG_DIR = None

    # @property
    # def test_case_kg_dir(self):
    #     return Base.__TEST_CASE_KG_DIR

    __OUTPUT_DIR = 'o'
    __TEST_CASE_O_FILE = None

    @property
    def test_case_o_file(self):
        return Base.__TEST_CASE_O_FILE

    __LOG = LOG

    @property
    def log(self):
        return Base.__LOG

    __ASSERTS = None

    @property
    def asserts(self):
        return Base.__ASSERTS

    # pylint: disable=R0201
    @asserts.setter
    def asserts(self, asserts):
        Base.__ASSERTS = asserts

    __VERIFIES = None

    @property
    def verifies(self):
        return Base.__VERIFIES

    __DRIVER = None

    @property
    def driver(self):
        return Base.__DRIVER

    @driver.setter
    def driver(self, item):
        self.__DRIVER = item

    # Application Specific Variables
    __MANAGE = None
    MANAGE = None

    @property
    def manage(self):
        return Base.__MANAGE

    __SERVERS = None
    SERVERS = None

    @property
    def servers(self):
        return Base.__SERVERS

    # __VCO_API = None
    # VCO_API = None

    # @property
    # def vco_api(self):
    #     return Base.__VCO_API

    # __VCO_API_HELPER = None
    # VCO_API_HELPER = None

    # @property
    # def vco_api_helper(self):
    #     return Base.__VCO_API_HELPER

    # __VCO_API_FEATURE = None
    # VCO_API_FEATURE = None

    # @property
    # def vco_api_feature(self):
    #     return Base.__VCO_API_FEATURE

    @classmethod
    def _harness_setup(cls, config=None):
        """ Sets up the test harness

        Args:
            config (dict): test harness configuration

        Raises:
            Exception: if no test config is parsed
        """

        if config:
            Base.__CONFIG = config
            Base.__ALL_SUT_CONFIG = config["sut"]
            Base.__DEVELOPMENT_CONFIG = config["development"]
            Base.__LOGGING_CONFIG = config["logging"]

            Base.__INTERPOLATORS = config.get("interpolate", {})
            Base.__SUPERSEDES = GLOBALS.SUPERSEDES
        else:
            raise Exception("Missing test configuration.")

    @classmethod
    def _sut_setup(cls, sut=None):
        """ Sets up the system under test (SUT). """
        # pylint: disable=W0613

        config = Base.__CONFIG
        Base.__SUT = config["sut"]

        if "manage" in config["sut"]:
            Base.__MANAGE = DictObject(Base.__SUT["manage"])

        if "servers" in config["sut"]:
            Base.__SERVERS = DictObject(Base.__SUT["servers"])

    @classmethod
    def _test_function_setup(cls, request):
        """ Sets up the test function related attributes.

        Details on some attributes values:
            __TEST_CASE_NAME - parametrized test case has both `originalname` and `name` attributes
                               non-empty, e.g. `test_foo[bar]` and `test_foo`, while plain test
                               case has non-empty `name` and `originalname` initialized to `None`.

        Args:
            request (pytest object): test function request instance
        """
        # pylint: disable=R0915

        Base.__REQUEST = request
        test_case_name = request.node.originalname or request.node.name
        configuration = request.config.configuration["logging"]

        Base.__TEST_CASE_NAME = str(test_case_name)
        try:
            Base.__TEST_CLASS_NAME = str(request.node.cls.__name__)
        except AttributeError:
            Base.__TEST_CLASS_NAME = ''

        test_module = str(request.node.module.__name__)
        Base.__TEST_MODULE_NAME = "%s.py" % test_module

        Base.__TEST_ID = '.'.join([test_module, Base.__TEST_CLASS_NAME, Base.__TEST_CASE_NAME])
        test_module_full_path = os.path.abspath(str(request.fspath))
        Base.__TEST_DIR = os.path.split(test_module_full_path)[0]
        component = Base.__TEST_DIR
        # dictate logs artifacts directory using configuration logging path and basetemp
        # path is as if user set env TEMP=path, basetemp is as if user had cli --basetemp dir
        output_file_name = time.strftime("%Y%m%d-%H%M%S") + ".log"
        basetemp = configuration.get("basetemp")
        logs_dir = configuration.get("path")
        if basetemp:
            # make abspath from configuration logging path, directly affecting o_dir
            o_dir = request.session.startdir.ensure_dir(basetemp).strpath
        elif logs_dir:
            # support pytest dev-mode cyclic directory generation under TEMP
            import pytest
            if os.environ.get('TEMP') != logs_dir:
                # TEMP=logs and use path=logs, would make logs/pytest-of-hapy/pytest-#/logs
                o_dir = pytest.ensuretemp(logs_dir).strpath
            else:
                o_dir = pytest.ensuretemp('').strpath
            output_file_name = "test.log"  # 1 log per folder, no need for name to have timestamps
        else:
            # legacy logging near tests
            o_dir = os.path.join(component, Base.__OUTPUT_DIR)

        # Generate test data details
        Base.__TEST_TD_DIR = os.path.join(Base.__TEST_DIR, Base.__TESTDATA_DIR)
        Base.__TEST_MODULE_TD_DIR = os.path.join(Base.__TEST_TD_DIR, Base.__TEST_MODULE_NAME)
        Base.__TEST_CLASS_TD_DIR = os.path.join(Base.__TEST_MODULE_TD_DIR, Base.__TEST_CLASS_NAME)
        Base.__TEST_CASE_TD_DIR = os.path.join(Base.__TEST_CLASS_TD_DIR, Base.__TEST_CASE_NAME)

        # # Generate test knowngoods details
        # Base.__TEST_MODULE_KG_DIR = os.path.join(Base.__TEST_MODULE_TD_DIR, Base.__KNOWNGOOD_DIR)
        # Base.__TEST_CLASS_KG_DIR = os.path.join(Base.__TEST_CLASS_TD_DIR, Base.__KNOWNGOOD_DIR)
        # Base.__TEST_CASE_KG_DIR = os.path.join(Base.__TEST_CASE_TD_DIR, Base.__KNOWNGOOD_DIR)

        # Generate test output details
        parts = request.node.nodeid.split('::')
        if '()' in parts:
            parts.remove('()')
        case_dir = os.path.join(o_dir, *parts)
        Base.__TEST_CASE_O_FILE = os.path.join(case_dir, output_file_name)
        Base.__create_dir(case_dir)

        # Store the test specific details
        Base.__TEST = {}
        Base.__TEST["id"] = Base.__TEST_ID
        Base.__TEST["component"] = component
        Base.__TEST["dir"] = Base.__TEST_DIR
        Base.__TEST["module_name"] = Base.__TEST_MODULE_NAME
        Base.__TEST["class_name"] = Base.__TEST_CLASS_NAME
        Base.__TEST["case_name"] = str(request.node.name.replace('[', '_').strip(']'))

        # Knowngoods
        Base.__TEST["module_kg_dir"] = Base.__TEST_MODULE_KG_DIR
        Base.__TEST["class_kg_dir"] = Base.__TEST_CLASS_KG_DIR
        Base.__TEST["case_kg_dir"] = Base.__TEST_CASE_KG_DIR

        Base._kg_file = os.path.join(Base.__TEST["case_kg_dir"],
                                     (Base.__TEST["case_name"] + '.knowngood'))
        Base._toml_kg_file = os.path.join(Base.__TEST["module_kg_dir"],
                                          (Base.__TEST_CASE_NAME + '.toml'))
        Base._kg_section = Base.__TEST["class_name"]
        Base._kg_loaded = False

        Base.__TEST["kg_file"] = Base._kg_file
        Base.__TEST["toml_kg_file"] = Base._toml_kg_file
        Base.__TEST["kg_section"] = Base._kg_section
        Base.__TEST["kg_loaded"] = Base._kg_loaded

        # Test Data
        Base.__TEST["td_dir"] = Base.__TEST_TD_DIR
        Base.__TEST["module_td_dir"] = Base.__TEST_MODULE_TD_DIR
        Base.__TEST["class_td_dir"] = Base.__TEST_CLASS_TD_DIR
        Base.__TEST["case_td_dir"] = Base.__TEST_CASE_TD_DIR

        # Test Output
        Base.__TEST["o_dir"] = o_dir
        Base.__TEST["case_o_dir"] = case_dir
        Base.__TEST["o_path"] = Base.__TEST_CASE_O_FILE

    @classmethod
    def _logger_setup(cls, logger):
        """ Logger dependency injection"""

        Base.__LOGGER = logger
        Base.__LOG = Base.__LOGGER.setup(Base.__TEST_CASE_O_FILE, Base.__TEST_MODULE_NAME,
                                         Base.__LOGGING_CONFIG)
        return Base.__LOG

    @classmethod
    def _logger_cleanup(cls):
        """ Cleans up the logger at the end of each test.

        Made part of each test flow to flush out the file handle of the logger, to prevent
        log messages to be recorded in .log files of other tests during parallel execution.
        """

        Base.__LOGGER.cleanup()

    @classmethod
    def _asserts_setup(cls, asserts):
        """ Asserts dependency injection. """

        Base.__ASSERTS = asserts
        return Base.__ASSERTS

    @classmethod
    def _asserts_cleanup(cls):
        """ Cleans up any asserts in memory.

        This method is invoked at the end of each test to create knowngoods and sections,
        if the update_knowngood flag is set in the config.
        """

        Base.__ASSERTS.assert_tear_down()

    @classmethod
    def _verifies_setup(cls, verifies):
        """ Verifies dependency injection. """

        Base.__VERIFIES = verifies

    @classmethod
    def _verifies_cleanup(cls):
        """ Cleans up any verifies in memory. """

        Base.__VERIFIES.verify_teardown()

    # @classmethod
    # def _vco_api_client_setup(cls, vco_api):
    #     """ VCO API dependency injection. """

    #     Base.__VCO_API = vco_api
    #     Base.VCO_API = vco_api

    #     return Base.__VCO_API

    # @classmethod
    # def _vco_api_helper_setup(cls, vco_api_helper):
    #     """ VCO API Helper dependency injection. """

    #     Base.__VCO_API_HELPER = vco_api_helper
    #     Base.VCO_API_HELPER = vco_api_helper

    #     return Base.__VCO_API_HELPER

    # @classmethod
    # def _vco_api_feature_setup(cls, vco_api_feature):
    #     """ VCO API feature dependency injection. """

    #     Base.__VCO_API_FEATURE = vco_api_feature
    #     Base.VCO_API_FEATURE = vco_api_feature

    #     return Base.__VCO_API_FEATURE

    @staticmethod
    def __create_dir(path):
        """ Creates an empty directory tree if not already present. """

        if not os.path.exists(path):
            os.makedirs(path)

    @classmethod
    def __supersede(cls, string):
        """ Supersedes a given pattern with registered substitutions

        Args:
            string (str): String to check for patterns

        Returns:
            string: superseded string
        """

        if Base.__SUPERSEDES:
            for supersede in Base.__SUPERSEDES:
                pattern_obj = re.compile(supersede["pattern"], re.MULTILINE)
                (string, _) = pattern_obj.subn(supersede["value"], string)
        else:
            Base.__LOG.critical("Asking to supersede, when no supersedes are defined.")

        return string

    @classmethod
    def __interpolate(cls, string):
        """ Interpolates occurrences of predefined substitutions with their corresponding values

        Args:
            string (str): string to check for interpolations

        Returns:
            string: interpolated string
        """
        # pylint: disable=W1401

        if Base.__INTERPOLATORS:
            for interpolator in Base.__INTERPOLATORS:
                pattern_obj = re.compile("\[\[ *?{} *?\]\]".format(interpolator), re.MULTILINE)
                (string, _) = pattern_obj.subn(
                    '{}'.format(Base.__INTERPOLATORS[interpolator]), string)
        else:
            Base.__LOG.critical("Asking to interpolate, when no interpolators are defined in "
                                "config.")

        return string

    @classmethod
    def __should_string_be_superseded_and_or_interpolated(cls, string_identifier):
        """ Assesses if the string identified by the arg should be processed

        The string_identifier is typically a file name or a config file label, essentially
        anything that identifies the string that needs to be superseded and/or interpolated or
        neither.

        Args:
            string_identifier (str): String identifier to decide processing

        Returns:
            tuple: booleans (supersede, interpolate), that indicate what kind of processing
                   needs to be done.
        """

        supersede = False
        interpolate = False

        # Regular expressions that control the criteria for superseding and interpolation
        supersede_and_interpolate = re.compile(
            '^(si|sni|ins|sandi|iands|supersede_and_interpolate)( |_|-)')
        only_supersede = re.compile('^(s|supersede)( |_|-)')
        only_interpolate = re.compile('^(i|interpolate)( |_|-)')

        if supersede_and_interpolate.match(string_identifier):
            supersede = True
            interpolate = True
            return (supersede, interpolate)

        if only_supersede.match(string_identifier):
            supersede = True
            return (supersede, interpolate)

        if only_interpolate.match(string_identifier):
            interpolate = True

        return (supersede, interpolate)

    @classmethod
    def read_file(cls, filepath):
        """ Reads the content of a file

        Args:
            filepath (str): complete file path of the file

        Returns:
            str: file content
        """

        fh = open(filepath, "r")
        string = fh.read()
        fh.close()
        return string

    @classmethod
    def supersede_and_or_interpolate_file(cls, filepath, string_criteria=None,
                                          supersede=True, interpolate=True):
        """ Supersede and/or interpolate content of a file

        If the string_criteria argument is passed, it will assess if the string argument needs to
        be processed, or it will directly look for any pattern matches in the passed string and
        supersede it with the registered substitution. Following which it will interpolate the
        superseded string with the configured interpolation.

        Args:
            filepath (str): Complete file path of the file that needs to be processed
            string_criteria (str): String identifier to decide processing
            supersede (bool): Whether to supersede or not
            interpolate (bool): Whether to interpolate or not

        Returns:
            str: processed string
        """

        string = Base.read_file(filepath)
        return cls.supersede_and_or_interpolate(string=string,
                                                string_criteria=string_criteria,
                                                supersede=supersede,
                                                interpolate=interpolate)

    @classmethod
    def supersede_and_or_interpolate(cls, string, string_criteria=None,
                                     supersede=True, interpolate=True):
        """ Supersede and/or interpolate a given string

        If the string_criteria argument is passed, it will assess if the string argument needs to
        be processed, or it will directly look for any pattern matches in the passed string and
        supersede it with the registered substitution. Following which it will interpolate the
        superseded string with the configured interpolation.

        Args:
            string (str): String that needs to be processed
            string_criteria (str): String identifier to decide processing
            supersede (bool): Whether to supersede or not
            interpolate (bool): Whether to interpolate or not

        Returns:
            str: processed string
        """

        if string_criteria:
            supersede, interpolate = Base.__should_string_be_superseded_and_or_interpolated(
                string_criteria)

        if not supersede and not interpolate:
            return string

        if supersede:
            string = Base.__supersede(string)
        if interpolate:
            string = Base.__interpolate(string)

        return string

    def read_test_data(self, file_name, td_dir=None):
        """ Returns testdata from file

        If no value is passed to the testdata_dir argument, all three folders will be searched
        in the following order:
        (1) test:case_td_dir (test method specific testdata)
        (2) test:class_td_dir (test class specific testdata)
        (3) test:module_td_dir (test module specific testdata)
        failing which, an IOError will be raised.

        Args:
            file_name (str): name of the file
            td_dir (str): path to the file

        Returns:
            dict: if file_name has a .json extension
            str: if file_name does not have a .json extension

        Raises:
            IOError: if testdata file_name is not found.
        """

        self.log.info("Searching testdata file: %s", file_name)
        fh = None
        if td_dir is None:
            td_dir = self.test["case_td_dir"]
            try:
                fh = open(os.path.join(td_dir, file_name), "r")
            except IOError:
                self.log.debug("Looking for testdata file {0} in test class directory, not found in"
                               " test case directory {1}.".format(file_name, td_dir))
            if not fh:
                td_dir = self.test["class_td_dir"]
                try:
                    fh = open(os.path.join(td_dir, file_name), "r")
                except IOError:
                    self.log.debug("Looking for testdata file {0} in test module directory, not "
                                   "found in test class directory {1}.".format(file_name, td_dir))
                if not fh:
                    td_dir = self.test["module_td_dir"]
                    try:
                        fh = open(os.path.join(td_dir, file_name), "r")
                    except IOError:
                        self.log.debug("Looking for testdata file {0} in testdata directory, not "
                                       "found in test module directory {1}."
                                       .format(file_name, td_dir))
                    if not fh:
                        td_dir = self.test["td_dir"] = self.test_td_dir
                        try:
                            fh = open(os.path.join(td_dir, file_name), "r")
                        except IOError as e:
                            exception_message = ("Test data file {0} does not exist in "
                                                 "the testdata directory.".format(file_name))
                            self.log.exception(exception_message)
                            raise IOError(e)

        else:
            try:
                fh = open(os.path.join(td_dir, file_name), "r")
            except IOError as e:
                exception_message = ("Test data file {0} does not exist in "
                                     "the testdata directory.".format(file_name))
                self.log.exception(exception_message)
                raise IOError(e)

        self.log.info("Reading testdata file: %s from location: %s", file_name, td_dir)
        test_data = fh.read()
        fh.close()

        test_data = self.supersede_and_or_interpolate(string=test_data, string_criteria=file_name)

        if file_name.endswith('.json'):
            test_data = json.loads(test_data)

        return test_data

    def get_test_data_file_path(self, file_name, td_dir=None):
        """ Returns testdata file's full path

        If no value is passed to the testdata_dir argument, all three folders will be searched
        in the following order:
            (1) test:case_td_dir (test method specific testdata)
            (2) test:class_td_dir (test class specific testdata)
            (3) test:module_td_dir (test module specific testdata)
        failing which, an IOError will be raised.

        Args:
            file_name (str): name of the file
            td_dir (str): path to the file

        Returns:
            string: full file path

        Raises:
            IOError: if testdata file_name is not found.
        """

        self.log.info("Searching testdata file: %s", file_name)

        if td_dir is None:
            # Checking for file at test case level
            td_dir = self.test["case_td_dir"]
            file_path = os.path.join(td_dir, file_name)
            if os.path.isfile(file_path):
                return file_path
            self.log.debug("Testdata file {0} not found in directory {1}".format(file_name, td_dir))

            # Checking for file at test class level
            td_dir = self.test["class_td_dir"]
            file_path = os.path.join(td_dir, file_name)
            if os.path.isfile(file_path):
                return file_path
            self.log.debug("Testdata file {0} not found in directory {1}".format(file_name, td_dir))

            # Checking for file at test module level
            td_dir = self.test["module_td_dir"]
            file_path = os.path.join(td_dir, file_name)
            if os.path.isfile(file_path):
                return file_path
            self.log.debug("Testdata file {0} not found in directory {1}".format(file_name, td_dir))

            # Checking for file at testdata level
            td_dir = self.test["td_dir"]
            file_path = os.path.join(td_dir, file_name)
            if os.path.isfile(file_path):
                return file_path
            self.log.debug("Testdata file {0} not found in directory {1}".format(file_name, td_dir))

        else:
            # Checking for file at given testdata directory
            file_path = os.path.join(td_dir, file_name)
            if os.path.isfile(file_path):
                return file_path
            self.log.debug("Testdata file {0} not found in directory {1}".format(file_name, td_dir))

        exception_message = ("Test data file {0} does not exist in "
                             "the testdata directory.".format(file_name))
        self.log.error(exception_message)
        raise IOError(exception_message)

    def get_test_data_dir_path(self, directory_name, td_dir=None):
        """ Returns the full path of a directory defined inside testdata directories

        If no value is passed to the testdata_dir argument, all three folders will be searched
        in the following order:
            (1) test:case_td_dir (test method specific testdata)
            (2) test:class_td_dir (test class specific testdata)
            (3) test:module_td_dir (test module specific testdata)
        failing which, an IOError will be raised.

        Args:
            directory_name (str): name of the directory
            td_dir (str): path to the file

        Returns:
            string: full directory path

        Raises:
            IOError: if testdata directory_name is not found.
        """

        self.log.info("Searching testdata directory: {}".format(directory_name))

        if td_dir is None:
            # Checking for directory at test case level
            td_dir = self.test["case_td_dir"]
            directory_path = os.path.join(td_dir, directory_name)
            if os.path.isdir(directory_path):
                return directory_path
            self.log.debug("Testdata directory {0} not found in directory {1}".format(
                directory_name,
                td_dir))

            # Checking for directory at test class level
            td_dir = self.test["class_td_dir"]
            directory_path = os.path.join(td_dir, directory_name)
            if os.path.isdir(directory_path):
                return directory_path
            self.log.debug("Testdata directory {0} not found in directory {1}".format(
                directory_name,
                td_dir))

            # Checking for directory at test module level
            td_dir = self.test["module_td_dir"]
            directory_path = os.path.join(td_dir, directory_name)
            if os.path.isdir(directory_path):
                return directory_path
            self.log.debug("Testdata directory {0} not found in directory {1}".format(
                directory_name,
                td_dir))

            # Checking for directory at testdata level
            td_dir = self.test["td_dir"]
            directory_path = os.path.join(td_dir, directory_name)
            if os.path.isdir(directory_path):
                return directory_path
            self.log.debug("Testdata directory {0} not found in directory {1}".format(
                directory_name,
                td_dir))

        else:
            # Checking for directory at given testdata directory
            directory_path = os.path.join(td_dir, directory_name)
            if os.path.isdir(directory_path):
                return directory_path
            self.log.debug("Testdata directory {0} not found in directory {1}".format(
                directory_name,
                td_dir))

        exception_message = ("Test data directory {0} does not exist in any of "
                             "the testdata directories.".format(directory_name))
        self.log.error(exception_message)
        raise IOError(exception_message)

    def replace_env_variables(self, config_file, word_to_replace="CICD_", strict=True):
        """ Replaces env variables with its values. Does not raise any exceptions.

        Args:
            config_file (str): path of the config file
            word_to_replace (str): prefix of the word to replace
            strict (bool): if True we dont replace missing env-setting, otherwise we reset value.
                           Caller can then raise if the key is still present after call.

        Example:
            Words like CICD_CLUSTER_HOST, CICD_CLUSTER_USERNAME are replaced if respective
            environment variables are present.

        Returns:
            str: config data with env variables replaced.
        """
        self.log.info(f'replacing vars in {config_file}')

        replaced_string = ""
        # pylint: disable=W1401
        pattern = re.compile('({}[.\w]+)'.format(word_to_replace))
        with open(config_file) as data_file:
            for line in data_file:
                match = re.findall(pattern, line)
                for word in match:
                    try:
                        env_value = os.environ[word].strip()
                    except KeyError:
                        # When CICD log env not set, then replace with INFO log-level
                        if 'CICD_LOG_LEVEL' in word:
                            env_value = 'INFO'
                        elif strict:
                            # caller can now detect presence of key and raise if required
                            env_value = word
                        else:
                            env_value = ''
                    line = line.replace(word, env_value)
                replaced_string += line

        return replaced_string

    def archive_dumps(self, directory):
        """ Archives the dumps under the given testcase directory

        Args:
            directory (str): Name of the directory to archive : send the absolute path

        Raises:
            Exception: if subprocess fails to execute `tree` on the archived directory
        """
        # pylint: disable=W0703

        parent = os.path.dirname(directory)
        base_dir = os.path.relpath(directory, parent)

        self.log.info(f"Archiving : {directory}")
        result = shutil.make_archive(directory, "zip", root_dir=parent, base_dir=base_dir)

        if result:
            os.system(f"rm -rf {directory}")
            self.log.info("Files zipped successfully")
            os.system(f"ls -lrt {parent}")
        else:
            self.log.error("Error took place in zipping")
        try:
            self.log.info(subprocess.check_output(f"tree {parent}", shell=True))
        except Exception as error:
            self.log.error(
                f"Error in generating the tree for the directory : Exception : {error}"
            )

        os.system(f"chmod -R 777 {parent}")


class DictObject(dict):
    """ Data structure to extend dict attribute access """

    def __init__(self, response):
        """ initialize a dict to DictObject

        Args:
            response (dict): dict to convert
        """
        super().__init__()

        self._response = response
        for k, v in response.items():
            if isinstance(v, dict):
                self[k] = DictObject(v)
            else:
                self[k] = v
            if isinstance(v, list):
                val_list = []
                for item in v:
                    if isinstance(item, dict):
                        val_list.append(DictObject(item))
                    else:
                        val_list.append(item)
                self[k] = val_list

    def __getattr__(self, name):
        """ extend attribute access

        Args:
            name (str): name of attribute

        Returns:
            object: attribute of response
        """

        return self.get(name)


BASE = Base()
