from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from students.models import Institution


# ==========================
# ✅ Custom User Manager
# ==========================
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


# ==========================
# ✅ User Model
# ==========================
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    status = models.BooleanField(default=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) 
    status = models.BooleanField(default=True)

    roles = models.ManyToManyField('Role', related_name='users', blank=True)
    institution = models.ForeignKey(
        Institution, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='staff_members' 
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username


# ==========================
# ✅ Role Model
# ==========================
class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


# ==========================
# ✅ Token Blacklist Model
# ==========================
class TokenBlackList(models.Model):
    token = models.CharField(max_length=512, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Blacklisted Token {self.id}"
