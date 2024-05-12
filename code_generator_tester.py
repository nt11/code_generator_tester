# chrome driver from https://chromedriver.storage.googleapis.com/index.html?path=114.0.5735.90/
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import tqdm
import pprint


def click_generate_code(browser_obj):
    """
    Click the Generate Code button
    :param browser_obj: the browser object
    :return: None
    """
    browser_obj.get(r"https://activation.inmodemd.com/activation/GenerateCode.aspx")

    # Wait until the page has loaded
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    #


def set_options(browser_obj, options):
    """
    Set the options for code generation
    :param browser_obj: the browser object
    :param options: either NONE, UNLIMITED, CODES_IN_ADVANCE, ENABLE_MORPHEUS_7MM
    :return: None
    """

    # Find the options checkboxes
    unlimited_checkbox = browser_obj.find_element(By.ID, "Unlimited")
    codes_in_advance_checkbox = browser_obj.find_element(By.ID, "CodesInAdvance")
    morpheus_7mm_enable_checkbox = browser_obj.find_element(By.ID, "Morpheus7mmEnable")

    # Check the required checkboxes
    if options == "UNLIMITED":
        unlimited_checkbox.click()
    elif options == "CODES_IN_ADVANCE":
        codes_in_advance_checkbox.click()
    elif options == "ENABLE_MORPHEUS_7MM":
        morpheus_7mm_enable_checkbox.click()


def set_serial_number(browser_obj, serial_number):
    """
    Set the serial number
    :param browser_obj: the browser object
    :param serial_number: Serial number
    :return: None
    """

    # Find the serial number input field
    serial_number_input = browser_obj.find_element(By.ID, "SerialNumber")

    # Clear the input field
    serial_number_input.clear()

    # Enter the serial number
    serial_number_input.send_keys(serial_number)


def month_name_to_number(month_name):
    """
    Convert a month name to a month number
    :param month_name:  Month name (e.g. "January")
    :return: month number (e.g. 1)
    """

    # Define a dictionary mapping month names to month numbers
    month_name_to_number_dict = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12}

    # Return the month number
    return month_name_to_number_dict[month_name.lower()]


def go_to_date(browser_obj, month, year):
    """
    Go to the specified date in the calendar
    :param month: integer representing the month
    :param year: integer representing the year (like 2024)
    :return: None
    """

    if month == 0 and year == 0:
        return

    # Locate the element containing the month name
    month_element = browser_obj.find_element(By.XPATH, '//td[@align="center" and @style="width:70%;"]')

    # Get the month name
    month_year = month_element.text
    # print(month_year)
    month_name, current_year = month_year.split(" ")
    # print(month_name, current_year)

    # Get the month number
    month_number = month_name_to_number(month_name)
    # print(month_number)

    # Get the difference in years
    year_difference = int(year) - int(current_year)
    # print(year_difference)

    # Get the difference in months
    month_difference = month - month_number
    # print(month_difference)

    # Get the number of times to click the next month arrow
    next_month_arrow_clicks = year_difference * 12 + month_difference
    # print(next_month_arrow_clicks)

    # Click the next month arrow the required number of times
    for i in range(next_month_arrow_clicks):
        next_month_arrow = browser_obj.find_element(By.XPATH, '//a[@title="Go to the next month"]')
        next_month_arrow.click()

    # Click the previous month arrow the required number of times
    for i in range(-next_month_arrow_clicks):
        previous_month_arrow = browser_obj.find_element(By.XPATH, '//a[@title="Go to the previous month"]')
        previous_month_arrow.click()

    # Click on the day 1
    table = browser.find_element(By.ID, "ExpirationDate")
    date_link = table.find_element(By.LINK_TEXT, "1")
    date_link.click()


def click_generate(browser_obj):
    """
    Click the Generate button
    :return: None
    """
    # Find the Generate button
    generate_button = browser_obj.find_element(By.ID, "Generate")

    # Click the Generate button
    generate_button.click()


def get_fields_from_table(browser_obj):
    """
    Get the fields from the table
    :param browser_obj: browser object
    :return:
    """

    # Find the table
    table = browser_obj.find_element(By.ID, "CodeTable")

    # Find all the rows in the table
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Loop through each row
    row_num = -1
    table_data = []
    for row in rows:
        # Find all the columns in the row
        columns = row.find_elements(By.TAG_NAME, "td")
        row_num += 1
        data = []
        # Loop through each column
        for column in columns:
            # Print the column text
            # print(column.text)

            if row_num > 0:
                data.append(column.text)
        if row_num > 0:
            table_data.append(data)
    return table_data


def click_back_to_main_menu(browser_obj):
    """
    Click the back to main menu button
    :param browser_obj: browser object
    :return: None
    """
    # Find the back to main menu button
    back_to_main_menu_button = browser_obj.find_element(By.ID, "Finish")

    # Click the back to main menu button
    back_to_main_menu_button.click()
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))


