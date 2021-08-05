import time
from datetime import datetime
import random

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

now = datetime.now()
reg_time = now.strftime("%H%M%S")
regname = "Gktest" + reg_time
random_un = str(random.randint(4, 2000))
password = "Password1"
new_article_for_file = "article" + random_un
new_about = "new about" + regname
post_content = "Lorem Ipsum is simply dummy text of the printing and typesetting industry."
enter_tag = "tag" + regname


def find_element(driver, search_type, value):
    element = WebDriverWait(
        driver, 10).until(
        EC.visibility_of_element_located((search_type, value))
    )
    return element


def conduit_cookie(browser):  # Cookie accepting
    cookie = browser.find_element_by_xpath(
        '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
    cookie.click()


def conduit_login(browser):  # login kiszervezve fgv-be
    browser.find_elements_by_css_selector("li.nav-item")[1].click()
    browser.find_element_by_css_selector("input[placeholder='Email']").send_keys("GarFelhasznalo1@gmail.com")
    browser.find_element_by_css_selector('input[placeholder="Password"]').send_keys(password)
    browser.find_element_by_css_selector('.btn.btn-lg.btn-primary.pull-xs-right').click()
    time.sleep(2)


def conduit_add_article(browser):  # adding new article in def
    time.sleep(3)
    browser.find_element_by_css_selector('a[href="#/editor"]').click()
    time.sleep(3)
    article_title = find_element(browser, By.CSS_SELECTOR, 'input[placeholder="Article Title"]')
    article_title.send_keys(new_article_for_file)
    browser.find_element_by_css_selector('input[placeholder="What\'s this article about?"]').send_keys(
        new_about)
    browser.find_element_by_css_selector('textarea[placeholder="Write your article (in markdown)"]').send_keys(
        post_content)
    browser.find_element_by_css_selector('input[placeholder="Enter tags"]').send_keys(enter_tag + Keys.TAB)
    browser.find_element_by_css_selector('button[type="submit"]').click()
    time.sleep(2)
