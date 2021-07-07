import time


from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from unlimited_studies.settings import BASE_DIR
from selenium import webdriver
from django.contrib.auth import get_user_model

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
        user_a = User(username="john", email="john@invalid.com")
        user_a_pw = "some_123_password"
        self.user_a_pw = user_a_pw
        user_a.is_staff = True
        user_a.is_superuser = False
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a

    def test_PageTitle(self):
        self.browser.get(("%s%s" % (self.live_server_url, "/login/")))
        self.assertIn("Unlimited-S", self.browser.title)
        # self.browser.get(self.live_server_url)
        # self.assertIn("Unlimited-S", self.browser.title)

    def test_login(self):
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
