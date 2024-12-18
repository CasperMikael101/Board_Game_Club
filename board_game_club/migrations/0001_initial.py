# Generated by Django 5.1.3 on 2024-11-14 11:48

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_available', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrowed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('returned_at', models.DateTimeField(blank=True, null=True)),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to=settings.AUTH_USER_MODEL)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='board_game_club.boardgame')),
            ],
        ),
    ]
