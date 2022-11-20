# Generated by Django 4.1.2 on 2022-11-18 01:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_socialmediaaccount'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeographicRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='geographicboundary',
            name='level',
            field=models.CharField(choices=[('nation', 'Nation'), ('state', 'State'), ('county', 'County'), ('municipality', 'Municipality')], default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='site',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
