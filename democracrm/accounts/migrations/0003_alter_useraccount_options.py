# Generated by Django 4.1.2 on 2022-11-26 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_organizationaccount_primary_contact_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useraccount',
            options={'verbose_name_plural': 'User Accounts'},
        ),
    ]