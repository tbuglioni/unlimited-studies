from django.test import TestCase
from django.urls import reverse
from studies.models import UserBookMany
from studies.tests.speed_set_up import SpeedSetUP


class AddNewStudentView(TestCase):
    def setUp(self):
        speed_set_up = SpeedSetUP()

        self.user_a = speed_set_up.set_up_user_a()
        self.user_b = speed_set_up.set_up_user_b()

        self.book_1 = speed_set_up.create_book_owner(self.user_a, order_book=1)

    def test_new_student_page_302_ok(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:add_new_student", kwargs={"book": self.book_1.id})
        )
        self.assertEqual(self.response.status_code, 302)

    def test_new_student_page_302_no_login(self):
        self.response = self.client.get(
            reverse("studies:add_new_student", kwargs={"book": self.book_1.id})
        )
        self.assertEqual(self.response.status_code, 302)

    def test_add_new_student(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")

        data = {"new_student": "lee"}
        self.response = self.client.post(
            reverse("studies:add_new_student",
                    kwargs={"book": self.book_1.id}),
            data,
            follow=True,
        )
        student_exist = UserBookMany.objects.filter(
            user=self.user_b, book=self.book_1
        ).exists()
        self.assertEqual(student_exist, True)

    def test_add_new_student_bad_username(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")

        data = {"new_student": "leeee"}
        self.response = self.client.post(
            reverse("studies:add_new_student",
                    kwargs={"book": self.book_1.id}),
            data,
            follow=True,
        )
        student_exist = UserBookMany.objects.filter(
            user=self.user_b, book=self.book_1
        ).exists()
        self.assertEqual(student_exist, False)
