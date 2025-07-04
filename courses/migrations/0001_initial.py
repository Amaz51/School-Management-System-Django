# Generated by Django 5.2.2 on 2025-07-02 10:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classes', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('class_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='classes.class')),
            ],
            options={
                'db_table': 'course',
            },
        ),
    ]
