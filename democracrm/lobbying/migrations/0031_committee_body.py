# Generated by Django 4.1.2 on 2022-11-15 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lobbying', '0030_legislation_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='committee',
            name='body',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='lobbying.governingbody'),
        ),
    ]