# Generated by Django 4.1.2 on 2022-11-19 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_organization_slug_alter_organization_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
