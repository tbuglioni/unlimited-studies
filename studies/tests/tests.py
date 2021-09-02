# from django.test import TestCase
# from unittest.mock import MagicMock
# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from django.conf import settings
# from studies.models import *
# import datetime
# from datetime import timedelta
# User = get_user_model()


# class StudiesDatabase(TestCase):
#

#     def test_count_book_users(self):
#         book_a = Book.objects.filter(users=self.user_a).count()
#         self.assertEqual(book_a, 2)

#         book_b = Book.objects.filter(users=self.user_b).count()
#         self.assertEqual(book_b, 0)

#     def test_count_chapter_users(self):
#         chapter_a = Chapter.objects.filter(book__users=self.user_a).count()
#         self.assertEqual(chapter_a, 2)

#         chapter_b = Chapter.objects.filter(book__users=self.user_b).count()
#         self.assertEqual(chapter_b, 0)

#     def test_count_note_users(self):
#         note_a = StudiesNotes.objects.filter(users=self.user_a).count()
#         self.assertEqual(note_a, 2)

#         note_b = StudiesNotes.objects.filter(users=self.user_b).count()
#         self.assertEqual(note_b, 0)


# from django.test import TestCase
# from studies.models import *
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# import datetime
# from datetime import timedelta
# User = get_user_model()


# class ViewPage(TestCase):
#     def setUp(self):


#     def test_delete_book_view_302_1(self):
#         """ delete_book_view : login(no), data(chapter_id, note_id), GET"""

#         self.response = self.client.get(
#             reverse("studies:delete_book", kwargs={'book': self.book_1.id}))
#         self.assertEqual(self.response.status_code, 302)

#     def test_delete_book_view_302_2(self):
#         """ delete_book_view : login(yes), data(chapter_id, note_id), GET"""
#         self.client.login(email="john@invalid.com",
#                           password="some_123_password")
#         self.response = self.client.get(
#             reverse("studies:delete_book", kwargs={'book': self.book_1.id}))
#         self.assertEqual(self.response.status_code, 302)


#     def test_start_game_view_200(self):
#         """ start_game_view : login(yes), data(), GET"""
#         self.client.login(email="john@invalid.com",
#                           password="some_123_password")
#         self.response = self.client.get(reverse("studies:game_auto"))
#         self.assertEqual(self.response.status_code, 200)
#         self.assertTemplateUsed(self.response, "studies/auto_game.html")
#         self.assertEqual(
#             self.response.context["game_list_auto"], [{'id': 1, 'sens': 'recto', 'text': 'good morning', 'response': 'bonjour'}]
#         )

#     def test_start_game_view_302(self):
#         """ start_game_view : login(no), data(), GET"""
#         self.response = self.client.get(reverse("studies:game_auto"))
#         self.assertEqual(self.response.status_code, 302)


# class ViewDatabase(TestCase):
#     def setUp(self):
#         self.TIME_NOW = datetime.date.today()
#         user_a = User(username="john", email="john@invalid.com")
#         user_a_pw = "some_123_password"
#         self.user_a_pw = user_a_pw
#         user_a.is_staff = True
#         user_a.is_teacher = False
#         user_a.is_superuser = False
#         user_a.set_password(user_a_pw)
#         user_a.save()
#         self.user_a = user_a

#         user_b = User(username="lee", email="lee@invalid.com")
#         user_b_pw = "some_123_password"
#         self.user_b_pw = user_b_pw
#         user_b.is_staff = True
#         user_b.is_teacher = True
#         user_b.is_superuser = False
#         user_b.set_password(user_b_pw)
#         user_b.save()
#         self.user_b = user_b

#         self.book_1 = Book.objects.create(
#             name="English", description="book to learn english", source_info="Author 1",)
#         self.book_1.users.add(self.user_a, through_defaults={"order_book":1})

#         self.chapter_1 = Chapter.objects.create(
#             name="vocabulary 1", order_chapter=1, book=self.book_1)

#         self.note_1 = StudiesNotes.objects.create(
#             text_recto="good morning", text_verso="bonjour", chapter=self.chapter_1, order_note=1, studie_verso=True)

#         self.note_1.users.add(self.user_a, through_defaults={
#             'lvl_recto': 2, "lvl_verso": 2})

