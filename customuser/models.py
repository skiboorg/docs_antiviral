from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from shop.models import PromoCode


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    first_name = None
    last_name = None
    email = models.EmailField('Эл. почта', unique=True)
    is_vip = models.BooleanField('Вип?', default=False)
    fio = models.CharField('ФИО', max_length=50, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True)
    comment = models.TextField('Комментарий', blank=True, null=True)
    is_allow_email = models.BooleanField('Согласен на рассылку', default=True)
    size = models.CharField('Размер', max_length=50, blank=True, null=True)
    height = models.CharField('Рост', max_length=50, blank=True, null=True)
    profile_ok = models.BooleanField(default=False)
    birthday = models.DateField('Д/Р',blank=True, null=True)
    promo_code = models.ForeignKey(PromoCode, blank=True, null=True, on_delete=models.SET_NULL,
                                   verbose_name='Промо код')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class Guest(models.Model):
    session = models.CharField('Ключ сессии', max_length=255, blank=True, null=True)
    email = models.EmailField('Эл. почта', blank=True, null=True)
    fio = models.CharField('ФИО', max_length=50, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True)
    promo_code = models.ForeignKey(PromoCode, blank=True, null=True, on_delete=models.SET_NULL,
                                   verbose_name='Промо код')

    def __str__(self):
        return 'Гостевой аккаунт. EMAIL : %s' % self.email

