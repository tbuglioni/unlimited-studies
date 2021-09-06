from django.test import TestCase
from django.urls import reverse
from studies.tests.speed_set_up import SpeedSetUP
from studies.models import (Chapter)


class DeleteChapterView(TestCase):
    def setUp(self):
        speed_set_up = SpeedSetUP()

        self.user_a = speed_set_up.set_up_user_a()

        self.book_1 = speed_set_up.create_book_owner(self.user_a, order_book=1)

        self.chapter_1 = speed_set_up.create_chapter(
            self.book_1, order_chapter=1)
        self.chapter_2 = speed_set_up.create_chapter(
            self.book_1, order_chapter=2)
        self.chapter_3 = speed_set_up.create_chapter(
            self.book_1, order_chapter=3)

    def test_delete_chapter_view_302_no_login(self):

        self.response = self.client.get(
            reverse("studies:delete_chapter", kwargs={
                    "chapter": self.chapter_2.id})
        )
        self.assertEqual(self.response.status_code, 302)

    def test_delete_chapter_view_302_login(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:delete_chapter", kwargs={
                    "chapter": self.chapter_2.id})
        )
        self.assertEqual(self.response.status_code, 302)

    def test_chapter_is_removed(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.client.get(
            reverse("studies:delete_chapter", kwargs={
                    "chapter": self.chapter_2.id})
        )
        number_chapter = Chapter.objects.all().count()
        self.assertEqual(number_chapter, 2)

    def test_order_after_remove_chapter(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.client.get(
            reverse("studies:delete_chapter", kwargs={
                    "chapter": self.chapter_2.id})
        )
        chapter_1 = Chapter.objects.get(id=self.chapter_1.id).order_chapter
        chapter_3 = Chapter.objects.get(id=self.chapter_3.id).order_chapter

        self.assertEqual(chapter_1, 1)
        self.assertEqual(chapter_3, 2)
