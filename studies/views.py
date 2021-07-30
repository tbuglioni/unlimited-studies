from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.http import JsonResponse
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from studies.logic.userAction import UserAction
from studies.logic.FeedDb import FeedDb

from studies.forms import StudiesNotesForm, BookForm, ChapterForm
from django.db.models import Avg, Max, Min

user_action = UserAction()
TIME_NOW = datetime.date.today()


@login_required
def personal_home_view(request, book=None):

    context = {}
    context["books"] = user_action.get_books(request)

    if book is not None:
        context["selectedBook"] = user_action.get_book_404(request, book)
    else:
        context["selectedBook"] = None

    if request.POST:
        user_action.create_or_update_book(request, context)

    return render(request, "studies/personal_home.html", context)


@login_required
def book_view(request, book, chapter=None):
    """ book with 0/1 selected chapter"""
    context = {}
    context["book"] = user_action.get_book_404(request, book)
    context["chapters"] = Chapter.objects.filter(book=book)

    if chapter is not None:
        context["chapter"] = user_action.get_chapter_404(
            request, chapter=chapter)
        context["notes"] = user_action.get_notes(request, chapter)
    else:
        context["chapter"] = None

    if request.POST:
        user_action.create_or_update_chapter(request, context, book, chapter)
    else:
        form_chapter = ChapterForm(instance=context["chapter"])
        context["form_chapter"] = form_chapter

    return render(request, "studies/book.html", context)


@login_required
def note_add_or_update(request, chapter=None, note=None):
    """ 1 note to add / change """
    context = {}
    context["chapter"] = chapter
    book = Chapter.objects.get(pk=chapter).book.id

    if note is not None:
        context["instance_note"] = user_action.get_note_404(request, note)

    else:
        context["instance_note"] = None  # new note

    if request.POST:

        form = StudiesNotesForm(
            request.POST, instance=context["instance_note"])
        context["form"] = form

        if form.is_valid():
            if context["instance_note"] is not None:
                form.save()
            else:
                obj = form.save(commit=False)

                obj.order_note = len(
                    user_action.get_notes(request, chapter)) + 1
                obj.chapter = user_action.get_chapter_404(request, chapter)
                obj.save()
                obj.users.add(request.user, through_defaults={})
                obj.save()

            return redirect('studies:book_page', chapter=chapter, book=book)

    else:
        context["form"] = StudiesNotesForm(instance=context["instance_note"])
    return render(request, "studies/note.html", context)


@login_required
def delete_book(request, book):
    selected_book = get_object_or_404(Book, pk=book, users=request.user)
    selected_book.delete()

    return redirect('studies:personal_home')


@login_required
def delete_chapter(request, chapter):
    selected_chapter = user_action.get_chapter_404(request, chapter)

    book = selected_chapter.book.id
    selected_chapter.delete()
    return redirect('studies:book_page', book=book)


@login_required
def delete_note(request, note):
    selected_note = user_action.get_note_404(request, note)
    book = selected_note.chapter.book.id
    chapter = selected_note.chapter.id
    selected_note.delete()
    return redirect('studies:book_page', book=book, chapter=chapter)


@login_required
def add_data_in_db(request):
    if not request.user.is_authenticated:
        return redirect("login")

    feed_db = FeedDb(request)
    feed_db.add_book("anglais")
    feed_db.add_chapter_in_book('vocabulaire 1')
    feed_db.add_note_from_csv()
    feed_db.add_chapter_in_book('vocabulaire 2')
    feed_db.add_note_from_csv()
    feed_db.add_chapter_in_book('vocabulaire ')
    feed_db.add_note_from_csv()

    return redirect('studies:personal_home')


@login_required
def start_game_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    context = {}
    context["game_list_auto"] = user_action.get_notes_todo(
        request, nbr_speed=3, nbr_long=2)

    return render(request, "studies/auto_game.html", context)


@login_required
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


@login_required
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


@login_required
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


@login_required
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
