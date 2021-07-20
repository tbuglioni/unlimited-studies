from studies.models import *
from django.shortcuts import render, redirect, get_object_or_404


class UserAction:
    def __init__(self):
        self.name = 1

    def get_books(self, request):
        context = {}
        context["books"] = Book.objects.filter(users=request.user)
        return context

    def get_one_book(self, request, book):
        context = {}
        context["book"] = get_object_or_404(Book, users=request.user, pk=book)
        context["chapters"] = Chapter.objects.filter(book=book)
        return context

    def add_or_update_book(self, request):
        pass

    def add_or_update_chapter(self, request):
        pass

    def add_or_update_note(self, request):
        pass

    def delete_book(self, request):
        pass

    def delete_chapter(self, request):
        pass

    def delete_note(self, request):
        pass

    def run_game_auto(self, request):
        pass

    def run_specific_game(self, request):
        pass
