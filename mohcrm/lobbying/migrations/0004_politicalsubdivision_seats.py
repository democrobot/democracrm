# Generated by Django 4.0.6 on 2022-10-08 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobbying', '0003_publicofficial_subdivision'),
    ]

    operations = [
        migrations.AddField(
            model_name='politicalsubdivision',
            name='seats',
            field=models.IntegerField(default=1),
        ),
    ]
