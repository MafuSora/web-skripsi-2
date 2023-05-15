# Generated by Django 4.1.4 on 2023-05-14 01:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skripsi_app', '0006_mahasiswa_angkatan'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sub_cpmk',
            old_name='id_jadwal_semester',
            new_name='id_nama_semester',
        ),
        migrations.RenameField(
            model_name='sub_cpmk',
            old_name='tahun',
            new_name='tahun_angkatan',
        ),
        migrations.AddField(
            model_name='cpmk',
            name='id_nama_semester',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='skripsi_app.jadwal_semester'),
        ),
        migrations.AddField(
            model_name='cpmk',
            name='keterangan_sub_cpmk',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='cpmk',
            name='tahun_angkatan',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
