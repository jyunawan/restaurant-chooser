# Generated by Django 5.2 on 2025-07-10 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_session_restaurantsuggestion_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurantsuggestion',
            name='session',
        ),
        migrations.RemoveField(
            model_name='session',
            name='creator',
        ),
        migrations.DeleteModel(
            name='Member',
        ),
        migrations.DeleteModel(
            name='RestaurantSuggestion',
        ),
        migrations.DeleteModel(
            name='Session',
        ),
    ]
