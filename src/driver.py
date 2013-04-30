"""
Selenium WebDriver Harness
Copyright (C) 2013 J. Daniel Lewis <jdanlewis@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import os
import time
import datetime
import Queue
from bs4 import BeautifulSoup
from suite import Suite
import settings


class Driver(object):
    """The Driver loads the specified test suites and each suite's UI maps.
    Test suites are launched concurrently. Results are printed to the the
    screen and to a log file."""
    def __init__(self, suite, **kwargs):

        # the store is a dictionary that each suite may use to save settings,
        # variables, and custom data
        self.store = {}
        # save optional args to store
        for k, v in kwargs.items():
            self.store[k] = v

        # initialize log and test suites
        self.log_data = {}
        self.suites = {}

        # check if `suite' is a directory
        if os.path.isdir(suite):
            settings.suites_directory = suite
            self.locate_ui_map_directory(settings.suites_directory)
            if self.store['xml']:
                # check if it is an XML file (JIRA filter output)
                self.load_test_suites_from_xml(self.store['xml'])
            else:
                # load all test suites contained within the directory
                self.load_all_test_suites()
        else:
            # otherwise, load the specified suite file
            settings.suites_directory = os.path.split(suite)[0]
            self.locate_ui_map_directory(settings.suites_directory)
            self.load_test_suite(suite)

    def run(self):
        """Run test suites concurrently and record statistics"""

        # initialize log and start time
        self.init_log()
        start_time = time.time()

        # create a queue of test suites to be run
        q = Queue.Queue()
        for suite in self.suites.items():
            q.put(suite)

        # spin up a few threads to process the test suites
        threads = []
        if settings.thread_count < q.qsize():
            thread_count = settings.thread_count
        else:
            thread_count = q.qsize()
        print "Launching %d test thread%s..." % \
            (thread_count, self.pluralize(thread_count))
        for i in range(thread_count):
            t = Suite(q, self.store, self.log)
            t.start()
            threads.append(t)

        # wait for the threads to finish
        while len(threads):
            try:
                threads[0].join()
                threads.pop(0)
            except KeyboardInterrupt:
                pass

        # print log and stats
        elapsed_time = time.time() - start_time
        self.print_log(elapsed_time)

    def log(self, key, value):
        """Logs a value to a given key (suite name)"""
        if not key in self.log_data:
            self.log_data[key] = []
        value = "%s: %s" % (datetime.datetime.now(), value)
        self.log_data[key].append(value)

    def init_log(self):
        """Initialize the log file"""
        f = open(settings.log_filename, "a")
        f.write("%s: Driver Starting\n" % datetime.datetime.now())
        f.write("Settings: %s\n" % repr(self.store))
        f.close()

    def print_log(self, elapsed_time):
        """Print the log to stdout and the log file"""
        f = open(settings.log_filename, "a")
        print
        f.write("\n")
        for suite, messages in self.log_data.items():
            print suite
            f.write(suite + "\n")
            for message in messages:
                print message
                f.write(message + "\n")
            print
            f.write("\n")
        minutes, seconds = divmod(elapsed_time, 60)
        message = "finished in %d minute%s %d second%s" % (
            minutes, self.pluralize(minutes),
            seconds, self.pluralize(seconds))
        print message
        f.write("%s\n%s\n" % (message, "-" * 80))
        f.close()

    def pluralize(self, n):
        return "" if int(n) == 1 else "s"

    def load_all_test_suites(self):
        """Load all test suites in the suites directory"""
        suite_files = os.listdir(settings.suites_directory)
        self.load_test_suite_files(suite_files)

    def load_test_suite_files(self, suite_files):
        """Loads a list of test suite files"""
        for fn in suite_files:
            filename = os.path.join(settings.suites_directory, fn)
            self.load_test_suite(filename)

    def load_test_suite(self, filename):
        """Load a single test suite"""
        if not os.path.isdir(filename):
            suite = []
            for line, number in self.load_file(filename):
                suite.append(self.load_ui_map(line))
            self.suites[filename] = suite

    def load_test_suites_from_xml(self, suite):
        """Load a series of test suites from an XML file"""
        with open(suite, "r") as f:
            xml = BeautifulSoup(f.read(), "xml")
        keys = [key.text for key in xml.find_all('key')]
        self.load_test_suite_files(keys)

    def load_ui_map(self, ui_map):
        """Load a UI Map"""
        filename = os.path.join(settings.ui_map_directory, ui_map)
        actions = []
        for line, number in self.load_file(filename):
            action = line.split(settings.delimeter)
            actions.append((action, number))
        return (ui_map, actions)

    def load_file(self, filename):
        """Loads a file, ignoring blank lines and comments, returning an array
        of stripped lines"""
        try:
            with open(filename, "r") as f:
                lines = f.readlines()
        except IOError, e:
            print "Error opening file", filename
            print e
            sys.exit(1)
        line_number = 0
        result = []
        for line in lines:
            line = line.strip()
            if len(line):  # ignore blank lines
                if line[0] != "#":  # ignore comments
                    result.append((line, line_number))
            line_number += 1
        return result

    def locate_ui_map_directory(self, path):
        """Traverse up path until UI map directory is found"""
        while path:
            target = os.path.join(path, settings.ui_map_directory_name)
            if os.path.isdir(target):
                settings.ui_map_directory = target
                return
            path = os.path.dirname(path)
        print "Cannot locate UI maps"
        sys.exit(1)
