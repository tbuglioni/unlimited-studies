from django.test import TestCase
from studies.models import *
from django.contrib.auth import get_user_model
import datetime
from datetime import timedelta
from studies.logic.game import Game
from unittest.mock import MagicMock
User = get_user_model()


class ViewDatabase(TestCase):
    def setUp(self):
        self.game = Game()
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

        self.note_3 = StudiesNotes.objects.create(
            text_recto="good morning", text_verso="bonjour", chapter=self.chapter_2, order_note=2, studie_verso=True)

        self.note_3.users.add(self.user_a, through_defaults={
            'lvl_recto': 8, "lvl_verso": 7})
        self.note_4 = StudiesNotes.objects.create(
            text_recto="good morning", text_verso="bonjour", chapter=self.chapter_2, order_note=3, studie_verso=True)

        self.note_4.users.add(self.user_a, through_defaults={
            'lvl_recto': 9, "lvl_verso": 10})
