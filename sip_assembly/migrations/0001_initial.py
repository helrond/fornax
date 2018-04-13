# Generated by Django 2.0 on 2018-04-13 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RightsStatement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basis', models.CharField(choices=[('Copyright', 'Copyright'), ('Statute', 'Statute'), ('License', 'License'), ('Other', 'Other')], max_length=64)),
                ('status', models.CharField(blank=True, choices=[('copyrighted', 'copyrighted'), ('public domain', 'public domain'), ('unknown', 'unknown')], max_length=64, null=True)),
                ('determination_date', models.DateField(blank=True, null=True)),
                ('jurisdiction', models.CharField(blank=True, max_length=2, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('terms', models.TextField(blank=True, null=True)),
                ('citation', models.TextField(blank=True, null=True)),
                ('note', models.TextField()),
                ('grant_act', models.CharField(choices=[('publish', 'Publish'), ('disseminate', 'Disseminate'), ('replicate', 'Replicate'), ('migrate', 'Migrate'), ('modify', 'Modify'), ('use', 'Use'), ('delete', 'Delete')], max_length=64)),
                ('grant_restriction', models.CharField(choices=[('allow', 'Allow'), ('disallow', 'Disallow'), ('conditional', 'Conditional')], max_length=64)),
                ('grant_start_date', models.DateField(blank=True, null=True)),
                ('grant_end_date', models.DateField(blank=True, null=True)),
                ('rights_granted_note', models.TextField()),
                ('doc_id_role', models.CharField(blank=True, max_length=255, null=True)),
                ('doc_id_type', models.CharField(blank=True, max_length=255, null=True)),
                ('doc_id_value', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SIP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aurora_uri', models.URLField()),
                ('component_uri', models.URLField()),
                ('process_status', models.CharField(choices=[(10, 'New transfer discovered'), (20, 'Rights added'), (30, 'Transfer documentation added'), (40, 'bag-info.txt updated'), (50, 'SIP rebagged'), (90, 'Delivered to Archivematica Transfer Source')], max_length=100)),
                ('machine_file_path', models.CharField(max_length=100)),
                ('machine_file_upload_time', models.DateTimeField()),
                ('machine_file_identifier', models.CharField(max_length=255, unique=True)),
                ('created_time', models.DateTimeField(auto_now=True)),
                ('modified_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='rightsstatement',
            name='sip',
            field=models.ForeignKey(on_delete='CASCADE', to='sip_assembly.SIP'),
        ),
    ]
