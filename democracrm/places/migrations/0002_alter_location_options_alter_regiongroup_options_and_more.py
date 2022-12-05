# Generated by Django 4.1.2 on 2022-12-02 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name_plural': True},
        ),
        migrations.AlterModelOptions(
            name='regiongroup',
            options={'verbose_name_plural': 'Region Groups'},
        ),
        migrations.AlterModelOptions(
            name='site',
            options={'verbose_name_plural': 'Sites'},
        ),
        migrations.AlterModelOptions(
            name='sitegroup',
            options={'verbose_name_plural': True},
        ),
        migrations.AddField(
            model_name='site',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='sitegroup',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
