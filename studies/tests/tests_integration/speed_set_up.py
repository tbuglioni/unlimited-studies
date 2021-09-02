
from django.contrib.auth import get_user_model
from studies.models import *
User = get_user_model()

class SpeedSetUP:
    """ new class """

    def set_up_user_a(self):
        user_a = User(username="john", email="john@invalid.com")
        user_a_pw = "some_123_password"
        user_a.is_staff = True
        user_a.is_teacher = True
        user_a.is_superuser = False
        user_a.set_password(user_a_pw)
        user_a.save()
        return user_a

    def set_up_user_b(self):
        user_b = User(username="lee", email="lee@invalid.com")
        user_b_pw = "some_123_password"
        user_b.is_staff = False
        user_b.is_teacher = False
        user_b.is_superuser = False
        user_b.set_password(user_b_pw)
        user_b.save()
        return user_b

    def create_book_owner(self, user, order_book: int):
        new_book = Book.objects.create(
            name="English", description="book to learn english", source_info="Author 1",)
        new_book.users.add(user, through_defaults={"order_book": order_book})
        return new_book

    def add_student_to_book(self, student, book, to_accept: bool = True, order_book: int = 1):
        new_student = UserBookMany.objects.create(
            user=student, user_fonction="student", book=book, to_accept=to_accept, order_book=order_book)
        return new_student

    def create_chapter(self, book, order_chapter: int):
        new_chapter = Chapter.objects.create(
            name="vocabulary 1", order_chapter=order_chapter, book=book)
        return new_chapter

    def create_note(self, chapter, order_note: int, recto: bool, verso: bool):
        new_note = StudiesNotes.objects.create(
            text_recto="good morning",
            text_verso="bonjour",
            chapter=chapter,
            order_note=order_note,
            studie_recto=recto,
            studie_verso=verso)
        return new_note

    def add_user_to_notes(self, user, note, lvl_recto: int = 1, lvl_verso: int = 1):
        if note.studie_recto == True:
            StudiesNotesProgression.objects.create(
                user=user, notes=note, level=lvl_recto, is_recto=True)

        if note.studie_verso == True:
            self.note1_progression_verso = StudiesNotesProgression.objects.create(
                user=user, notes=note, level=lvl_verso, is_recto=False)
