# Selenium Harness #

## Overview ##

Selenium WebDriver is a web browser automation tool. The WebDriver API allows access to Selenium's functionality through programming languages such as Python, Ruby, and Java. Selenium Harness is a homegrown framework using the Python WebDriver bindings to take advantage of Selenium's native functionality, and additionally:

* extend and customize Selenium's commands, allowing functionality beyond the web browser (e.g., FTP access, sending e-mail, accessing databases or the filesystem)
* simplify the automation process using syntax similar to Selenium IDE's output 
* optimize Selenium's native commands and expedite the automation process (e.g. automatically waiting for an element to exist and become visible before attempting user interaction)
* improve performance by executing multiple test suites concurrently
* provide detailed logging of test results
* integrate with JIRA Test Cases

## Dependencies ##

The following packages are required and can be installed via Pip:

* BeautifulSoup4
* selenium

## Execution ##

To run the Selenium Python WebDriver without any parameters:

`$ python run.py`

<table>
    <thead>
        <th>Parameter</th>
        <th>Description</th>
        <th>Default</th>
    </thead>
    <tr>
        <td>-h, --help</td>
        <td>Show the help message and exit.</td>
        <td></td>
    </tr>
    <tr>
        <td>-s SUITE, --suite SUITE</td>
        <td>Required SUITE specifies the test suite or the test suite directory. If a directory is specified, every file within the directory will be executed as a test suite. </td>
        <td></td>
    </tr>
    <tr>
        <td>-b BASE, --base BASE</td>
        <td>BASE specifies the base URL to use. If not specified, the program will scan for the base.url file, starting with the suite directory and traversing upwards.</td>
        <td></td>
    </tr>
    <tr>
    <td>-t TIER, --tier TIER</td>
    <td>TIER specifies the development tier to use, e.g. qa or dev. The tier may be substituted in the default base URL or utilized by custom scripts, for example when accessing XML files organized by development tier on an FTP server.</td>
    <td>qa</td>
    </tr>
    <tr>
        <td>-d, --debug </td>
        <td>Debug mode; provides verbose output.    </td>
        <td></td>
    </tr>
    <tr>
        <td>-x, --xml</td>
        <td>Loads suite file data from an XML file. Used in conjunction with the -s parameter, allowing for JIRA filter output to drive automation. </td>
        <td></td>
    </tr>
</table>

