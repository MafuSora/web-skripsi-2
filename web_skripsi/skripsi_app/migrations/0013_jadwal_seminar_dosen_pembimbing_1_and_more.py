# Generated by Django 4.1.4 on 2023-05-14 03:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skripsi_app', '0012_remove_jadwal_seminar_dosen_pembimbing_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jadwal_seminar',
            name='dosen_pembimbing_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pembimbing_1', to='skripsi_app.dosen'),
        ),
        migrations.AddField(
            model_name='jadwal_seminar',
            name='dosen_pembimbing_2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pembimbing_2', to='skripsi_app.dosen'),
        ),
        migrations.AddField(
            model_name='jadwal_seminar',
            name='dosen_penguji_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='penguji_1', to='skripsi_app.dosen'),
        ),
        migrations.AddField(
            model_name='jadwal_seminar',
            name='dosen_penguji_2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='penguji_2', to='skripsi_app.dosen'),
        ),
        migrations.AddField(
            model_name='jadwal_seminar',
            name='mahasiswa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mahasiswa', to='skripsi_app.mahasiswa'),
        ),
    ]
