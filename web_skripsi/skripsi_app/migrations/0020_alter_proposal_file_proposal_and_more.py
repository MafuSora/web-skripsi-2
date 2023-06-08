# Generated by Django 4.1.4 on 2023-05-24 20:00

import django.core.validators
from django.db import migrations, models
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('skripsi_app', '0019_alter_dosen_nip_alter_mahasiswa_nim'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='file_proposal',
            field=models.FileField(storage=gdstorage.storage.GoogleDriveStorage(), upload_to='proposal_mahasiswa/', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
        migrations.AlterField(
            model_name='usulantopik',
            name='file_topik',
            field=models.FileField(storage=gdstorage.storage.GoogleDriveStorage(), upload_to='topik_mahasiswa/', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
    ]