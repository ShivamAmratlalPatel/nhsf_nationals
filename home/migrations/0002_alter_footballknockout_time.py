# Generated by Django 4.1.4 on 2023-02-20 00:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="footballknockout",
            name="time",
            field=models.TimeField(null=True),
        ),
    ]
