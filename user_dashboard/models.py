from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.core.serializers.json import DjangoJSONEncoder
import json

class JSONField(models.TextField):
    def to_dict(self, value):
        return json.loads(value)

    def to_json(self, value):
        return json.dumps(value)

    def to_python(self, value):
        if value == "":
            return None
        try:
            if isinstance(value, str):
                return self.to_dict(value)
        except ValueError:
            pass
        return value

    def from_db_value(self, value, *args):
        return self.to_python(value)

    def get_db_prep_save(self, value, *args, **kwargs):
        if value == "":
            return None
        if isinstance(value, dict):
            value = json.dumps(value, cls=DjangoJSONEncoder)
        return value

#Models for all the API's in the database
class Api(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, default='icon')
    slug = models.SlugField(null=False, unique=True, default=title)
    docs_url = models.CharField(max_length=255,default='')
    # stats = models.CharField(max_length=255, default='3req/hr')
    get_settings = models.URLField(blank=True)
    post_settings = models.URLField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    #is_active = models.BooleanField("api_status", default=False)
    #project = models.ManyToManyField(Project, related_name='project_api', blank=True)
    #project = models.ForeignKey(Project, related_name='UserApis', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('docs', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
          
# class Configs(models.Model):
#     konfigs = JSONField(null=True, blank=True)
#     konfigd_api = models.ForeignKey(Api, related_name='configurations', on_delete=models.CASCADE)
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now_add=True)  
#     #
#     def __str__(self):
#         return 'configurations'


class Project(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE,)
    token = models.UUIDField(null=True, blank=True)
    api_settings = JSONField(null=True, blank=True)
    project_api = models.ManyToManyField(Api, through='Configs' , related_name='project_api', blank=True)
    last_project = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    def add_api(api, projet):
        if api in projet.project_api.all():
            projet.project_api.remove(api)
            message = "Removed"
            return message
        else:
            projet.project_api.add(api)
            message = "Added"
            return message
    #Keep track of lastProject
    def save(self, *args, **kwargs):
        if self.last_project:
            try:
                temp = Project.objects.get(last_project=True)
                if self != temp:
                    temp.last_project = False
                    temp.save()
            except Project.DoesNotExist:
                pass
        super(Project, self).save(*args, **kwargs)

class Configs(models.Model):
    konfigs = JSONField(null=True, blank=True)
    project = models.ForeignKey(Project,related_name='configurations', on_delete=models.CASCADE)
    konfigd_api = models.ForeignKey(Api, related_name='configurations', on_delete=models.CASCADE)
    is_active = models.BooleanField("api_status", default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return 'configurations'
        