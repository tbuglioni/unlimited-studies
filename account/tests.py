from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):

        user_a = User(username="john", email="john@invalid.com")
        user_a_pw = "some_123_password"
        self.user_a_pw = user_a_pw
        user_a.is_staff = True
        user_a.is_teacher = True
        user_a.is_superuser = False
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a

    # models
    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)  # ==
        self.assertNotEqual(user_count, 0)  # !=

    def test_user_password(self):
        self.assertTrue(self.user_a.check_password(self.user_a_pw))

    def test_user_is_staff(self):
        self.assertTrue(self.user_a.is_staff)

    def test_user_is_not_superuser(self):
        self.assertFalse(self.user_a.is_superuser)

    # views
    def test_logout_url(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    def test_login_url(self):
        data = {"username": "john", "password": self.user_a_pw}
        response = self.client.post(reverse("login"), data, follow=True)
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_login_if_log(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")
        self.client.logout

    def test_account_url(self):
        response = self.client.get(reverse("account"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/")

    def test_account_if_log(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        response = self.client.get(reverse("account"))
        self.assertEqual(response.status_code, 200)
        self.client.logout

    def test_redirect_url(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_register_if_log(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")
        self.client.logout

    # template
    def test_login_using_template(self):
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, "account/login.html")

    def test_register_using_template(self):
        response = self.client.get(reverse("register"))
        self.assertTemplateUsed(response, "account/register.html")

    def test_account_using_template(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        response = self.client.get(reverse("account"))
        self.assertTemplateUsed(response, "account/account.html")
        self.client.logout

    def test_login_post(self):
        response = self.client.post(
            reverse("login"),
            {"email": "john@invalid.com", "password": "some_123_password"},
        )
        self.assertEqual(response.status_code, 302)

    def test_register_post(self):
        response = self.client.post(
            reverse("register"),
            {
                "email": "johnn@invalid.com",
                "username": "johny",
                "password1": "some_123_password",
                "password2": "some_123_password",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_login_post_invalid(self):
        response = self.client.post(
            reverse("register"),
            {
                "email": "johnninvalid.com",
                "username": "johnnny",
                "password1": "some_123_password",
                "password2": "some_123_password",
            },
        )
        self.assertEqual(response.status_code, 200)


class test_form_valid(TestCase):
    def setUp(self):

        user_a = User(username="john", email="john@invalid.com")
        user_a_pw = "some_123_password"
        self.user_a_pw = user_a_pw
        user_a.is_staff = True
        user_a.is_superuser = False
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a

    def test_account_update_form(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")

        response = self.client.post(
            reverse("account"), data={"mail": "test321@gmail.com"}
        )

        self.assertEqual(response.status_code, 200)

    def test_register_form(self):
        response = self.client.post(
            reverse("register"),
            data={
                "mail": "test321@gmail.com",
                "username": "test123",
                "password1": "some_123_password",
                "password2": "some_123_password",
            },
        )

        self.assertEqual(response.status_code, 200)
