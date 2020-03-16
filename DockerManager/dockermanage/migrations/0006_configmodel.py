# Generated by Django 3.0.3 on 2020-03-16 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dockermanage', '0005_volumesmode'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigModel',
            fields=[
                ('id', models.CharField(max_length=120, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('data', models.CharField(max_length=15000)),
                ('lables', models.CharField(help_text='json type', max_length=15000)),
            ],
            options={
                'verbose_name': 'Config',
                'verbose_name_plural': 'Config',
            },
        ),
    ]
