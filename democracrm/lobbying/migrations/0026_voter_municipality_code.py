# Generated by Django 4.1.4 on 2022-12-14 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lobbying", "0025_voter_political_party_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="voter",
            name="municipality_code",
            field=models.CharField(default="TMP", max_length=50),
            preserve_default=False,
        ),
    ]
