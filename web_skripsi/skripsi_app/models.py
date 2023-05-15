# from tokenize import blank_re
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from gdstorage.storage import GoogleDriveStorage
from django.core.validators import RegexValidator

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()
# Create your models here.

class jadwal_semester(models.Model):
    id_jadwal_semester = models.BigAutoField(primary_key=True)
    nama_semester = models.CharField(max_length=100,null=True)
    tanggal_awal_semester = models.DateField(default=now,null=True)
    tanggal_akhir_semester = models.DateField(default=now,null=True)

    def __str__(self):
        return str(self.nama_semester)
    
    


class mahasiswa(models.Model):
    nim = models.BigIntegerField(primary_key=True)
    semester_daftar_skripsi = models.ForeignKey(
        jadwal_semester, null=True, on_delete= models.SET_NULL)
    angkatan=models.IntegerField()
    id_user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_file = models.ImageField(upload_to="photo_mhs/", blank=True, storage=gd_storage)

    def __str__(self):
        # return str(self.nim) + "-" + str(User.objects.get(username=self.id_user).first_name)
        return str(self.nim) + "-" + str(self.id_user.first_name)


class dosen(models.Model):
    nip = models.BigIntegerField(primary_key=True)
    id_user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_file = models.ImageField(upload_to="photo_dosen/", blank=True, storage=gd_storage)

    def __str__(self):
        return str(self.id_user.first_name) + "-" + str(self.nip)
    
    
    


class kompartemen(models.Model):
    id_kompartemen = models.BigAutoField(primary_key=True)
    nama_kompartemen = models.CharField(max_length=60)

    def __str__(self):
        return str(self.nama_kompartemen)


class kompartemendosen(models.Model):
    id_dosen_kompartemen = models.BigAutoField(primary_key=True)
    id_kompartemen = models.ForeignKey(
        kompartemen, on_delete=models.CASCADE)
    nip = models.OneToOneField(dosen, on_delete=models.CASCADE, max_length=200)

    def __str__(self):
        return str(self.nip) + "-" + str(self.id_kompartemen)


class usulantopik(models.Model):
    id_usulan_topik = models.BigAutoField(primary_key=True)
    nim = models.ForeignKey(mahasiswa, on_delete=models.CASCADE)
    permintaan_dosen_1 = models.ForeignKey(dosen, on_delete=models.DO_NOTHING)
    permintaan_dosen_2 = models.CharField(max_length=100,null=True)
    judul_topik = models.CharField(max_length=60)
    file_topik = models.FileField(upload_to="topik_mahasiswa/", storage=gd_storage)
    keterangan = models.TextField(blank=True)
    tanggal_buat = models.DateTimeField(auto_now_add=True)
    tanggal_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nim) + "-" + str(self.judul_topik)




class evaluasitopik(models.Model):
    ACC = 'ACC'
    REVISI = 'Revisi'
    SUBMIT = 'Submit'
    DALAM_EVALUASI = 'Dalam Evaluasi'
    status_choices = [
        (ACC, 'ACC'),
        (REVISI, 'Revisi'),
        (SUBMIT, 'Submit'),
        (DALAM_EVALUASI, 'Dalam Evaluasi'),
    ]
    id_evaluasi_topik = models.BigAutoField(primary_key=True)
    id_dosen_kompartemen = models.ForeignKey(
        kompartemendosen, on_delete=models.CASCADE)
    id_usulan_topik = models.ForeignKey(usulantopik, on_delete=models.CASCADE)
    # choices
    status_topik = models.CharField(
        choices=status_choices, max_length=60, default=SUBMIT)
    catatan = models.TextField(blank=True)
    tanggal_buat = models.DateTimeField(auto_now_add=True)
    tanggal_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id_usulan_topik) + "-" + str(self.status_topik)


class roledosen(models.Model):
    P1 = 'Pembimbing 1'
    P2 = 'Pembimbing 2'
    US1 = 'Penguji Seminar Proposal 1'
    US2 = 'Penguji Seminar Proposal 2'
    UH1 = 'Penguji Seminar Hasil 1'
    UH2 = 'Penguji Seminar Hasil 2'
    role_dosen_choices = [
        (P1, 'Pembimbing 1'),
        (P2, 'Pembimbing 2'),
        (US1, 'Penguji Seminar Proposal 1'),
        (US2, 'Penguji Seminar Proposal 2'),
        (UH1, 'Penguji Seminar Hasil 1'),
        (UH2, 'Penguji Seminar Hasil 2'),
    ]
    status_choices = [
        ("Active", "Active"),
        ("Finished", "Finished"),
    ]
    id_role_dosen = models.BigAutoField(
        primary_key=True)
    nip = models.ForeignKey(dosen, on_delete=models.CASCADE)
    nim = models.ForeignKey(mahasiswa, on_delete=models.CASCADE)
    role = models.CharField(choices=role_dosen_choices, max_length=200)
    status = models.CharField(choices=status_choices,
                              max_length=200, blank=True)
    tanggal_buat = models.DateTimeField(auto_now_add=True)
    tanggal_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nip) + "-" + str(self.nim) + "-" + str(self.role)

