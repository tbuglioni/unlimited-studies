from django.test import TestCase
from django.urls import reverse
from studies.tests.speed_set_up import SpeedSetUP
from studies.models import (StudiesNotes,
                            StudiesNotesProgression)


class NoteAddUpdateView(TestCase):
    def setUp(self):
        speed_set_up = SpeedSetUP()

        self.user_a = speed_set_up.set_up_user_a()
        self.user_b = speed_set_up.set_up_user_b()

        self.book_1 = speed_set_up.create_book_owner(self.user_a, order_book=1)

        self.chapter_1 = speed_set_up.create_chapter(
            self.book_1, order_chapter=1)

        self.note_1 = speed_set_up.create_note(
            chapter=self.chapter_1, order_note=1, recto=True, verso=True
        )
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_1, lvl_recto=5, lvl_verso=5
        )

        self.note_2 = speed_set_up.create_note(
            chapter=self.chapter_1, order_note=1, recto=True, verso=False
        )
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_2, lvl_recto=5, lvl_verso=5
        )

        self.note_3 = speed_set_up.create_note(
            chapter=self.chapter_1, order_note=1, recto=False, verso=True
        )
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_3, lvl_recto=5, lvl_verso=5
        )

    def test_book_page_with_chapter_302_1(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:specific_note", kwargs={
                    "chapter": self.chapter_1.id})
        )
        self.assertEqual(self.response.status_code, 302)

    def test_book_page_with_chapter_notes_302_2(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse(
                "studies:specific_note",
                kwargs={"chapter": self.chapter_1.id, "note": self.note_1.id},
            )
        )
        self.assertEqual(self.response.status_code, 302)

    def test_book_page_with_notes_302_3(self):
        self.response = self.client.get(
            reverse(
                "studies:specific_note",
                kwargs={"chapter": self.chapter_1.id, "note": self.note_1.id},
            )
        )
        self.assertEqual(self.response.status_code, 302)

    def test_add_new_note(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        data = {
            "text_recto": "hello world",
            "text_verso": "some text",
            "studie_recto": True,
            "studie_verso": True,
        }
        response = self.client.post(
            reverse("studies:specific_note", kwargs={
                    "chapter": self.chapter_1.id}),
            data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        note_a = StudiesNotes.objects.filter(
            users=self.user_a).distinct().count()
        self.assertEqual(note_a, 4)

    def test_update_note_1(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")

        # note 1 true/true -> true/true
        data = {
            "note_id": self.note_1.id,
            "text_recto": "hello world",
            "text_verso": "some text",
            "studie_recto": True,
            "studie_verso": True,
        }
        response = self.client.post(
            reverse(
                "studies:specific_note",
                kwargs={"chapter": self.chapter_1.id, "note": self.note_1.id},
            ),
            data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        note_all = StudiesNotes.objects.filter(
            users=self.user_a).distinct().count()
        self.assertEqual(note_all, 3)

        nbr_note_progression = StudiesNotesProgression.objects.filter(
            notes_id=self.note_1.id, user_id=self.user_a.id
        ).count()
        self.assertEqual(nbr_note_progression, 2)

    def test_update_note_2(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        # note 1 true/true -> false/false
        data = {
            "note_id": self.note_1.id,
            "text_recto": "hello world",
            "text_verso": "some text",
            "studie_recto": False,
            "studie_verso": False,
        }
        self.client.post(
            reverse(
                "studies:specific_note",
                kwargs={"chapter": self.chapter_1.id, "note": self.note_1.id},
            ),
            data,
            follow=True,
        )
        nbr_note_progression = StudiesNotesProgression.objects.filter(
            notes_id=self.note_1.id, user_id=self.user_a.id
        ).count()
        self.assertEqual(nbr_note_progression, 0)

    def test_update_note_3(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        # note 2 true/false -> false/true
        data = {
            "note_id": self.note_2.id,
            "text_recto": "hello world",
            "text_verso": "some text",
            "studie_recto": False,
            "studie_verso": True,
        }
        self.client.post(
            reverse(
                "studies:specific_note",
                kwargs={"chapter": self.chapter_1.id, "note": self.note_2.id},
            ),
            data,
            follow=True,
        )
        nbr_note_progression = StudiesNotesProgression.objects.filter(
            notes_id=self.note_2.id, user_id=self.user_a.id
        ).count()
        self.assertEqual(nbr_note_progression, 1)

    def test_update_note_4(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        # note 2 true/false -> true/true
        data = {
            "note_id": self.note_2.id,
            "text_recto": "hello world",
            "text_verso": "some text",
            "studie_recto": True,
            "studie_verso": True,
        }
        self.client.post(
            reverse(
                "studies:specific_note",
                kwargs={"chapter": self.chapter_1.id, "note": self.note_2.id},
            ),
            data,
            follow=True,
        )
        nbr_note_progression = StudiesNotesProgression.objects.filter(
            notes_id=self.note_2.id, user_id=self.user_a.id
        ).count()
        self.assertEqual(nbr_note_progression, 2)
        # test update_note_for_student

    def test_update_note_5(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        # note 3 false/true -> true/true
        data = {
            "note_id": self.note_3.id,
            "text_recto": "hello world",
            "text_verso": "some text",
            "studie_recto": True,
            "studie_verso": True,
        }
        self.client.post(
            reverse(
                "studies:specific_note",
                kwargs={"chapter": self.chapter_1.id, "note": self.note_3.id},
            ),
            data,
            follow=True,
        )
        nbr_note_progression = StudiesNotesProgression.objects.filter(
            notes_id=self.note_3.id, user_id=self.user_a.id
        ).count()
        self.assertEqual(nbr_note_progression, 2)
        # test update_note_for_student
