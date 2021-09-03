import random
from studies.models import *
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from datetime import timedelta


class Game:

    def __init__(self):
        self.game_list_auto = []
        self.notes_todo = []
        self.TIME_NOW = timezone.now()

    def __notes_todo(self, request, speed=True, number_of_notes=10):
        """ find notes to run auto game """
        if speed:
            self.notes_todo = StudiesNotesProgression.objects.filter(user_id=request.user.id, level__lte=5, next_studied_date__lte=self.TIME_NOW).distinct(
            ).select_related('notes').order_by("notes__chapter__book__userbookmany__order_book", "notes__chapter")[:number_of_notes]

        else:
            self.notes_todo = StudiesNotesProgression.objects.filter(user_id=request.user.id, level__gte=6, next_studied_date__lte=self.TIME_NOW).distinct(
            ).select_related('notes').order_by("notes__chapter__book__userbookmany__order_book", "notes__chapter")[:number_of_notes]

    def __split_notes(self):
        """ splits selected notes into dict """
        for elt in self.notes_todo:
            if (elt.is_recto == True):
                self.game_list_auto.append({
                    "id": elt.id,
                    "sens": "recto",
                    "text": elt.notes.text_recto,
                    "response": elt.notes.text_verso,
                    "book": elt.notes.chapter.book.name,
                    "chapter": elt.notes.chapter.name,
                })

            elif (elt.is_recto == False):
                self.game_list_auto.append({
                    "id": elt.id,
                    "sens": "verso",
                    "text": elt.notes.text_verso,
                    "response": elt.notes.text_recto,
                    "book": elt.notes.chapter.book.name,
                    "chapter": elt.notes.chapter.name,
                })

    def get_notes_todo(self, request, nbr_speed=10, nbr_long=10):
        """ get notes auto mode, split them and return all """
        self.__notes_todo(request, speed=True, number_of_notes=nbr_speed)
        self.__split_notes()
        self.__notes_todo(request, speed=False, number_of_notes=nbr_long)
        self.__split_notes()
        random.shuffle(self.game_list_auto)
        return self.game_list_auto

    def __update_lvl(self, note, days):
        """ Update the current level of the given note"""
        if note.level < 10:
            note.level += 1
        note.last_studied_date = self.TIME_NOW
        note.next_studied_date = self.TIME_NOW + timedelta(days=days)
        note.save()

    def __conditional_update(self, note):
        """ update note in a conditional lvl """

        if note.level <= 4:
            self.__update_lvl(note, 1)  # 1 day

        elif note.level == 5:
            self.__update_lvl(note, 3)  # 3 day

        elif note.level == 6:
            self.__update_lvl(note, 7)  # 1 week

        elif note.level == 7:
            self.__update_lvl(note, 30)  # 1 month

        elif note.level == 8:
            self.__update_lvl(note, 90)  # 3 month

        elif note.level == 9:
            self.__update_lvl(note, 182)  # 6 month

        elif note.level == 10:
            self.__update_lvl(note, 364)  # 1 year

    def __reset_lvl(self, note):
        """ Reset the level of the note"""
        note.level = 1
        note.last_studied_date = self.TIME_NOW
        note.next_studied_date = self.TIME_NOW + timedelta(days=1)

        note.save()

    def change_lvl(self, request, note_id, win=True):
        """ update the lvl of a note or reset it """

        result = get_object_or_404(
            StudiesNotesProgression, pk=note_id, user=request.user)
        if win:
            self.__conditional_update(result)
        else:
            self.__reset_lvl(result)
