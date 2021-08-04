from django.db import models
from django.conf import settings
from django.db.models.expressions import F
from django.utils import timezone


class Book(models.Model):
    name = models.CharField(max_length=255, null=False)
    order_book = models.PositiveSmallIntegerField(default=1)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="UserBookMany", related_name="books"
    )
    description = models.TextField(max_length=1000, null=True, blank=True)
    source_info = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.id}-{self.name}"

    class Meta:
        ordering = ["order_book"]
        indexes = [
            models.Index(fields=["order_book"]),
        ]


class UserBookMany(models.Model):
    FONCTION = (
        ("owner", "owner"),
        ("student", "student"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=False, blank=False)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, null=False, blank=False)
    user_fonction = models.CharField(
        max_length=255, null=False, default="owner", choices=FONCTION
    )
    # level to make a progressive access to chapter

    def __str__(self):
        return f"{self.user} - {self.book} - {self.user_fonction}"

    class Meta:
        unique_together = [
            ["user", "book"],
        ]
        indexes = [
            models.Index(
                fields=["user", "book"],
            ),
        ]


class Chapter(models.Model):
    name = models.CharField(max_length=255, null=False)
    order_chapter = models.PositiveSmallIntegerField(default=1)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}-{self.name}"

    class Meta:
        ordering = ["book", "order_chapter"]
        indexes = [
            models.Index(fields=["book", "order_chapter"]),
        ]


class StudiesNotes(models.Model):

    # data and order
    order_note = models.PositiveSmallIntegerField(default=1)
    text_recto = models.TextField(max_length=1000, null=False)
    text_verso = models.TextField(max_length=1000, null=False)

    # to studie
    studie_recto = models.BooleanField(default=True)
    studie_verso = models.BooleanField(default=False)

    # refer to
    created_at = models.DateField(auto_now_add=True, null=True)
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, null=False, blank=False
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="StudiesNotesProgression",
        related_name="notes",
    )

    def __str__(self):
        return "note" + str(self.id)

    class Meta:
        verbose_name = "Note"  # in_page singular
        verbose_name_plural = "Notes to studies"  # main page plural
        ordering = ["order_note", "created_at"]
        indexes = [
            models.Index(fields=["chapter", "order_note"]),
        ]


class StudiesNotesProgression(models.Model):
    LVL = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "6"),
        (7, "7"),
        (8, "8"),
        (9, "9"),
        (10, "10"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    notes = models.ForeignKey(StudiesNotes, on_delete=models.CASCADE)

    # lvl
    lvl_recto = models.PositiveSmallIntegerField(
        default=1, choices=LVL, null=False)
    lvl_verso = models.PositiveSmallIntegerField(
        default=1, choices=LVL, null=False)

    # time

    last_studied_date_recto = models.DateField(null=True, blank=True)
    last_studied_date_verso = models.DateField(null=True, blank=True)

    next_studied_date_recto = models.DateField(
        null=True, blank=True, default=timezone.now
    )
    next_studied_date_verso = models.DateField(
        null=True, blank=True, default=timezone.now
    )
    # others
    flaged = models.BooleanField(default=False, null=False)


class GlobalDailyAnalysis(models.Model):
    # 10 jours
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False
    )
    date = models.DateField(auto_now_add=True, null=False)
    number_of_studies = models.PositiveIntegerField(default=0, null=False)
    number_of_win = models.PositiveIntegerField(default=0, null=False)
    number_of_lose = models.PositiveIntegerField(default=0, null=False)
    all_studied_1_time = models.PositiveIntegerField(default=0, null=False)

    def __str__(self):
        return self.user

    class Meta:
        ordering = ["user", "date"]
        indexes = [
            models.Index(fields=["user", "date"]),
        ]


class GlobalMonthlyAnalysis(models.Model):
    # 12 mois
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False
    )
    date = models.DateField(auto_now_add=True, null=False)
    number_of_studies = models.PositiveIntegerField(default=0)
    number_of_win = models.PositiveIntegerField(default=0)
    number_of_lose = models.PositiveIntegerField(default=0)
    all_studied_1_time = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user

    class Meta:
        ordering = ["user", "date"]
        indexes = [
            models.Index(fields=["user", "date"]),
        ]


class Settings(models.Model):
    LVL = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False
    )
    daily_target = models.PositiveSmallIntegerField(default=50, null=False)
    default_lvl = models.PositiveSmallIntegerField(
        default=1, choices=LVL, null=False)

    def __str__(self):
        return self.user

    class Meta:
        ordering = ["user"]
