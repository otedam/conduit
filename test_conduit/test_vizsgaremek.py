# A választott teszt alkalmazásnak legalább az alábbi funkcióit kell lefedni tesztekkel:
#  Regisztráció +
#  Bejelentkezés +
#  Adatkezelési nyilatkozat használata +
#  Adatok listázása ?
#  Több oldalas lista bejárása +
#  Új adat bevitel +
#  Ismételt és sorozatos adatbevitel adatforrásból +
#  Meglévő adat módosítás +
#  Adat vagy adatok törlése +
#  Adatok lementése felületről +
#  Kijelentkezés +
from datetime import datetime
import time

# import self as self
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
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

        # self.browser = webdriver.Chrome("C://chromedriver.exe")
        self.browser.get(URL_main)
        self.browser.maximize_window()

    def teardown(self):  # Minden teszt utan bezarja a dolgainkat.
        self.browser.quit()

    def test_cookie_001(self):  # Cookie accepting
        # cookie = self.browser.find_element_by_xpath(
        #       '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        cookie = find_element(self.browser, By.XPATH,
                              '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        cookie.click()
        # except:
        #  print("cookie clicked")

    def test_home_page_appearance_002(
            self):  # A fenti setup metodussal megnyitjuk a honlapot majd checkoljuk a title-ját a honlapnak
        conduit = self.browser.title
        # print(conduit)
        assert conduit == "Conduit"

    def test_register_003(self):
        conduit_cookie(self.browser)
        self.browser.find_element_by_xpath("/html/body//a[contains(@href,'register')]").click()
        self.browser.find_element_by_xpath("//input[@type='text'][@placeholder='Username']").send_keys(
            "GarFelhasznalo1")
        self.browser.find_element_by_xpath("//input[@type='text'][@placeholder='Email']").send_keys(
            "GarFelhasznalo1@gmail.com")
        self.browser.find_element_by_xpath("//input[@placeholder='Password']").send_keys("Password1")
        # time.sleep(2)
        # self.browser.find_element_by_css_selector(".btn.btn-lg.btn-primary.pull-xs-right").click()
        button_reg = find_element(self.browser, By.CSS_SELECTOR, ".btn.btn-lg.btn-primary.pull-xs-right")
        button_reg.click()
        # self.browser.find_element_by_xpath('//button[@class="btn login-btn"]').click()
        welcome = find_element(self.browser, By.CSS_SELECTOR, ".swal-title")

        # welcome = WebDriverWait(self.browser, 5).until(
        #     EC.visibility_of_element_located((By.CSS_SELECTOR, ".swal-title"))
        # )
        welcome_text = welcome.text
        # print(welcome_text)
        assert welcome_text == "Welcome!"
        self.browser.find_element_by_css_selector(".swal-button.swal-button--confirm").click()
        nav_bar_list = self.browser.find_elements_by_css_selector("li.nav-item")
        logined_name = nav_bar_list[3].text
        # print(logined_name)
        assert logined_name == "GarFelhasznalo1"

    def test_navigate_to_login_004(self):
        conduit_cookie(self.browser)
        nav_bar_list = self.browser.find_elements_by_css_selector("li.nav-item")
        logined_name = nav_bar_list[1].text
        # print(logined_name)
        assert logined_name == "Sign in"
        self.browser.find_elements_by_css_selector("li.nav-item")[1].click()
        self.browser.find_element_by_css_selector("input[placeholder='Email']").send_keys("GarFelhasznalo1@gmail.com")
        self.browser.find_element_by_css_selector('input[placeholder="Password"]').send_keys("Password1")
        # time.sleep(3)
        # self.browser.find_element_by_css_selector('.btn.btn-lg.btn-primary.pull-xs-right').click()
        sign_in_button = find_element(self.browser, By.CSS_SELECTOR, '.btn.btn-lg.btn-primary.pull-xs-right')
        sign_in_button.click()
        time.sleep(2)
        nav_link_list = self.browser.find_elements_by_class_name('nav-link')
        # nav_link_list = find_element(self.browser, By.CSS_SELECTOR, 'nav-link')
        signed_in_name = nav_link_list[3].text
        # print(signed_in_name)
        assert signed_in_name == "GarFelhasznalo1"

    def test_adding_new_article_005(self):
        conduit_cookie(self.browser)
        conduit_login(self.browser)
        # self.browser.find_element_by_css_selector('a.nav-link.router-link-exact-active.active').click()
        self.browser.find_element_by_css_selector('a[href="#/editor"]').click()
        # self.browser.switch_to.window(self.browser.window_handles[0])
        # time.sleep(2)
        # self.browser.find_element_by_css_selector('input[placeholder="Article Title"]').send_keys(new_article_for_file)
        new_article_input = find_element(self.browser, By.CSS_SELECTOR, 'input[placeholder="Article Title"]')
        new_article_input.send_keys(new_article_for_file)
        self.browser.find_element_by_css_selector('input[placeholder="What\'s this article about?"]').send_keys(
            new_about)
        self.browser.find_element_by_css_selector('textarea[placeholder="Write your article (in markdown)"]').send_keys(
            post_content)
        self.browser.find_element_by_css_selector('input[placeholder="Enter tags"]').send_keys(enter_tag + Keys.TAB)
        self.browser.find_element_by_css_selector('button[type="submit"]').click()
        # time.sleep(5)
        # new_content_text = self.browser.find_element_by_xpath('//textarea[@placeholder="Write a comment..."]')
        new_content_text = find_element(self.browser, By.XPATH, '//textarea[@placeholder="Write a comment..."]')
        new_content_text.send_keys(post_content)

        # post_comment_button = self.browser.find_element_by_xpath('//button[text()="Post Comment"]')
        # # print(post_comment_button)
        # post_comment_button.click()
        # time.sleep(4)
        # #
        # new_comment = WebDriverWait(self.browser, 10).until(
        #     EC.visibility_of_element_located((By.CSS_SELECTOR, "p.card-text"))
        # )
        # nc = new_comment.text
        # print(nc)
        # assert "Lorem" in nc

    # def test_edit_article_006(self):
    #     print("6.")
    #     self.test_adding_new_post_005()
    #     self.browser.find_element_by_xpath('//div//span//a[@class="btn btn-sm btn-outline-secondary"]//span[1]').click()
    #     # URL_to_edit_article = URL_editor + new_article
    #     # self.browser.get(URL_to_edit_article)
    #     time.sleep(2)
    #     art_tit = self.browser.find_element_by_css_selector('input[placeholder="Article Title"]')
    #     art_tit.clear()
    #     art_tit.send_keys("modified article title")
    #     time.sleep(4)
    #     # self.browser.find_element_by_css_selector('input[placeholder="What\'s this article about?"]').send_keys("modified what about")
    #     # self.browser.find_element_by_css_selector('textarea[placeholder="Write your article (in markdown)"]').send_keys("modified article\'s text")
    #     # self.browser.find_element_by_css_selector('input[placeholder="Enter tags"]').send_keys("mod_tag")
    #     # time.sleep(3)
    #     self.browser.find_element_by_css_selector('button[type="submit"]').click()
    #     print("submit küldve")
    #     time.sleep(3)
    #     assert_text = self.browser.find_element_by_tag_name('//h1').text
    #     # assert_text = self.browser.find_element_by_xpath('//div[@class="container"]/h1').text
    #     # assert_text = self.browser.find_element_by_css_selector('div[class="container"] h1').text
    #
    #     # assert_text = self.browser.find_element_by_css_selector('div:nth-child(2) div.article-page:nth-child(2) div.banner div.container > h1:nth-child(1)').text
    #     print(assert_text)
    #     assert "modified" in assert_text

    def test_edit_settings_006(self):
        conduit_login(self.browser)
        self.browser.find_element_by_css_selector('a[href="#/settings"]').click()
        # time.sleep(2)
        # bio = self.browser.find_element_by_css_selector('textarea[placeholder="Short bio about you"]')
        bio = find_element(self.browser, By.CSS_SELECTOR, 'textarea[placeholder="Short bio about you"]')
        bio.clear()
        bio.send_keys('Tesztelek')
        time.sleep(2)
        self.browser.find_element_by_css_selector('.btn.btn-lg.btn-primary.pull-xs-right').click()

        # update = WebDriverWait(self.browser, 5).until(
        #     EC.visibility_of_element_located((By.CSS_SELECTOR, ".swal-title"))
        # )
        update = find_element(self.browser, By.CSS_SELECTOR, ".swal-title")
        update_text = update.text
        print(update_text)
        assert update_text == "Update successful!"
        self.browser.find_element_by_css_selector(".swal-button.swal-button--confirm").click()
        time.sleep(2)
        nav_bar_list = self.browser.find_elements_by_css_selector("li.nav-item")
        nav_bar_list[3].click()
        time.sleep(2)
        mod_setting = self.browser.find_element_by_css_selector('div[class="user-info"] p').text
        assert mod_setting == 'Tesztelek'

    def test_pagination_007(self):
        conduit_cookie(self.browser)
        # browser.find_element_by_css_selector(".navbar-brand.router-link-active").click()
        # time.sleep(2)
        page_links = self.browser.find_elements_by_class_name("page-link")
        hossz = len(page_links)
        for page in page_links:
            if page.text != hossz:
                page.click()
            else:
                assert page.text == hossz

    def test_adding_data_from_file_008(self):
        conduit_cookie(self.browser)
        conduit_login(self.browser)
        conduit_add_article(self.browser)
        with open("adat.txt", "r") as file:
            comment_list = file.readlines()
            my_list2 = [s[:-1] for s in comment_list]
            for idx, val in enumerate(my_list2):
                new_content_text = find_element(self.browser, By.XPATH, '//textarea[@placeholder="Write a comment..."]')

                # time.sleep(1)
                # new_content_text = self.browser.find_element_by_xpath('//textarea[@placeholder="Write a comment..."]')
                new_content_text.send_keys(val)
                time.sleep(1)
                self.browser.find_element_by_xpath('//button[text()="Post Comment"]').click()
                # just_comment = find_element(self.browser, By.CLASS_NAME, "card-text")

                time.sleep(1)
                just_comment = self.browser.find_elements_by_class_name("card-text")
                # print("my_list2: ", idx, "értéke: ", val)
                # print("just_comment lista", idx, "szövege ", just_comment[0].text)
                assert val == just_comment[0].text

    def test_writing_data_to_file_009(self):
        conduit_login(self.browser)
        self.browser.get(URL_articles)
        time.sleep(2)
        # just_comment = find_element(self.browser, By.CLASS_NAME, "card-text")
        just_comment = self.browser.find_elements_by_class_name("card-text")

        with open("adat_kiir.txt", "w") as file_ki:
            for idx, val in enumerate(just_comment):
                val1 = val.text + "\n"
                # print(val1)
                file_ki.write(val1)

    def test_del_article_010(self):
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

    def test_logout_011(self):
        conduit_login(self.browser)
        time.sleep(2)
        nav_link_list = self.browser.find_elements_by_css_selector('a.nav-link')
        nav_link_list[4].click()
        nav_bar_list = self.browser.find_elements_by_css_selector("li.nav-item")
        without_logined_name = nav_bar_list[1].text
        # print(without_logined_name)
        assert without_logined_name == "Sign in"

# A testet a terminalbol a:  python -m pytest parancsal inditjuk
# A pytestet allure segedlettel a: python -m pytest --alluredir=./out            Az = utan a mappat kell megadnunk ahova mentse a json formatumokat.
# Sajat allure server inditása: allure serve ./out
