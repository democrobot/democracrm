# Generated by Django 4.1.2 on 2022-11-15 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobbying', '0023_organization_alter_campaign_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='relationship',
            field=models.CharField(blank=True, choices=[('ally', 'Ally'), ('opponent', 'Opponent'), ('unknown', 'Unknown')], max_length=255, null=True),
        ),
    ]
