# Generated by Django 3.2.18 on 2023-04-11 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-pinned', '-updated', '-created']},
        ),
        migrations.AddField(
            model_name='post',
            name='pinned',
            field=models.BooleanField(default=False),
        ),
    ]
