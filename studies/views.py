from datetime import timedelta
from django.forms.models import fields_for_model
from django.http import JsonResponse
import datetime
from django.db.models import Q
import random
from itertools import chain
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .models import *
from studies.logic.userAction import UserAction
from studies.logic.FeedDb import FeedDb

from studies.forms import StudiesNotesForm, BookForm, ChapterForm
from django.db.models import Avg, Max, Min

user_action = UserAction()
TIME_NOW = datetime.date.today()


def personal_home_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    # context["form_chapter"] = ChapterForm()
    # context["books"] = user_action.get_books(request)
    context = user_action.get_books(request)
    if request.POST:
        form_book = BookForm(request.POST)
        if form_book.is_valid():

            book = form_book.save(commit=False)
            book.order_book = len(Book.objects.filter(users=request.user)) + 1
            book.save()
            book.users.add(request.user, through_defaults={
                'user_fonction': "owner", "level_chapter": 1})
            book.save()
            return redirect('studies:personal_home')
        else:
            context["form_book"] = form_book

    return render(request, "studies/personal_home.html", context)


def book_view(request, book, chapter=None):
    """ book with 0/1 selected chapter"""
    context = {}
    context["book"] = get_object_or_404(Book,
                                        users=request.user, pk=book)
    context["chapters"] = Chapter.objects.filter(book=book)

    if chapter is not None:
        context["notes"] = StudiesNotes.objects.filter(chapter=chapter)

    if request.POST:
        form_chapter = ChapterForm(request.POST)
        context["form_chapter"] = form_chapter
        if form_chapter.is_valid():
            chapter = Chapter.objects.create(
                book=Book.objects.get(pk=book, users=request.user), name=form_chapter.cleaned_data["name"],
                order_chapter=len(Chapter.objects.filter(book=book)) + 1)
            return redirect('studies:book_page', book=book, chapter=chapter.id)
    else:
        form_chapter = ChapterForm()
        context["form_chapter"] = form_chapter

    return render(request, "studies/book.html", context)


def note_add_or_update(request, chapter=None, note=None):
    """ 1 note to add / change """
    context = {}
    context["chapter"] = chapter
    book = Chapter.objects.get(pk=chapter).book.id

    if note is not None:
        instance_note = StudiesNotes.objects.get(
            chapter__book__users=request.user, pk=note)

        context["instance_note"] = instance_note  # update note

    else:
        instance_note = None  # new note

        context["instance_note"] = instance_note

    if request.POST:

        form = StudiesNotesForm(request.POST, instance=instance_note)
        context["form"] = form

        if form.is_valid():
            if instance_note is not None:
                form.save()
            else:
                obj = form.save(commit=False)

                obj.order_note = len(
                    StudiesNotes.objects.filter(users=request.user, chapter__pk=chapter)) + 1
                obj.chapter = Chapter.objects.get(pk=chapter)
                obj.save()
                obj.users.add(request.user, through_defaults={})
                obj.save()

            return redirect('studies:book_page', chapter=chapter, book=book)

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
    return redirect('studies:book_page', book=book)


def delete_note(request, note):
    selected_note = get_object_or_404(
        StudiesNotes, pk=note, chapter__book__users=request.user)
    book = selected_note.chapter.book.id
    chapter = selected_note.chapter.id
    selected_note.delete()
    return redirect('studies:book_page', book=book, chapter=chapter)


def add_data_in_db(request):
    if not request.user.is_authenticated:
        return redirect("login")

    feed_db = FeedDb(request)
    feed_db.add_book("anglais")
    feed_db.add_chapter_in_book('vocabulaire 1')
    feed_db.add_note_from_csv()
    feed_db.add_chapter_in_book('vocabulaire 2')
    feed_db.add_note_from_csv()
    feed_db.add_chapter_in_book('vocabulaire 3')
    feed_db.add_note_from_csv()

    return redirect('studies:personal_home')


def start_game_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    context = {}
    context["game_list_auto"] = []
    context["today"] = TIME_NOW

# SPEED GROUP
    speed = StudiesNotesProgression.objects.filter(
        (
            Q(lvl_recto__lt=6)
            & Q(notes__studie_recto=True)
            & Q(next_studied_date_recto__lte=TIME_NOW, user=request.user)
        )
        | (
            Q(lvl_verso__lt=6)
            & Q(notes__studie_verso=True)
            & Q(next_studied_date_verso__lte=TIME_NOW, user=request.user)
        )
    ).order_by("notes__chapter__book", "notes__chapter")[:10]

    for elt in speed:
        if elt.next_studied_date_recto <= TIME_NOW and elt.notes.studie_recto is True:
            context["game_list_auto"].append({
                "id": elt.id,
                "sens": "recto",
                "text": elt.notes.text_recto,
                "response": elt.notes.text_verso,
                "class_button_true": "ajax-true-recto",
                "class_button_wrong": "ajax-wrong-recto",

            })
        elif elt.next_studied_date_verso <= TIME_NOW and elt.notes.studie_verso is True:
            context["game_list_auto"].append({
                "id": elt.id,
                "sens": "verso",
                "text": elt.notes.text_verso,
                "response": elt.notes.text_recto,
                "class_button_true": "ajax-true-verso",
                "class_button_wrong": "ajax-wrong-verso",


            })
