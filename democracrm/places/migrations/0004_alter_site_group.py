# Generated by Django 4.1.2 on 2022-12-02 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0003_alter_site_mailing_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='places.sitegroup'),
        ),
    ]
