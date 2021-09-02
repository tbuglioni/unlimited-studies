from studies.models import *
from django.db.models import Avg
from django.db.models import Count, F, Value
import datetime
from django.utils import timezone


class Analyse:
    def __init__(self, request):
        self.time_now = datetime.date.today()
        self.request = request

    def update_data(self):
        """ get repetitive query """
        # data
        self.notes = StudiesNotesProgression.objects.filter(
            user=self.request.user).select_related('notes')

        self.note_recto_true = self.notes.filter(
            notes__studie_recto=True)
        self.note_verso_true = self.notes.filter(
            notes__studie_verso=True)

    def get_nbr_of_notes(self):
        """ return the numbers of notes"""
        return StudiesNotes.objects.filter(users=self.request.user).distinct().count()

    def get_recap_daily_notes(self):
        """ return a list with 10 lasts days and the number of win/fail"""

        # precharge with head of list for pie graph
        recap_dict = {"list_date": ["Date"],
                      "list_win": ["Win"], "list_fail": ["Fail"]}
        data = GlobalDailyAnalysis.objects.filter(user=self.request.user)[:10]
        if data:
            for elt in data:
                recap_dict["list_date"].append(
                    f"{elt.date.strftime('%d/%m/%y')}")
                recap_dict["list_win"].append(elt.number_of_win)
                recap_dict["list_fail"].append(elt.number_of_lose)

            return recap_dict

        else:
            self.time_now = datetime.date.today()
            return self.time_now, 0, 0

    def get_global_lvl_avg(self):
        """ return the lvl average of all the notes"""

        try:
            lvl_avg = round(StudiesNotesProgression.objects.filter(
                user=self.request.user).aggregate(Avg('level'))["level__avg"], 2)
        except TypeError:
            lvl_avg = 0
        return lvl_avg

    def get_list_lvl_avg_each_book(self):
        """ return a list of each book(level average)"""
        list_avg = []
        books = Book.objects.filter(users=self.request.user).order_by(
            'userbookmany__order_book')
        for book in books:
            try:
                lvl_avg = StudiesNotesProgression.objects.filter(
                    user=self.request.user, notes__chapter__book_id=book.id).aggregate(Avg('level'))["level__avg"]

                lvl_avg = round(lvl_avg, 2)
            except TypeError:
                lvl_avg = 0
            list_avg.append(lvl_avg)

        return list_avg

    def get_list_lvl_avg_each_chapter_one_book(self, book_id):
        """ return a list of each chapter(level average) in one book"""
        list_avg = []
        chapters = Chapter.objects.filter(
            book__users=self.request.user, book_id=book_id)
        for chapter in chapters:
            try:
                lvl_avg = StudiesNotesProgression.objects.filter(
                    user=self.request.user, notes__chapter=chapter.id).aggregate(Avg('level'))["level__avg"]
                lvl_avg = round(lvl_avg, 2)

            except TypeError:
                lvl_avg = 0
            list_avg.append(lvl_avg)

        return list_avg

    def get_nbr_notes_todoo(self):
        """ return number of notes to studies"""
        todoo = StudiesNotesProgression.objects.filter(
            user=self.request.user, next_studied_date__lte=self.time_now).count()
        return todoo

    def get_notes_studied_today(self):
        """ count all notes studied today"""
        obj, created = GlobalDailyAnalysis.objects.get_or_create(
            user=self.request.user, date=self.time_now)
        return obj.number_of_studies

    def __update_notes_studied_today(self, note_true, note_false):
        """ update the number of notes studied today"""
        self.time_now = datetime.date.today()
        obj, created = GlobalDailyAnalysis.objects.get_or_create(
            user=self.request.user, date=self.time_now)

        obj.number_of_studies = F('number_of_studies') + \
            (note_true + note_false)
        obj.number_of_win = F('number_of_win') + note_true
        obj.number_of_lose = F('number_of_lose') + note_false
        obj.save()

    def get_notes_studied_this_month(self):
        """ count all notes studied this month"""

        date_now = self.time_now
        obj, created = GlobalMonthlyAnalysis.objects.get_or_create(
            user=self.request.user, date__month=date_now.month)
        return obj.number_of_studies

    def __update_notes_studied_this_month(self, note_true, note_false):
        """ update the number of notes studied this month"""
        date_now = self.time_now
        obj, created = GlobalMonthlyAnalysis.objects.get_or_create(
            user=self.request.user, date__month=date_now.month)

        obj.number_of_studies = F('number_of_studies') + \
            (note_true + note_false)
        obj.number_of_win = F('number_of_win') + note_true
        obj.number_of_lose = F('number_of_lose') + note_false
        obj.save()

    def update_analysis(self, note_true, note_false):
        """ update the number of notes studied this day and month)"""
        self.__update_notes_studied_today(note_true, note_false)
        self.__update_notes_studied_this_month(note_true, note_false)
