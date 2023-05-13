# Generated by Django 4.1.4 on 2023-05-13 20:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skripsi_app', '0004_remove_sub_cpmk_id_sub_cpmk'),
    ]

    operations = [
        migrations.AddField(
            model_name='penilaian',
            name='id_sub_cpmk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='skripsi_app.sub_cpmk'),
        ),
        migrations.AddField(
            model_name='sub_cpmk',
            name='id_sub_cpmk',
            field=models.CharField(default=1, max_length=60, validators=[django.core.validators.RegexValidator('^\\S+$', 'Tidak boleh memiliki spasi')]),
            preserve_default=False,
        ),
    ]
