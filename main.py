# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import time
import re
from bs4 import BeautifulSoup


def parseWorks(tableHTML):
    soup = BeautifulSoup(tableHTML, "html.parser")
    menu = {}
    i = 1
    print("Select work:")
    for tr in soup.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 0:
            print(f'{i}. for {tds[0].get_text()[::-1]}')
            menu[i] = tds[0].find('a')['href']
            i = i + 1
    select = int(input("Your choice:"))
    return menu[select]


def parseTirgul(tableHTML):
    soup = BeautifulSoup(tableHTML, "html.parser")
    menu = {}
    i = 1
    print("Select train:")
    for tr in soup.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 0:
            print(f'{i}. for {tds[0].get_text()[::-1]}')
            menu[i] = tds[2].find('a')['href']
            i = i + 1
    select = int(input("Your choice:"))
    return menu[select]


def parseTrainNum(tableHTML):
    soup = BeautifulSoup(tableHTML, "html.parser")
    menu = {}
    i = 1
    print("Select train num:")
    for tr in soup.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 0:
            print(f'{i}. for {tds[0].get_text()[::-1]}')
            menu[i] = tds[0].find('a')['href']
            i = i + 1
    select = int(input("Your choice:"))
    return menu[select]


def main():
    # Init
    driver = webdriver.Chrome(executable_path="./chromedriver")
    driver.implicitly_wait(30)
    base_url = "https://halomda.org/"
    verificationErrors = []
    accept_next_alert = True

    # Login
    driver.get("https://halomda.org/TestingDriverMy/WelcomeGuest-MichlalaWeb.php")
    driver.find_element_by_id("UserName").clear()
    driver.find_element_by_id("UserName").send_keys("313475063")
    driver.find_element_by_id("PassWord").clear()
    driver.find_element_by_id("PassWord").send_keys("313475063")
    driver.find_element_by_id("SubmitBtn").click()

    # Select work
    work = parseWorks(driver.find_element_by_xpath(
        "//table").get_attribute('outerHTML'))
    driver.get("https://halomda.org/" + work)

    # Select Tirgul
    tirgul = parseTirgul(driver.find_element_by_xpath(
        "//table").get_attribute('outerHTML'))
    driver.get("https://halomda.org/" + tirgul)

    # Select train number
    index = parseTrainNum(driver.find_element_by_xpath(
        "//table").get_attribute('outerHTML'))
    driver.get("https://halomda.org/" + index)


if __name__ == "__main__":
    main()
