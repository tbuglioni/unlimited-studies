from django.test import TestCase
from django.urls import reverse
from studies.models import Book, UserBookMany
from studies.tests.speed_set_up import SpeedSetUP


class DeleteBookView(TestCase):
    def setUp(self):
        speed_set_up = SpeedSetUP()

        self.user_a = speed_set_up.set_up_user_a()
        self.book_1 = speed_set_up.create_book_owner(self.user_a, order_book=1)
        self.book_2 = speed_set_up.create_book_owner(self.user_a, order_book=2)
        self.book_3 = speed_set_up.create_book_owner(self.user_a, order_book=3)

    def test_delete_book(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:delete_book", kwargs={"book": self.book_2.id})
        )
        self.assertEqual(self.response.status_code, 302)
        book_a = Book.objects.filter(users=self.user_a).count()
        self.assertEqual(book_a, 2)

    def test_update_book_order_on_delete(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:delete_book", kwargs={"book": self.book_2.id})
        )
        book_1 = UserBookMany.objects.get(book=self.book_1).order_book
        self.assertEqual(book_1, 1)
        book_3 = UserBookMany.objects.get(book=self.book_3).order_book
        self.assertEqual(book_3, 2)
