# Generated by Django 4.0.6 on 2022-10-08 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobbying', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PoliticalSubdivision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='publicofficial',
            name='is_elected',
            field=models.BooleanField(default=True),
        ),
    ]
