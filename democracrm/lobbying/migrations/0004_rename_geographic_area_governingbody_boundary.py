# Generated by Django 4.1.2 on 2022-11-18 01:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lobbying', '0003_alter_publicofficial_office'),
    ]

    operations = [
        migrations.RenameField(
            model_name='governingbody',
            old_name='geographic_area',
            new_name='boundary',
        ),
    ]
