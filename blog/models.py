from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator


class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)


class UserData(AbstractUser):

    username = None
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name
    

class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999)])
    image = models.ImageField(max_length=2097152)  # 2 MB

    def __str__(self):
        return self.title


class AccessTokensBlackList(models.Model):
    user = models.ForeignKey(UserData, on_delete = models.SET_NULL, null = True, blank = False)
    jti = models.CharField(unique = True, max_length=255)
    token = models.TextField()
    expires_at = models.DateTimeField()
    class Meta:
        db_table = "AccessTokensBlacklist"

    def __str__(self):
        return self.token