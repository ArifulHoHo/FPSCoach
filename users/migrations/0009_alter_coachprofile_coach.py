# Generated by Django 4.2 on 2023-04-07 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_coachprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coachprofile',
            name='coach',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]
