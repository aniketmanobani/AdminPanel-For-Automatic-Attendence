# Generated by Django 2.2.5 on 2020-02-05 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amsapp', '0003_branch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]