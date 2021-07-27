from studies.models import *
import csv


class FeedDb:
    def __init__(self, request):
        self.request = request
        self.book = None
        self.chapter = None
        self.book_order_loop = 1
        self.chapter_order_loop = 1
        self.note_order_loop = 1

    def add_book(self, name):
        """ add new book """
        self.book, created = Book.objects.get_or_create(
            name=name,
            order_book=self.book_order_loop,
            description="hello world", source_info='wikipedia is bad :)')

        self.book.users.add(self.request.user, through_defaults={})
        self.book_order_loop += 1

    def add_chapter_in_book(self, name):
        self.chapter, created = Chapter.objects.get_or_create(
            name=name,
            order_chapter=self.chapter_order_loop,
            book=self.book,
        )
        self.chapter_order_loop += 1

    def add_note_in_chapter(self, text_recto, text_verso, studie_verso, lvl_recto, lvl_verso):
        word_it_1, created = StudiesNotes.objects.get_or_create(
            text_recto=text_recto,
            text_verso=text_verso,
            chapter=self.chapter,
            order_note=self.note_order_loop,
            studie_verso=studie_verso,

        )
        self.note_order_loop += 1

        word_it_1.users.add(self.request.user, through_defaults={
            'lvl_recto': str(lvl_recto), "lvl_verso": str(lvl_verso)})

    def add_note_from_csv(self):
        with open("studies/logic/data.csv") as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                self.add_note_in_chapter(
                    row[0], row[1], row[2], row[3], row[4])
