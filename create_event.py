#!/usr/bin/env python3

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, timedelta, datetime



def create_event(event_name, dates, earliest=18, latest=0, timezone='Europe/Berlin', testing=False):
    display = Display()
    display.start()
    driver = webdriver.Firefox()
    driver.get('https://when2meet.com')
    assert 'When2meet' in driver.title
    __insert_data(event_name, dates, earliest, latest, timezone, driver)

    if testing:
        print('Test finished successfully.')
    else:
        __submit(driver)
        print(__get_url(event_name, driver))

    driver.quit()
    display.stop()

def __get_url(event_name, driver):
    url = ''

    try:
        element = WebDriverWait(driver, 10).until(
                EC.title_contains(event_name)
        )
    finally:
        url = driver.current_url
    
    return url


def __insert_data(event_name, dates, earliest, latest, timezone, driver):
    __set_event_name(event_name, driver)
    __select("TimeZone", timezone, driver)
    __select("NoEarlierThan", earliest, driver)
    __select("NoLaterThan", latest, driver)
    __select_dates(dates, driver)


def __set_event_name(name, driver):
    name_field = driver.find_element(By.ID, "NewEventName")
    name_field.clear()
    name_field.send_keys(name)


def __select(name, option, driver):
    select = Select(driver.find_element(By.NAME, name))
    select.select_by_value(str(option))


def __select_dates(dates, driver):
    for date in dates:
        fdate = date.strftime('%Y-%m-%d')
        elem = driver.find_element(By.XPATH, f'//*[@value="{fdate}"]')
        elem_name = elem.get_property('id').replace('DateOf', 'Day')
        driver.find_element(By.ID, elem_name).click()


def get_dates_between(first_date, last_date):
    for n in range(int((last_date - first_date).days + 1)):
        yield first_date + timedelta(n)


def __submit(driver):
    xpath = '/html/body/div[2]/form/table/tbody/tr[3]/td/input'
    submit_button = driver.find_element(By.XPATH, xpath)
    assert 'Create Event' in submit_button.get_property('value')
    submit_button.click()


def __read_args():
    import argparse

    parser = argparse.ArgumentParser(prog='When2Meet CLI',
                                     description='Client for creating events on When2Meet.com')
    parser.add_argument('name', type=str)
    parser.add_argument('earliest_date', type=str)
    parser.add_argument('last_date', type=str)
    parser.add_argument('-e', '--not-earlier-than', default=18)
    parser.add_argument('-l', '--not-later-than', default=0)
    parser.add_argument('--timezone', default='Europe/Berlin')
    parser.add_argument('--testing', default=False, action='store_true')

    return parser.parse_args()


if __name__ == '__main__':
    args = __read_args()

    earliest_date = datetime.strptime(args.earliest_date, '%Y-%m-%d').date()
    last_date = datetime.strptime(args.last_date, '%Y-%m-%d').date()

    dates = get_dates_between(earliest_date, last_date)
    create_event(args.name, dates, args.not_earlier_than, args.not_later_than, args.timezone, args.testing) 

