# Generated by Django 4.1.2 on 2022-11-23 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobbying', '0015_alter_supportlevel_campaign_support_and_more'),
        ('organizing', '0011_alter_person_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='targets',
            field=models.ManyToManyField(to='lobbying.publicoffice'),
        ),
    ]
