# Generated by Django 3.2.18 on 2023-04-05 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fan_database', '0010_auto_20230405_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]