# Generated by Django 4.1.2 on 2022-11-22 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lobbying', '0012_supportlevel_campaign_support_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='supportlevel',
            options={'verbose_name_plural': 'Support Levels'},
        ),
        migrations.AddField(
            model_name='publicofficial',
            name='party',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='lobbying.politicalparty'),
        ),
        migrations.AlterField(
            model_name='publicofficial',
            name='title',
            field=models.CharField(default='Legislator', max_length=255),
        ),
    ]
