from django.dispatch import receiver
from allauth.account.signals import user_signed_up, user_logged_in
from user_dashboard.models import Project
from django.db.models import ObjectDoesNotExist

@receiver(user_logged_in)
@receiver(user_signed_up)
def default_project(sender, **kwargs):
    user = kwargs.pop('user')
    print(user)
    try:
        extra_data = user.socialaccount_set.get(provider='google').extra_data
    except ObjectDoesNotExist:
        name = user.last_project
        print(name)
        if name:
            project = Project.objects.filter(user=user).get(last_project=True)
        else:
            project = Project.objects.create(name='Default Project', user = user, token = uuid.uuid4().hex, last_project=True)
            project.save()
        user.save()