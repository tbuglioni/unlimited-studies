from django.test import RequestFactory, TestCase
from studies.logic.game import Game
from studies.models import StudiesNotesProgression
from studies.tests.speed_set_up import SpeedSetUP


class GameTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        speed_set_up = SpeedSetUP()
        self.game = Game()

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
            user=self.user_a, note=self.note_2, lvl_recto=5, lvl_verso=5
        )

        self.note_3 = speed_set_up.create_note(
            chapter=self.chapter_1, order_note=1, recto=False, verso=True
        )
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_3, lvl_recto=1, lvl_verso=1
        )

    def test_get_notes_todo(self):
        request = self.factory.get("hello/world")
        request.user = self.user_a

        elements = self.game.get_notes_todo(request)

        self.assertEqual(len(elements), 5)

    def test_change_lvl_level_recto_true(self):
        request = self.factory.get("hello/world")
        request.user = self.user_a

        note_progression = StudiesNotesProgression.objects.filter(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True
        )[0]
        self.game.change_lvl(request, note_progression.id, True)

        note_progression = StudiesNotesProgression.objects.filter(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=True
        )[0]
        self.assertEqual(note_progression.level, 2)

    def test_change_lvl_level_verso_true(self):
        request = self.factory.get("hello/world")
        request.user = self.user_a

        note_progression = StudiesNotesProgression.objects.filter(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=False
        )[0]
        self.game.change_lvl(request, note_progression.id, True)

        note_progression = StudiesNotesProgression.objects.filter(
            user_id=self.user_a.id, notes_id=self.note_1.id, is_recto=False
        )[0]
        self.assertEqual(note_progression.level, 2)

    def test_change_lvl_level_recto_false(self):
        request = self.factory.get("hello/world")
        request.user = self.user_a

        note_progression = StudiesNotesProgression.objects.filter(
            user_id=self.user_a.id, notes_id=self.note_2.id, is_recto=True
        )[0]
        self.game.change_lvl(request, note_progression.id, False)

        note_progression = StudiesNotesProgression.objects.filter(
            user_id=self.user_a.id, notes_id=self.note_2.id, is_recto=True
        )[0]
        self.assertEqual(note_progression.level, 1)

    def test_change_lvl_level_verso_false(self):
        request = self.factory.get("hello/world")
        request.user = self.user_a

        note_progression = StudiesNotesProgression.objects.filter(
            user_id=self.user_a.id, notes_id=self.note_2.id, is_recto=False
        )[0]
        self.game.change_lvl(request, note_progression.id, False)

        note_progression = StudiesNotesProgression.objects.filter(
            user_id=self.user_a.id, notes_id=self.note_2.id, is_recto=False
        )[0]
        self.assertEqual(note_progression.level, 1)
