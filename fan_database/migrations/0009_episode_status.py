# Generated by Django 3.2.18 on 2023-04-05 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fan_database', '0008_deleterequest_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
    ]
