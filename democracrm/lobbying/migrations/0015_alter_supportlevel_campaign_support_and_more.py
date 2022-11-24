# Generated by Django 4.1.2 on 2022-11-23 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobbying', '0014_publicofficial_is_leadership_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportlevel',
            name='campaign_support',
            field=models.CharField(choices=[('Strongly Supports', 'Strongly Supports'), ('Supports', 'Supports'), ('Undecided On', 'Undecided On'), ('Opposes', 'Opposes'), ('Strongly Opposes', 'Strongly Opposes')], max_length=255),
        ),
        migrations.AlterField(
            model_name='supportlevel',
            name='legislation_support',
            field=models.CharField(choices=[('Strongly Supports', 'Strongly Supports'), ('Supports', 'Supports'), ('Undecided On', 'Undecided On'), ('Opposes', 'Opposes'), ('Strongly Opposes', 'Strongly Opposes')], max_length=255),
        ),
    ]
