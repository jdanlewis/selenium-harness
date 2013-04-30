import Queue
import threading
from copy import deepcopy
from selenium import webdriver as selenium_webdriver
from page import Page
# exceptions
from httplib import BadStatusLine
from urllib2 import URLError
from selenium.common.exceptions import WebDriverException
from traceback import print_exc

# a global lock shared by all threads (for prettier printing)
lock = threading.Lock()


class Suite(threading.Thread):
    """The Suite class runs a webdriver test suite as a separate thread."""
    def __init__(self, q, store, log):
        global lock
        super(Suite, self).__init__()
        self.q = q  # queue of test suites
        self.store = deepcopy(store)
        self.log = log
        self.lock = lock

    def run(self):
        try:
            webdriver = selenium_webdriver.Firefox()
            with self.lock:
                print "Starting", self.name
            while True:
                try:
                    suite_name, suite = self.q.get_nowait()
                    log = lambda message: self.log(suite_name, message)
                    for ui_map, actions in suite:
                        # log the UI map name if in debug mode
                        if self.store['debug']:
                            log(ui_map)
                        # create the page and test it
                        page = Page(
                            suite_name,
                            actions,
                            webdriver,
                            self.store,
                            self.log
                        )
                        page.test()
                    # suite is complete: success!
                    log("Suite Passed")
                except Queue.Empty:
                    # nothing left to consume
                    break
                except WebDriverException, e:
                    # Houston, we have a problem
                    try:
                        log("X Page Failed: %s" % ui_map)
                        log("X %s" % e)
                        log("X Suite Failed: %s" % suite_name)
                    except:
                        # these variables (log, ui_map, suite_name)
                        # may not be assigned yet on CTL-C
                        pass
        # the following exceptions occur on CTL-C
        except KeyboardInterrupt:
            pass
        except URLError:
            pass
        except BadStatusLine:
            pass
        except Exception, e:
            print "Exception:", e
            print e.__class__
            print_exc()

        with self.lock:
            print "Exiting", self.name
        # close webdriver
        try:
            webdriver.quit()
        except:
            pass
