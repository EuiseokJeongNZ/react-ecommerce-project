# models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra):
        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        extra.setdefault("is_active", True)
        return self.create_user(username, email, password, **extra)

class User(AbstractBaseUser):  # ← PermissionsMixin 제거
    id           = models.AutoField(primary_key=True)
    username     = models.CharField(max_length=150, unique=True)
    email        = models.EmailField(unique=True)
    password     = models.CharField(max_length=255)
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login   = models.DateTimeField(null=True, blank=True)
    date_joined  = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD  = "username"
    REQUIRED_FIELDS = ["email"]

    objects = MyUserManager()

    class Meta:
        db_table = "users"
        managed = False

    def __str__(self):
        return self.username

    # 권한 체크를 아주 단순화(permissions 시스템 안 쓸 것이므로)
    def has_perm(self, perm, obj=None):
        return self.is_superuser or self.is_staff

    def has_module_perms(self, app_label):
        return self.is_superuser or self.is_staff
