from django.test import TestCase
from django.urls import reverse
from .speed_set_up import SpeedSetUP
from studies.models import *


class TeacherView(TestCase):
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

        self.chapter_5 = speed_set_up.create_chapter(
            self.book_3, order_chapter=1)

        self.note_1 = speed_set_up.create_note(
            chapter=self.chapter_1, order_note=1, recto=True, verso=True)
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_1, lvl_recto=5, lvl_verso=5)

        self.note_2 = speed_set_up.create_note(
            chapter=self.chapter_2, order_note=1, recto=True, verso=True)
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_2, lvl_recto=3, lvl_verso=8)

        self.note_1 = speed_set_up.create_note(
            chapter=self.chapter_5, order_note=1, recto=True, verso=True)
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_1, lvl_recto=5, lvl_verso=5)

        speed_set_up.add_user_to_notes(
            user=self.user_b, note=self.note_1, lvl_recto=5, lvl_verso=5)

        self.student_1 = speed_set_up.add_student_to_book(
            self.user_a, self.book_4, to_accept=True, order_book=4)
        self.student_2 = speed_set_up.add_student_to_book(
            self.user_b, self.book_2, to_accept=True, order_book=2)
        self.student_3 = speed_set_up.add_student_to_book(
            self.user_b, self.book_3, to_accept=False, order_book=3)

    def test_teacher_page_200(self):
        """ teacher_view : login(yes)), GET"""
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:teacher_page", kwargs={'book': self.book_1.id}))
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "studies/teacher.html")

    def test_teacher_page_302(self):
        """ teacher_view : login(no), GET"""

        self.response = self.client.get(
            reverse("studies:teacher_page", kwargs={'book': self.book_1.id}))
        self.assertEqual(self.response.status_code, 302)

    def test_context(self):
        """ teacher_view : login(yes)), GET"""
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:teacher_page", kwargs={'book': self.book_1.id}))

        # book1
        self.assertEqual(
            self.response.context["book"], self.book_1.id)
        self.assertEqual(self.response.context["error"], 0)
        self.assertEqual(
            self.response.context["user_in_acceptation"].count(), 0)
        self.assertEqual(
            self.response.context["user_accepted"], [])

        # book2 (student in acceptation)
        self.response = self.client.get(
            reverse("studies:teacher_page", kwargs={'book': self.book_2.id}))
        self.assertEqual(
            self.response.context["user_in_acceptation"].count(), 1)
        self.assertEqual(
            self.response.context["user_accepted"], [])

        # book3 (student accepted)
        self.response = self.client.get(
            reverse("studies:teacher_page", kwargs={'book': self.book_3.id}))
        self.assertEqual(
            self.response.context["user_in_acceptation"].count(), 0)
        self.assertEqual(
            self.response.context["user_accepted"], [{'username': 'lee', 'lvl_avg': 5.0, 'user_id': self.user_b.id}])
