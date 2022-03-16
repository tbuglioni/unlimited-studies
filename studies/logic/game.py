import random
from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone
from studies.models import StudiesNotesProgression


class Game:
    """ run game, and update notes after each games"""

    def __init__(self):
        self.game_list_auto = []
        self.notes_todo = []
        self.TIME_NOW = timezone.now()

    def __notes_todo(self, request,
                     speed: bool = True,
                     number_of_notes: int = 10):
        """find notes to run auto game"""
        if speed:
            self.notes_todo = (
                StudiesNotesProgression.objects.filter(
                    user=request.user,
                    level__lte=5
                )
                .select_related("notes")
                .distinct()
                .order_by(
                    "notes__chapter__book__userbookmany__order_book",
                    "notes__chapter"
                )[:number_of_notes]
            )

        else:
            self.notes_todo = (
                StudiesNotesProgression.objects.filter(
                    user=request.user,
                    level__gte=6,
                    next_studied_date__lte=self.TIME_NOW,
                )
                .select_related("notes")
                .distinct()
                .order_by(
                    "notes__chapter__book__userbookmany__order_book",
                    "notes__chapter"
                )[:number_of_notes]
            )

    def __split_notes(self):
        """splits selected notes into dict"""
        for elt in self.notes_todo:
            if elt.is_recto:
                self.game_list_auto.append(
                    {
                        "id": elt.id,
                        "sens": "recto",
                        "text": elt.notes.text_recto,
                        "response": elt.notes.text_verso,
                        "book": elt.notes.chapter.book.name,
                        "chapter": elt.notes.chapter.name,
                    }
                )

            elif elt.is_recto is False:
                self.game_list_auto.append(
                    {
                        "id": elt.id,
                        "sens": "verso",
                        "text": elt.notes.text_verso,
                        "response": elt.notes.text_recto,
                        "book": elt.notes.chapter.book.name,
                        "chapter": elt.notes.chapter.name,
                    }
                )

    def get_notes_todo(self, request, nbr_speed: int = 10, nbr_long: int = 10):
        """get notes auto mode, split them and return all"""
        self.__notes_todo(request, speed=True, number_of_notes=nbr_speed)
        self.__split_notes()
        self.__notes_todo(request, speed=False, number_of_notes=nbr_long)
        self.__split_notes()
        random.shuffle(self.game_list_auto)

        exit_list = []
        for elt in self.game_list_auto:
            if elt not in exit_list:
                exit_list.append(elt)

        return exit_list

    def __update_lvl(self, note, days: int):
        """Update the current level of the given note"""
        if note.level < 10:
            note.level += 1
        note.last_studied_date = self.TIME_NOW
        note.next_studied_date = self.TIME_NOW + timedelta(days=days)
        note.save()

    def __conditional_update(self, note):
        """update note in a conditional lvl"""

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
        """Reset the level of the note"""
        note.level = 1
        note.last_studied_date = self.TIME_NOW
        note.next_studied_date = self.TIME_NOW + timedelta(days=1)

        note.save()

    def change_lvl(self, request, note_id: int, win: bool = True):
        """update the lvl of a note or reset it"""

        result = get_object_or_404(
            StudiesNotesProgression, pk=note_id, user=request.user
        )
        if win:
            self.__conditional_update(result)
        else:
            self.__reset_lvl(result)
