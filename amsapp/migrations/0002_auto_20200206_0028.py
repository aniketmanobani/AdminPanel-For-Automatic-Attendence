# Generated by Django 2.2.5 on 2020-02-05 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amsapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extendedusers',
            name='fname',
        ),
        migrations.RemoveField(
            model_name='extendedusers',
            name='lname',
        ),
        migrations.RemoveField(
            model_name='extendedusers',
            name='registration_date',
        ),
    ]
