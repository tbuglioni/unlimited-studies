from django.test import RequestFactory, TestCase
from studies.logic.userAction import UserAction
from studies.models import Book, Chapter, StudiesNotes
from studies.tests.speed_set_up import SpeedSetUP


class UserActionTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        speed_set_up = SpeedSetUP()
        self.user_action = UserAction()

        self.user_a = speed_set_up.set_up_user_a()

        self.book_1 = speed_set_up.create_book_owner(self.user_a, order_book=1)

        self.chapter_1 = speed_set_up.create_chapter(
            self.book_1, order_chapter=1)

        self.note_1 = speed_set_up.create_note(
            chapter=self.chapter_1, order_note=1, recto=True, verso=True
        )
        speed_set_up.add_user_to_notes(
            user=self.user_a, note=self.note_1, lvl_recto=5, lvl_verso=5
        )

    def test_get_books(self):
        request = self.factory.get("hello/world")
        request.user = self.user_a

        elements = self.user_action.get_books(request)

        self.assertEqual(elements[0], self.book_1)

    def test_get_UserBookMany(self):
        request = self.factory.get("/a/test/path/")
        request.user = self.user_a

        elements = self.user_action.get_UserBookMany(request)

        self.assertEqual(elements[0].book_id, self.book_1.id)

    def test_get_book_404(self):
        request = self.factory.get("/a/test/path/")
        request.user = self.user_a

        element = self.user_action.get_book_404(request, self.book_1.id)

        self.assertEqual(element, self.book_1)

    def test_create_book(self):
        factory = RequestFactory()
        data = {
            "name": "name1",
            "description": "description1",
            "source_info": "source_info1",
            "order_book": 1,
        }
        request = factory.post("/a/test/path/", data)
        request.user = self.user_a
        context = {}
        context["selectedBook"] = None

        self.user_action.create_or_update_book(request, context)

        book_counter = Book.objects.all().count()
        self.assertEqual(book_counter, 2)

    def test_update_book(self):
        factory = RequestFactory()
        data = {
            "name": "name1",
            "description": "description1",
            "source_info": "source_info1",
            "order_book": 1,
            "book_id": self.book_1.id,
        }
        request = factory.post("/a/test/path/", data)
        request.user = self.user_a
        context = {}
        context["selectedBook"] = self.book_1.id

        self.user_action.create_or_update_book(request, context)

        book_counter = Book.objects.all().count()
        self.assertEqual(book_counter, 1)

    def test_get_chapters(self):
        request = self.factory.get("hello/world")
        request.user = self.user_a

        elements = self.user_action.get_chapters(request, self.book_1.id)

        self.assertEqual(elements[0], self.chapter_1)

    def test_get_chapter_404(self):
        request = self.factory.get("/a/test/path/")
        request.user = self.user_a

        element = self.user_action.get_chapter_404(request, self.chapter_1.id)

        self.assertEqual(element, self.chapter_1)

    def test_create_chapter(self):
        factory = RequestFactory()
        data = {
            "name": "name1",
            "order_chapter": 2,
        }
        request = factory.post("/a/test/path/", data)
        request.user = self.user_a
        context = {}
        context["chapter"] = None
        context["book"] = self.book_1

        self.user_action.create_or_update_chapter(
            request, context, self.book_1.id)

        chapter_counter = Chapter.objects.all().count()
        self.assertEqual(chapter_counter, 2)

    def test_update_chapter(self):
        factory = RequestFactory()
        data = {
            "name": "name1",
            "order_chapter": 2,
            "chapter_id": self.chapter_1.id,
        }
        request = factory.post("/a/test/path/", data)
        request.user = self.user_a
        context = {}
        context["chapter"] = self.chapter_1.id

        self.user_action.create_or_update_chapter(
            request, context, self.book_1.id)

        chapter_counter = Chapter.objects.all().count()
        self.assertEqual(chapter_counter, 1)

    def test_get_notes(self):
        request = self.factory.get("hello/world")
        request.user = self.user_a

        elements = self.user_action.get_notes(request, self.chapter_1.id)

        self.assertEqual(elements[0], self.note_1)

    def test_get_note_404(self):
        request = self.factory.get("/a/test/path/")
        request.user = self.user_a

        element = self.user_action.get_note_404(request, self.note_1.id)

        self.assertEqual(element, self.note_1)

    def test_create_note(self):
        factory = RequestFactory()
        data = {
            "text_recto": "text_r",
            "text_verso": "text_v",
            "studie_recto": True,
            "studie_verso": True,
        }
        request = factory.post("/a/test/path/", data)
        request.user = self.user_a
        context = {}
        context["instance_note"] = None

        self.user_action.create_or_update_note(
            request, context, self.chapter_1.id)

        StudiesNotes_counter = StudiesNotes.objects.all().count()
        self.assertEqual(StudiesNotes_counter, 2)

    def test_update_note(self):
        factory = RequestFactory()
        data = {
            "text_recto": "text_r",
            "text_verso": "text_v",
            "studie_recto": True,
            "studie_verso": True,
            "note_id": self.note_1.id,
        }
        request = factory.post("/a/test/path/", data)
        request.user = self.user_a
        context = {}
        context["instance_note"] = self.note_1.id

        self.user_action.create_or_update_note(
            request, context, self.chapter_1.id)

        StudiesNotes_counter = StudiesNotes.objects.all().count()
        self.assertEqual(StudiesNotes_counter, 1)
