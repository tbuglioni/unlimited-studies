import datetime

from django.test import RequestFactory, TestCase
from studies.logic.analyse import Analyse
from studies.models import GlobalDailyAnalysis, GlobalMonthlyAnalysis
from studies.tests.speed_set_up import SpeedSetUP


class AnalyseTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        speed_set_up = SpeedSetUP()

        self.user_a = speed_set_up.set_up_user_a()
        self.user_b = speed_set_up.set_up_user_b()

        self.book_1 = speed_set_up.create_book_owner(self.user_a, order_book=1)
        self.book_2 = speed_set_up.create_book_owner(self.user_a, order_book=2)

        self.chapter_1 = speed_set_up.create_chapter(
            self.book_1, order_chapter=1)
        self.chapter_2 = speed_set_up.create_chapter(
            self.book_2, order_chapter=1)

        self.note_1 = speed_set_up.create_note(
            chapter=self.chapter_1, order_note=1, recto=True, verso=True
        )
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_1, lvl_recto=5, lvl_verso=5
        )
        speed_set_up.add_user_to_notes(
            user=self.user_b, note=self.note_1, lvl_recto=5, lvl_verso=5
        )

        self.note_2 = speed_set_up.create_note(
            chapter=self.chapter_2, order_note=1, recto=True, verso=True
        )
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_2, lvl_recto=2, lvl_verso=2
        )

        self.student_1 = speed_set_up.add_student_to_book(
            self.user_b, self.book_1, to_accept=False, order_book=1
        )
        self.student_2 = speed_set_up.add_student_to_book(
            self.user_b, self.book_2, to_accept=True, order_book=2
        )

    def test_get_nbr_of_notes(self):
        request = self.factory.get("hello/world")
        request.user = self.user_a

        self.analyse = Analyse(request)
        elements = self.analyse.get_nbr_of_notes()

        self.assertEqual(elements, 2)

    def test_get_recap_daily_notes(self):
        request = self.factory.get("hello/world")
        request.user = self.user_a

        self.analyse = Analyse(request)

        elements = self.analyse.get_recap_daily_notes()

        self.assertEqual(elements, (datetime.date.today(), 0, 0))

    def test_get_global_lvl_avg(self):
        request = self.factory.get("hello/world")
        request.user = self.user_a

        self.analyse = Analyse(request)

        elements = self.analyse.get_global_lvl_avg()

        self.assertEqual(elements, 3.5)

    def test_get_list_lvl_avg_each_book(self):
        request = self.factory.get("hello/world")
        request.user = self.user_a

        self.analyse = Analyse(request)

        elements = self.analyse.get_list_lvl_avg_each_book()

        self.assertEqual(elements, [5.0, 2.0])

    def test_get_list_lvl_avg_each_chapter_one_book(self):
        request = self.factory.get("hello/world")
        request.user = self.user_a

        self.analyse = Analyse(request)

        elements = self.analyse.get_list_lvl_avg_each_chapter_one_book(
            self.book_1.id)

        self.assertEqual(elements, [5.0])

    def test_get_nbr_notes_todoo(self):
        request = self.factory.get("hello/world")
        request.user = self.user_a

        self.analyse = Analyse(request)

        elements = self.analyse.get_nbr_notes_todoo()

        self.assertEqual(elements, 4)

    def test_get_notes_studied_today(self):
        request = self.factory.get("hello/world")
        request.user = self.user_a

        self.analyse = Analyse(request)

        elements = self.analyse.get_notes_studied_today()

        self.assertEqual(elements, 0)

    def test_get_notes_studied_this_month(self):
        request = self.factory.get("hello/world")
        request.user = self.user_a

        self.analyse = Analyse(request)

        elements = self.analyse.get_notes_studied_this_month()

        self.assertEqual(elements, 0)

    def test_update_analysis(self):
        request = self.factory.get("hello/world")
        request.user = self.user_a

        self.analyse = Analyse(request)

        self.analyse.update_analysis(2, 2)

        day = GlobalDailyAnalysis.objects.filter(user=self.user_a)[
            0].number_of_win
        month = GlobalMonthlyAnalysis.objects.filter(user=self.user_a)[
            0].number_of_win

        self.assertEqual(day, 2)
        self.assertEqual(month, 2)

    def test_students_avg(self):
        request = self.factory.get("hello/world")
        request.user = self.user_a

        self.analyse = Analyse(request)

        students = self.analyse.students_avg(self.book_1.id)
        self.assertEqual(
            students,
            [
                {
                    "lvl_avg": 5.0,
                    "user_id": self.user_b.id,
                    "username": self.user_b.username,
                }
            ],
        )

    def test_book_to_add_as_student(self):
        request = self.factory.get("hello/world")
        request.user = self.user_b

        self.analyse = Analyse(request)

        books_list = self.analyse.book_to_add_as_student(request)
        self.assertEqual(
            books_list,
            [
                {
                    "book_name": self.book_2.name,
                    "book_id": self.book_2.id,
                    "book_description": self.book_2.description,
                    "owner": self.user_a.username,
                    "counter": 1,
                }
            ],
        )
