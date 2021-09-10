from django.test import TestCase
from django.urls import reverse
from studies.models import Chapter
from studies.tests.speed_set_up import SpeedSetUP


class BookView(TestCase):
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
            self.book_1, order_chapter=2)
        self.chapter_3 = speed_set_up.create_chapter(
            self.book_1, order_chapter=3)
        self.chapter_4 = speed_set_up.create_chapter(
            self.book_1, order_chapter=4)

        self.note_1 = speed_set_up.create_note(
            chapter=self.chapter_1, order_note=1, recto=True, verso=True
        )
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_1, lvl_recto=5, lvl_verso=5
        )
        self.note_2 = speed_set_up.create_note(
            chapter=self.chapter_2, order_note=1, recto=True, verso=True
        )
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_2, lvl_recto=3, lvl_verso=8
        )

        self.student_1 = speed_set_up.add_student_to_book(
            self.user_a, self.book_4, to_accept=True, order_book=4
        )

    def test_book_page_200(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:book_page", kwargs={"book": self.book_1.id})
        )
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "studies/book.html")

    def test_book_page_with_chapter_200(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse(
                "studies:book_page",
                kwargs={"book": self.book_1.id, "chapter": self.chapter_1.id},
            )
        )
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "studies/book.html")

    def test_book_page_with_chapter_302(self):
        self.response = self.client.get(
            reverse(
                "studies:book_page",
                kwargs={"book": self.book_1.id, "chapter": self.chapter_1.id},
            )
        )
        self.assertEqual(self.response.status_code, 302)

    def test_add_new_chapter(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        data = {"name": "hello world"}
        response = self.client.post(
            reverse("studies:book_page", kwargs={"book": self.book_1.id}),
            data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        chapter_a = Chapter.objects.filter(book__users=self.user_a).count()
        self.assertEqual(chapter_a, 5)

    def test_update_chapter(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        data = {
            "name": "hello world",
            "chapter_id": self.chapter_1.id,
            "order_chapter": 2,
        }
        response = self.client.post(
            reverse(
                "studies:book_page",
                kwargs={"book": self.book_1.id, "chapter": self.chapter_1.id},
            ),
            data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        chapter_a = Chapter.objects.filter(book__users=self.user_a).count()
        self.assertEqual(chapter_a, 4)
        chapter_end_1 = Chapter.objects.get(id=self.chapter_1.id)
        self.assertEqual(chapter_end_1.order_chapter, 2)

        chapter_end_2 = Chapter.objects.get(id=self.chapter_2.id)
        self.assertEqual(chapter_end_2.order_chapter, 1)

        chapter_end_3 = Chapter.objects.get(id=self.chapter_3.id)
        self.assertEqual(chapter_end_3.order_chapter, 3)

    def test_context(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse(
                "studies:book_page",
                kwargs={"book": self.book_1.id, "chapter": self.chapter_1.id},
            )
        )

        self.assertEqual(self.response.context["user_fonction"], "owner")
        self.assertEqual(self.response.context["book"].name, "English")
        self.assertEqual(self.response.context["chapters"].count(), 4)
        self.assertEqual(
            self.response.context["chapters_notes_avg"], [5.0, 5.5, 0, 0])
        self.assertEqual(self.response.context["chapter"].name, "vocabulary 1")
        self.assertEqual(self.response.context["notes"].number, 1)
