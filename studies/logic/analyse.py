import datetime
from datetime import timedelta
from account.models import Account
from django.db.models import Avg, F
from studies.models import (Book, Chapter, GlobalDailyAnalysis,
                            GlobalMonthlyAnalysis, StudiesNotes,
                            StudiesNotesProgression, UserBookMany)


class Analyse:
    """ get study analysis """

    def __init__(self, request):
        self.time_now = datetime.date.today()
        self.request = request

    def get_nbr_of_notes(self):
        """return the numbers of notes"""
        return (
            StudiesNotes.objects.filter(
                users=self.request.user).distinct().count())

    def get_recap_daily_notes(self):
        """return a list with 10 lasts days and the number of win/fail"""
        self.__delete_old_data()

        # precharge with head of list for pie graph
        recap_dict = {"list_date": ["Date"],
                      "list_win": ["Win"], "list_fail": ["Fail"]}
        data = GlobalDailyAnalysis.objects.filter(user=self.request.user)[:11]
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

    def __delete_old_data(self):
        """ delete daily > 10j and month > 12"""
        GlobalDailyAnalysis.objects.filter(
            user=self.request.user, date__lte=self.time_now - timedelta(days=10)).delete()
        GlobalMonthlyAnalysis.objects.filter(
            user=self.request.user, date__lte=self.time_now - timedelta(days=364)).delete()

    def get_global_lvl_avg(self):
        """return the lvl average of all the notes"""

        try:
            lvl_avg = round(
                StudiesNotesProgression.objects.filter(
                    user=self.request.user
                ).aggregate(Avg("level"))["level__avg"],
                2,
            )
        except TypeError:
            lvl_avg = 0
        return lvl_avg

    def get_list_lvl_avg_each_book(self):
        """return a list of each book(level average)"""
        list_avg = []
        books = Book.objects.filter(
            users=self.request.user, userbookmany__to_accept=False).order_by(
            "userbookmany__order_book"
        )

        notes_progression = StudiesNotesProgression.objects.filter(
            user=self.request.user, notes__chapter__book__in=books
        ).values("notes__chapter__book_id", "level")

        for book in books:
            try:
                data_list = (
                    [nbr["level"] for nbr in notes_progression
                     if nbr["notes__chapter__book_id"] == book.id])

                data_sum, date_len = sum(data_list), len(data_list)
                if data_sum and date_len:
                    lvl_avg = data_sum / date_len
                    lvl_avg = round(lvl_avg, 2)
                else:
                    lvl_avg = 0
            except TypeError:
                lvl_avg = 0

            list_avg.append({"name": book.name, "level": lvl_avg})

        return list_avg

    def get_list_lvl_avg_each_chapter_one_book(self, book_id: int):
        """return a list of each chapter(level average) in one book"""
        list_avg = []
        chapters = Chapter.objects.filter(
            book__users=self.request.user,
            book__userbookmany__to_accept=False,
            book_id=book_id
        )
        for chapter in chapters:
            try:
                lvl_avg = StudiesNotesProgression.objects.filter(
                    user=self.request.user, notes__chapter=chapter.id
                ).aggregate(Avg("level"))["level__avg"]
                lvl_avg = round(lvl_avg, 2)

            except TypeError:
                lvl_avg = 0
            list_avg.append({"name": chapter.name, "level": lvl_avg})

        return list_avg

    def get_nbr_notes_todoo(self):
        """return number of notes to studies"""
        todoo = StudiesNotesProgression.objects.filter(
            user=self.request.user, next_studied_date__lte=self.time_now
        ).count()
        return todoo

    def get_notes_studied_today(self):
        """count all notes studied today"""
        obj, _ = GlobalDailyAnalysis.objects.get_or_create(
            user=self.request.user, date=self.time_now
        )
        return obj.number_of_studies

    def __update_notes_studied_today(self, note_true: int, note_false: int):
        """update the number of notes studied today"""
        self.time_now = datetime.date.today()
        obj, _ = GlobalDailyAnalysis.objects.get_or_create(
            user=self.request.user, date=self.time_now
        )

        obj.number_of_studies = (
            F("number_of_studies") + (note_true + note_false))
        obj.number_of_win = F("number_of_win") + note_true
        obj.number_of_lose = F("number_of_lose") + note_false
        obj.save()

    def get_notes_studied_this_month(self):
        """count all notes studied this month"""

        date_now = self.time_now
        obj, created = GlobalMonthlyAnalysis.objects.get_or_create(
            user=self.request.user, date__month=date_now.month
        )
        return obj.number_of_studies

    def __update_notes_studied_this_month(self,
                                          note_true: int,
                                          note_false: int):
        """update the number of notes studied this month"""
        date_now = self.time_now
        obj, created = GlobalMonthlyAnalysis.objects.get_or_create(
            user=self.request.user, date__month=date_now.month
        )

        obj.number_of_studies = F("number_of_studies") + \
            (note_true + note_false)
        obj.number_of_win = F("number_of_win") + note_true
        obj.number_of_lose = F("number_of_lose") + note_false
        obj.save()

    def update_analysis(self, note_true: int, note_false: int):
        """update the number of notes studied this day and month)"""
        self.__update_notes_studied_today(note_true, note_false)
        self.__update_notes_studied_this_month(note_true, note_false)

    @staticmethod
    def students_avg(book: int):
        """return list with each students in 1 book"""
        list_user = UserBookMany.objects.filter(
            user_fonction="student", to_accept=False, book=book
        ).select_related("user")

        exit_list = []

        for elt in list_user:
            username = elt.user.username
            user_id = elt.user_id
            try:
                lvl_avg = (
                    StudiesNotesProgression.objects
                    .filter(
                        user=elt.user, notes__chapter__book_id=book)
                    .aggregate(Avg("level"))[
                        "level__avg"
                    ])
                lvl_avg = round(lvl_avg, 2)

            except TypeError:
                lvl_avg = 0
            exit_list.append(
                {"username": username, "lvl_avg": lvl_avg, "user_id": user_id}
            )
        return exit_list

    @staticmethod
    def book_to_add_as_student(request):
        """return the book to add as student"""
        data_list = (
            UserBookMany.objects.filter(user=request.user, to_accept=True)
            .select_related("book")
            .select_related("user")
        )
        exit_list = []

        for elt in data_list:
            book_name = elt.book.name
            book_id = elt.book_id
            book_description = elt.book.description
            owner = (
                Account.objects.filter(
                    userbookmany__user_fonction="owner",
                    userbookmany__book_id=book_id
                )
                .first()
                .username
            )
            counter = StudiesNotes.objects.filter(
                chapter__book_id=book_id).count()
            if counter is None:
                counter = 0

            exit_list.append(
                {
                    "book_name": book_name,
                    "book_id": book_id,
                    "book_description": book_description,
                    "owner": owner,
                    "counter": counter,
                }
            )
        return exit_list
