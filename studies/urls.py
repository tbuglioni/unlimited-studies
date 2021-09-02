from django.urls import path
from . import views

app_name = "studies"

urlpatterns = [
    path("", views.personal_home_view, name="personal_home"),
    path("student", views.student_view, name="student_page"),
    path("teacher/<int:book>", views.teacher_view, name="teacher_page"),
    path("teacher/<int:book>/<int:error>",
         views.teacher_view, name="teacher_page"),
    path("teacher/add/<int:book>",
         views.add_new_student_in_book_view, name="add_new_student"),

    path("subscribe/<int:book>", views.subscribe_book_view, name="subscribe_book"),
    path("<int:book>", views.personal_home_view, name="personal_home"),

    # get
    path("book/<int:book>", views.book_view, name="book_page"),
    path("book/<int:book>/<int:chapter>",
         views.book_view, name="book_page"),

    # note:
    path("chapter/<int:chapter>",
         views.note_add_or_update_view, name="specific_note"),
    path("chapter/<int:chapter>/<int:note>",
         views.note_add_or_update_view, name="specific_note"),

    # delete
    path("delete/book/<int:book>", views.delete_book_view, name="delete_book"),
    path("delete/chapter/<int:chapter>",
         views.delete_chapter_view, name="delete_chapter"),
    path("delete/note/<int:note>", views.delete_note_view, name="delete_note"),


    # teacher - student subscription
    path("unsubscribe/<int:book>",
         views.unsubscribe_book_view, name="unsubscribe_book"),
    path("unsubscribe/student<int:student>/<int:book>",
         views.unsubscribe_student_by_owner_view, name="unsubscribe_student"),


    path("game_auto/<int:speed>/<int:long>",
         views.start_game_view, name="game_auto"),
    path("game_auto", views.start_game_view, name="game_auto"),
]
