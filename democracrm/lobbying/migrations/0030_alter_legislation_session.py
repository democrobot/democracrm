# Generated by Django 4.1.2 on 2022-11-15 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lobbying', '0029_legislation_body_session_committee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='legislation',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='lobbying.session'),
        ),
    ]
