from django.test import TestCase
from django.urls import reverse
from studies.tests.speed_set_up import SpeedSetUP


class DeleteNoteView(TestCase):
    def setUp(self):
        speed_set_up = SpeedSetUP()

        self.user_a = speed_set_up.set_up_user_a()

        self.book_1 = speed_set_up.create_book_owner(self.user_a, order_book=1)

        self.chapter_1 = speed_set_up.create_chapter(
            self.book_1, order_chapter=1)

        self.note_1 = speed_set_up.create_note(
            chapter=self.chapter_1, order_note=1, recto=True, verso=True
        )
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_1, lvl_recto=1, lvl_verso=1
        )

        self.note_2 = speed_set_up.create_note(
            chapter=self.chapter_1, order_note=1, recto=True, verso=True
        )
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_2, lvl_recto=1, lvl_verso=1
        )

        self.note_3 = speed_set_up.create_note(
            chapter=self.chapter_1, order_note=1, recto=True, verso=True
        )
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_3, lvl_recto=1, lvl_verso=1
        )

    def test_delete_note_view_302_no_log(self):
        self.response = self.client.get(
            reverse("studies:delete_note", kwargs={"note": self.note_1.id})
        )
        self.assertEqual(self.response.status_code, 302)

    def test_delete_note_view_302_log(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:delete_note", kwargs={"note": self.note_1.id})
        )
        self.assertEqual(self.response.status_code, 302)
