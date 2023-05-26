# Generated by Django 4.2 on 2023-04-10 19:27

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_review_coachid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coachprofile',
            name='session_price',
            field=models.IntegerField(default=500),
        ),
        migrations.CreateModel(
            name='BookSession',
            fields=[
                ('session_price', models.IntegerField()),
                ('payment_id', models.CharField(blank=True, max_length=10, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('bookUser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookUser', to='users.profile')),
                ('coachBooked', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]
