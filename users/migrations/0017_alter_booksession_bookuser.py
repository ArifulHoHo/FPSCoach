# Generated by Django 4.2 on 2023-04-12 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booksession',
            name='bookUser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookuser', to='users.profile'),
        ),
    ]