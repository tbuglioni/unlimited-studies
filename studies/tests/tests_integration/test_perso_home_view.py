from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from studies.models import Book, UserBookMany
from studies.tests.speed_set_up import SpeedSetUP


class PersonalHome(TestCase):
    def setUp(self):
        speed_set_up = SpeedSetUP()

        self.user_a = speed_set_up.set_up_user_a()
        self.user_b = speed_set_up.set_up_user_b()

        self.book_1 = speed_set_up.create_book_owner(self.user_a, order_book=1)
        self.book_2 = speed_set_up.create_book_owner(self.user_a, order_book=2)
        self.book_3 = speed_set_up.create_book_owner(self.user_a, order_book=3)
        self.book_4 = speed_set_up.create_book_owner(self.user_b, order_book=1)

        self.chapter_1 = speed_set_up.create_chapter(
            self.book_1, order_chapter=1)
        self.chapter_2 = speed_set_up.create_chapter(
            self.book_2, order_chapter=1)

        self.note_1 = speed_set_up.create_note(
            chapter=self.chapter_1, order_note=1, recto=True, verso=True
        )
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_1, lvl_recto=1, lvl_verso=1
        )

        self.note_2 = speed_set_up.create_note(
            chapter=self.chapter_2, order_note=2, recto=True, verso=True
        )
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_2, lvl_recto=3, lvl_verso=8
        )

        self.student_1 = speed_set_up.add_student_to_book(
            self.user_a, self.book_4, to_accept=True, order_book=4
        )

    def test_perso_home_page_returns_200(self):

        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(reverse("studies:personal_home"))
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "studies/personal_home.html")

    def test_perso_home_page_returns_200_with_book(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:personal_home", kwargs={"book": self.book_1.id})
        )
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "studies/personal_home.html")

    def test_perso_home_page_302(self):
        self.response = self.client.get(reverse("studies:personal_home"))
        self.assertEqual(self.response.status_code, 302)

    def test_add_new_book(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")

        data = {
            "name": "hello world",
            "description": "some description",
            "source_info": "some source",
            "users": self.user_a,
        }
        response = self.client.post(
            reverse("studies:personal_home"), data, follow=True)
        self.assertEqual(response.status_code, 200)
        book_a = Book.objects.filter(users=self.user_a).count()
        self.assertEqual(book_a, 5)

    def test_update_book(self):

        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        data = {
            "book_id": self.book_1.id,
            "name": "hello world",
            "description": "some description",
            "source_info": "some source",
            "order_book": 2,
        }
        response = self.client.post(
            reverse("studies:personal_home", kwargs={"book": self.book_1.id}),
            data,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        book_a = Book.objects.filter(users=self.user_a).count()
        self.assertEqual(book_a, 4)

        book_1_progression = UserBookMany.objects.get(
            user=self.user_a, book=self.book_1
        ).order_book
        self.assertEqual(book_1_progression, 2)

    def test_context(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:personal_home", kwargs={"book": self.book_1.id})
        )

        self.assertEqual(self.response.context["books"][0].name, "English")
        self.assertEqual(self.response.context["books"].count(), 3)
        self.assertEqual(self.response.context["books_info"].count(), 3)
        self.assertEqual(self.response.context["new_book_from_teacher"], True)
        self.assertEqual(self.response.context["todoo"], 4)
        self.assertEqual(self.response.context["all_notes"], 2)
        self.assertEqual(self.response.context["all_notes_avg"], 3.25)
        self.assertEqual(self.response.context["books_avg"], [1.0, 5.5, 0, 0])
        self.assertEqual(self.response.context["Today_recap"], 0)
        self.assertEqual(self.response.context["month_recap"], 0)
        self.assertEqual(
            self.response.context["recap_data"]["list_date"][1],
            timezone.now().strftime("%d/%m/%y"),
        )
        self.assertEqual(self.response.context["selectedBook"], self.book_1)