class jadwal_seminar(models.Model):
    tahapan_choices = [
        ("Seminar Proposal", 'Seminar Proposal'),
        ("Seminar Hasil", 'Seminar Hasil'),
        ]
    ruangan_seminar_choices = [
        ("Ruang Seminar A", 'Ruang Seminar A'),
        ("Ruang Seminar B", 'Ruang Seminar B'),
        ("Ruang Meeting A", 'Ruang Meeting A'),
        ]
    id_jadwal_seminar = models.BigAutoField(primary_key=True)
    # mahasiswa = models.CharField(max_length=100,null=True)
    # dosen_pembimbing_1 = models.CharField(max_length=100,null=True)
    # dosen_pembimbing_2 = models.CharField(max_length=100,null=True)
    # dosen_penguji_1 = models.CharField(max_length=60,null=True)
    # dosen_penguji_2 = models.CharField(max_length=60,null=True)
    mahasiswa = models.ForeignKey(mahasiswa, on_delete=models.CASCADE, related_name='mahasiswa')
    dosen_pembimbing_1 = models.ForeignKey(roledosen, on_delete=models.CASCADE, related_name='pembimbing_1')
    dosen_pembimbing_2 = models.ForeignKey(roledosen, null=True, on_delete=models.SET_NULL, related_name='pembimbing_2')
    dosen_penguji_1 = models.ForeignKey(roledosen, on_delete=models.CASCADE, related_name='penguji_1')
    dosen_penguji_2 = models.ForeignKey(roledosen, on_delete=models.CASCADE, related_name='penguji_2')
    tahap_seminar=models.CharField(choices=tahapan_choices, max_length=60,null=True)
    ruang_seminar=models.CharField(choices=ruangan_seminar_choices, max_length=60,null=True)
    tanggal_seminar = models.DateField(default=now,null=True)
    waktu_seminar = models.TimeField(default=now,null=True)
    tanggal_buat = models.DateTimeField(auto_now_add=True)
    tanggal_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.tanggal_seminar) + "-" + str(self.mahasiswa)+ "-" + str(self.tahap_seminar)



class detailpenilaian(models.Model):
    tahapan_choices = [
        ("Bimbingan", 'Bimbingan'),
        ("Seminar Proposal", 'Seminar Proposal'),
        ("Seminar Hasil", 'Seminar Hasil'),
        ]
    status_kelulusan_choices=[
        ("Lulus", 'Lulus'),
        ("Tidak Lulus", 'Tidak Lulus'),
        ]
    id_detail_penilaian = models.BigAutoField(primary_key=True)
    id_jadwal_seminar=models.ForeignKey(
        jadwal_seminar,null=True, on_delete=models.CASCADE)
    nama_tahap = models.CharField(choices=tahapan_choices, max_length=60)
    id_role_dosen = models.ForeignKey(
        roledosen, on_delete=models.CASCADE)

    hasil_review = models.TextField(blank=True)
    status_kelulusan = models.CharField(choices=status_kelulusan_choices, max_length=60)
    tanggal_buat = models.DateTimeField(auto_now_add=True)
    tanggal_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id_role_dosen) + "-" + str(self.status_kelulusan)+ "-" + str(self.hasil_review)


class proposal(models.Model):
    proposal_awal = 'Proposal Awal'
    proposal_awal_revisi = 'Proposal Awal (Revisi Seminar Proposal)'
    laporan_akhir = 'Laporan Akhir'
    laporan_akhir_revisi = 'Laporan Akhir (Revisi Seminar Hasil)'
    status_choices = [
        (proposal_awal, 'Proposal Awal (BAB 1 - BAB 3)'),
        (proposal_awal_revisi, 'Proposal Awal (BAB 1 - BAB 3) Revisi Seminar Proposal'),
        (laporan_akhir, 'Laporan Akhir (BAB 1 - BAB 5)'),
        (laporan_akhir_revisi, 'Laporan Akhir (BAB 1 - BAB 5) Revisi Seminar Hasil'),  
    ]
    id_proposal = models.BigAutoField(primary_key=True)
    nim = models.ForeignKey(mahasiswa, on_delete=models.CASCADE)
    nama_tahap = models.CharField(choices=status_choices, max_length=60)
    judul_proposal = models.CharField(max_length=60)
    file_proposal = models.FileField(
        upload_to="proposal_mahasiswa/", storage=gd_storage)
    keterangan = models.TextField(blank=True)
    tanggal_buat = models.DateTimeField(auto_now_add=True)
    tanggal_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nim) + "-" + str(self.judul_proposal)


