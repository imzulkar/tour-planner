# Generated by Django 5.0.3 on 2024-06-06 15:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tour_planner", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="weatherupdate",
            name="avg_temp",
            field=models.FloatField(default=0.0),
        ),
    ]
