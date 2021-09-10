from account.models import Account
from django.shortcuts import get_object_or_404, redirect
from studies.forms import BookForm, ChapterForm, StudiesNotesForm
from studies.models import (Book, Chapter, StudiesNotes,
                            StudiesNotesProgression, UserBookMany)


class UserAction:
    """ create/read/update/delete books/chapter/notes """

    def get_books(self, request):
        """get all books from 1 user"""
        books = Book.objects.filter(
            users=request.user, userbookmany__to_accept=False
        ).order_by("userbookmany__order_book")
        return books

    def get_UserBookMany(self, request):
        """get all books from 1 user"""
        data = UserBookMany.objects.filter(user=request.user, to_accept=False)
        return data

    def get_book_404(self, request, book: int):
        """get 1 book from 1 user"""
        book = get_object_or_404(Book, pk=book, users=request.user)
        return book

    def create_or_update_book(self, request, context: dict):
        """create a new book or update an existing one"""
        form_book = BookForm(request.POST)

        if form_book.is_valid():
            if context["selectedBook"] is not None:
                self.__update_existing_book(form_book, request)
            else:
                self.__create_new_book(form_book, request)
        else:
            print("error")
        return redirect("home")

    def __create_new_book(self, form_book, request):
        """ create new book and update counter"""
        name, description, source_info = self.__extract_data_book_post(
            form_book)

        new_book = Book.objects.create(
            name=name, description=description, source_info=source_info
        )

        self.__update_new_book_order(request, new_book)

    def __update_new_book_order(self, request, new_book):
        """ update new book counter """
        book_counter = (
            UserBookMany.objects.filter(
                user=request.user, to_accept=False
            ).count()
            + 1
        )
        new_book.users.add(
            request.user, through_defaults={"order_book": book_counter}
        )
        new_book.save()

    def __extract_data_book_post(self, form_book):
        """ get data, via POST, and create/return variables """
        name = form_book.cleaned_data["name"]
        description = form_book.cleaned_data["description"]
        source_info = form_book.cleaned_data["source_info"]
        return name, description, source_info

    def __update_existing_book(self, form_book, request):
        """ udpate existing book and update all books order"""
        name, description, source_info = self.__extract_data_book_post(
            form_book)
        order_book = form_book.cleaned_data["order_book"]
        book_id = form_book.cleaned_data["book_id"]

        self.__update_book_if_data(
            name, book_id, request, description, source_info)

        self.__update_existing_books_order(request, book_id, order_book)

    def __update_existing_books_order(self, request, book_id, order_book):
        """ update order for each books to 1 user """
        books_before = (
            UserBookMany.objects.filter(
                user=request.user, to_accept=False)
            .order_by("order_book")
            .exclude(book=book_id,
                     user=request.user)[: (order_book - 1)]
        )
        books_after = (
            UserBookMany.objects.filter(
                user=request.user, to_accept=False)
            .order_by("order_book")
            .exclude(book=book_id,
                     user=request.user)[(order_book - 1):]
        )
        loop = 1

        for elt in books_before:
            elt.order_book = loop
            loop += 1
            elt.save()

        UserBookMany.objects.filter(book=book_id,
                                    user=request.user).update(
            order_book=loop
        )
        loop += 1

        for elt in books_after:
            elt.order_book = loop
            loop += 1
            elt.save()

    def __update_book_if_data(self, name, book_id,
                              request, description, source_info):
        """ update book if data is not empty """
        if name:
            Book.objects.filter(id=book_id, users=request.user).update(
                name=name,
                description=description,
                source_info=source_info
            )

    def get_chapters(self, request, book: int):
        """get all chapters from 1 user in 1 book"""
        chapters = Chapter.objects.filter(book__users=request.user, book=book)
        return chapters

    def get_chapter_404(self, request, chapter: int):
        """get 1 chapter from 1 user in 1 book"""
        chapter = get_object_or_404(
            Chapter, pk=chapter, book__users=request.user)
        return chapter

    def create_or_update_chapter(self, request, context: dict, book: int):
        """create a new chapter or update an existing one"""
        form_chapter = ChapterForm(request.POST)
        context["form_chapter"] = form_chapter

        if form_chapter.is_valid():
            if context["chapter"] is not None:
                self.__update_existing_chapter(form_chapter, request, book)
            else:
                self.__create_new_chapter(form_chapter, book, request, context)

    def __create_new_chapter(self, form_chapter, book, request, context):
        """ create new chapter and add order"""
        name = form_chapter.cleaned_data["name"]
        chapter_counter = (
            Chapter.objects.filter(
                book=book, book__users=request.user).count()
            + 1
        )
        Chapter.objects.create(
            name=name,
            order_chapter=chapter_counter,
            book=context["book"]
        )

    def __update_existing_chapter(self, form_chapter, request, book):
        """ update chapter and order """
        name = form_chapter.cleaned_data["name"]
        order_chapter = form_chapter.cleaned_data["order_chapter"]
        chapter_id = form_chapter.cleaned_data["chapter_id"]

        Chapter.objects.filter(id=chapter_id,
                               book__users=request.user).update(
            name=name, order_chapter=order_chapter
        )
        self.__update_existing_chapters_order(
            book, request, chapter_id, order_chapter)

    def __update_existing_chapters_order(self, book,
                                         request, chapter_id, order_chapter):
        """ update existing chapters order """
        chapters_before = (
            Chapter.objects.filter(book=book, book__users=request.user)
            .order_by("order_chapter")
            .exclude(id=chapter_id)[: (order_chapter - 1)]
        )
        chapters_after = (
            Chapter.objects.filter(book=book, book__users=request.user)
            .order_by("order_chapter")
            .exclude(id=chapter_id)[(order_chapter - 1):]
        )
        loop = 1

        for elt in chapters_before:
            elt.order_chapter = loop
            loop += 1
            elt.save()

        Chapter.objects.filter(id=chapter_id, book=book).update(
            order_chapter=loop
        )
        loop += 1

        for elt in chapters_after:
            elt.order_chapter = loop
            loop += 1
            elt.save()

    def get_notes(self, request, chapter: int):
        """get all notes from 1 user in 1 chapter"""
        notes = StudiesNotes.objects.filter(
            chapter__book__users=request.user, chapter=chapter
        )
        return notes

    def get_note_404(self, request, note: int):
        """get 1 note from 1 user in 1 chapter"""
        note = get_object_or_404(
            StudiesNotes, pk=note, chapter__book__users=request.user
        )
        return note

    def create_or_update_note(self, request, context: dict, chapter: int):
        """create a new chapter or update an existing one"""
        form = StudiesNotesForm(request.POST)
        context["form"] = form

        if form.is_valid():
            if context["instance_note"] is not None:
                self.__update_existing_note(form, chapter, request)

            else:
                self.__create_new_note(form, request, chapter)

    def __create_new_note(self, form, request, chapter):
        """Create a new note"""
        text_recto, text_verso, studie_recto, studie_verso = (
            self.__extract_data_note_post(
                form))

        new_note = StudiesNotes(
            text_recto=text_recto,
            text_verso=text_verso,
            studie_recto=studie_recto,
            studie_verso=studie_verso,
        )

        new_note.order_note = (
            self.get_notes(request, chapter).distinct().count() + 1
        )
        new_note.chapter = self.get_chapter_404(request, chapter)
        new_note.save()

        self.create_note_progression_each_users(chapter, new_note)

    def create_note_progression_each_users(self, chapter, new_note):
        """create note progression for each owner/students of this note"""
        list_users = Account.objects.filter(books__chapter__id=chapter)
        objs = []
        for elt in list_users:
            if new_note.studie_recto:
                objs.append(
                    StudiesNotesProgression(
                        user_id=elt.id,
                        notes_id=new_note.id,
                        is_recto=True,
                    )
                )

            if new_note.studie_verso:
                objs.append(
                    StudiesNotesProgression(
                        user_id=elt.id,
                        notes_id=new_note.id,
                        is_recto=False,
                    )
                )
        StudiesNotesProgression.objects.bulk_create(objs)

    def __update_existing_note(self, form, chapter, request):
        """ update an existing note and all ratached note_progression"""
        text_recto, text_verso, studie_recto, studie_verso = (
            self.__extract_data_note_post(form))
        note_id = form.cleaned_data["note_id"]

        list_users_with_this_note = Account.objects.filter(
            books__chapter__id=chapter)

        is_note_progression_recto, is_note_progression_verso = (
            self.__check_previous_data_in_note(note_id))

        self.__update_note_selected(note_id, request, text_recto,
                                    text_verso, studie_recto, studie_verso)

        self.__if_add_note_progression_for_each_users(
            studie_recto, is_note_progression_recto,
            list_users_with_this_note, note_id, studie_verso,
            is_note_progression_verso)

        self.__if_delete_note_progression_for_each_users(
            studie_recto, is_note_progression_recto,
            note_id, studie_verso, is_note_progression_verso)

    def __if_delete_note_progression_for_each_users(
            self, studie_recto, is_note_progression_recto,
            note_id, studie_verso, is_note_progression_verso):
        """delete notes-progression if required by comparaison
        between previous and new data
        """
        if studie_recto is False and is_note_progression_recto:
            StudiesNotesProgression.objects.filter(
                notes=note_id, is_recto=True
            ).delete()

        if studie_verso is False and is_note_progression_verso:
            StudiesNotesProgression.objects.filter(
                notes=note_id, is_recto=False
            ).delete()

    def __if_add_note_progression_for_each_users(
            self, studie_recto, is_note_progression_recto,
            list_users_with_this_note, note_id, studie_verso,
            is_note_progression_verso):
        """add note progression if required by comparaison
        between previous and new data
        """
        objs = []
        if studie_recto and is_note_progression_recto is False:
            for elt in list_users_with_this_note:
                objs.append(
                    StudiesNotesProgression(
                        user_id=elt.id,
                        notes_id=note_id,
                        is_recto=True,))
        if studie_verso and is_note_progression_verso is False:
            for elt in list_users_with_this_note:
                objs.append(
                    StudiesNotesProgression(
                        user_id=elt.id,
                        notes_id=note_id,
                        is_recto=False,))
        StudiesNotesProgression.objects.bulk_create(objs)

    def __update_note_selected(
            self, note_id, request, text_recto,
            text_verso, studie_recto, studie_verso):
        """ update existing note with new data"""
        StudiesNotes.objects.filter(
            id=note_id, chapter__book__users=request.user
        ).update(
            text_recto=text_recto,
            text_verso=text_verso,
            studie_recto=studie_recto,
            studie_verso=studie_verso,
        )

    def __check_previous_data_in_note(self, note_id):
        """ check note(study_recto/study__verso) before update"""
        is_note_progression_recto = (
            StudiesNotesProgression.objects.filter(
                notes=note_id, is_recto=True
            ).exists())
        is_note_progression_verso = (
            StudiesNotesProgression.objects.filter(
                notes=note_id, is_recto=False
            ).exists())
        return is_note_progression_recto, is_note_progression_verso

    def __extract_data_note_post(self, form):
        """ get data from POST"""
        text_recto = form.cleaned_data["text_recto"]
        text_verso = form.cleaned_data["text_verso"]
        studie_recto = form.cleaned_data["studie_recto"]
        studie_verso = form.cleaned_data["studie_verso"]
        return text_recto, text_verso, studie_recto, studie_verso
