from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from studies.logic.userAction import UserAction
from studies.logic.analyse import Analyse
from studies.logic.game import Game

from studies.logic.FeedDb import FeedDb
from django.db.models import Q

TIME_NOW = datetime.date.today()
new_game = Game()


@login_required
def personal_home_view(request, book=None):
    """ personal page with books and feedback"""
    user_action = UserAction()

    context = {}
    context["books"] = user_action.get_books(request)
    current_analyse = Analyse(request)

    context["todoo"] = current_analyse.get_nbr_notes_todoo()
    context["all_notes"] = current_analyse.get_nbr_of_notes()
    context["all_notes_avg"] = current_analyse.get_lvl_avg()
    context["books_avg"] = current_analyse.get_list_lvl_avg_each_book()
    context["Today_recap"] = current_analyse.get_notes_studied_today()
    context["month_recap"] = current_analyse.get_notes_studied_this_month()

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
    user_action = UserAction()
    context = {}
    context["book"] = user_action.get_book_404(request, book)
    context["chapters"] = Chapter.objects.filter(book=book)

    if chapter is not None:
        context["chapter"] = user_action.get_chapter_404(
            request, chapter=chapter)
        paginator = Paginator(
            user_action.get_notes(request, chapter), 100)
        page = request.GET.get('page', 1)
        try:
            context["notes"] = paginator.page(page)
        except Paginator.PageNotAnInteger:
            context["notes"] = paginator.page(1)
        except Paginator.EmptyPage:
            context["notes"] = paginator.page(paginator.num_pages)
    else:
        context["chapter"] = None

    if request.POST:
        user_action.create_or_update_chapter(request, context, book, chapter)

    return render(request, "studies/book.html", context)


@ login_required
def note_add_or_update(request, chapter=None, note=None):
    """ 1 note to add / change """
    user_action = UserAction()
    context = {}
    context["chapter"] = chapter
    book = Chapter.objects.get(pk=chapter).book.id

    if note is not None:
        context["instance_note"] = user_action.get_note_404(request, note)

    else:
        context["instance_note"] = None  # new note

    if request.POST:
        user_action.create_or_update_note(request, context, chapter)

    return redirect('studies:book_page', chapter=chapter, book=book)


@ login_required
def delete_book(request, book):
    user_action = UserAction()
    """ delete 1 book"""
    selected_book = get_object_or_404(Book, pk=book, users=request.user)
    selected_book.delete()

    return redirect('studies:personal_home')


@ login_required
def delete_chapter(request, chapter):
    user_action = UserAction()
    """ delete 1 chapter"""
    selected_chapter = user_action.get_chapter_404(request, chapter)

    book = selected_chapter.book.id
    selected_chapter.delete()
    return redirect('studies:book_page', book=book)


@ login_required
def delete_note(request, note):
    user_action = UserAction()
    """ delete 1 note"""
    selected_note = user_action.get_note_404(request, note)
    book = selected_note.chapter.book.id
    chapter = selected_note.chapter.id
    selected_note.delete()
    return redirect('studies:book_page', book=book, chapter=chapter)


@ login_required
def add_data_in_db(request):
    """ feed db with data """
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


@ login_required
def start_game_view(request):
    """ start auto game in a specific page """
    if request.POST:
        data_list = json.loads(request.POST.get('exit_list'))
        print(data_list)
        for elt in data_list:
            print(elt['id'], elt['sens'], elt['win'])
            new_game.change_lvl(request, elt['id'], elt['sens'], elt['win'])
        
        new_game.cleaned_data()
        return JsonResponse({"status": "ok"})

    context = {}
    new_game.cleaned_data()
    context["game_list_auto"] = new_game.get_notes_todo(
        request, nbr_speed=2, nbr_long=2)

    return render(request, "studies/auto_game.html", context)


@ login_required
def note_true_recto(request):
    """ valid 1 note recto and change lvl/next studie """
    user_action = UserAction()
    note_id = request.POST.get("Product_id")
    user_action.change_lvl(request, note_id, sens="recto", win=True)
    return JsonResponse({"status": "ok"})


@ login_required
def note_true_verso(request):
    """ valid 1 note verso and change lvl/next studie """
    user_action = UserAction()
    note_id = request.POST.get("Product_id")
    user_action.change_lvl(request, note_id, sens="verso", win=True)
    return JsonResponse({"status": "ok"})


@ login_required
def note_wrong_recto(request):
    """ unvalid 1 note recto and change lvl/next studie """
    user_action = UserAction()
    note_id = request.POST.get("Product_id")
    user_action.change_lvl(request, note_id, sens="recto", win=False)
    return JsonResponse({"status": "ok"})


@ login_required
def note_wrong_verso(request):
    """ unvalid 1 note verso and change lvl/next studie """
    user_action = UserAction()
    note_id = request.POST.get("Product_id")
    user_action.change_lvl(request, note_id, sens="verso", win=False)
    return JsonResponse({"status": "ok"})
