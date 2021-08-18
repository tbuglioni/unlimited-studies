from studies.models import *
from django.db.models import Avg
from django.db.models import Count, F, Value
import datetime


class Analyse:
    def __init__(self):
        self.time_now = None

    def get_request(self, request):
        self.request = request

    def update_data(self):
        # data
        self.time_now = datetime.date.today()
        self.notes = StudiesNotesProgression.objects.filter(
            user=self.request.user).select_related('notes')

        # db_cache
        self.note_recto_true = self.notes.filter(
            notes__studie_recto=True)
        self.note_verso_true = self.notes.filter(
            notes__studie_verso=True)

    def get_nbr_of_notes(self):
        return self.notes.count()

    def get_recap_daily_notes(self):
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
        try:
            lvl_avg = round(
                (self.note_recto_true.aggregate(
                    Avg('lvl_recto'))["lvl_recto__avg"]
                    +
                 self.note_verso_true.aggregate(Avg('lvl_verso'))["lvl_verso__avg"])/2, 2)
        except TypeError:
            lvl_avg = 0
        return lvl_avg

    def get_list_lvl_avg_each_book(self):
        list_avg = []
        books = Book.objects.filter(users=self.request.user)
        for book in books:
            try:
                lvl_avg = (self.note_recto_true.filter(notes__chapter__book__id=book.id).aggregate(
                    Avg('lvl_recto'))["lvl_recto__avg"]
                    +
                    self.note_verso_true.filter(notes__chapter__book_id=book.id).aggregate(Avg('lvl_verso'))["lvl_verso__avg"])/2

                lvl_avg = round(lvl_avg, 2)
            except TypeError:
                lvl_avg = 0
            list_avg.append(lvl_avg)

        return list_avg

    def get_list_lvl_avg_each_chapter_one_book(self, book_id):
        list_avg = []
        chapters = Chapter.objects.filter(
            book__users=self.request.user, book_id=book_id).select_related('book')
        for chapter in chapters:
            try:
                lvl_avg = (self.note_recto_true.filter(notes__chapter__id=chapter.id).aggregate(
                    Avg('lvl_recto'))["lvl_recto__avg"]
                    +
                    self.note_verso_true.filter(notes__chapter__id=chapter.id).aggregate(Avg('lvl_verso'))["lvl_verso__avg"])/2
                lvl_avg = round(lvl_avg, 2)
            except TypeError:
                lvl_avg = 0
            list_avg.append(lvl_avg)

        return list_avg

    def get_nbr_notes_todoo(self):
        todoo_recto = self.note_recto_true.filter(
            next_studied_date_recto__lte=self.time_now)
        todoo_verso = self.note_verso_true.filter(
            next_studied_date_verso__lte=self.time_now)
        return todoo_recto.count() + todoo_verso.count()

    def get_notes_studied_today(self):
        obj, created = GlobalDailyAnalysis.objects.get_or_create(
            user=self.request.user, date=self.time_now)
        return obj.number_of_studies

    def __update_notes_studied_today(self, note_true, note_false):
        self.time_now = datetime.date.today()
        obj, created = GlobalDailyAnalysis.objects.get_or_create(
            user=self.request.user, date=self.time_now)

        obj.number_of_studies = F('number_of_studies') + \
            (note_true + note_false)
        obj.number_of_win = F('number_of_win') + note_true
        obj.number_of_lose = F('number_of_lose') + note_false
        obj.save()

    def get_notes_studied_this_month(self):
        date_now = self.time_now
        obj, created = GlobalMonthlyAnalysis.objects.get_or_create(
            user=self.request.user, date__month=date_now.month)
        return obj.number_of_studies

    def __update_notes_studied_this_month(self, note_true, note_false):
        date_now = self.time_now
        obj, created = GlobalMonthlyAnalysis.objects.get_or_create(
            user=self.request.user, date__month=date_now.month)

        obj.number_of_studies = F('number_of_studies') + \
            (note_true + note_false)
        obj.number_of_win = F('number_of_win') + note_true
        obj.number_of_lose = F('number_of_lose') + note_false
        obj.save()

    def update_analysis(self, note_true, note_false):
        self.__update_notes_studied_today(note_true, note_false)
        self.__update_notes_studied_this_month(note_true, note_false)
