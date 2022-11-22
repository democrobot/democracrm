# Generated by Django 4.1.2 on 2022-11-22 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobbying', '0013_alter_supportlevel_options_publicofficial_party_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicofficial',
            name='is_leadership',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='publicofficial',
            name='leadership_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
