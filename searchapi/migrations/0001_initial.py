# Generated by Django 2.0.7 on 2018-07-06 03:09

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('uid', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('thumbnail', models.URLField()),
                ('fullname', models.CharField(max_length=60, null=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('location', models.CharField(max_length=80, null=True)),
                ('created', models.DateTimeField()),
                ('followers', models.PositiveIntegerField()),
                ('languages', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50), size=None)),
            ],
        ),
    ]
