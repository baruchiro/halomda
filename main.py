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
import db
import sys

rights = ["תשובה נכונה", "נכון!", "תוצאה נכונה", "בוצעה", "בוצע"]


def parseWorks(tableHTML):
    soup = BeautifulSoup(tableHTML, "html.parser")
    menu = {}
    i = 1
    print("Select work:")
    for tr in soup.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 0:
            print(f'{i}. for {tds[0].get_text()[::-1]}')
            menu[i] = tds[0].find('a')['href'], tds[0].get_text()
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
            menu[i] = tds[2].find('a')['href'], tds[0].get_text()
            i = i + 1
    #select = int(input("Your choice:"))
    return menu  # [select]


def parseTrainNum(tableHTML) -> dict:
    soup = BeautifulSoup(tableHTML, "html.parser")
    menu = {}
    i = 1
    print("Select train num:")
    for tr in soup.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 0:
            print(f'{i}. for {tds[0].get_text()[::-1]}')
            menu[i] = tds[0].find('a')['href'], tds[0].get_text()
            i = i + 1
    #select = int(input("Your choice:"))
    return menu  # [select]


def parseHints(table):
    soup = BeautifulSoup(table, "html.parser")
    return [img['onclick'] for img in soup.find_all('img')]


def getQuestion(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('img')['src']


def specificTask(driver, work, section, task):
    success = False
    question = getQuestion(driver.find_element_by_id(
        "Question").get_attribute('outerHTML'))
    answer = db.tryGet(question)
    if not answer:
        # Get Question
        driver.execute_script("HintBtnClick()")
        results = parseHints(driver.find_element_by_id(
            "HintsTable").get_attribute('outerHTML'))
        for ans in results:

            driver.execute_script(ans)
            driver.execute_script("event = {keyCode:13};KeyDownEvent(event);")

            text = driver.find_element_by_id(
                "OutWindow").get_attribute('innerText')
            success = any(x in text for x in rights)

            if success:
                db.add(question, ans, work, section, task)
                return question

    return None


def workAgainstQuestion(driver, work, section, task):
    counter = 0

    while counter < 5:
        res = specificTask(driver, work, section, task)
        if res:
            counter = 0
        else:
            counter = counter + 1
            print(counter)

        driver.refresh()


def main():
    username = input("Enter user name (id number):")
    password = input("Enter user name (id number):")
    try:
        # Init
        driver = webdriver.Chrome(executable_path="./chromedriver.exe")
        driver.implicitly_wait(30)
        base_url = "https://halomda.org/"
        verificationErrors = []
        accept_next_alert = True

        while True:
            # Login
            driver.get(
                "https://halomda.org/TestingDriverMy/WelcomeGuest-MichlalaWeb.php")
            driver.find_element_by_id("UserName").clear()
            driver.find_element_by_id("UserName").send_keys(username)
            driver.find_element_by_id("PassWord").clear()
            driver.find_element_by_id("PassWord").send_keys(password)
            driver.find_element_by_id("SubmitBtn").click()

            # Select work
            path, work = parseWorks(driver.find_element_by_xpath(
                "//table").get_attribute('outerHTML'))
            driver.get("https://halomda.org/" + path)

            # Select Section
            sections = parseTirgul(driver.find_element_by_xpath(
                "//table").get_attribute('outerHTML'))
            for section in sections.values():
                print(f'------{section[1][::-1]}----------')
                driver.get("https://halomda.org/" + section[0])

                # Select Task
                tasks = parseTrainNum(driver.find_element_by_xpath(
                    "//table").get_attribute('outerHTML'))
                for task in tasks.values():
                    print(f'------{task[1][::-1]}----------')
                    driver.get("https://halomda.org/" + task[0])

                    # We are in train!
                    workAgainstQuestion(driver, work, section[1], task[1])
    except Exception as e:
        print(e)
    finally:
        input("end, press enter")
        driver.close()
        db.save()


if __name__ == "__main__":
    main()
