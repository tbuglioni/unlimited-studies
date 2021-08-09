from django.test import TestCase
from unittest.mock import MagicMock
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from studies.models import *
import datetime
from datetime import timedelta
User = get_user_model()


class StudiesPage(TestCase):
    def setUp(self):

        user_a = User(username="john", email="john@invalid.com")
        user_a_pw = "some_123_password"
        self.user_a_pw = user_a_pw
        user_a.is_staff = True
        user_a.is_teacher = True
        user_a.is_superuser = False
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a

        self.book_1 = Book.objects.create(
            name="English", order_book=1, description="book to learn english", source_info="Author 1",)
        self.book_1.users.add(self.user_a, through_defaults={})

        self.chapter_1 = Chapter.objects.create(
            name="vocabulary 1", order_chapter=1, book=self.book_1)

        self.note_1 = StudiesNotes.objects.create(
            text_recto="good moring", text_verso="bonjour", chapter=self.chapter_1, order_note=1, studie_verso=True)

        self.note_1.users.add(self.user_a, through_defaults={
            'lvl_recto': 1, "lvl_verso": 1})

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
            reverse("studies:personal_home", kwargs={'book': self.book_1.id}))
        self.assertEqual(self.response.status_code, 200)

        self.assertTemplateUsed(self.response, "studies/personal_home.html")

    def test_perso_home_page_302(self):
        self.response = self.client.get(reverse("studies:personal_home"))
        self.assertEqual(self.response.status_code, 302)

    def test_book_page(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:book_page", kwargs={'book': self.book_1.id}))
        self.assertEqual(self.response.status_code, 200)

    def test_book_page_with_chapter_200(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:book_page", kwargs={'book': self.book_1.id, 'chapter': self.chapter_1.id}))
        self.assertEqual(self.response.status_code, 200)

    def test_book_page_with_chapter_302(self):
        self.response = self.client.get(
            reverse("studies:book_page", kwargs={'book': self.book_1.id, 'chapter': self.chapter_1.id}))
        self.assertEqual(self.response.status_code, 302)

    def test_start_game_view_200(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(reverse("studies:game_auto"))
        self.assertEqual(self.response.status_code, 200)

        self.assertTemplateUsed(self.response, "studies/auto_game.html")

    def test_start_game_view_302(self):
        self.response = self.client.get(reverse("studies:game_auto"))
        self.assertEqual(self.response.status_code, 302)


class StudiesDatabase(TestCase):
    def setUp(self):
        self.TIME_NOW = datetime.date.today()
        user_a = User(username="john", email="john@invalid.com")
        user_a_pw = "some_123_password"
        self.user_a_pw = user_a_pw
        user_a.is_staff = True
        user_a.is_teacher = False
        user_a.is_superuser = False
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a

        user_b = User(username="lee", email="lee@invalid.com")
        user_b_pw = "some_123_password"
        self.user_b_pw = user_b_pw
        user_b.is_staff = True
        user_b.is_teacher = True
        user_b.is_superuser = False
        user_b.set_password(user_b_pw)
        user_b.save()
        self.user_b = user_b

        self.book_1 = Book.objects.create(
            name="English", order_book=1, description="book to learn english", source_info="Author 1",)
        self.book_1.users.add(self.user_a, through_defaults={})

        self.chapter_1 = Chapter.objects.create(
            name="vocabulary 1", order_chapter=1, book=self.book_1)

        self.note_1 = StudiesNotes.objects.create(
            text_recto="good morning", text_verso="bonjour", chapter=self.chapter_1, order_note=1, studie_verso=True)

        self.note_1.users.add(self.user_a, through_defaults={
            'lvl_recto': 1, "lvl_verso": 1})

        self.book_2 = Book.objects.create(
            name="English", order_book=1, description="book to learn english", source_info="Author 1",)
        self.book_2.users.add(self.user_a, through_defaults={})

        self.chapter_2 = Chapter.objects.create(
            name="vocabulary 2", order_chapter=1, book=self.book_2)

        self.note_2 = StudiesNotes.objects.create(
            text_recto="good morning", text_verso="bonjour", chapter=self.chapter_2, order_note=1, studie_verso=True)

        self.note_2.users.add(self.user_a, through_defaults={
            'lvl_recto': 1, "lvl_verso": 1})

    def test_count_book_users(self):
        book_a = Book.objects.filter(users=self.user_a).count()
        self.assertEqual(book_a, 2)

        book_b = Book.objects.filter(users=self.user_b).count()
        self.assertEqual(book_b, 0)

    def test_count_chapter_users(self):
        chapter_a = Chapter.objects.filter(book__users=self.user_a).count()
        self.assertEqual(chapter_a, 2)

        chapter_b = Chapter.objects.filter(book__users=self.user_b).count()
        self.assertEqual(chapter_b, 0)

    def test_count_note_users(self):
        note_a = StudiesNotes.objects.filter(users=self.user_a).count()
        self.assertEqual(note_a, 2)

        note_b = StudiesNotes.objects.filter(users=self.user_b).count()
        self.assertEqual(note_b, 0)

    def test_upgrade_note_lvl_recto_1_5(self):
        for i in range(1, 6):
            with self.subTest(i=i):
                self.client.login(email="john@invalid.com",
                                  password="some_123_password")
                note = StudiesNotes.objects.create(
                    text_recto="hello", text_verso="world", chapter=self.chapter_1, order_note=1, studie_verso=True)

                note.users.add(self.user_a, through_defaults={
                    'lvl_recto': i, "lvl_verso": 1})

                data = {"Product_id": note.id}
                response = self.client.post(
                    reverse("studies:note_true_recto"), data, follow=True
                )
                self.assertEqual(response.status_code, 200)

                note = StudiesNotesProgression.objects.get(notes=note.id)
                self.assertEqual(note.lvl_recto, i + 1)
                self.assertEqual(note.next_studied_date_recto,
                                 self.TIME_NOW + timedelta(days=1))

    def test_upgrade_note_lvl_verso_1_5(self):
        for i in range(1, 6):
            with self.subTest(i=i):
                # login
                self.client.login(email="john@invalid.com",
                                  password="some_123_password")

                # new note
                note = StudiesNotes.objects.create(
                    text_recto="hello", text_verso="world", chapter=self.chapter_1, order_note=1, studie_verso=True)

                note.users.add(self.user_a, through_defaults={
                    'lvl_recto': 1, "lvl_verso": i})

                # send id to perform task
                data = {"Product_id": note.id}
                response = self.client.post(
                    reverse("studies:note_true_verso"), data, follow=True)

                # check exit
                self.assertEqual(response.status_code, 200)

                note = StudiesNotesProgression.objects.get(notes=note.id)
                self.assertEqual(note.lvl_verso, i + 1)
                self.assertEqual(note.next_studied_date_verso,
                                 self.TIME_NOW + timedelta(days=1))

    def test_reset_note_lvl_recto_1_10(self):
        for i in range(1, 11):
            with self.subTest(i=i):
                # login
                self.client.login(email="john@invalid.com",
                                  password="some_123_password")

                # new note
                note = StudiesNotes.objects.create(
                    text_recto="hello", text_verso="world", chapter=self.chapter_1, order_note=1, studie_verso=True)

                note.users.add(self.user_a, through_defaults={
                    'lvl_recto': i, "lvl_verso": 1})

                # send id to perform task
                data = {"Product_id": note.id}
                response = self.client.post(
                    reverse("studies:note_wrong_recto"), data, follow=True)

                # check exit
                self.assertEqual(response.status_code, 200)

                note = StudiesNotesProgression.objects.get(notes=note.id)
                self.assertEqual(note.lvl_recto, 1)
                self.assertEqual(note.next_studied_date_recto,
                                 self.TIME_NOW + timedelta(days=1))

    def test_reset_note_lvl_verso_1_10(self):
        for i in range(1, 11):
            with self.subTest(i=i):
                self.client.login(email="john@invalid.com",
                                  password="some_123_password")
                note = StudiesNotes.objects.create(
                    text_recto="hello", text_verso="world", chapter=self.chapter_1, order_note=1, studie_verso=True)

                note.users.add(self.user_a, through_defaults={
                    'lvl_recto': 1, "lvl_verso": i})

                data = {"Product_id": note.id}
                response = self.client.post(
                    reverse("studies:note_wrong_verso"), data, follow=True
                )
                self.assertEqual(response.status_code, 200)

                note = StudiesNotesProgression.objects.get(notes=note.id)
                self.assertEqual(note.lvl_verso, 1)
                self.assertEqual(note.next_studied_date_verso,
                                 self.TIME_NOW + timedelta(days=1))

    def test_add_new_book(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        data = {"name": "hello world", "description": "some description",
                "source_info": "some source"}
        response = self.client.post(
            reverse("studies:personal_home"), data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        book_a = Book.objects.filter(users=self.user_a).count()
        self.assertEqual(book_a, 3)

    def test_update_book(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        data = {"name": "hello world", "description": "some description",
                "source_info": "some source"}
        response = self.client.post(
            reverse("studies:personal_home", kwargs={'book': self.book_1.id}), data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        book_a = Book.objects.filter(users=self.user_a).count()
        self.assertEqual(book_a, 2)

    def test_add_new_chapter(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        data = {"name": "hello world"}
        response = self.client.post(
            reverse("studies:book_page", kwargs={'book': self.book_1.id}), data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        chapter_a = Chapter.objects.filter(book__users=self.user_a).count()
        self.assertEqual(chapter_a, 3)

    def test_update_chapter(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        data = {"name": "hello world"}
        response = self.client.post(
            reverse("studies:book_page", kwargs={'book': self.book_1.id, 'chapter': self.chapter_1.id}), data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        chapter_a = Chapter.objects.filter(book__users=self.user_a).count()
        self.assertEqual(chapter_a, 2)

    def test_add_new_note(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        data = {"text_recto": "hello world", "text_verso": "some text",
                'studie_recto': True, 'studie_verso': True}
        response = self.client.post(
            reverse("studies:specific_note", kwargs={'chapter': self.chapter_1.id}), data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        note_a = StudiesNotes.objects.filter(users=self.user_a).count()
        self.assertEqual(note_a, 3)

    def test_update_note(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        data = {"text_recto": "hello world", "text_verso": "some text",
                'studie_recto': True, 'studie_verso': True}
        response = self.client.post(
            reverse("studies:specific_note", kwargs={'chapter': self.chapter_1.id, 'note': self.note_1.id}), data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        note_a = StudiesNotes.objects.filter(users=self.user_a).count()
        self.assertEqual(note_a, 2)

    def test_delete_book(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:delete_book", kwargs={'book': self.book_1.id}))
        self.assertEqual(self.response.status_code, 302)
        book_a = Book.objects.filter(users=self.user_a).count()
        self.assertEqual(book_a, 1)

    def test_delete_chapter(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:delete_chapter", kwargs={'chapter': self.chapter_1.id}))

        self.assertEqual(self.response.status_code, 302)
        chapter_a = Chapter.objects.filter(book__users=self.user_a).count()
        self.assertEqual(chapter_a, 1)

    def test_delete_note(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:delete_note", kwargs={'note': self.note_1.id}))

        self.assertEqual(self.response.status_code, 302)
        note_a = StudiesNotes.objects.filter(users=self.user_a).count()
        self.assertEqual(note_a, 1)
