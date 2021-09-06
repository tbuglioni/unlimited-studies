from django.test import TestCase
from django.urls import reverse
from studies.tests.speed_set_up import SpeedSetUP
from django.utils import timezone
from datetime import timedelta
from studies.models import StudiesNotesProgression
TIME_NOW = timezone.now()


class StartGameView(TestCase):
    def setUp(self):
        self.time_now = timezone.now()

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
            chapter=self.chapter_1, order_note=2, recto=True, verso=True
        )
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_2, lvl_recto=5, lvl_verso=5
        )

        self.note_3 = speed_set_up.create_note(
            chapter=self.chapter_1, order_note=3, recto=True, verso=True
        )
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_3, lvl_recto=5, lvl_verso=5
        )

    def test_start_game_view_200(self):
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(reverse("studies:game_auto"))
        self.assertTemplateUsed(self.response, "studies/auto_game.html")

    def test_update_lvl_1_2(self):

        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)
        note_to_update.level = 1
        note_to_update.save()

        self.client.login(email="john@invalid.com",
                          password="some_123_password")

        data = {"note_id": note_to_update.id, "win": "true"}
        self.client.post(
            reverse("studies:game_auto"), data, follow=True
        )
        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)

        self.assertEqual(note_to_update.level, 2)
        self.assertEqual(note_to_update.next_studied_date.strftime('%d/%m/%y'),
                         (self.time_now + timedelta(
                             days=1)).strftime('%d/%m/%y'))

    def test_update_lvl_2_3(self):

        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)
        note_to_update.level = 2
        note_to_update.save()

        self.client.login(email="john@invalid.com",
                          password="some_123_password")

        data = {"note_id": note_to_update.id, "win": "true"}
        self.client.post(
            reverse("studies:game_auto"), data, follow=True
        )
        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)

        self.assertEqual(note_to_update.level, 3)
        self.assertEqual(note_to_update.next_studied_date.strftime('%d/%m/%y'),
                         (self.time_now + timedelta(
                             days=1)).strftime('%d/%m/%y'))

    def test_update_lvl_3_4(self):

        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)
        note_to_update.level = 3
        note_to_update.save()

        self.client.login(email="john@invalid.com",
                          password="some_123_password")

        data = {"note_id": note_to_update.id, "win": "true"}
        self.client.post(
            reverse("studies:game_auto"), data, follow=True
        )
        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)

        self.assertEqual(note_to_update.level, 4)
        self.assertEqual(note_to_update.next_studied_date.strftime('%d/%m/%y'),
                         (self.time_now + timedelta(
                             days=1)).strftime('%d/%m/%y'))

    def test_update_lvl_4_5(self):

        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)
        note_to_update.level = 4
        note_to_update.save()

        self.client.login(email="john@invalid.com",
                          password="some_123_password")

        data = {"note_id": note_to_update.id, "win": "true"}
        self.client.post(
            reverse("studies:game_auto"), data, follow=True
        )
        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)

        self.assertEqual(note_to_update.level, 5)
        self.assertEqual(note_to_update.next_studied_date.strftime('%d/%m/%y'),
                         (self.time_now + timedelta(
                             days=1)).strftime('%d/%m/%y'))

    def test_update_lvl_5_6(self):

        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)
        note_to_update.level = 5
        note_to_update.save()

        self.client.login(email="john@invalid.com",
                          password="some_123_password")

        data = {"note_id": note_to_update.id, "win": "true"}
        self.client.post(
            reverse("studies:game_auto"), data, follow=True
        )
        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)

        self.assertEqual(note_to_update.level, 6)
        self.assertEqual(note_to_update.next_studied_date.strftime('%d/%m/%y'),
                         (self.time_now + timedelta(
                             days=3)).strftime('%d/%m/%y'))

    def test_update_lvl_6_7(self):

        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)
        note_to_update.level = 6
        note_to_update.save()

        self.client.login(email="john@invalid.com",
                          password="some_123_password")

        data = {"note_id": note_to_update.id, "win": "true"}
        self.client.post(
            reverse("studies:game_auto"), data, follow=True
        )
        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)

        self.assertEqual(note_to_update.level, 7)
        self.assertEqual(note_to_update.next_studied_date.strftime('%d/%m/%y'),
                         (self.time_now + timedelta(
                             days=7)).strftime('%d/%m/%y'))

    def test_update_lvl_7_8(self):

        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)
        note_to_update.level = 7
        note_to_update.save()

        self.client.login(email="john@invalid.com",
                          password="some_123_password")

        data = {"note_id": note_to_update.id, "win": "true"}
        self.client.post(
            reverse("studies:game_auto"), data, follow=True
        )
        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)

        self.assertEqual(note_to_update.level, 8)
        self.assertEqual(note_to_update.next_studied_date.strftime('%d/%m/%y'),
                         (self.time_now + timedelta(
                             days=30)).strftime('%d/%m/%y'))

    def test_update_lvl_8_9(self):

        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)
        note_to_update.level = 8
        note_to_update.save()

        self.client.login(email="john@invalid.com",
                          password="some_123_password")

        data = {"note_id": note_to_update.id, "win": "true"}
        self.client.post(
            reverse("studies:game_auto"), data, follow=True
        )
        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)

        self.assertEqual(note_to_update.level, 9)
        self.assertEqual(note_to_update.next_studied_date.strftime('%d/%m/%y'),
                         (self.time_now + timedelta(
                             days=90)).strftime('%d/%m/%y'))

    def test_update_lvl_9_10(self):

        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)
        note_to_update.level = 9
        note_to_update.save()

        self.client.login(email="john@invalid.com",
                          password="some_123_password")

        data = {"note_id": note_to_update.id, "win": "true"}
        self.client.post(
            reverse("studies:game_auto"), data, follow=True
        )
        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)

        self.assertEqual(note_to_update.level, 10)
        self.assertEqual(note_to_update.next_studied_date.strftime('%d/%m/%y'),
                         (self.time_now + timedelta(
                             days=182)).strftime('%d/%m/%y'))

    def test_update_lvl_10_10(self):

        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)
        note_to_update.level = 10
        note_to_update.save()

        self.client.login(email="john@invalid.com",
                          password="some_123_password")

        data = {"note_id": note_to_update.id, "win": "true"}
        self.client.post(
            reverse("studies:game_auto"), data, follow=True
        )
        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)

        self.assertEqual(note_to_update.level, 10)
        self.assertEqual(note_to_update.next_studied_date.strftime('%d/%m/%y'),
                         (self.time_now + timedelta(
                             days=364)).strftime('%d/%m/%y'))

    def test_update_lvl_10_1_when_fail(self):

        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)
        note_to_update.level = 10
        note_to_update.save()

        self.client.login(email="john@invalid.com",
                          password="some_123_password")

        data = {"note_id": note_to_update.id, "win": "false"}
        self.client.post(
            reverse("studies:game_auto"), data, follow=True
        )
        note_to_update = StudiesNotesProgression.objects.get(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)

        self.assertEqual(note_to_update.level, 1)
        self.assertEqual(note_to_update.next_studied_date.strftime('%d/%m/%y'),
                         (self.time_now + timedelta(
                             days=1)).strftime('%d/%m/%y'))
