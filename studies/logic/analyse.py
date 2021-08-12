from studies.models import *
from django.db.models import Avg
import datetime


class Analyse:
    def __init__(self, request):
        self.request = request
        self.TIME_NOW = datetime.date.today()
        self.notes = StudiesNotesProgression.objects.filter(
            user=request.user)
        self.note_recto_true = self.notes.filter(
            notes__studie_recto=True)
        self.note_verso_true = self.notes.filter(
            notes__studie_verso=True)

    def get_nbr_of_notes(self):
        return self.notes.count()

    def get_lvl_avg(self):
        try:
            lvl_avg = round(
                self.note_recto_true.aggregate(Avg('lvl_recto'))[
                    "lvl_recto__avg"]
                + self.note_verso_true.aggregate(Avg('lvl_verso'))["lvl_verso__avg"], 2)
        except TypeError:
            lvl_avg = 0
        return lvl_avg

    def get_list_lvl_avg_each_book(self):
        list_avg = []
        books = Book.objects.filter(users=self.request.user)
        for book in books:
            try:
                lvl_avg = round(
                    self.note_recto_true.filter(notes__chapter__book__id=book.id).aggregate(
                        Avg('lvl_recto'))["lvl_recto__avg"]

                    + self.note_verso_true.filter(notes__chapter__book__id=book.id).aggregate(Avg('lvl_verso'))["lvl_verso__avg"], 2)
            except TypeError:
                lvl_avg = 0
            list_avg.append(lvl_avg)

        return list_avg

    def get_nbr_notes_todoo(self):
        todoo_recto = self.note_recto_true.filter(
            next_studied_date_recto__lte=self.TIME_NOW)
        todoo_verso = self.note_verso_true.filter(
            next_studied_date_verso__lte=self.TIME_NOW)
        return todoo_recto.count() + todoo_verso.count()

    def get_notes_studied_today(self):
        obj, created = GlobalDailyAnalysis.objects.get_or_create(
            user=self.request.user, date=self.TIME_NOW)
        return obj.number_of_studies

    def get_notes_studied_this_month(self):
        obj, created = GlobalMonthlyAnalysis.objects.get_or_create(
            user=self.request.user, date=self.TIME_NOW)
        return obj.number_of_studies
