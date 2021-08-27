from django.test import TestCase
from unittest.mock import MagicMock
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from studies.models import *
import datetime
from datetime import timedelta
User = get_user_model()


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
            name="English", description="book to learn english", source_info="Author 1",)
        self.book_1.users.add(self.user_a, through_defaults={"order_book":1})

        self.chapter_1 = Chapter.objects.create(
            name="vocabulary 1", order_chapter=1, book=self.book_1)

        self.note_1 = StudiesNotes.objects.create(
            text_recto="good morning", text_verso="bonjour", chapter=self.chapter_1, order_note=1, studie_verso=True)

        self.note_1.users.add(self.user_a, through_defaults={
            'lvl_recto': 1, "lvl_verso": 1})

        self.book_2 = Book.objects.create(
            name="English", description="book to learn english", source_info="Author 1",)
        self.book_2.users.add(self.user_a, through_defaults={"order_book":1})

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
