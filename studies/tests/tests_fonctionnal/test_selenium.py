import time


from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from unlimited_studies.settings import BASE_DIR
from selenium import webdriver
from django.contrib.auth import get_user_model
from studies.tests.speed_set_up import SpeedSetUP

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("window-size=1920x1080")

User = get_user_model()


class MySeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome(
            executable_path=str(BASE_DIR / "webdrivers" / "chromedriver"),
            options=chrome_options,
        )
        cls.browser.implicitly_wait(30)
        cls.browser.maximize_window()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.quit()

    def setUp(self):
        speed_set_up = SpeedSetUP()

        self.user_a = speed_set_up.set_up_user_a()
        self.book_1 = speed_set_up.create_book_owner(self.user_a, order_book=1)

    def test_nav(self):
        self.browser.get(("%s%s" % (self.live_server_url, "/logout/")))
        self.browser.get(("%s%s" % (self.live_server_url, "/login/")))
        mail = self.browser.find_element_by_id("id_email")
        password = self.browser.find_element_by_id("id_password")
        submit = self.browser.find_element_by_id("submit_login")
        mail.send_keys("john@invalid.com")
        password.send_keys("some_123_password")
        submit.click()
        time.sleep(1)
        cur_url = self.browser.current_url
        self.assertEqual(cur_url, (self.live_server_url + "/"))

        perso_home = self.browser.find_element_by_id("button_personal_home")
        perso_home.click()
        time.sleep(3)
        cur_url = self.browser.current_url
        self.assertEqual(cur_url, (self.live_server_url + "/studies/"))

        notice_page = self.browser.find_element_by_id("button_notice_page")
        notice_page.click()
        time.sleep(3)
        cur_url = self.browser.current_url
        self.assertEqual(cur_url, (self.live_server_url + "/#help-section"))

        account_page = self.browser.find_element_by_id("account_page")
        account_page.click()
        time.sleep(3)
        cur_url = self.browser.current_url
        self.assertEqual(cur_url, (self.live_server_url + "/account/"))
