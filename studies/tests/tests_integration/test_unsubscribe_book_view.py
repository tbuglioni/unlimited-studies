from django.test import TestCase
from django.urls import reverse
from studies.tests.speed_set_up import SpeedSetUP
from studies.models import (UserBookMany)


class UnsubscribeBookView(TestCase):
    def setUp(self):
        speed_set_up = SpeedSetUP()

        self.user_a = speed_set_up.set_up_user_a()
        self.user_b = speed_set_up.set_up_user_b()

        self.book_1 = speed_set_up.create_book_owner(self.user_a, order_book=1)
        self.book_2 = speed_set_up.create_book_owner(self.user_a, order_book=2)
        self.book_3 = speed_set_up.create_book_owner(self.user_a, order_book=3)

        self.student_1 = speed_set_up.add_student_to_book(
            self.user_b, self.book_1, to_accept=False, order_book=1
        )

        self.student_2 = speed_set_up.add_student_to_book(
            self.user_b, self.book_2, to_accept=False, order_book=2
        )

        self.student_3 = speed_set_up.add_student_to_book(
            self.user_b, self.book_3, to_accept=False, order_book=3
        )

    def test_unsubscribe_book(self):
        self.client.login(email="lee@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:unsubscribe_book",
                    kwargs={"book": self.book_2.id})
        )
        self.assertEqual(self.response.status_code, 302)
        book_a = UserBookMany.objects.filter(user=self.user_b).count()
        self.assertEqual(book_a, 2)

    def test_update_book_order_after_unsubscribe_book(self):
        self.client.login(email="lee@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:unsubscribe_book",
                    kwargs={"book": self.book_2.id})
        )
        book_1 = UserBookMany.objects.get(
            book=self.book_1, user=self.user_b).order_book
        self.assertEqual(book_1, 1)
        book_3 = UserBookMany.objects.get(
            book=self.book_3, user=self.user_b).order_book
        self.assertEqual(book_3, 2)
