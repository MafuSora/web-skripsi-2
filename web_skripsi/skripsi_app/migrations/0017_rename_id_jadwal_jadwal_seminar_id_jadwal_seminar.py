# Generated by Django 4.1.4 on 2023-05-14 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skripsi_app', '0016_alter_detailpenilaian_id_jadwal_seminar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jadwal_seminar',
            old_name='id_jadwal',
            new_name='id_jadwal_seminar',
        ),
    ]
