# Generated by Django 4.1.2 on 2022-11-14 21:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lobbying', '0021_alter_campaign_options_campaign_is_public_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='campaign',
            options={'ordering': ['-priority', 'name']},
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='is_complete',
        ),
    ]