class bimbingan(models.Model):
    ACC = 'ACC'
    REVISI = 'Revisi'
    SUBMIT = 'Submit'
    DALAM_EVALUASI = 'Dalam Evaluasi'
    status_choices = [
        (ACC, 'ACC'),
        (REVISI, 'Revisi'),
        (SUBMIT, 'Submit'),
        (DALAM_EVALUASI, 'Dalam Evaluasi'),
    ]
    id_bimbingan = models.BigAutoField(primary_key=True)
    id_proposal = models.ForeignKey(
        proposal, on_delete=models.CASCADE)
    id_role_dosen = models.ForeignKey(
        roledosen, on_delete=models.CASCADE)
    status_bimbingan = models.CharField(
        choices=status_choices, max_length=60, default=SUBMIT)
    # file_proposal = models.FileField(
    #     upload_to="proposal_mahasiswa/", storage=gd_storage)
    catatan = models.TextField(blank=True)
    tanggal_buat = models.DateTimeField(auto_now_add=True)
    tanggal_update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id_proposal) + "-" + str(self.id_role_dosen) + "-" + str(self.status_bimbingan)


class cpmk(models.Model):
    id_tabel_cpmk = models.BigAutoField(primary_key=True)
    id_cpmk = models.CharField(max_length=60,validators=[RegexValidator(r'^\S+$', 'Tidak boleh memiliki spasi')])
    id_nama_semester=models.ForeignKey(
        jadwal_semester, null=True, on_delete= models.SET_NULL)
    tahun_angkatan=models.IntegerField()
    keterangan_sub_cpmk = models.TextField(blank=True)
    # id_cpmk = models.CharField(primary_key=True,max_length=60)
    keterangan_cpmk = models.TextField(blank=True)
    
    def __str__(self):
        return  str(self.id_cpmk) + "-" + str(self.tahun_angkatan) + "-" + str(self.id_nama_semester) + "-" + str(self.keterangan_cpmk) 
        # return str(self.id_cpmk) + "-" + str(self.keterangan_cpmk) 
    
class sub_cpmk(models.Model):
    id_tabel_sub_cpmk = models.BigAutoField(primary_key=True)
    id_sub_cpmk = models.CharField(max_length=60,validators=[RegexValidator(r'^\S+$', 'Tidak boleh memiliki spasi')])
    id_nama_semester=models.ForeignKey(
        jadwal_semester, null=True, on_delete= models.SET_NULL)
    tahun_angkatan=models.IntegerField()
    keterangan_sub_cpmk = models.TextField(blank=True)
    id_cpmk = models.ForeignKey(
        cpmk, on_delete=models.CASCADE)
    bobot_persen_sempro = models.CharField(max_length=60,blank=True)
    bobot_sempro = models.FloatField(blank=True,default=0)
    bobot_persen_semhas = models.CharField(max_length=60,blank=True)
    bobot_semhas = models.FloatField(blank=True,default=0)
    bobot_persen_pembimbing = models.CharField(max_length=60,blank=True)
    bobot_pembimbing = models.FloatField(blank=True,default=0)
    
    def __str__(self):
        # return  str(self.keterangan_sub_cpmk) 
        return str(self.id_sub_cpmk) + "-" + str(self.tahun_angkatan) + "-" + str(self.id_nama_semester) + "-" + str(self.keterangan_sub_cpmk)  
        # return str(self.id_sub_cpmk) + "-" + str(self.keterangan_sub_cpmk) 


    
    
class penilaian(models.Model):
    id_penilaian = models.BigAutoField(primary_key=True)
    id_detail_penilaian = models.ForeignKey(
        detailpenilaian, null=True, on_delete= models.CASCADE)
    id_sub_cpmk = models.ForeignKey(sub_cpmk,on_delete= models.CASCADE,null=True)
    nilai = models.IntegerField(blank=True,null=True)
    tanggal_buat = models.DateTimeField(auto_now_add=True)
    tanggal_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id_penilaian) + "-"+str(self.id_sub_cpmk.id_sub_cpmk)+ "-" + str(self.nilai)
    # + str(self.id_sub_cpmk.id_sub_cpmk)+ "-" 




class notifikasi(models.Model):
    id_notifikasi = models.BigAutoField(primary_key=True)
    nip= models.CharField(max_length=100,null=True)
    nim= models.CharField(max_length=100,null=True)
    messages=models.TextField()
    status=models.BooleanField(default=False)
    tanggal_buat = models.DateTimeField(auto_now_add=True)
    tanggal_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.messages) + "-" + str(self.status)