# LONG GROUP
    long = StudiesNotesProgression.objects.filter(
        (
            Q(lvl_recto__gt=5)
            & Q(notes__studie_verso=True)
            & Q(next_studied_date_recto__lte=TIME_NOW, user=request.user)
        )
        | (
            Q(lvl_verso__gt=5)
            & Q(notes__studie_recto=True)
            & Q(next_studied_date_verso__lte=TIME_NOW, user=request.user)
        )
    ).order_by("notes__chapter__book", "notes__chapter")[:40]

    for elt in long:
        if elt.next_studied_date_recto <= TIME_NOW and elt.notes.studie_recto is True:
            context["game_list_auto"].append({
                "id": elt.id,
                "sens": "recto",
                "text": elt.notes.text_recto,
                "response": elt.notes.text_verso,
                "class_button_true": "ajax-true-recto",
                "class_button_wrong": "ajax-wrong-recto",

            })
        elif elt.next_studied_date_verso <= TIME_NOW and elt.notes.studie_verso is True:
            context["game_list_auto"].append({
                "id": elt.id,
                "sens": "verso",
                "text": elt.notes.text_verso,
                "response": elt.notes.text_recto,
                "class_button_true": "ajax-true-verso",
                "class_button_wrong": "ajax-wrong-verso",


            })

    # 1 +1j date.today()
    # 2 +1 week
    # 3 +4 week
    # 4 +12 week
    # 5 24 week
# ENDING
    random.shuffle(context["game_list_auto"])

    return render(request, "studies/auto_game.html", context)


def note_true_recto(request):
    id = request.POST.get("Product_id")
    result = get_object_or_404(
        StudiesNotesProgression, pk=id, user=request.user)
    if result.lvl_recto <= 5:
        result.lvl_recto += 1
        result.last_studied_date_recto = TIME_NOW
        result.next_studied_date_recto = TIME_NOW + timedelta(days=1)

    elif result.lvl_recto == 6:
        result.lvl_recto += 1
        result.last_studied_date_recto = TIME_NOW
        result.next_studied_date_recto = TIME_NOW + timedelta(weeks=1)

    elif result.lvl_recto == 7:
        result.lvl_recto += 1
        result.last_studied_date_recto = TIME_NOW
        result.next_studied_date_recto = TIME_NOW + timedelta(weeks=4)

    elif result.lvl_recto == 8:
        result.lvl_recto += 1
        result.last_studied_date_recto = TIME_NOW
        result.next_studied_date_recto = TIME_NOW + timedelta(weeks=12)

    elif result.lvl_recto == 9:
        result.lvl_recto += 1
        result.last_studied_date_recto = TIME_NOW
        result.next_studied_date_recto = TIME_NOW + timedelta(weeks=24)

    elif result.lvl_recto == 10:
        result.last_studied_date_recto = TIME_NOW
        result.next_studied_date_recto = TIME_NOW + timedelta(weeks=36)

    result.save()

    return JsonResponse({"operation_result": result.notes.text_recto})


def note_true_verso(request):
    id = request.POST.get("Product_id")
    result = get_object_or_404(
        StudiesNotesProgression, pk=id, user=request.user)
    if result.lvl_verso <= 5:
        result.lvl_verso += 1
        result.last_studied_date_verso = TIME_NOW
        result.next_studied_date_verso = TIME_NOW + timedelta(days=1)

    elif result.lvl_verso == 6:
        result.lvl_verso += 1
        result.last_studied_date_verso = TIME_NOW
        result.next_studied_date_verso = TIME_NOW + timedelta(weeks=1)

    elif result.lvl_verso == 7:
        result.lvl_verso += 1
        result.last_studied_date_verso = TIME_NOW
        result.next_studied_date_verso = TIME_NOW + timedelta(weeks=4)

    elif result.lvl_verso == 8:
        result.lvl_verso += 1
        result.last_studied_date_verso = TIME_NOW
        result.next_studied_date_verso = TIME_NOW + timedelta(weeks=12)

    elif result.lvl_verso == 9:
        result.lvl_verso += 1
        result.last_studied_date_verso = TIME_NOW
        result.next_studied_date_verso = TIME_NOW + timedelta(weeks=24)

    elif result.lvl_verso == 10:
        result.last_studied_date_verso = TIME_NOW
        result.next_studied_date_verso = TIME_NOW + timedelta(weeks=36)

    result.save()

    return JsonResponse({"operation_result": result.notes.text_recto})


def note_wrong_recto(request):
    id = request.POST.get("Product_id")
    result = get_object_or_404(
        StudiesNotesProgression, pk=id, user=request.user)
    result.lvl_recto = 1
    result.last_studied_date_recto = TIME_NOW
    result.next_studied_date_recto = TIME_NOW + timedelta(days=1)

    result.save()

    fav = request.POST.get("fav")
    print("A EGAL ", fav, "_false_recto")

    return JsonResponse({"operation_result": fav})


def note_wrong_verso(request):
    id = request.POST.get("Product_id")
    result = get_object_or_404(
        StudiesNotesProgression, pk=id, user=request.user)
    result.lvl_verso = 1
    result.last_studied_date_verso = TIME_NOW
    result.next_studied_date_verso = TIME_NOW + timedelta(days=1)

    result.save()

    fav = request.POST.get("fav")

    return JsonResponse({"operation_result": fav})
