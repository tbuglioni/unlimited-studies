from django.test import TestCase
from django.urls import reverse
from studies.models import UserBookMany
from studies.tests.speed_set_up import SpeedSetUP


class UnsubscribeStudentBookView(TestCase):
    def setUp(self):
        speed_set_up = SpeedSetUP()

        self.user_a = speed_set_up.set_up_user_a()
        self.user_b = speed_set_up.set_up_user_b()

        self.book_1 = speed_set_up.create_book_owner(self.user_a, order_book=1)
        self.book_2 = speed_set_up.create_book_owner(self.user_a, order_book=2)
        self.book_3 = speed_set_up.create_book_owner(self.user_b, order_book=1)

        self.student_1 = speed_set_up.add_student_to_book(
            self.user_b, self.book_1, to_accept=True, order_book=2
        )
        self.student_2 = speed_set_up.add_student_to_book(
            self.user_b, self.book_2, to_accept=False, order_book=3
        )

    def test_unsubscribe_student_book_not_accepted(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse(
                "studies:unsubscribe_student",
                kwargs={"book": self.book_1.id, "student": self.user_b.id},
            )
        )

        self.assertEqual(self.response.status_code, 302)

        nbr_book = UserBookMany.objects.filter(user=self.user_b).count()
        self.assertEqual(nbr_book, 2)

    def test_unsubscribe_student_book_accepted(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse(
                "studies:unsubscribe_student",
                kwargs={"book": self.book_2.id, "student": self.user_b.id},
            )
        )

        self.assertEqual(self.response.status_code, 302)

        nbr_book = UserBookMany.objects.filter(user=self.user_b).count()
        self.assertEqual(nbr_book, 2)
