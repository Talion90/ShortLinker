# Generated by Django 3.2.9 on 2021-11-05 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('long_link', models.URLField(unique=True)),
                ('short_link', models.URLField(unique=True)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='shortlink',
            name='long_link',
        ),
        migrations.DeleteModel(
            name='LongLink',
        ),
        migrations.DeleteModel(
            name='ShortLink',
        ),
    ]
