from datetime import datetime
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import random
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from defs import find_element, conduit_cookie, conduit_login, conduit_add_article

now = datetime.now()
reg_time = now.strftime("%H%M%S")
regname = "Gktest" + reg_time
random_un = str(random.randint(4, 2000))
new_article_for_file = "article" + random_un
new_about = "new about" + regname
post_content = "Lorem Ipsum is simply dummy text of the printing and typesetting industry."
enter_tag = "tag" + regname
URL_main = "http://localhost:1667"
URL_articles = "http://localhost:1667/#/articles/" + new_article_for_file


class TestConduitApp(object):  # A classnak a Test szoval kell kezdodnie.
    def setup(self):  # Minden teszt metodus elott felsetupolja a pytest a driverunket.
        self.browser_options = Options()
        self.browser_options.headless = True
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=self.browser_options)
        self.browser.get(URL_main)
        self.browser.maximize_window()

    def teardown(self):  # Minden teszt utan bezarja a dolgainkat.
        self.browser.quit()

    def test_cookie_001(self):  # Cookie accepting
        cookie = find_element(self.browser, By.XPATH,
                              '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        cookie.click()

    def test_home_page_appearance_002(
            self):  # A fenti setup metodussal megnyitjuk a honlapot majd checkoljuk a title-ját a honlapnak
        conduit = self.browser.title
        assert conduit == "Conduit"

    def test_register_003(self):  # Regisztráció
        conduit_cookie(self.browser)
        self.browser.find_element_by_xpath("/html/body//a[contains(@href,'register')]").click()
        self.browser.find_element_by_xpath("//input[@type='text'][@placeholder='Username']").send_keys(
            "GarFelhasznalo1")
        self.browser.find_element_by_xpath("//input[@type='text'][@placeholder='Email']").send_keys(
            "GarFelhasznalo1@gmail.com")
        self.browser.find_element_by_xpath("//input[@placeholder='Password']").send_keys("Password1")
        button_reg = find_element(self.browser, By.CSS_SELECTOR, ".btn.btn-lg.btn-primary.pull-xs-right")
        button_reg.click()
        welcome = find_element(self.browser, By.CSS_SELECTOR, ".swal-title")
        welcome_text = welcome.text
        assert welcome_text == "Welcome!"
        self.browser.find_element_by_css_selector(".swal-button.swal-button--confirm").click()
        nav_bar_list = self.browser.find_elements_by_css_selector("li.nav-item")
        logined_name = nav_bar_list[3].text
        assert logined_name == "GarFelhasznalo1"

    def test_navigate_to_login_004(self):  # login testing
        conduit_cookie(self.browser)
        nav_bar_list = self.browser.find_elements_by_css_selector("li.nav-item")
        logined_name = nav_bar_list[1].text
        assert logined_name == "Sign in"
        self.browser.find_elements_by_css_selector("li.nav-item")[1].click()
        self.browser.find_element_by_css_selector("input[placeholder='Email']").send_keys("GarFelhasznalo1@gmail.com")
        self.browser.find_element_by_css_selector('input[placeholder="Password"]').send_keys("Password1")
        sign_in_button = find_element(self.browser, By.CSS_SELECTOR, '.btn.btn-lg.btn-primary.pull-xs-right')
        sign_in_button.click()
        time.sleep(2)
        nav_link_list = self.browser.find_elements_by_class_name('nav-link')
        signed_in_name = nav_link_list[3].text
        assert signed_in_name == "GarFelhasznalo1"

    def test_adding_new_article_005(self):  # adding new artice testing
        conduit_cookie(self.browser)
        conduit_login(self.browser)
        self.browser.find_element_by_css_selector('a[href="#/editor"]').click()
        new_article_input = find_element(self.browser, By.CSS_SELECTOR, 'input[placeholder="Article Title"]')
        new_article_input.send_keys(new_article_for_file)
        self.browser.find_element_by_css_selector('input[placeholder="What\'s this article about?"]').send_keys(
            new_about)
        self.browser.find_element_by_css_selector('textarea[placeholder="Write your article (in markdown)"]').send_keys(
            post_content)
        self.browser.find_element_by_css_selector('input[placeholder="Enter tags"]').send_keys(enter_tag + Keys.TAB)
        self.browser.find_element_by_css_selector('button[type="submit"]').click()
        new_content_text = find_element(self.browser, By.XPATH, '//textarea[@placeholder="Write a comment..."]')
        new_content_text.send_keys(post_content)

    def test_edit_settings_006(self):  # edit setting for bio modification
        conduit_login(self.browser)
        self.browser.find_element_by_css_selector('a[href="#/settings"]').click()
        bio = find_element(self.browser, By.CSS_SELECTOR, 'textarea[placeholder="Short bio about you"]')
        bio.clear()
        bio.send_keys('Tesztelek')
        time.sleep(2)
        self.browser.find_element_by_css_selector('.btn.btn-lg.btn-primary.pull-xs-right').click()
        update = find_element(self.browser, By.CSS_SELECTOR, ".swal-title")
        update_text = update.text
        assert update_text == "Update successful!"
        self.browser.find_element_by_css_selector(".swal-button.swal-button--confirm").click()
        time.sleep(2)
        nav_bar_list = self.browser.find_elements_by_css_selector("li.nav-item")
        nav_bar_list[3].click()
        time.sleep(2)
        mod_setting = self.browser.find_element_by_css_selector('div[class="user-info"] p').text
        assert mod_setting == 'Tesztelek'

    def test_pagination_007(self):  # lapozó tesztelése
        conduit_cookie(self.browser)
        page_links = self.browser.find_elements_by_class_name("page-link")
        hossz = len(page_links)
        for page in page_links:
            if page.text != hossz:
                page.click()
            else:
                assert page.text == hossz

    def test_adding_data_from_file_008(self):  # add comments from file
        conduit_cookie(self.browser)
        conduit_login(self.browser)
        conduit_add_article(self.browser)
        with open("adat.txt", "r") as file:
            comment_list = file.readlines()
            my_list2 = [s[:-1] for s in comment_list]
            for idx, val in enumerate(my_list2):
                new_content_text = find_element(self.browser, By.XPATH, '//textarea[@placeholder="Write a comment..."]')
                new_content_text.send_keys(val)
                time.sleep(1)
                self.browser.find_element_by_xpath('//button[text()="Post Comment"]').click()
                time.sleep(1)
                just_comment = self.browser.find_elements_by_class_name("card-text")
                assert val == just_comment[0].text

    def test_writing_data_to_file_009(self):  # write comments back to file
        conduit_login(self.browser)
        self.browser.get(URL_articles)
        time.sleep(2)
        just_comment = self.browser.find_elements_by_class_name("card-text")

        with open("adat_kiir.txt", "w") as file_ki:
            for idx, val in enumerate(just_comment):
                val1 = val.text + "\n"
                file_ki.write(val1)

    def test_del_article_010(self):     # delete article
        conduit_cookie(self.browser)
        conduit_login(self.browser)
        conduit_add_article(self.browser)
        delete_article = self.browser.find_element_by_css_selector('button.btn.btn-outline-danger.btn-sm')
        delete_article.click()
        time.sleep(2)
        try:
            self.browser.find_element_by_link_text(URL_articles).click()
        except NoSuchElementException:
            print("article deleted")

    def test_logout_011(self):  # testing logout
        conduit_login(self.browser)
        time.sleep(2)
        nav_link_list = self.browser.find_elements_by_css_selector('a.nav-link')
        nav_link_list[4].click()
        nav_bar_list = self.browser.find_elements_by_css_selector("li.nav-item")
        without_logined_name = nav_bar_list[1].text
        assert without_logined_name == "Sign in"
