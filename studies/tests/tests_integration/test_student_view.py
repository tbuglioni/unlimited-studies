from django.test import TestCase
from django.urls import reverse
from studies.tests.speed_set_up import SpeedSetUP


class StudentView(TestCase):
    def setUp(self):
        speed_set_up = SpeedSetUP()

        self.user_a = speed_set_up.set_up_user_a()
        self.user_b = speed_set_up.set_up_user_b()

        self.book_1 = speed_set_up.create_book_owner(self.user_b, order_book=1)

        self.chapter_1 = speed_set_up.create_chapter(
            self.book_1, order_chapter=1)

        self.note_1 = speed_set_up.create_note(
            chapter=self.chapter_1, order_note=1, recto=True, verso=True
        )
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_1, lvl_recto=5, lvl_verso=5
        )

        self.student_1 = speed_set_up.add_student_to_book(
            self.user_a, self.book_1, to_accept=True, order_book=1
        )

    def test_student_page_200(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(reverse("studies:student_page"))
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "studies/student.html")

    def test_book_page_302(self):

        self.response = self.client.get(reverse("studies:student_page"))
        self.assertEqual(self.response.status_code, 302)

    def test_context(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(reverse("studies:student_page"))

        self.assertEqual(
            self.response.context["book_to_check"][0]["book_id"],
            self.book_1.id
        )
        self.assertEqual(
            self.response.context["book_to_check"][0]["book_name"],
            self.book_1.name
        )
        self.assertEqual(
            self.response.context["book_to_check"][0]["book_description"],
            self.book_1.description,
        )
        self.assertEqual(
            self.response.context["book_to_check"][0]["counter"], 1)
        self.assertEqual(
            self.response.context["book_to_check"][0]["owner"],
            self.user_b.username
        )
