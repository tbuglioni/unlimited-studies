from django.test import TestCase
from studies.models import *
from django.urls import reverse
from django.contrib.auth import get_user_model
import datetime
from datetime import timedelta
User = get_user_model()


class ViewPage(TestCase):
    def setUp(self):

        # Create 1 user
        user_a = User(username="john", email="john@invalid.com")
        user_a_pw = "some_123_password"
        self.user_a_pw = user_a_pw
        user_a.is_staff = True
        user_a.is_teacher = True
        user_a.is_superuser = False
        user_a.set_password(user_a_pw)
        user_a.save()
        self.user_a = user_a

        # Create 1 book,chapter,note
        self.book_1 = Book.objects.create(
            name="English", order_book=1, description="book to learn english", source_info="Author 1",)
        self.book_1.users.add(self.user_a, through_defaults={})

        self.chapter_1 = Chapter.objects.create(
            name="vocabulary 1", order_chapter=1, book=self.book_1)

        self.note_1 = StudiesNotes.objects.create(
            text_recto="good morning", text_verso="bonjour", chapter=self.chapter_1, order_note=1, studie_verso=True)

        self.note_1.users.add(self.user_a, through_defaults={
            'lvl_recto': 1, "lvl_verso": 1})

    def test_perso_home_page_returns_200(self):
        """ personal_home_view : login(yes), data(no), GET"""

        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(reverse("studies:personal_home"))
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "studies/personal_home.html")

    def test_perso_home_page_returns_200_with_book(self):
        """ personal_home_view : login(yes), data(book_id), GET"""

        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:personal_home", kwargs={'book': self.book_1.id}))
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "studies/personal_home.html")

    def test_perso_home_page_302(self):
        """ personal_home_view : login(no), data(no), GET"""
        self.response = self.client.get(reverse("studies:personal_home"))
        self.assertEqual(self.response.status_code, 302)

    def test_book_page(self):
        """ book_view : login(yes), data(book_id), GET"""
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:book_page", kwargs={'book': self.book_1.id}))
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "studies/book.html")

    def test_book_page_with_chapter_200(self):
        """ book_view : login(yes), data(book_id, chapter_id), GET"""
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:book_page", kwargs={'book': self.book_1.id, 'chapter': self.chapter_1.id}))
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "studies/book.html")

    def test_book_page_with_chapter_302(self):
        """ book_view : login(no), data(book_id, chapter_id), GET"""
        self.response = self.client.get(
            reverse("studies:book_page", kwargs={'book': self.book_1.id, 'chapter': self.chapter_1.id}))
        self.assertEqual(self.response.status_code, 302)

    def test_book_page_with_notes_302_1(self):
        """ note_add_or_update_view : login(yes), data(chapter_id), GET"""
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:specific_note", kwargs={'chapter': self.chapter_1.id}))
        self.assertEqual(self.response.status_code, 302)

    def test_book_page_with_notes_302_2(self):
        """ note_add_or_update_view : login(yes), data(chapter_id, note_id), GET"""
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:specific_note", kwargs={'chapter': self.chapter_1.id, 'note': self.note_1.id}))
        self.assertEqual(self.response.status_code, 302)

    def test_book_page_with_notes_302_3(self):
        """ note_add_or_update_view : login(no), data(chapter_id, note_id), GET"""
        self.response = self.client.get(
            reverse("studies:specific_note", kwargs={'chapter': self.chapter_1.id, 'note': self.note_1.id}))
        self.assertEqual(self.response.status_code, 302)

    def test_delete_book_view_302_1(self):
        """ delete_book_view : login(no), data(chapter_id, note_id), GET"""

        self.response = self.client.get(
            reverse("studies:delete_book", kwargs={'book': self.book_1.id}))
        self.assertEqual(self.response.status_code, 302)

    def test_delete_book_view_302_2(self):
        """ delete_book_view : login(yes), data(chapter_id, note_id), GET"""
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:delete_book", kwargs={'book': self.book_1.id}))
        self.assertEqual(self.response.status_code, 302)

    def test_delete_chapter_view_302_1(self):
        """ delete_chapter_view : login(no), data(chapter_id, note_id), GET"""

        self.response = self.client.get(
            reverse("studies:delete_chapter", kwargs={'chapter': self.chapter_1.id}))
        self.assertEqual(self.response.status_code, 302)

    def test_delete_chapter_view_302_2(self):
        """ delete_chapter_view : login(yes), data(chapter_id, note_id), GET"""
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:delete_chapter", kwargs={'chapter': self.chapter_1.id}))
        self.assertEqual(self.response.status_code, 302)

    def test_delete_note_view_302_1(self):
        """ delete_note_view : login(no), data(chapter_id, note_id), GET"""

        self.response = self.client.get(
            reverse("studies:delete_note", kwargs={'note': self.note_1.id}))
        self.assertEqual(self.response.status_code, 302)

    def test_delete_note_view_302_2(self):
        """ delete_note_view : login(yes), data(chapter_id, note_id), GET"""
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:delete_note", kwargs={'note': self.note_1.id}))
        self.assertEqual(self.response.status_code, 302)

    def test_start_game_view_200(self):
        """ start_game_view : login(yes), data(), GET"""
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(reverse("studies:game_auto"))
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "studies/auto_game.html")

    def test_start_game_view_302(self):
        """ start_game_view : login(no), data(), GET"""
        self.response = self.client.get(reverse("studies:game_auto"))
        self.assertEqual(self.response.status_code, 302)


