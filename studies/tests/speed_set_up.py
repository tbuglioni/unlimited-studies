from django.contrib.auth import get_user_model
from studies.models import (Book, Chapter, StudiesNotes,
                            StudiesNotesProgression, UserBookMany)

User = get_user_model()


class SpeedSetUP:
    """new class"""

    @staticmethod
    def set_up_user_a():
        """ create user a """
        user_a = User(username="john", email="john@invalid.com")
        user_a_pw = "some_123_password"
        user_a.is_staff = True
        user_a.is_teacher = True
        user_a.is_superuser = False
        user_a.set_password(user_a_pw)
        user_a.save()
        return user_a

    @staticmethod
    def set_up_user_b():
        """ create user b """
        user_b = User(username="lee", email="lee@invalid.com")
        user_b_pw = "some_123_password"
        user_b.is_staff = False
        user_b.is_teacher = False
        user_b.is_superuser = False
        user_b.set_password(user_b_pw)
        user_b.save()
        return user_b

    @staticmethod
    def create_book_owner(user, order_book: int):
        """ create book with 1 owner """
        new_book = Book.objects.create(
            name="English",
            description="book to learn english",
            source_info="Author 1",
        )
        new_book.users.add(user, through_defaults={"order_book": order_book})
        return new_book

    @staticmethod
    def add_student_to_book(
        student, book, to_accept: bool = True, order_book: int = 1
    ):
        """ Add a student to the book. """
        new_student = UserBookMany.objects.create(
            user=student,
            user_fonction="student",
            book=book,
            to_accept=to_accept,
            order_book=order_book,
        )
        return new_student

    @staticmethod
    def create_chapter(book, order_chapter: int):
        """ Create a chapter"""
        new_chapter = Chapter.objects.create(
            name="vocabulary 1", order_chapter=order_chapter, book=book
        )
        return new_chapter

    @staticmethod
    def create_note(chapter, order_note: int, recto: bool, verso: bool):
        """ create new note """
        new_note = StudiesNotes.objects.create(
            text_recto="good morning",
            text_verso="bonjour",
            chapter=chapter,
            order_note=order_note,
            studie_recto=recto,
            studie_verso=verso,
        )
        return new_note

    def add_user_to_notes(self, user, note, lvl_recto: int = 1,
                          lvl_verso: int = 1):
        """ add user to notes and add conditional progressions recto/verso"""
        if note.studie_recto:
            StudiesNotesProgression.objects.create(
                user=user, notes=note, level=lvl_recto, is_recto=True
            )

        if note.studie_verso:
            self.note1_progression_verso = (
                StudiesNotesProgression.objects.create(
                    user=user, notes=note, level=lvl_verso, is_recto=False
                ))
