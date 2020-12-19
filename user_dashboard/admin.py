from django.contrib import admin
from .models import Api, Project, Configs

class ApiAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','docs_url')
    prepopulated_fields = {'slug': ('title')}

class ConfigAdmin(admin.ModelAdmin):
    list_display = ('konfigd_api','created_on', 'updated_on')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name','user')

admin.site.register(Api)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Configs, ConfigAdmin)