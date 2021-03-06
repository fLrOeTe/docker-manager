# Generated by Django 2.2.10 on 2020-03-05 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dockermanage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=64, unique=True, verbose_name='主机名')),
                ('ip', models.CharField(blank=True, max_length=30, null=True, verbose_name='ip')),
            ],
            options={
                'verbose_name': 'asset',
                'db_table': 'asset',
                'verbose_name_plural': 'asset',
            },
        ),
        migrations.CreateModel(
            name='ImageTModel',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('tag', models.CharField(max_length=50)),
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('time', models.CharField(max_length=100)),
                ('size', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'ImageT',
                'verbose_name_plural': 'ImageT',
            },
        ),
    ]
