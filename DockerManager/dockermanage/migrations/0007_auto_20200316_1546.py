# Generated by Django 3.0.3 on 2020-03-16 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dockermanage', '0006_configmodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='configmodel',
            old_name='lables',
            new_name='lable',
        ),
    ]
