# Generated by Django 2.2.5 on 2020-01-17 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sip_assembly', '0004_auto_20181118_2151'),
    ]

    operations = [
        migrations.AddField(
            model_name='sip',
            name='origin',
            field=models.CharField(
                choices=[
                    ('aurora',
                     'Aurora'),
                    ('legacy_digital',
                     'Legacy Digital Processing'),
                    ('digitization',
                     'Digitization')],
                default='aurora',
                max_length=20),
        ),
    ]
