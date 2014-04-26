import os
import sys
import argparse
from src.driver import Driver


def main():
    """Parse the command line arguments and launch the driver"""

    # create the Parser
    parser = argparse.ArgumentParser(
        description='Run Selenium WebDriver tests.')
    parser.add_argument(
        '-s', '--suite',
        required=True,
        help='test suite or suite directory')
    parser.add_argument(
        '-b', '--base',
        default=None,
        help='base URL')
    parser.add_argument(
        '-t', '--tier',
        default='qa',
        help='development tier')
    parser.add_argument(
        '-d', '--debug',
        action="store_true",
        help='debug mode')
    parser.add_argument(
        '-x', '--xml',
        default=None,
        help='XML input file')

    # get a dictionary of arguments
    args = vars(parser.parse_args())

    # if a base URL is not specified, scan for it
    if args['base'] is None:
        try:
            url = find_base_url(args['suite'])
            # if needed, replace the tier
            if "%(tier)" in url:
                url = url.replace("%(tier)", args['tier'])
            args['base'] = url
        except IOError, e:
            parser.print_help()
            print "error:", e
            sys.exit(1)

    # start the driver
    driver = Driver(**args)
    driver.run()


def find_base_url(suite_directory):
    """Locates the default base URL file, base.url, traversing up from the
    initial suite directory"""

    base_file = "base.url"
    # get the initial path from the suite directory
    if os.path.isdir(suite_directory):
        path = suite_directory
    else:
        path = os.path.dirname(suite_directory)

    # find the base URL file
    while path:
        filename = os.path.join(path, base_file)
        if os.path.isfile(filename):
            # we found the file
            with open(filename) as f:
                url = f.readline().strip()
            return url
        # go up a directory
        path = os.path.dirname(path)

    # if we get here, we can't find the default base.url file
    raise IOError("cannot find base URL file (%s)" % base_file)


if __name__ == "__main__":
    main()