def get_data_for_scenario(browser_obj, serial, date_month, date_year, options) -> list[list]:
    """
    Get the data from the table for a given scenario
    :param browser_obj: browser object
    :param serial: serial number
    :param date_month: month number
    :param date_year: year (like 2024)
    :param options: options for code generation
    :return: table data
    """

    set_serial_number(browser_obj=browser_obj, serial_number=serial)
    set_options(browser_obj=browser_obj, options=options)
    go_to_date(browser_obj=browser_obj, month=date_month, year=date_year)
    click_generate(browser_obj=browser_obj)
    table_data_returned = get_fields_from_table(browser_obj=browser_obj)
    click_back_to_main_menu(browser_obj=browser_obj)
    click_generate_code(browser_obj=browser_obj)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    return table_data_returned


def iterate_scenarios(browser_obj, scenarios, serial, ctr):
    """
    Iterate over a list of scenarios and get the data for each scenario
    :param browser_obj: browser object
    :param scenarios: list of scenarios
    :param serial: serial number
    :param ctr: counter
    :return: None
    """

    db = []
    for scenario in scenarios:
        table_data_returned = get_data_for_scenario(browser_obj=browser_obj, serial=serial,
                                                    date_month=scenario["date_month"], date_year=scenario["date_year"],
                                                    options=scenario["options"])
        for row in table_data_returned:
            try:
                db.append({'ctr': ctr, 'serial': serial, 'scenario_month': scenario["date_month"],
                           'scenario_year': scenario["date_year"], 'scenario_options': scenario["options"],
                           'date_month': row[0], 'code': row[1]
                           })
            except:
                db.append({'ctr': ctr, 'serial': serial, 'scenario_month': scenario["date_month"],
                           'scenario_year': scenario["date_year"], 'scenario_options': scenario["options"],
                           'date_month': "ERROR", 'code': "ERROR"
                           })
    return db


if __name__ == "__main__":

    # get credentials from file
    with open("credentials.txt", "r") as f:
        credentials = f.readlines()
        username_cred = credentials[0].strip()
        password_cred = credentials[1].strip()

    service = Service(r"/Users/nirt11/PycharmProjects/code_generator_tester/geckodriver")
    browser = webdriver.Firefox(service=service)

    # Wait up to 10 seconds for the page to load
    wait = WebDriverWait(browser, 10)

    browser.get(r"https://activation.inmodemd.com/activation/")
    # browser.get("https://activation.inmodemd.com/activation/MainMenu.aspx")

    # Wait until the page has loaded
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # enter User NAme as "revital" and Password as "revital"
    # find the username input field

    username = browser.find_element(By.ID, "LoginPage_UserName")
    password = browser.find_element(By.ID, "LoginPage_Password")
    login_button = browser.find_element(By.ID, "LoginPage_LoginButton")
    # enter the username

    username.send_keys(username_cred)
    password.send_keys(password_cred)

    # click the login button
    login_button.click()
    # browser.get(r"https://activation.inmodemd.com/activation/GenerateCode.aspx")
    #
    # # Wait until the page has loaded
    # wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    # #
    click_generate_code(browser_obj=browser)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    scenarios = [{"date_month": 7, "date_year": 2025, "options": "NONE"},
                 {"date_month": 8, "date_year": 2027, "options": "NONE"},
                 {"date_month": 9, "date_year": 2028, "options": "NONE"},
                 {"date_month": 10, "date_year": 2029, "options": "NONE"},
                 {"date_month": 11, "date_year": 2030, "options": "NONE"},
                 {"date_month": 7, "date_year": 2031, "options": "NONE"},

                 ]

    for i in range(1, 13):
        scenarios.append({"date_month": i, "date_year": 2020, "options": "NONE"})

    scenarios_additional = [{"date_month": 0, "date_year": 0, "options": "UNLIMITED"},
                            {"date_month": 0, "date_year": 0, "options": "CODES_IN_ADVANCE"},
                            {"date_month": 0, "date_year": 0, "options": "ENABLE_MORPHEUS_7MM"},
                            ]
    scenarios = scenarios + scenarios_additional

    df_input = pd.read_csv("ISB.csv")
    ctr = 1
    db = []
    for serial in tqdm.tqdm(df_input["Serial"]):
        db_single = iterate_scenarios(ctr=ctr, browser_obj=browser, scenarios=scenarios, serial=serial)
        db = db + db_single
        ctr += 1
        if ctr == 4:
            break

    df = pd.DataFrame(db)
    df.to_csv("output.csv")

   # print(db)

    # # Wait until the page has loaded
    # wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    #
    # set_serial_number(browser_obj=browser, serial_number="M50325541")
    # set_options(browser_obj=browser, options="UNLIMITED")
    # go_to_date(browser_obj=browser, month=12, year=2025)
    # click_generate(browser_obj=browser)
    # table_data_returned = get_fields_from_table(browser_obj=browser)
    # print(table_data_returned)
    # time.sleep(2)
    # click_back_to_main_menu(browser_obj=browser)
    # time.sleep(2)
    # click_generate_code(browser_obj=browser)

    # # Wait until the page has loaded
