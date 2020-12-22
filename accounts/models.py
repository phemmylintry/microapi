from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager
import uuid

class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(_("Username"), unique=True, max_length=255)
    first_name = models.CharField(_('First Name'), max_length=255)
    last_name = models.CharField(_('Last Name'), max_length=255)
    is_staff = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    email = models.EmailField(_('email address'), unique=True)
    image = models.ImageField(blank=True, null=True)
    last_project = models.CharField(_("Just saving the name of the last project"), max_length=255, null=True)
    proj_list = models.ManyToManyField("user_dashboard.Project", related_name='project', blank=True, symmetrical=False)
    date_joined = models.DateTimeField(default=timezone.now)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomUserManager()


    def __str__(self):
        return self.email


    def add_project(project, name):
        name.proj_list.add(project)
        added = True
        return added


    def add_api(api, name):
        name.api_list.add(api)
        added = True
        return added


from django.dispatch import receiver
from allauth.account.signals import user_signed_up, user_logged_in
from user_dashboard.models import Project
from django.db.models import ObjectDoesNotExist

@receiver(user_logged_in)
@receiver(user_signed_up)
def default_project(sender, **kwargs):
    user = kwargs.pop('user')
    try:
        extra_data = user.socialaccount_set.get(provider='google').extra_data
    except ObjectDoesNotExist:
        pass
    name = user.last_project
    print(name)
    if name is None:
        try:
            project = Project.objects.filter(user=user).get(last_project=True)
        except ObjectDoesNotExist:
            project = Project.objects.create(name='Default Project', user = user, token = uuid.uuid4().hex, last_project=True)
            project.save()
        user.save()