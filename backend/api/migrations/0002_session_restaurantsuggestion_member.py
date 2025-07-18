# Generated by Django 5.2 on 2025-07-07 23:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join_code', models.CharField(blank=True, max_length=6, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('stage', models.CharField(choices=[('0', 'Suggesting'), ('1', 'Banning'), ('2', 'Voting'), ('3', 'Results')], max_length=1)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'session',
                'verbose_name_plural': 'sessions',
            },
        ),
        migrations.CreateModel(
            name='RestaurantSuggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_banned', models.BooleanField(default=False)),
                ('picks', models.IntegerField(default=0)),
                ('votes', models.IntegerField(default=0)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session', to='api.session')),
            ],
            options={
                'verbose_name': 'restaurant',
                'verbose_name_plural': 'restaurants',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.session')),
            ],
        ),
    ]
