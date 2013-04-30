from random import randint
from time import time, sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select  # , WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException
)
import settings


class Page(object):
    """The Page class imports a UI Map associated with a particular page and
    runs tests against the page."""
    def __init__(
            self,
            name,  # name of the page (used for logging)
            actions,  # actions list
            webdriver,  # the webdriver
            store,  # a store (dictionary) shared with the suite
            log  # log message function
    ):
        # actions is a list of lists
        # each element represents a particular action to take on the page
        # actions are performed sequentially until the list is complete
        self.actions = actions
        self.by_map = {
            "xpath": By.XPATH,
            "id": By.ID,
            "css": By.CSS_SELECTOR
        }
        self.key_map = {
            "down": Keys.DOWN,
            "up": Keys.UP,
            "left": Keys.LEFT,
            "right": Keys.RIGHT,
            "return": Keys.RETURN,
            "page_down": Keys.PAGE_DOWN,
            "page_up": Keys.PAGE_UP
        }
        self.webdriver = webdriver
        self.store = store
        self.log = lambda message: log(name, message)

    def test(self):
        """Perform the tests specified by the UI Map for the current page"""
        commands = {
            # command: (function, num_parameters)
            "action_new": (self.action_new, 0),
            "action_move_to_element": (self.action_move_to_element, 2),
            "action_click": (self.action_click, 0),
            "action_keys": (self.action_keys, 1),
            "action_perform": (self.action_perform, 0),
            "base_url": (self.set_base_url, 1),
            "clear": (self.clear, 2),
            "clear_type": (self.clear_type, 3),
            "click": (self.click, 2),
            "click_all": (self.click_all, 2),
            "delay": (self.delay, 1),
            "exec": (self.execute, 1),
            "find_frame": (self.find_frame, 2),
            "keys": (self.keys, 3),
            "log": (self.log, 1),
            "log_var": (self.log_var, 1),
            "open": (self.open_url, 1),
            "random_ssn": (self.random_ssn, 2),
            "select": (self.select, 3),
            "select_by_value": (self.select_by_value, 3),
            "set_window_size": (self.set_window_size, 2),
            "store_attribute": (self.store_attribute, 4),
            "store_text": (self.store_text, 3),
            "switch_to_default": (self.switch_to_default, 0),
            "switch_to_frame": (self.switch_to_frame, 1),
            "type": (self.send_keys, 3),
            "type_var": (self.send_var, 3),
            "verify_text": (self.verify_text, 3)
        }
        current_action = 1
        length = len(self.actions)
        for action, line_number in self.actions:
            if self.store['debug']:
                self.log(repr(action))
            try:
                cmd = action[0]
                function, num_params = commands[cmd]
                params = action[1:1 + num_params]
            except IndexError:
                raise ValueError("invalid action: %s" % action)
            except KeyError:
                raise ValueError("unknown action: %s" % action)
            # execute the command
            function(*params)
            # delay between actions
            sleep(settings.action_delay)
            # page delay occurs before executing the last action
            current_action += 1
            if current_action == length:
                sleep(settings.page_delay)

    """Action Functions"""

    def action_new(self):
        """Create a new Action Chain"""
        self.action_chain = ActionChains(self.webdriver)

    def action_move_to_element(self, by, target):
        """Adds to the current Action Chain, moving the mouse to the specified
        element"""
        el = self.wait_for_element(by, target)
        self.action_chain.move_to_element(el)

    def action_click(self):
        """Adds a mouse click to the current Action Chain"""
        self.action_chain.click()

    def action_keys(self, value):
        """Adds sending keys to the current Action Chain"""
        keys = self.map_keys(value)
        self.action_chain.send_keys(keys)

    def action_perform(self):
        """Performs the Action Chain"""
        self.action_chain.perform()

    def clear(self, by, target):
        """Clear an element"""
        element = self.wait_for_element(by, target)
        element.clear()

    def clear_type(self, by, target, value):
        """Clear an element, then send keys"""
        self.clear(by, target)
        self.send_keys(by, target, value)

    def click(self, by, target):
        """Click on an element"""
        self.wait_for_element_click(by, target)

    def click_all(self, by, target):
        """Click on all target elements, ignoring WebDriver exceptions"""
        by = self.get_by_method(by)
        elements = self.webdriver.find_elements(by, target)
        for element in elements:
            try:
                element.click()
            except (WebDriverException, NoSuchElementException):
                pass

    def delay(self, n):
        """Delay n milliseconds"""
        sleep(float(n) / 1000.0)

    def execute(self, string):
        """Execute a string of arbitrary Python code"""
        exec string in self.store

    def find_frame(self, by, target):
        """Find and switch to the frame containing the target element"""
        by = self.get_by_method(by)

        def find_frame_by_target():
            if not self.scan_frames(by, target):
                raise NoSuchElementException

        self.wait(find_frame_by_target,
                  Exception("Cannot find frame for element: %s" % target))

    def keys(self, by, target, value):
        """Send a string of special keys to a target"""
        keys = self.map_keys(value)
        self.send_keys(by, target, keys)

    def log_message(self, string):
        """Logs a string"""
        self.log(string)

    def log_var(self, key):
        """Logs a store variable"""
        self.log_message(self.store[key])

    def open_url(self, url):
        """Open a URL using the driver's base URL"""
        self.webdriver.get(self.store['base'] + url)

    def random_ssn(self, variable):
        """Generates a random SSN, saving it to a store variable"""
        num = "%09d" % randint(1, 999999999)
        ssn = '-'.join([num[:3], num[3:5], num[5: 9]])
        self.store[variable] = ssn

    def select(self, by, target, value):
        """Select an option from a select box"""
        element = self.wait_for_element(by, target)
        self.wait(
            lambda: Select(element).select_by_visible_text(value),
            "cannot select option: %s" % value
        )

    def select_by_value(self, by, target, value):
        """Select an option from a select box"""
        element = self.wait_for_element(by, target)
        self.wait(
            lambda: Select(element).select_by_value(value),
            "cannot select value: %s" % value
        )

    def set_window_size(self, width, height):
        """Sets the size of the browser window"""
        self.webdriver.set_window_size(width, height)

    def send_keys(self, by, target, value):
        """Send keys to an element"""
        element = self.wait_for_element_click(by, target)
        element.send_keys(value)

    def send_var(self, by, target, var):
        """Send a store variable string to an element"""
        value = self.store[var]
        self.send_keys(by, target, value)

    def set_base_url(self, url):
        """Sets the base URL, allowing tier substitution"""
        if "%(tier)" in url:
            url = url.replace("%(tier)", self.store["tier"])
        self.store["base"] = url

    def store_attribute(self, by, target, attr, var):
        """Stores an elements text"""
        element = self.wait_for_element(by, target)
        self.store[var] = element.get_attribute(attr)

    def switch_to_default(self):
        """Switch to top frame"""
        self.webdriver.switch_to_default_content()

    def switch_to_frame(self, frame):
        """Switch to a frame"""
        try:
            frame = int(frame)
        except ValueError:
            pass
        self.wait(
            lambda: self.webdriver.switch_to_frame(frame),
            "cannot find frame: %s" % str(frame)
        )

    def store_text(self, by, target, var):
        """Stores an elements text"""
        element = self.wait_for_element(by, target)
        self.store[var] = element.text

    def verify_text(self, by, target, text):
        """Verifies that text is exists within the target"""
        element = self.wait_for_element(by, target)
        if text not in element.text:
            raise WebDriverException("cannot verify text: %s" % text)

    """Helper functions"""

    def get_by_method(self, by):
        """Verify the By method is available"""
        if by not in self.by_map:
            raise ValueError("unknown By method: %s" % by)
        return self.by_map[by]

    def map_keys(self, value):
        """Splits value by commas, returning a string of mapped Keys"""
        try:
            keys = [self.key_map[key] for key in value.split(',')]
        except KeyError:
            raise ValueError("unknown key mapping: %s" % value)
        return ''.join(keys)

    def scan_frames(self, by, target, path_to_current_frame=[]):
        """Recursively scan frames for an element, returning the element if
        found, false if not"""
        try:
            return self.webdriver.find_element(by, target)
        except (WebDriverException, NoSuchElementException):
            pass
        # switch to current frame
        self.webdriver.switch_to_default_content()
        for frame in path_to_current_frame:
            self.webdriver.switch_to_frame(frame)
        # get all children frames
        frames = self.webdriver.find_elements_by_tag_name('iframe')
        for frame in frames:
            # scan each child
            el = self.scan_frames(by, target, path_to_current_frame + [frame])
            if el:
                return el

    def wait(self, func, error, timeout=settings.wait_timeout):
        """Helper function to handle generic webdriver waits"""
        stop_time = time() + timeout
        while time() < stop_time:
            try:
                return func()
            except (WebDriverException, NoSuchElementException):
                sleep(settings.attempt_delay)
        raise TimeoutException(error)

    def wait_for_element(self, by, target):
        """Wait for an element to be available"""
        by = self.get_by_method(by)
        return self.wait(lambda: self.webdriver.find_element(by, target),
                         "cannot find element: %s" % target)

    def wait_for_element_click(self, by, target):
        """Wait until an element is clicked"""
        element = self.wait_for_element(by, target)
        self.wait(lambda: element.click(),
                  "cannot click element: %s" % target)
        return element
