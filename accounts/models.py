from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email, is_active=True, 
            is_superuser=False, date_joined=now
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email, is_active=True, is_staff=True, 
            is_superuser=True, date_joined=now, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('E-mail', null=False, blank=False, unique=True)
     
    is_staff = models.BooleanField('staff status', default=False)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    is_active = models.BooleanField('active', default=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in User._meta.fields]

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        