#         self.book_2 = Book.objects.create(
#             name="English", description="book to learn english", source_info="Author 1",)
#         self.book_2.users.add(self.user_a, through_defaults={"order_book":1})

#         self.chapter_2 = Chapter.objects.create(
#             name="vocabulary 2", order_chapter=1, book=self.book_2)

#         self.note_2 = StudiesNotes.objects.create(
#             text_recto="good morning", text_verso="bonjour", chapter=self.chapter_2, order_note=1, studie_verso=True)

#         self.note_2.users.add(self.user_a, through_defaults={
#             'lvl_recto': 2, "lvl_verso": 2})


#

#     def test_delete_note(self):
#         """ delete_note_view : login(yes), data(note_id), GET"""
#         self.client.login(email="john@invalid.com",
#                           password="some_123_password")
#         self.response = self.client.get(
#             reverse("studies:delete_note", kwargs={'note': self.note_1.id}))

#         self.assertEqual(self.response.status_code, 302)
#         note_a = StudiesNotes.objects.filter(users=self.user_a).count()
#         self.assertEqual(note_a, 1)

#     def test_start_game_view_200_POST_1(self):
#         """ start_game_view : login(yes), data(), POST"""
#         self.client.login(email="john@invalid.com",
#                           password="some_123_password")

#         data = {"note_id": self.note_1.id, "note_sens": "verso", "win": "true"}
#         response = self.client.post(
#             reverse("studies:game_auto"), data, follow=True
#         )
#         status_code = response.status_code
#         self.assertEqual(status_code, 200)
#         note_a = StudiesNotesProgression.objects.get(
#             user=self.user_a, notes=1)
#         self.assertEqual(note_a.lvl_verso, 3)
#         self.assertEqual(note_a.next_studied_date_verso,
#                          self.TIME_NOW + timedelta(days=1))

#     def test_start_game_view_200_POST_2(self):
#         """ start_game_view : login(yes), data(), POST"""
#         self.client.login(email="john@invalid.com",
#                           password="some_123_password")

#         data = {"note_id": self.note_1.id, "note_sens": "recto", "win": "false"}
#         response = self.client.post(
#             reverse("studies:game_auto"), data, follow=True
#         )
#         status_code = response.status_code
#         self.assertEqual(status_code, 200)
#         note_a = StudiesNotesProgression.objects.get(
#             user=self.user_a, notes=1)
#         self.assertEqual(note_a.lvl_recto, 1)
#         self.assertEqual(note_a.next_studied_date_recto,
#                          self.TIME_NOW + timedelta(days=1))

#     def test_subscribe_book_view(self):
#         self.client.login(email="lee@invalid.com",
#                           password="some_123_password")
#         book_before = Book.objects.filter(users=self.user_b).count()
#         self.assertEqual(book_before, 0)
#         chapter_before = Chapter.objects.filter(book__users=self.user_b).count()
#         self.assertEqual(chapter_before, 0)
#         note_progression_before = StudiesNotesProgression.objects.filter(user=self.user_b).count()
#         self.assertEqual(note_progression_before, 0)

#         data = {"new_student": "lee"}
#         self.response = self.client.post(
#             reverse("studies:add_new_student", kwargs={'book': self.book_1.id}), data, follow=True
#         )
#         self.response = self.client.get(
#             reverse("studies:subscribe_book", kwargs={'book': self.book_1.id}))
#         book_after = Book.objects.filter(users=self.user_b).count()
#         self.assertEqual(book_after, 1)
#         chapter_after = Chapter.objects.filter(book__users=self.user_b).count()
#         self.assertEqual(chapter_after, 1)
#         note_progression_after = StudiesNotesProgression.objects.filter(user=self.user_b).count()
#         self.assertEqual(note_progression_after, 1)

#         self.response = self.client.get(
#             reverse("studies:unsubscribe_book", kwargs={'book': 1}))
#         book_end = Book.objects.filter(users=self.user_b).count()
#         self.assertEqual(book_end, 0)
#         chapter_end = Chapter.objects.filter(book__users=self.user_b).count()
#         self.assertEqual(chapter_end, 0)
#         note_progression_end = StudiesNotesProgression.objects.filter(user=self.user_b).count()
#         self.assertEqual(note_progression_end, 0)


#
