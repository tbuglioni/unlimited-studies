from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):  # comportement en creant un user
    def create_user(
        self, email, username, password=None
    ):  # il faut ajouter les champs de USERNAME_FIELD et REQUIRED_FIELD ici

        if not email:
            raise ValueError("user must have an email address")
        if not username:
            raise ValueError("user must have an username")

        # creer l'utilisateur:
        user = self.model(
            email=self.normalize_email(email),  # convertie les caracteres en minuscule
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_teacher = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# ajouter dans setting le lien vers ce nouveau model user
# AUTH_USER_MODEL = 'account.Account'


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    # required any time:
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    # not required (exemple):
    # first_name = models.CharField(max_length=30, blank=True, null=True)

    USERNAME_FIELD = "email"  # champ de "login"
    REQUIRED_FIELDS = [
        "username",
    ]  # champ obligatoire

    objects = MyAccountManager()  # indiquer ou est le manager

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
