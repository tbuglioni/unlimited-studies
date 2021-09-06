from django.test import TestCase
from django.urls import reverse
from studies.tests.speed_set_up import SpeedSetUP
from studies.models import (StudiesNotesProgression)


class SubscribeBookView(TestCase):
    def setUp(self):
        speed_set_up = SpeedSetUP()

        self.user_a = speed_set_up.set_up_user_a()
        self.user_b = speed_set_up.set_up_user_b()

        self.book_1 = speed_set_up.create_book_owner(self.user_a, order_book=1)
        self.book_2 = speed_set_up.create_book_owner(self.user_a, order_book=2)

        self.chapter_1 = speed_set_up.create_chapter(
            self.book_1, order_chapter=1)
        self.chapter_2 = speed_set_up.create_chapter(
            self.book_1, order_chapter=2)

        self.note_1 = speed_set_up.create_note(
            chapter=self.chapter_1, order_note=1, recto=True, verso=True
        )
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_1, lvl_recto=5, lvl_verso=5
        )

        self.note_2 = speed_set_up.create_note(
            chapter=self.chapter_2, order_note=1, recto=True, verso=False
        )
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_2, lvl_recto=3, lvl_verso=3
        )

        self.student_1 = speed_set_up.add_student_to_book(
            self.user_b, self.book_1, to_accept=True, order_book=1
        )
        self.student_2 = speed_set_up.add_student_to_book(
            self.user_b, self.book_2, to_accept=True, order_book=2
        )

    def test_subscribe_book_page_302_ok(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:subscribe_book", kwargs={"book": self.book_1.id})
        )
        self.assertEqual(self.response.status_code, 302)

    def test_subscribe_book_302(self):

        self.response = self.client.get(
            reverse("studies:subscribe_book", kwargs={"book": self.book_1.id})
        )
        self.assertEqual(self.response.status_code, 302)

    def test_subscribe_book(self):
        self.client.login(email="lee@invalid.com",
                          password="some_123_password")

        # book1 (note:recto:true, verso:true)
        self.response = self.client.get(
            reverse("studies:subscribe_book", kwargs={"book": self.book_1.id})
        )
        number_notes_to_b = StudiesNotesProgression.objects.filter(
            user=self.user_b, notes_id=self.note_1.id
        ).count()

        self.assertEqual(number_notes_to_b, 2)

        # book2 (note: recto:true, verso:false)
        self.response = self.client.get(
            reverse("studies:subscribe_book", kwargs={"book": self.book_2.id})
        )
        number_notes_to_b = StudiesNotesProgression.objects.filter(
            user=self.user_b, notes_id=self.note_2.id
        ).count()

        self.assertEqual(number_notes_to_b, 1)
