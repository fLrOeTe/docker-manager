# Generated by Django 3.0.3 on 2020-03-09 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dockermanage', '0003_ipampoolmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagetmodel',
            name='id',
            field=models.CharField(help_text='the id of the images', max_length=200, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='imagetmodel',
            name='name',
            field=models.CharField(help_text='the images name,is required', max_length=100),
        ),
        migrations.AlterField(
            model_name='imagetmodel',
            name='tag',
            field=models.CharField(help_text='the tag of images', max_length=50),
        ),
        migrations.AlterField(
            model_name='imagetmodel',
            name='time',
            field=models.CharField(help_text='create time', max_length=100),
        ),
    ]
