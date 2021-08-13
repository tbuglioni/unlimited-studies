import random
from studies.models import *
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from datetime import timedelta


class Game:

    def __init__(self):
        self.game_list_auto = []
        self.notes_todo = []
        self.TIME_NOW = datetime.date.today()
        
    def cleaned_data(self):
        self.game_list_auto = []
        self.notes_todo = []
        

    def __notes_todo(self, request, speed=True, number_of_notes=10):
        """ find notes to run auto game """
        if speed:
            self.notes_todo = StudiesNotesProgression.objects.filter(
                (
                    Q(lvl_recto__lt=6)
                    & Q(notes__studie_recto=True)
                    & Q(next_studied_date_recto__lte=self.TIME_NOW, user=request.user)
                )
                | (
                    Q(lvl_verso__lt=6)
                    & Q(notes__studie_verso=True)
                    & Q(next_studied_date_verso__lte=self.TIME_NOW, user=request.user)
                )
            ).select_related('notes').order_by("notes__chapter__book", "notes__chapter")[:number_of_notes]

        else:
            self.notes_todo = StudiesNotesProgression.objects.filter(
                (
                    Q(lvl_recto__gt=5)
                    & Q(notes__studie_verso=True)
                    & Q(next_studied_date_recto__lte=self.TIME_NOW, user=request.user)
                )
                | (
                    Q(lvl_verso__gt=5)
                    & Q(notes__studie_recto=True)
                    & Q(next_studied_date_verso__lte=self.TIME_NOW, user=request.user)
                )
            ).select_related('notes').order_by("notes__chapter__book", "notes__chapter")[:number_of_notes]

    def __split_notes(self, speed=True):
        """ splits selected notes into dict """
        for elt in self.notes_todo:

            if speed:
                if (elt.next_studied_date_recto <= self.TIME_NOW
                        and elt.notes.studie_recto is True
                        and elt.lvl_recto < 6):
                    self.game_list_auto.append({
                        "id": elt.id,
                        "sens": "recto",
                        "text": elt.notes.text_recto,
                        "response": elt.notes.text_verso,
                    })

                elif (elt.next_studied_date_verso <= self.TIME_NOW
                      and elt.notes.studie_verso is True
                      and elt.lvl_verso < 6):
                    self.game_list_auto.append({
                        "id": elt.id,
                        "sens": "verso",
                        "text": elt.notes.text_verso,
                        "response": elt.notes.text_recto,
                    })
            else:
                if (elt.next_studied_date_recto <= self.TIME_NOW
                        and elt.notes.studie_recto is True
                        and elt.lvl_recto > 5):
                    self.game_list_auto.append({
                        "id": elt.id,
                        "sens": "recto",
                        "text": elt.notes.text_recto,
                        "response": elt.notes.text_verso,
                    })

                elif (elt.next_studied_date_verso <= self.TIME_NOW
                      and elt.notes.studie_verso is True
                      and elt.lvl_verso > 5):
                    self.game_list_auto.append({
                        "id": elt.id,
                        "sens": "verso",
                        "text": elt.notes.text_verso,
                        "response": elt.notes.text_recto,
                    })

    def get_notes_todo(self, request, nbr_speed=10, nbr_long=10):
        """ get notes auto mode, split them and return all """
        self.__notes_todo(request, speed=True, number_of_notes=nbr_speed)
        self.__split_notes(speed=True)
        self.__notes_todo(request, speed=False, number_of_notes=nbr_long)
        self.__split_notes(speed=False)
        random.shuffle(self.game_list_auto)
        return self.game_list_auto

    def __update_lvl(self, note, sens, days):
        """ Update the current level of the given note"""
        if sens == "recto":
            note.lvl_recto += 1
            note.last_studied_date_recto = self.TIME_NOW
            note.next_studied_date_recto = self.TIME_NOW + timedelta(days=days)

        elif sens == "verso":
            note.lvl_verso += 1
            note.last_studied_date_verso = self.TIME_NOW
            note.next_studied_date_verso = self.TIME_NOW + timedelta(days=days)
        note.save()

    def __conditional_update(self, note, sens):
        """ update note in a conditional lvl """
        if sens == "recto":
            if note.lvl_recto <= 5:
                self.__update_lvl(note, sens, 1)  # 1 day

            elif note.lvl_recto == 6:
                self.__update_lvl(note, sens, 7)  # 1 week

            elif note.lvl_recto == 7:
                self.__update_lvl(note, sens, 30)  # 1 month

            elif note.lvl_recto == 8:
                self.__update_lvl(note, sens, 90)  # 3 month

            elif note.lvl_recto == 9:
                self.__update_lvl(note, sens, 182)  # 6 month

            elif note.lvl_recto == 10:
                self.__update_lvl(note, sens, 364)  # 1 year

        elif sens == "verso":
            if note.lvl_verso <= 5:
                self.__update_lvl(note, sens, 1)  # 1 day
            elif note.lvl_verso == 6:
                self.__update_lvl(note, sens, 7)  # 1 week
            elif note.lvl_verso == 7:
                self.__update_lvl(note, sens, 30)  # 1 month
            elif note.lvl_verso == 8:
                self.__update_lvl(note, sens, 90)  # 3 month
            elif note.lvl_verso == 9:
                self.__update_lvl(note, sens, 182)  # 6 month
            elif note.lvl_verso == 10:
                self.__update_lvl(note, sens, 364)  # 1 year

    def __reset_lvl(self, note, sens):
        """ Reset the level of the note"""
        if sens == "recto":
            note.lvl_recto = 1
            note.last_studied_date_recto = self.TIME_NOW
            note.next_studied_date_recto = self.TIME_NOW + timedelta(days=1)

        elif sens == "verso":
            note.lvl_verso = 1
            note.last_studied_date_verso = self.TIME_NOW
            note.next_studied_date_verso = self.TIME_NOW + timedelta(days=1)
        note.save()

    def change_lvl(self, request, note_id, sens, win=True):
        """ update the lvl of a note or reset it """

        result = get_object_or_404(
            StudiesNotesProgression, pk=note_id, user=request.user)
        if sens == "recto":
            if win:
                self.__conditional_update(result, sens)
            else:
                self.__reset_lvl(result, "recto")

        if sens == "verso":
            if win:
                self.__conditional_update(result, sens)
            else:
                self.__reset_lvl(result, "verso")
