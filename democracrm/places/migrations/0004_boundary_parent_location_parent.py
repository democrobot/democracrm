# Generated by Django 4.1.2 on 2022-11-27 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0003_remove_boundary_parent_remove_location_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='boundary',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='places.boundary', verbose_name='parent'),
        ),
        migrations.AddField(
            model_name='location',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='places.location', verbose_name='parent'),
        ),
    ]
