# Generated by Django 4.2 on 2023-04-07 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_coachprofile_coach'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='session_price',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='vote_ratio',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='vote_total',
        ),
    ]