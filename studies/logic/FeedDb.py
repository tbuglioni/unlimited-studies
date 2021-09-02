# from studies.models import *
# import csv
# from account.models import Account

# class FeedDb:
#     def __init__(self, request):
#         self.request = request
#         self.book = None
#         self.chapter = None
#         self.book_order_loop = 1
#         self.chapter_order_loop = 1
#         self.note_order_loop = 1

#     def add_book(self, name):
#         """ add new book """
#         self.book, created = Book.objects.get_or_create(
#             name=name,
#             description="hello world", source_info='wikipedia is bad :)')

#         self.book.users.add(self.request.user, through_defaults={"order_book":self.book_order_loop})
#         self.book_order_loop += 1

#     def add_chapter_in_book(self, name):
#         self.chapter, created = Chapter.objects.get_or_create(
#             name=name,
#             order_chapter=self.chapter_order_loop,
#             book=self.book,
#         )
#         self.chapter_order_loop += 1

#     def add_note_in_chapter(self, text_recto, text_verso, studie_verso, lvl_recto, lvl_verso):
#         word_it_1= StudiesNotes.objects.create(
#             text_recto=text_recto,
#             text_verso=text_verso,
#             chapter=self.chapter,
#             order_note=self.note_order_loop,
#             studie_verso=studie_verso,

#         )
#         self.note_order_loop += 1
#         list_users = Account.objects.filter(books__chapter=self.chapter)
#         print(list_users)
#         objs = []
#         for elt in list_users:
#                     if word_it_1.studie_recto == True :
#                         objs.append(StudiesNotesProgression(
#                         user_id=elt.id,
#                         notes_id=word_it_1.id,
#                         is_recto=True,
#                         level=lvl_recto
#                         ))

#                     if word_it_1.studie_verso == True:
#                         objs.append(StudiesNotesProgression(
#                         user_id=elt.id,
#                         notes_id=word_it_1.id,
#                         is_recto=False,
#                         level=lvl_verso
#                         ))

#         StudiesNotesProgression.objects.bulk_create(objs)

#     def add_note_from_csv(self):
#         with open("studies/logic/data.csv") as csvfile:
#             reader = csv.reader(csvfile, delimiter=';')
#             for row in reader:
#                 self.add_note_in_chapter(
#                     row[0], row[1], row[2], row[3], row[4])
