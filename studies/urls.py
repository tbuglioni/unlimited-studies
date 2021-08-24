from django.urls import path
from . import views

app_name = "studies"

urlpatterns = [
    path("", views.personal_home_view, name="personal_home"),
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
    path("unsubscribe/book/<int:book>", views.unsubscribe_book_view, name="unsubscribe_book"),
    path("delete/chapter/<int:chapter>",
         views.delete_chapter_view, name="delete_chapter"),
    path("delete/note/<int:note>", views.delete_note_view, name="delete_note"),


    path("feed_db", views.add_data_in_db_view, name="feed_db"),

    path("game_auto/<int:speed>/<int:long>",
         views.start_game_view, name="game_auto"),
    path("game_auto", views.start_game_view, name="game_auto"),
]
