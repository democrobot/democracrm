# Generated by Django 4.1.4 on 2022-12-15 00:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("lobbying", "0026_voter_municipality_code"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="legislationgroup",
            options={"verbose_name_plural": "Legislation Group"},
        ),
        migrations.RenameField(
            model_name="publicofficialposition",
            old_name="service_end",
            new_name="end_date",
        ),
        migrations.RenameField(
            model_name="publicofficialposition",
            old_name="service_start",
            new_name="start_date",
        ),
    ]
