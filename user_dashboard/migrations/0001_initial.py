# Generated by Django 3.1.3 on 2020-11-11 18:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import user_dashboard.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Api',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('icon', models.CharField(default='icon', max_length=255)),
                ('slug', models.SlugField(default=models.CharField(max_length=255), unique=True)),
                ('docs_url', models.CharField(default='', max_length=255)),
                ('get_settings', models.URLField(blank=True)),
                ('post_settings', models.URLField(blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Configs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('konfigs', user_dashboard.models.JSONField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False, verbose_name='api_status')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('konfigd_api', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='configurations', to='user_dashboard.api')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('token', models.UUIDField(blank=True, null=True)),
                ('api_settings', user_dashboard.models.JSONField(blank=True, null=True)),
                ('last_project', models.BooleanField(default=False)),
                ('project_api', models.ManyToManyField(blank=True, related_name='project_api', through='user_dashboard.Configs', to='user_dashboard.Api')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='configs',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='configurations', to='user_dashboard.project'),
        ),
    ]
