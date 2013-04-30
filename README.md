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

## Actions ##

UI maps specify a list of actions to be run for a particular page. Actions are described below:

<table>
<thead>
<th>Action</th><th>Description</th><th>Format</th>
</thead>
<tr><td>action_new</td><td>Create a new Action Chain</td><td>action_new</td></tr>
<tr><td>action_move_to_element</td><td>Adds to the current Action Chain, moving the mouse to the specified element</td><td>action_move_to_element|selector|element</td></tr>
<tr><td>action_click</td><td>Adds a mouse click the current Action Chain</td><td>action_click</td></tr>
<tr><td>action_keys</td><td>Adds to the current Action Chain, sending a sequence of special keys (up, down, left, right)</td><td>action_keys|key1,key2,key3</td></tr>
<tr><td>action_perform</td><td>Performs the Action Chain</td><td>action_perform</td></tr>
<tr><td>base_url</td><td>Change the base URL. The tier parameter can be used in the URL. For example, if the parameter --tier dev is used, base_url|http://%(tier)host.com evaluates to the base URL http://devhost.com.</td><td>base_url|URL</td></tr>
<tr><td>clear</td><td>Clear an input's text</td><td>clear|selector|element</td></tr>
<tr><td>clear_type</td><td>Clears an input's text then sends keys to the element</td><td>type_var|selector|element|variable</td></tr>
<tr><td>click</td><td>Click on an element</td><td>click|selector|element</td></tr>
<tr><td>click_all</td><td>Click all elements</td><td>click|selector|element</td></tr>
<tr><td>delay</td><td>Delay a specified number of milliseconds</td><td>delay|milliseconds</td></tr>
<tr><td>exec</td><td>Evaluate arbitrary Python code with access to store variables</td><td>exec|code</td></tr>
<tr><td>find_frame</td><td>Search through all iframes for target element, switching to frame</td><td>find_frame|selector|element</td></tr>
<tr><td>keys</td><td>Send a sequence of special keys (up, down, left, right) to a target</td><td>keys|selector|element|key1,key2,key3</td></tr>
<tr><td>log</td><td>Output a string</td><td>log|string</td></tr>
<tr><td>log_var</td><td>Output a variable's value</td><td>log_var|variable</td></tr>
<tr><td>open</td><td>Open a URL (appended to a base URL)</td><td>open|URL</td></tr>
<tr><td>random_ssn</td><td>Generates a random Social Security Number, saving it to variable</td><td>random_ssn|variable</td></tr>
<tr><td>select</td><td>Select an option from a select box element by visible text</td><td>select|selector|element|option</td></tr>
<tr><td>select_by_value</td><td>Select an option from a select box element by value</td><td>select|selector|element|option</td></tr>
<tr><td>set_window_size</td><td>Set the browser's window size, in pixels</td><td>set_window_size|width|height</td></tr>
<tr><td>store_attribute</td><td>Store an element's attribute into a variable</td><td>store_text|selector|element|attribute|variable</td></tr>
<tr><td>store_text</td><td>Store an element's text into a variable</td><td>store_text|selector|element|variable</td></tr>
<tr><td>switch_to_default</td><td>Switch to the top frame (frame 0)</td><td>switch_to_default</td></tr>
<tr><td>switch_to_frame</td><td>Switch to a frame by name or number</td><td>switch_to_frame|frame</td></tr>
<tr><td>type</td><td>Send keys to an element</td><td>type|selector|element|keys</td></tr>
<tr><td>type_var</td><td>Send the value of a variable to an element</td><td>type_var|selector|element|variable</td></tr>
<tr><td>verify_text</td><td>Verify that text exists within an element</td><td>verify_text|selector|element|text</td></tr>
</table>


### Element and Selector ###
The Selenium specific parameters, element and selector, mirror the output of Selenium's IDE.

**selector**
Specifies the method used to select an element. Selector must be one of the following values:
* id
* css
* xpath
**element**
Describes the element to target using the specified selector.

### Examples ###

    # sends the keys "03032022" to an element with the ID "expirationDate":
    type|id|expirationDate|03032022
    
    # clicks on a button, located using xpath selector:
    click|xpath|//input[@value='Continue']

    # clicks on a button, located using the css selector:
    click|css|#accord-2 > div.accord-content.padded > div.accord-controls.padded > input.accord-button-next

    # stores the value of an input into a variable:
    store_attribute|id|__o3id0|value|REFERENCE_NUMBER

    # use an Action Chain to click on an element and send arrow keys:
    action_new
    action_move_to_element|xpath|/html/body/div/span/ span
    action_click
    action_keys|down,down,down,return
    action_perform

For more information, check out Locating UI Elements section in the [WebDriver documentation](http://seleniumhq.org/docs/03_webdriver.jsp).

### Actions to Consider Adding ###

* open_base: Open a URL without appending to the base URL
* is_hidden   
* is_visible  
* assert: Assert the return value of a boolean action 



