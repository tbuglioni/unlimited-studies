from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from studies.logic.userAction import UserAction
from studies.forms import StudiesNotesForm

user_action = UserAction()


def personal_home_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = user_action.get_books(request)

    return render(request, "studies/personal_home.html", context)


def book_view_only(request, book):
    """ book with no chapter selected"""

    context = user_action.get_one_book(request, book)

    return render(request, "studies/book.html", context)


def book_view_chapter(request, book, chapter):
    """ book with one selected chapter"""
    context = {}
    context["book"] = get_object_or_404(Book,
                                        users=request.user, pk=book)
    context["chapters"] = Chapter.objects.filter(book=book)

    context["notes"] = StudiesNotes.objects.filter(chapter=chapter)

    return render(request, "studies/book.html", context)


def custom_note_view(request, chapter=None, note=None):
    """ 1 note to add / change """
    context = {}
    context["chapter"] = chapter
    book = Chapter.objects.get(pk=chapter).book.id

    if note is not None:
        instance_note = StudiesNotes.objects.get(
            chapter__book__users=request.user, pk=note)

        context["instance_note"] = instance_note

    else:
        instance_note = None

    context["instance_note"] = instance_note
    print(f"-------------ID = {note}--------------")
    print(f"-------------Instance = {instance_note}--------------")

    if request.POST:
        print(f"-------------POST--------------")
        form = StudiesNotesForm(request.POST, instance=instance_note)
        context["form"] = form

        if form.is_valid():
            print("------ CLEAN = ", form.cleaned_data, "------")
            form.save()

            return redirect('studies:book_chapter', chapter=chapter, book=book)

    else:
        context["form"] = StudiesNotesForm(instance=instance_note)
    return render(request, "studies/note.html", context)


def delete_book(request, book):
    selected_book = get_object_or_404(Book, pk=book, users=request.user)
    selected_book.delete()

    return redirect('studies:personal_home')


def delete_chapter(request, chapter):
    selected_chapter = get_object_or_404(
        Chapter, pk=chapter, book__users=request.user)
    book = selected_chapter.book.id
    selected_chapter.delete()
    return redirect('studies:book_only', book=book)


def delete_note(request, note):
    selected_note = get_object_or_404(
        StudiesNotes, pk=note, chapter__book__users=request.user)
    book = selected_note.chapter.book.id
    chapter = selected_note.chapter.id
    selected_note.delete()
    return redirect('studies:book_chapter', book=book, chapter=chapter)


def add_data_in_db(request):
    if not request.user.is_authenticated:
        return redirect("login")

    italien, created = Book.objects.get_or_create(
        name="italien",
        order_book=1,
        description="hello world in italia", source_info='wikipedia is bad :)')

    italien.users.add(request.user, through_defaults={
                      'user_fonction': "owner", "level_chapter": 3})

    anglais, created = Book.objects.get_or_create(
        name="anglais",
        order_book=2,
        description="hello world in england", source_info='wikipedia is bad :)')

    anglais.users.add(request.user, through_defaults={
                      'user_fonction': "owner", "level_chapter": 2})

    francais, created = Book.objects.get_or_create(
        name="francais",
        order_book=3,
        description="hello world in france", source_info='wikipedia is bad :)')

    francais.users.add(request.user, through_defaults={
        'user_fonction': "owner", "level_chapter": 2})

    vocabulaire_it, created = Chapter.objects.get_or_create(
        name="vocabulaire",
        order_chapter=1,
        book=italien,
    )

    vocabulaire_en, created = Chapter.objects.get_or_create(
        name="vocabulaire",
        order_chapter=1,
        book=anglais,
    )
    vocabulaire_fr, created = Chapter.objects.get_or_create(
        name="vocabulaire",
        order_chapter=1,
        book=francais,
    )

    word_it_1, created = StudiesNotes.objects.get_or_create(
        text_recto="bongiorno",
        text_verso="bonjour",
        chapter=vocabulaire_it,
        order_note=1,
        studie_verso=True,

    )

    word_it_1.users.add(request.user, through_defaults={
        'lvl_recto': "4", "lvl_verso": 3})

    word_it_2, created = StudiesNotes.objects.get_or_create(
        text_recto="ciao",
        text_verso="salut",
        chapter=vocabulaire_it,
        order_note=2,
        studie_verso=True,

    )
    word_it_2.users.add(request.user, through_defaults={
        'lvl_recto': "3", "lvl_verso": 2})

    word_it_3, created = StudiesNotes.objects.get_or_create(
        text_recto="grazie",
        text_verso="merci",
        chapter=vocabulaire_it,
        order_note=3,
        studie_verso=True,

    )

    word_it_3.users.add(request.user, through_defaults={
        'lvl_recto': "2", "lvl_verso": 1})

    return redirect('studies:personal_home')
