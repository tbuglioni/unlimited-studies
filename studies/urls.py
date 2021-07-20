from django.urls import path
from . import views

app_name = "studies"

urlpatterns = [
    path("", views.personal_home_view, name="personal_home"),

    # get
    path("book/<int:book>", views.book_view, name="book_page"),
    path("book/<int:book>/<int:chapter>",
         views.book_view, name="book_page"),

    #add or update
    # book


    # chapter

    # note:
    path("note/<int:chapter>", views.note_add_or_update, name="specific_note"),
    path("note/<int:chapter>/<int:note>",
         views.note_add_or_update, name="specific_note"),

    # delete
    path("delete/book/<int:book>", views.delete_book, name="delete_book"),
    path("delete/chapter/<int:chapter>",
         views.delete_chapter, name="delete_chapter"),
    path("delete/note/<int:note>", views.delete_note, name="delete_note"),


    path("feed_db", views.add_data_in_db, name="feed_db"),
]
