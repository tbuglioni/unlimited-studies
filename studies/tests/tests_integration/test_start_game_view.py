from django.test import TestCase
from django.urls import reverse
from .speed_set_up import SpeedSetUP
from studies.models import *
from django.utils import timezone
from datetime import timedelta

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
            chapter=self.chapter_1, order_note=1, recto=True, verso=True)
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_1, lvl_recto=1, lvl_verso=1)

        self.note_2 = speed_set_up.create_note(
            chapter=self.chapter_1, order_note=2, recto=True, verso=True)
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_2, lvl_recto=5, lvl_verso=5)

        self.note_3 = speed_set_up.create_note(
            chapter=self.chapter_1, order_note=3, recto=True, verso=True)
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_3, lvl_recto=5, lvl_verso=5)

    def test_start_game_view_200(self):
        """ start_game_view : login(yes), data(), GET"""
        self.client.login(email="john@invalid.com",
                          password="some_123_password")
        self.response = self.client.get(reverse("studies:game_auto"))
        self.assertTemplateUsed(self.response, "studies/auto_game.html")

    # def __loop_lvl(self, note_to_update, data, lvl_target: int, days_added: int):

    #     self.client.post(
    #         reverse("studies:game_auto"), data, follow=True
    #     )
    #     self.assertEqual(note_to_update[0].level, lvl_target)
    #     self.assertEqual(note_to_update[0].next_studied_date.strftime('%d/%m/%y'),
    #                      (self.time_now + timedelta(days=days_added)).strftime('%d/%m/%y'))

    # def test_start_game_view_200_POST_win(self):
    #     """ start_game_view : login(yes), data(), POST"""
    #     self.client.login(email="john@invalid.com",
    #                       password="some_123_password")
    #     note_to_update = StudiesNotesProgression.objects.filter(
    #         user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)

    #     data = {"note_id": note_to_update[0].id, "win": "true"}

    #     self.__loop_lvl(data, note_to_update, lvl_target=2, days_added=1)
    #     self.__loop_lvl(data, note_to_update, lvl_target=3, days_added=1)
    #     self.__loop_lvl(data, note_to_update, lvl_target=4, days_added=1)
    #     self.__loop_lvl(data, note_to_update, lvl_target=5, days_added=1)
    #     self.__loop_lvl(data, note_to_update, lvl_target=6, days_added=3)
    #     self.__loop_lvl(data, note_to_update, lvl_target=7, days_added=7)
    #     self.__loop_lvl(data, note_to_update, lvl_target=8, days_added=30)
    #     self.__loop_lvl(data, note_to_update, lvl_target=9, days_added=90)
    #     self.__loop_lvl(data, note_to_update, lvl_target=10, days_added=182)
    #     self.__loop_lvl(data, note_to_update, lvl_target=10, days_added=364)
    #     self.__loop_lvl(data, note_to_update, lvl_target=10, days_added=364)

    # def test_start_game_view_200_POST_fail(self):
    #     """ start_game_view : login(yes), data(), POST"""
    #     self.client.login(email="john@invalid.com",
    #                       password="some_123_password")
    #     note_to_update = StudiesNotesProgression.objects.filter(
    #         user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True)

    #     data = {"note_id": note_to_update[0].id, "win": "true"}
    #     self.__loop_lvl(data, note_to_update, lvl_target=2, days_added=1)
    #     self.__loop_lvl(data, note_to_update, lvl_target=3, days_added=1)

    #     data = {"note_id": note_to_update.id, "win": "false"}
    #     self.__loop_lvl(data, note_to_update, lvl_target=1, days_added=1)
