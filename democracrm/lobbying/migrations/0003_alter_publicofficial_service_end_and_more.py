# Generated by Django 4.1.2 on 2022-12-04 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobbying', '0002_supportlevel_campaign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicofficial',
            name='service_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='publicofficial',
            name='service_start',
            field=models.DateField(blank=True, null=True),
        ),
    ]
