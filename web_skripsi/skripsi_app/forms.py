# Library Validator
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.validators import validate_email,MaxValueValidator,MinValueValidator,MinLengthValidator,MaxLengthValidator
# library form
from django import forms
# from django.db import models

# User Form
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# Model Reference
from django.contrib.auth.models import User
# , Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import cpmk,jadwal_seminar,penilaian, bimbingan,notifikasi, detailpenilaian, evaluasitopik, proposal,notifikasi, roledosen, usulantopik, dosen, kompartemen, mahasiswa, kompartemendosen,jadwal_semester, sub_cpmk
# from .widget import DatePickerInput, TimePickerInput, DateTimePickerInput

# widget library
from .widget import DatePickerInput, TimePickerInput
# , DateTimePickerInput
# from django.forms.widgets import TimeInput

# Function untuk menampilkan waktu
import time,datetime

# menampilakan tanggal
tanggalan=datetime.datetime.now()
tahun=tanggalan.strftime("%Y")


def file_size(value): # add this to some file where you can import it from
    limit = 10 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File terlalu besar. Ukuran file maksimal 10 MB.')
# User Form
def ubac_email_validator(value):
    if not value.endswith('ub.ac.id'):
        raise ValidationError('Alamat email harus menggunakan domain email ub.ac.id')
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email, ubac_email_validator])
    first_name = forms.CharField(max_length=120, required=True,label='Nama Lengkap')
    class Meta:
        model = User
        fields = ['first_name',  "email", "username",
                  "password1", "password2"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['first_name'].label = 'Nama Lengkap'
        # self.fields['id_user'].label = 'Username'


class NimForm(forms.ModelForm):
    nim=forms.CharField(validators=[RegexValidator(r'^\S+$', 'Tidak boleh ada spasi')])
    angkatan = forms.IntegerField(
        validators=[MinValueValidator(2004),MaxValueValidator(int(tahun))])
    class Meta:
        model = mahasiswa
        fields = ['nim'
        ,"semester_daftar_skripsi","angkatan"
        ]
    


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email, ubac_email_validator])
    first_name = forms.CharField(max_length=120, required=True,label='Nama Lengkap')
    class Meta:
        model = User
        fields = ['first_name', "email", "username",
                  "password1", "password2"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['first_name'].label = 'Nama Lengkap'
        # self.fields['id_user'].label = 'Username'

class UpdateAdminUserForm(UserChangeForm):
    email = forms.EmailField(required=True, validators=[validate_email, ubac_email_validator])
    first_name = forms.CharField(max_length=120, required=True,label='Nama Lengkap')
    class Meta:
        model = User
        fields = ["username", "email", "first_name"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['first_name'].label = 'Nama Lengkap'
        
class UpdateUserForm(UserChangeForm):
    # email = forms.EmailField(required=True, validators=[validate_email, ubac_email_validator])
    # first_name = forms.CharField(max_length=30, required=True,label='Full Name')
    class Meta:
        model = User
        fields = ["username",
                #   , "email",
                "first_name"
                  ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['first_name'].label = 'Nama Lengkap'

class NipForm(forms.ModelForm):
    # photo_file = forms.ImageField()
    nip=forms.CharField(validators=[RegexValidator(r'^\S+$', 'Tidak boleh ada spasi')])
    class Meta:
        
        model = dosen
        fields = ['nip', "photo_file"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nip'].label = 'NIP'




# Form dosen
class UpdateAdminDosenForm(forms.ModelForm):
    nip=forms.CharField(validators=[RegexValidator(r'^\S+$', 'Tidak boleh ada spasi')])
    class Meta:
        model = dosen
        fields = ["nip","id_user","photo_file"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nip'].label = 'NIP'
        self.fields['id_user'].label = 'Username'


class DosenForm(forms.ModelForm):
    nip=forms.CharField(validators=[RegexValidator(r'^\S+$', 'Tidak boleh ada spasi')])
    class Meta:
        model = dosen
        fields = ["nip", "id_user", "photo_file"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nip'].label = 'NIP'
        self.fields['id_user'].label = 'Username'


class UpdateDosenForm(forms.ModelForm):
    class Meta:
        model = dosen
        fields = ["photo_file"]

# kompartemen


class KompartemenForm(forms.ModelForm):
    class Meta:
        model = kompartemen
        fields = ["nama_kompartemen"]

# Mahasiswa


class MahasiswaForm(forms.ModelForm):
    nim=forms.CharField(validators=[RegexValidator(r'^\S+$', 'Tidak boleh ada spasi')]) 
    angkatan = forms.IntegerField(
        validators=[MinValueValidator(2004),MaxValueValidator(int(tahun))])
    class Meta:
        
        model = mahasiswa
        fields = ["nim", "id_user","semester_daftar_skripsi","angkatan", "photo_file"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nim'].label = 'NIM'
        self.fields['id_user'].label = 'Username'


class UpdateAdminMahasiswaForm(forms.ModelForm):
    nim=forms.CharField(validators=[RegexValidator(r'^\S+$', 'Tidak boleh ada spasi')])
    angkatan = forms.IntegerField(
        validators=[MinValueValidator(2004),MaxValueValidator(int(tahun))])
    class Meta:
        model = mahasiswa
        fields = ["nim","id_user","semester_daftar_skripsi","angkatan","photo_file"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nim'].label = 'NIM'
        self.fields['id_user'].label = 'Username'
    
class UpdateMahasiswaForm(forms.ModelForm):
    class Meta:
        model = mahasiswa
        fields = ["photo_file"]

# Dosen kompartemen


class KompartemenDosenForm(forms.ModelForm):
    
    class Meta:
        model = kompartemendosen
        fields = ["nip", "id_kompartemen"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nip'].label = ' Dosen'
        self.fields['id_kompartemen'].label = 'Kompartemen'
    
#  Usulan Topik


class UsulanTopikFormFull(forms.ModelForm):
    data_dosen =dosen.objects.all()[0:]
    # print(data_dosen)
    # Dosen
    ListDosen= [None]
    for fields in data_dosen:
        ListDosen += [fields]
    ChoiceDosen= list(zip(ListDosen, ListDosen))
    # print(ChoiceDosen)
    permintaan_dosen_2=forms.ChoiceField(choices=ChoiceDosen,required=False)
    file_topik = forms.FileField(validators=[file_size])
    class Meta:
        model = usulantopik
        fields = ["nim", "permintaan_dosen_1", 
                  "permintaan_dosen_2",
                  "judul_topik","status_pengajuan", "file_topik", "keterangan"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['nim'].label = 'Mahasiswa'
        data_dosen =dosen.objects.all()[0:]
        ListDosen= [None]
        for fields in data_dosen:
            ListDosen += [fields]
        ChoiceDosen= list(zip(ListDosen, ListDosen))
        # print(ChoiceDosen)
        instance = kwargs.get('instance')
        # print(instance.dosen_pembimbing_1)
        if instance:
            choices = [(instance.permintaan_dosen_2,instance.permintaan_dosen_2 )]+ChoiceDosen
            # print(choices)
            choices = list(set(choices))
            # print(choices)
            self.fields['permintaan_dosen_2'].choices = choices 
            
    def clean(self):
        cleaned_data = super().clean()
        permintaan_dosen_1 = cleaned_data.get("permintaan_dosen_1")
        permintaan_dosen_2 = cleaned_data.get("permintaan_dosen_2")
        # print(permintaan_dosen_1)
        # print(permintaan_dosen_2)
        # print(permintaan_dosen_2==permintaan_dosen_1)
        # print(str(permintaan_dosen_2)==str(permintaan_dosen_1))

        # Cek duplikat antara field dosen
        if str(permintaan_dosen_2)==str(permintaan_dosen_1) :
            # print("True")
            raise ValidationError("Dosen tidak boleh duplikat.")
        
        
        return cleaned_data
            
            


class UsulanTopikForm(forms.ModelForm):
    data_dosen =dosen.objects.all()[0:]
    # Dosen
    ListDosen= [None]
    for fields in data_dosen:
        ListDosen += [fields]
    ChoiceDosen= list(zip(ListDosen, ListDosen))
    permintaan_dosen_2=forms.ChoiceField(choices=ChoiceDosen,required=False)
    file_topik = forms.FileField(validators=[file_size])
    class Meta:
        model = usulantopik
        fields = [ "permintaan_dosen_1", 
                  "permintaan_dosen_2",
                  "judul_topik","status_pengajuan", "file_topik", "keterangan"]
        
    def clean(self):
        cleaned_data = super().clean()
        permintaan_dosen_1 = cleaned_data.get("permintaan_dosen_1")
        permintaan_dosen_2 = cleaned_data.get("permintaan_dosen_2")
        # print(permintaan_dosen_1)
        # print(permintaan_dosen_2)
        # print(permintaan_dosen_2==permintaan_dosen_1)
        # print(str(permintaan_dosen_2)==str(permintaan_dosen_1))
        # Cek duplikat antara field dosen
        if (permintaan_dosen_2== permintaan_dosen_1) :
            print("True")
            raise ValidationError("Dosen tidak boleh duplikat.")
        
        
        return cleaned_data
# evaluasi topik


class EvaluasiTopikFormFull(forms.ModelForm):
    catatan= forms.CharField(widget=forms.Textarea, validators=[
        MinLengthValidator(200, 'Panjang karakter minimum adalah 200.')
    ])
    class Meta:
        model = evaluasitopik
        fields = ["id_dosen_kompartemen", "id_usulan_topik",
                  "status_topik", "catatan"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_dosen_kompartemen'].label = 'Pasangan Dosen & Kompartemen'
        self.fields['id_usulan_topik'].label = 'Usulan Topik'


class EvaluasiTopikFormSekertarisDepartemen(forms.ModelForm):
    class Meta:
        model = evaluasitopik
        fields = ["id_dosen_kompartemen"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_dosen_kompartemen'].label = 'Pasangan Dosen & Kompartemen'


class EvaluasiTopikFormKompartemen(forms.ModelForm):
    catatan= forms.CharField(widget=forms.Textarea, validators=[
        MinLengthValidator(200, 'Panjang karakter minimum adalah 200.')
    ])
    class Meta:
        model = evaluasitopik
        fields = ["status_topik", "catatan"]
    


# class DosenPembimbingForm(forms.ModelForm):
#     class Meta:
#         model = DosenPembimbing
#         fields = ["nip", "nim", "Role"]

# Form Proposal
class ProposalFormFull(forms.ModelForm):
    file_proposal = forms.FileField(validators=[file_size])
    class Meta:
        model = proposal
        fields = [  "nim","nama_tahap", "judul_proposal",
                  "file_proposal", "keterangan"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nim'].label = 'Mahasiswa'
        self.fields['judul_proposal'].label = 'Judul Berkas Skripsi'
        self.fields['file_proposal'].label = 'File Berkas Skripsi'
class ProposalForm(forms.ModelForm):
    file_proposal = forms.FileField(validators=[file_size])
    class Meta:
        model = proposal
        fields = [  "nama_tahap", "judul_proposal",
                  "file_proposal", "keterangan"]
                  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['judul_proposal'].label = 'Judul Berkas Skripsi'
        self.fields['file_proposal'].label = 'File Berkas Skripsi'


class ProposalFormRead(forms.ModelForm):
    file_proposal = forms.FileField(validators=[file_size])
    class Meta:
        model = proposal
        fields = [  "nim","nama_tahap", "judul_proposal",
                  "file_proposal", "keterangan"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nim'].label = 'Mahasiswa'
        self.fields['judul_proposal'].label = 'Judul Berkas Skripsi'
        self.fields['file_proposal'].label = 'File Berkas Skripsi'

# Form Role Dosen
class RoleDosenForm(forms.ModelForm):
    class Meta:
        model = roledosen
        fields = ["nip",  "nim", "role", "status"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nip'].label = 'Dosen'
        self.fields['nim'].label = 'Mahasiswa'


class RoleDosenFormSekdept(forms.ModelForm):
    class Meta:
        model = roledosen
        fields = ["nip", "role", "status"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nip'].label = 'Dosen'


class RoleDosenFormUpdateSekdept(forms.ModelForm):
    class Meta:
        model = roledosen
        fields = ["nip", "nim", "role", "status"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nip'].label = 'Dosen'
        self.fields['nim'].label = 'Mahasiswa'

# Form Detail Penilaian
class DetailPenilaianForm(forms.ModelForm):
    class Meta:
        model = detailpenilaian
        fields = ["id_role_dosen"
                #   , "id_jadwal_seminar"
                  ,"status_kelulusan","hasil_review"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_role_dosen'].label = 'Pasangan Dosen & Mahasiswa'
        


class DetailPenilaianFormDosen(forms.ModelForm):
    class Meta:
        model = detailpenilaian
        fields = [ 
                #   "id_jadwal_seminar",
                  "status_kelulusan","hasil_review"]
        
class DetailPenilaianFormBimbingan(forms.ModelForm):
    class Meta:
        model = detailpenilaian
        fields = [ "status_kelulusan","hasil_review"]

class DetailPenilaianIDDosen(forms.ModelForm):
    class Meta:
        model = detailpenilaian
        fields = [ "id_role_dosen"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_role_dosen'].label = 'Pasangan Dosen & Mahasiswa'

class DetailPenilaianDosenForm(forms.ModelForm):
    class Meta:
        model = detailpenilaian
        fields = [
            # "id_jadwal_seminar",
            "status_kelulusan","hasil_review"]

# Form Bimbingan
class BimbinganForm(forms.ModelForm):
    class Meta:
        model = bimbingan
        fields = ["id_proposal",  "id_role_dosen",
                  "status_bimbingan", "catatan"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_proposal'].label = 'Proposal'
        self.fields['id_role_dosen'].label = 'Pasangan Dosen & Mahasiswa'


class BimbinganFormDosen(forms.ModelForm):
    class Meta:
        model = bimbingan
        fields = [
                  "status_bimbingan", "catatan"]


class BimbinganFormDosenUpdate(forms.ModelForm):
    class Meta:
        model = bimbingan
        fields = [ "status_bimbingan", "catatan"]

# Form Penilaian 
class PenilaianForm(forms.ModelForm):
    # sub_cpmk_2= forms.CharField(disabled=True)
    
    # ini juga tanda
    id_sub_cpmk_= forms.CharField(widget=forms.Textarea(attrs={'disabled': 'disabled','rows': 3}),required=False, label= "Sub CPMK")
    
    # id_sub_cpmk= forms.ModelChoiceField(queryset=sub_cpmk.objects.all())
    
    # tanda tadi yang aktif yang ini 
    id_sub_cpmk= forms.ModelChoiceField(queryset=sub_cpmk.objects.all(),widget=forms.HiddenInput(), label= "Sub CPMK")
    nilai = forms.IntegerField(validators=[MaxValueValidator(100)])
    # id_sub_cpmk= forms.ModelChoiceField(queryset=sub_cpmk.objects.all(),widget=forms.HiddenInput())

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.instance:
    #         self.fields['id_sub_cpmk'].widget.attrs['selected'] = self.instance.id_sub_cpmk.pk

    # def clean_field_name(self):
    #     if self.instance and self.cleaned_data['id_sub_cpmk'] != self.instance.id_sub_cpmk:
    #         self.cleaned_data['id_sub_cpmk'] = self.instance.id_sub_cpmk
    #     return self.cleaned_data['id_sub_cpmk']
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # self.fields['sub_cpmk_2'].widget = forms.HiddenInput()
    #     self.fields['sub_cpmk_disable'].initial = self.fields['id_sub_cpmk'].initial
   
    class Meta:
        model = penilaian
        fields = [
            "id_sub_cpmk_","id_sub_cpmk",
            "nilai" ]
        
        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     if 'initial' in kwargs:
        #         self.fields['id_sub_cpmk_'].initial = kwargs['initial'].get('id_sub_cpmk_', '')
     
        # widgets = {
        #     'id_sub_cpmk': forms.ModelChoiceField(queryset=sub_cpmk.objects.all(),widget=forms.Select(attrs={'disabled': 'disabled', 'selected': 'selected'}))
        # }
        
# Form Sub CMK 
class SubCPMKForm(forms.ModelForm):
    tahun_angkatan=forms.IntegerField(validators=[MinValueValidator(2004),MaxValueValidator(int(tahun)+1)])
    id_sub_cpmk=forms.CharField(validators=[RegexValidator(r'^\S+$', 'Tidak boleh ada spasi')])
    bobot_sempro=forms.FloatField(validators=[MaxValueValidator(1)])
    bobot_semhas=forms.FloatField(validators=[MaxValueValidator(1)])
    bobot_pembimbing=forms.FloatField(validators=[MaxValueValidator(1)])
    # bobot_persen_sempro=forms.CharField(validators=[RegexValidator(r'^[\d%]*$', 'Hanya angka dan simbol persen (%) yang diperbolehkan.'),MaxLengthValidator(4, 'Harus terdiri dari tepat 4 Karakter.')])
    # bobot_persen_semhas=forms.CharField(validators=[RegexValidator(r'^[\d%]*$', 'Hanya angka dan simbol persen (%) yang diperbolehkan.'),MaxLengthValidator(4, 'Harus terdiri dari tepat 4 Karakter.')])
    # bobot_persen_pembimbing=forms.CharField(validators=[
    #     RegexValidator(r'^[\d/]+$', 'Hanya angka dan simbol persen (%) yang diperbolehkan.'),
    #     MaxLengthValidator(4, 'Harus terdiri dari tepat 4 karakter.'),
    # ])
    bobot_persen_sempro=forms.CharField(validators=[RegexValidator(r'^[\d%]+$', 'Hanya angka dan simbool persen  yang diperbolehkan.'),MaxLengthValidator(4, 'Harus terdiri dari tepat 4 Karakter.')])
    bobot_persen_semhas=forms.CharField(validators=[RegexValidator(r'^[\d%]+$', 'Hanya angka dan simbool persen  yang diperbolehkan.'),MaxLengthValidator(4, 'Harus terdiri dari tepat 4 Karakter.')])
    bobot_persen_pembimbing=forms.CharField(validators=[RegexValidator(r'^[\d%]+$', 'Hanya angka dan simbool persen  yang diperbolehkan.'),MaxLengthValidator(4, 'Harus terdiri dari tepat 4 Karakter.')])
    class Meta:
        
        model = sub_cpmk
        fields = ["id_sub_cpmk",'id_nama_semester',"tahun_angkatan","keterangan_sub_cpmk",
                  "id_cpmk","bobot_persen_sempro","bobot_sempro","bobot_persen_semhas","bobot_semhas","bobot_persen_pembimbing","bobot_pembimbing"]
        # ,"id_nama_semester"
        
    def clean(self):
        cleaned_data = super().clean()
        my_text_value_1 = cleaned_data.get('bobot_persen_sempro')
        my_text_value_2 = cleaned_data.get('bobot_persen_semhas')
        my_text_value_3 = cleaned_data.get('bobot_persen_pembimbing')
        print(cleaned_data)
        print(my_text_value_1)
        print(my_text_value_2)
        print(my_text_value_3)
        if my_text_value_1 and my_text_value_1.count('%') != 1 :
                raise forms.ValidationError("Harus hanya terdapat tepat satu persen (%) dalam nilai.")
        if my_text_value_2 and my_text_value_2.count('%')!=1 :
                raise forms.ValidationError("Harus hanya terdapat tepat satu persen (%) dalam nilai.")
        if my_text_value_3  and my_text_value_3.count('%')!=1:
                raise forms.ValidationError("Harus hanya terdapat tepat satu persen (%) dalam nilai.")
        if my_text_value_1 and '%' in my_text_value_1:
            # Validasi tambahan jika garis miring ada di dalam nilai
            # Contoh: Memastikan garis miring tidak di awal atau akhir nilai
            if my_text_value_1.startswith('%') or my_text_value_1.endswith('%'):
                raise forms.ValidationError("Persen (%) tidak boleh berada di awal atau akhir nilai.")
        if my_text_value_2 and '%' in my_text_value_2:
            # Validasi tambahan jika garis miring ada di dalam nilai
            # Contoh: Memastikan garis miring tidak di awal atau akhir nilai
            if my_text_value_2.startswith('%') or my_text_value_2.endswith('%'):
                raise forms.ValidationError("Persen (%) tidak boleh berada di awal atau akhir nilai.")
        if my_text_value_3 and '%' in my_text_value_3:
            # Validasi tambahan jika garis miring ada di dalam nilai
            # Contoh: Memastikan garis miring tidak di awal atau akhir nilai
            if my_text_value_3.startswith('%') or my_text_value_3.endswith('%'):
                raise forms.ValidationError("Persen (%) tidak boleh berada di awal atau akhir nilai.")
        return cleaned_data
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_nama_semester'].label = 'Nama Semester'
        self.fields['id_sub_cpmk'].label = 'Sub CPMK'
        self.fields['id_cpmk'].label = 'CPMK'
        
        
   
        # self.fields['keterangan_cpmk_utama'].label = 'Keterangan CPMK'
    # def clean_my_field(self):
    #     data = self.cleaned_data['id_sub_cpmk']
    #     if ' ' in data:
    #         raise ValidationError("Field tidak boleh mengandung spasi")
        # return data

# Form CPMK 
class CPMKForm(forms.ModelForm):
    tahun_angkatan = forms.IntegerField(validators=[MinValueValidator(2004),MaxValueValidator(int(tahun)+1)])
    id_cpmk=forms.CharField(validators=[RegexValidator(r'^\S+$', 'Tidak boleh ada spasi')])
    class Meta:
        model = cpmk
        fields = ["id_cpmk",'id_nama_semester',"tahun_angkatan","keterangan_cpmk"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_nama_semester'].label = 'Nama Semester'
        self.fields['id_cpmk'].label = 'CPMK'
        self.fields['keterangan_cpmk'].label = 'Keterangan CPMK'



# class PenilaianForm(forms.ModelForm):
#     id_sub_cpmk= forms.ModelChoiceField(queryset=sub_cpmk.objects.all() ,attrs={'readonly': 'True'})
#     class Meta:
#         model = penilaian
#         fields = ["id_sub_cpmk", "nilai" ]

# Form Notifikasi
class NotifikasiForm(forms.ModelForm):
    class Meta:
        model = notifikasi
        fields = ["status" ]



# Form Jadwal Seminar
class JadwalForm(forms.ModelForm):

    dosen_pembimbing_1= forms.ModelChoiceField(queryset=roledosen.objects.filter(role="Pembimbing 1").filter(status="Active"),required=True)
    dosen_pembimbing_2= forms.ModelChoiceField(queryset=roledosen.objects.filter(role="Pembimbing 2").filter(status="Active"),required=False)
    dosen_penguji_1= forms.ModelChoiceField(queryset=roledosen.objects.filter(role="Penguji Seminar Proposal 1").filter(status="Active")|roledosen.objects.filter(role="Penguji Seminar Hasil 1").filter(status="Active"),required=True)
    dosen_penguji_2= forms.ModelChoiceField(queryset=roledosen.objects.filter(role="Penguji Seminar Proposal 2").filter(status="Active")|roledosen.objects.filter(role="Penguji Seminar Hasil 2").filter(status="Active"),required=True)
    tanggal_seminar= forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    waktu_seminar= forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    # dosen_penguji_1= forms.ChoiceField(choices=ChoiceDosen,required=True)
    # dosen_penguji_2= forms.ChoiceField(choices=ChoiceDosen,required=True)
    # # tanggal_seminar= forms.DateField(widget=DatePickerInput,required=False,initial=tanggal_seminar)
    # # waktu_seminar= forms.TimeField(widget=Time24Input())
    # # Waktu_Seminar= forms.DateTimeField(input_formats=["%d %b %Y %H:%M:%S %Z"],required=False, default=)
    # # Dosen_Penguji_2= forms.ModelChoiceField(queryset=Dosen.objects.all())1
    class Meta:
        model = jadwal_seminar
        fields = ["mahasiswa", "dosen_pembimbing_1","dosen_pembimbing_2","dosen_penguji_1","dosen_penguji_2","tahap_seminar","ruang_seminar","tanggal_seminar","waktu_seminar" ]
            
    def clean(self):
        cleaned_data = super().clean()
        mahasiswa = cleaned_data.get("mahasiswa")
        tahap_seminar = cleaned_data.get("tahap_seminar")
        dosen_pembimbing_1 = cleaned_data.get("dosen_pembimbing_1")
        dosen_pembimbing_2 = cleaned_data.get("dosen_pembimbing_2")
        dosen_penguji_1 = cleaned_data.get("dosen_penguji_1")
        dosen_penguji_2 = cleaned_data.get("dosen_penguji_2")

        # Cek duplikat antara field dosen
        if ((dosen_pembimbing_1 and dosen_pembimbing_1.nip) and \
            (dosen_pembimbing_2 and dosen_pembimbing_2.nip) and \
            dosen_pembimbing_1.nip.nip == dosen_pembimbing_2.nip.nip) or \
        ((dosen_pembimbing_1 and dosen_pembimbing_1.nip) and \
            (dosen_penguji_1 and dosen_penguji_1.nip) and \
            dosen_pembimbing_1.nip.nip == dosen_penguji_1.nip.nip) or \
        ((dosen_pembimbing_1 and dosen_pembimbing_1.nip) and \
            (dosen_penguji_2 and dosen_penguji_2.nip) and \
            dosen_pembimbing_1.nip.nip == dosen_penguji_2.nip.nip) or \
        ((dosen_pembimbing_2 and dosen_pembimbing_2.nip) and \
            (dosen_penguji_1 and dosen_penguji_1.nip) and \
            dosen_pembimbing_2.nip.nip == dosen_penguji_1.nip.nip) or \
        ((dosen_pembimbing_2 and dosen_pembimbing_2.nip) and \
            (dosen_penguji_2 and dosen_penguji_2.nip) and \
            dosen_pembimbing_2.nip.nip == dosen_penguji_2.nip.nip) or \
        ((dosen_penguji_1 and dosen_penguji_1.nip) and \
            (dosen_penguji_2 and dosen_penguji_2.nip) and \
            dosen_penguji_1.nip.nip == dosen_penguji_2.nip.nip):
            raise ValidationError("Dosen tidak boleh duplikat.")
        
        if (mahasiswa and mahasiswa.nim) and \
            not((dosen_pembimbing_1 and dosen_pembimbing_1.nim) and mahasiswa.nim == dosen_pembimbing_1.nim.nim) and \
            not((dosen_pembimbing_2 and dosen_pembimbing_2.nim) and mahasiswa.nim == dosen_pembimbing_2.nim.nim) and \
            not((dosen_penguji_1 and dosen_penguji_1.nim) and mahasiswa.nim == dosen_penguji_1.nim.nim) and \
            not((dosen_penguji_2 and dosen_penguji_2.nim) and mahasiswa.nim == dosen_penguji_2.nim.nim):
            raise ValidationError("NIM mahasiswa berbeda dengan NIM dosen.")
        
        if tahap_seminar=="Seminar Proposal":
            if dosen_penguji_1.role != "Penguji Seminar Proposal 1":
                raise ValidationError("Tahap Seminar dengan Role Dosen Penguji 1 Tidak Sesuai.")
            if dosen_penguji_2.role != "Penguji Seminar Proposal 2":
                raise ValidationError("Tahap Seminar dengan Role Dosen Penguji 2 Tidak Sesuai.")
            
        if tahap_seminar=="Seminar Hasil":
            if dosen_penguji_1.role != "Penguji Seminar Hasil 1":
                raise ValidationError("Tahap Seminar dengan Role Dosen Penguji 1 Tidak Sesuai.")
            if dosen_penguji_2.role != "Penguji Seminar Hasil 2":
                raise ValidationError("Tahap Seminar dengan Role Dosen Penguji 2 Tidak Sesuai.")
        
        
        return cleaned_data
            
class JadwalFormTanpaFilter(forms.ModelForm):

    dosen_pembimbing_1= forms.ModelChoiceField(queryset=roledosen.objects.filter(role="Pembimbing 1"),required=True)
    dosen_pembimbing_2= forms.ModelChoiceField(queryset=roledosen.objects.filter(role="Pembimbing 2"),required=False)
    dosen_penguji_1= forms.ModelChoiceField(queryset=roledosen.objects.filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(role="Penguji Seminar Hasil 1"),required=True)
    dosen_penguji_2= forms.ModelChoiceField(queryset=roledosen.objects.filter(role="Penguji Seminar Proposal 2")|roledosen.objects.filter(role="Penguji Seminar Hasil 2"),required=True)
    tanggal_seminar= forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    waktu_seminar= forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    # dosen_penguji_1= forms.ChoiceField(choices=ChoiceDosen,required=True)
    # dosen_penguji_2= forms.ChoiceField(choices=ChoiceDosen,required=True)
    # # tanggal_seminar= forms.DateField(widget=DatePickerInput,required=False,initial=tanggal_seminar)
    # # waktu_seminar= forms.TimeField(widget=Time24Input())
    # # Waktu_Seminar= forms.DateTimeField(input_formats=["%d %b %Y %H:%M:%S %Z"],required=False, default=)
    # # Dosen_Penguji_2= forms.ModelChoiceField(queryset=Dosen.objects.all())1
    class Meta:
        model = jadwal_seminar
        fields = ["mahasiswa", "dosen_pembimbing_1","dosen_pembimbing_2","dosen_penguji_1","dosen_penguji_2","tahap_seminar","ruang_seminar","tanggal_seminar","waktu_seminar" ]
            
    def clean(self):
        cleaned_data = super().clean()
        mahasiswa = cleaned_data.get("mahasiswa")
        tahap_seminar = cleaned_data.get("tahap_seminar")
        dosen_pembimbing_1 = cleaned_data.get("dosen_pembimbing_1")
        dosen_pembimbing_2 = cleaned_data.get("dosen_pembimbing_2")
        dosen_penguji_1 = cleaned_data.get("dosen_penguji_1")
        dosen_penguji_2 = cleaned_data.get("dosen_penguji_2")

        # Cek duplikat antara field dosen
        if ((dosen_pembimbing_1 and dosen_pembimbing_1.nip) and \
            (dosen_pembimbing_2 and dosen_pembimbing_2.nip) and \
            dosen_pembimbing_1.nip.nip == dosen_pembimbing_2.nip.nip) or \
        ((dosen_pembimbing_1 and dosen_pembimbing_1.nip) and \
            (dosen_penguji_1 and dosen_penguji_1.nip) and \
            dosen_pembimbing_1.nip.nip == dosen_penguji_1.nip.nip) or \
        ((dosen_pembimbing_1 and dosen_pembimbing_1.nip) and \
            (dosen_penguji_2 and dosen_penguji_2.nip) and \
            dosen_pembimbing_1.nip.nip == dosen_penguji_2.nip.nip) or \
        ((dosen_pembimbing_2 and dosen_pembimbing_2.nip) and \
            (dosen_penguji_1 and dosen_penguji_1.nip) and \
            dosen_pembimbing_2.nip.nip == dosen_penguji_1.nip.nip) or \
        ((dosen_pembimbing_2 and dosen_pembimbing_2.nip) and \
            (dosen_penguji_2 and dosen_penguji_2.nip) and \
            dosen_pembimbing_2.nip.nip == dosen_penguji_2.nip.nip) or \
        ((dosen_penguji_1 and dosen_penguji_1.nip) and \
            (dosen_penguji_2 and dosen_penguji_2.nip) and \
            dosen_penguji_1.nip.nip == dosen_penguji_2.nip.nip):
            raise ValidationError("Dosen tidak boleh duplikat.")
        
        if (mahasiswa and mahasiswa.nim) and \
            not((dosen_pembimbing_1 and dosen_pembimbing_1.nim) and mahasiswa.nim == dosen_pembimbing_1.nim.nim) and \
            not((dosen_pembimbing_2 and dosen_pembimbing_2.nim) and mahasiswa.nim == dosen_pembimbing_2.nim.nim) and \
            not((dosen_penguji_1 and dosen_penguji_1.nim) and mahasiswa.nim == dosen_penguji_1.nim.nim) and \
            not((dosen_penguji_2 and dosen_penguji_2.nim) and mahasiswa.nim == dosen_penguji_2.nim.nim):
            raise ValidationError("NIM mahasiswa berbeda dengan NIM dosen.")
        
        if tahap_seminar=="Seminar Proposal":
            if dosen_penguji_1.role != "Penguji Seminar Proposal 1":
                raise ValidationError("Tahap Seminar dengan Role Dosen Penguji 1 Tidak Sesuai.")
            if dosen_penguji_2.role != "Penguji Seminar Proposal 2":
                raise ValidationError("Tahap Seminar dengan Role Dosen Penguji 2 Tidak Sesuai.")
            
        if tahap_seminar=="Seminar Hasil":
            if dosen_penguji_1.role != "Penguji Seminar Hasil 1":
                raise ValidationError("Tahap Seminar dengan Role Dosen Penguji 1 Tidak Sesuai.")
            if dosen_penguji_2.role != "Penguji Seminar Hasil 2":
                raise ValidationError("Tahap Seminar dengan Role Dosen Penguji 2 Tidak Sesuai.")
        
        
        return cleaned_data
   

# Form Jadwal Semester
class JadwalSemesterForm(forms.ModelForm):
    # OPTIONS = [
    #     ('Semester Ganjil', 'Semester Ganjil'),
    #     ('Semester Genap', 'Semester Genap'),
        
    # ]
    # my_choice = forms.ChoiceField(choices=OPTIONS, label= "Nama Semester")
    tahun_semester=forms.CharField(validators=[RegexValidator(r'^[\d/]+$', 'Hanya angka dan garis miring yang diperbolehkan.'),MinLengthValidator(9, 'Harus terdiri dari tepat 9 Karakter.'),MaxLengthValidator(9, 'Harus terdiri dari tepat 9 Karakter.')])
    tanggal_awal_semester= forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    tanggal_akhir_semester= forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = jadwal_semester
        fields = ["nama_semester","tahun_semester","tanggal_awal_semester","tanggal_akhir_semester"]
    def clean(self):
        cleaned_data = super().clean()
        my_text_value = cleaned_data.get('tahun_semester')
        if my_text_value and my_text_value.count('/') != 1:
                raise forms.ValidationError("Harus hanya terdapat tepat satu garis miring (/) dalam nilai.")
        if my_text_value and '/' in my_text_value:
            # Validasi tambahan jika garis miring ada di dalam nilai
            # Contoh: Memastikan garis miring tidak di awal atau akhir nilai
            if my_text_value.startswith('/') or my_text_value.endswith('/'):
                raise forms.ValidationError("Garis miring (/) tidak boleh berada di awal atau akhir nilai.")
        return cleaned_data

   