class ViewDatabase(TestCase):
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
            'lvl_recto': 2, "lvl_verso": 2})

        self.book_2 = Book.objects.create(
            name="English", order_book=1, description="book to learn english", source_info="Author 1",)
        self.book_2.users.add(self.user_a, through_defaults={})

        self.chapter_2 = Chapter.objects.create(
            name="vocabulary 2", order_chapter=1, book=self.book_2)

        self.note_2 = StudiesNotes.objects.create(
            text_recto="good morning", text_verso="bonjour", chapter=self.chapter_2, order_note=1, studie_verso=True)

        self.note_2.users.add(self.user_a, through_defaults={
            'lvl_recto': 2, "lvl_verso": 2})

    def test_add_new_book(self):
        """ personal_home_view : login(yes), data(), POST"""
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
        """ personal_home_view : login(yes), data(book_id), POST"""

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
        """ book_view : login(yes), data(book_id), POST"""
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
        """ book_view : login(yes), data(book_id,chapter_id), POST"""
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
        """ note_add_or_update_view : login(yes), data(chapter_id), POST"""
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
        """ note_add_or_update_view : login(yes), data(chapter_id,note_id), POST"""
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
        """ delete_book_view : login(yes), data(book_id), GET"""
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:delete_book", kwargs={'book': self.book_1.id}))
        self.assertEqual(self.response.status_code, 302)
        book_a = Book.objects.filter(users=self.user_a).count()
        self.assertEqual(book_a, 1)

    def test_delete_chapter(self):
        """ delete_chapter_view : login(yes), data(chapter_id), GET"""
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:delete_chapter", kwargs={'chapter': self.chapter_1.id}))

        self.assertEqual(self.response.status_code, 302)
        chapter_a = Chapter.objects.filter(book__users=self.user_a).count()
        self.assertEqual(chapter_a, 1)

    def test_delete_note(self):
        """ delete_note_view : login(yes), data(note_id), GET"""
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(
            reverse("studies:delete_note", kwargs={'note': self.note_1.id}))

        self.assertEqual(self.response.status_code, 302)
        note_a = StudiesNotes.objects.filter(users=self.user_a).count()
        self.assertEqual(note_a, 1)

    def test_start_game_view_200_POST_1(self):
        """ start_game_view : login(yes), data(), POST"""
        self.client.login(email="john@invalid.com",
                          password="some_123_password")

        data = {"note_id": 1, "note_sens": "verso", "win": "true"}
        response = self.client.post(
            reverse("studies:game_auto"), data, follow=True
        )
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        note_a = StudiesNotesProgression.objects.get(
            user=self.user_a, notes=1)
        self.assertEqual(note_a.lvl_verso, 3)
        self.assertEqual(note_a.next_studied_date_verso,
                         self.TIME_NOW + timedelta(days=1))

    def test_start_game_view_200_POST_2(self):
        """ start_game_view : login(yes), data(), POST"""
        self.client.login(email="john@invalid.com",
                          password="some_123_password")

        data = {"note_id": 1, "note_sens": "recto", "win": "false"}
        response = self.client.post(
            reverse("studies:game_auto"), data, follow=True
        )
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        note_a = StudiesNotesProgression.objects.get(
            user=self.user_a, notes=1)
        self.assertEqual(note_a.lvl_recto, 1)
        self.assertEqual(note_a.next_studied_date_recto,
                         self.TIME_NOW + timedelta(days=1))
