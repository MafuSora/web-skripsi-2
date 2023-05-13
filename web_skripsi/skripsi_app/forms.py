from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django import forms
# from django.db import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
# , Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import cpmk,jadwal_seminar,penilaian, bimbingan,notifikasi, detailpenilaian, evaluasitopik, proposal,notifikasi, roledosen, usulantopik, dosen, kompartemen, mahasiswa, kompartemendosen,jadwal_semester
# , sub_cpmk
# from .widget import DatePickerInput, TimePickerInput, DateTimePickerInput
from .widget import DatePickerInput, TimePickerInput
# , DateTimePickerInput
# from django.forms.widgets import TimeInput
# User Form
from django.core.validators import validate_email,MaxValueValidator


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email])
    first_name = forms.CharField(max_length=30, required=True,label='Full Name')
    class Meta:
        model = User
        fields = ['first_name',  "email", "username",
                  "password1", "password2"]


class NimForm(forms.ModelForm):
    class Meta:
        model = mahasiswa
        fields = ['nim'
        ,"semester_daftar_skripsi"
        ]
    


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email])
    first_name = forms.CharField(max_length=30, required=True,label='Full Name')
    class Meta:
        model = User
        fields = ['first_name', "email", "username",
                  "password1", "password2"]


class NipForm(forms.ModelForm):
    # photo_file = forms.ImageField()
    class Meta:
        
        model = dosen
        fields = ['nip', "photo_file"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nip'].label = 'NIP'


class UpdateAdminUserForm(UserChangeForm):
    email = forms.EmailField(required=True, validators=[validate_email])
    first_name = forms.CharField(max_length=30, required=True,label='Full Name')
    class Meta:
        model = User
        fields = ["username", "email", "first_name"]
class UpdateUserForm(UserChangeForm):
    # email = forms.EmailField(required=True, validators=[validate_email])
    # first_name = forms.CharField(max_length=30, required=True,label='Full Name')
    class Meta:
        model = User
        fields = ["username"]

# dosen
class UpdateAdminDosenForm(forms.ModelForm):
    class Meta:
        model = dosen
        fields = ["nip","id_user","photo_file"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nip'].label = 'NIP'
        self.fields['id_user'].label = 'Username'


class DosenForm(forms.ModelForm):
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
    class Meta:
        model = mahasiswa
        fields = ["nim", "id_user", "photo_file"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nim'].label = 'NIM'
        self.fields['id_user'].label = 'Username'


class UpdateAdminMahasiswaForm(forms.ModelForm):
    class Meta:
        model = mahasiswa
        fields = ["nim","id_user","semester_daftar_skripsi","photo_file"]
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
    class Meta:
        model = usulantopik
        fields = ["nim", "permintaan_dosen_1", 
                  "permintaan_dosen_2",
                  "judul_topik", "file_topik", "keterangan"]
        
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

    class Meta:
        model = usulantopik
        fields = [ "permintaan_dosen_1", 
                  "permintaan_dosen_2",
                  "judul_topik", "file_topik", "keterangan"]
        
    def clean(self):
        cleaned_data = super().clean()
        permintaan_dosen_1 = cleaned_data.get("permintaan_dosen_1")
        permintaan_dosen_2 = cleaned_data.get("permintaan_dosen_2")
        print(permintaan_dosen_1)
        print(permintaan_dosen_2)
        print(permintaan_dosen_2==permintaan_dosen_1)
        print(str(permintaan_dosen_2)==str(permintaan_dosen_1))
        # Cek duplikat antara field dosen
        if (permintaan_dosen_2== permintaan_dosen_1) :
            print("True")
            raise ValidationError("Dosen tidak boleh duplikat.")
        
        
        return cleaned_data
# evaluasi topik


class EvaluasiTopikFormFull(forms.ModelForm):
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
    class Meta:
        model = evaluasitopik
        fields = ["status_topik", "catatan"]
    


# class DosenPembimbingForm(forms.ModelForm):
#     class Meta:
#         model = DosenPembimbing
#         fields = ["nip", "nim", "Role"]


class ProposalFormFull(forms.ModelForm):
    class Meta:
        model = proposal
        fields = [  "nim","nama_tahap", "judul_proposal",
                  "file_proposal", "keterangan"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nim'].label = 'Mahasiswa'
class ProposalForm(forms.ModelForm):
    class Meta:
        model = proposal
        fields = [  "nama_tahap", "judul_proposal",
                  "file_proposal", "keterangan"

]
class ProposalFormRead(forms.ModelForm):
    class Meta:
        model = proposal
        fields = [  "nim","nama_tahap", "judul_proposal",
                  "file_proposal", "keterangan"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nim'].label = 'Mahasiswa'


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


class DetailPenilaianForm(forms.ModelForm):
    class Meta:
        model = detailpenilaian
        fields = ["id_role_dosen",  "hasil_review","status_kelulusan"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_role_dosen'].label = 'Pasangan Dosen & Mahasiswa'
        


class DetailPenilaianFormDosen(forms.ModelForm):
    class Meta:
        model = detailpenilaian
        fields = [  "hasil_review","status_kelulusan"]

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
        fields = ["hasil_review","status_kelulusan"]

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


# class SubCPMKForm(forms.ModelForm):
#     class Meta:
#         model = sub_cpmk
#         fields = ["keterangan_sub_cpmk","cpmk_utama","keterangan_cpmk_utama", "bobot_persen_sempro","bobot_sempro","bobot_persen_semhas","bobot_semhas","bobot_persen_pembimbing","bobot_pembimbing"]



class PenilaianForm(forms.ModelForm):
    # sub_cpmk_2= forms.CharField(disabled=True)
    
    # ini juga tanda
    # id_sub_cpmk_= forms.CharField(widget=forms.Textarea(attrs={'disabled': 'disabled','rows': 3}),required=False, label= "Sub CPMK")
    
    # id_sub_cpmk= forms.ModelChoiceField(queryset=sub_cpmk.objects.all())
    
    # tanda tadi yang aktif yang ini 
    # id_sub_cpmk= forms.ModelChoiceField(queryset=sub_cpmk.objects.all(),widget=forms.HiddenInput(), label= "Sub CPMK")
    
    # nilai = forms.IntegerField(validators=[MaxValueValidator(100)])
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
            # "id_sub_cpmk_","id_sub_cpmk",
            "nilai" ]
        
        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     if 'initial' in kwargs:
        #         self.fields['id_sub_cpmk_'].initial = kwargs['initial'].get('id_sub_cpmk_', '')
     
        # widgets = {
        #     'id_sub_cpmk': forms.ModelChoiceField(queryset=sub_cpmk.objects.all(),widget=forms.Select(attrs={'disabled': 'disabled', 'selected': 'selected'}))
        # }
# class SubCPMKForm(forms.ModelForm):
#     class Meta:
#         # id_sub_cpmk=forms.CharField()
#         id_sub_cpmk=forms.CharField(validators=[RegexValidator(r'^\S+$', 'Tidak boleh ada spasi')])
#         model = sub_cpmk
#         fields = ["id_sub_cpmk","keterangan_sub_cpmk",
#                   "id_cpmk", 
#                   "bobot_persen_sempro","bobot_sempro","bobot_persen_semhas","bobot_semhas","bobot_persen_pembimbing","bobot_pembimbing"]
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['id_sub_cpmk'].label = 'Sub CPMK'
#         self.fields['id_cpmk'].label = 'CPMK'
        # self.fields['keterangan_cpmk_utama'].label = 'Keterangan CPMK'
    # def clean_my_field(self):
    #     data = self.cleaned_data['id_sub_cpmk']
    #     if ' ' in data:
    #         raise ValidationError("Field tidak boleh mengandung spasi")
        # return data

class CPMKForm(forms.ModelForm):
    class Meta:
        model = cpmk
        fields = ["id_cpmk","keterangan_cpmk"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_cpmk'].label = 'CPMK'
        self.fields['keterangan_cpmk'].label = 'Keterangan CPMK'



# class PenilaianForm(forms.ModelForm):
#     id_sub_cpmk= forms.ModelChoiceField(queryset=sub_cpmk.objects.all() ,attrs={'readonly': 'True'})
#     class Meta:
#         model = penilaian
#         fields = ["id_sub_cpmk", "nilai" ]

class NotifikasiForm(forms.ModelForm):
    class Meta:
        model = notifikasi
        fields = ["status" ]


# class Time24Input(forms.TimeInput):
#     input_type = 'time'
#     format = '%H:%M'
# class Time24Input(TimeInput):
#     input_type = 'time'
#     format = '%H:%M:%S'

#     def __init__(self, attrs=None):
#         attrs = {'class': 'form-control'}
#         super().__init__(attrs)

class JadwalForm(forms.ModelForm):
    data_dosen =dosen.objects.all()[0:]
    data_mahasiswa =mahasiswa.objects.all()[0:]
    # data_mahasiswa =mahasiswa.objects.all()[0:]
    # data_mahasiswa =mahasiswa.objects.all()[0:]
    # Mahasiswa
    ListMahasiswa= [None]
    for fields in data_mahasiswa:
        ListMahasiswa += [fields]
    ChoiceMahasiswa= list(zip(ListMahasiswa, ListMahasiswa))
    # Dosen
    ListDosen= [None]
    for fields in data_dosen:
        ListDosen += [fields]
    ChoiceDosen= list(zip(ListDosen, ListDosen))

    mahasiswa= forms.ChoiceField(choices=ChoiceMahasiswa,required=True)
    dosen_pembimbing_1= forms.ChoiceField(choices=ChoiceDosen,required=True)
    dosen_pembimbing_2= forms.ChoiceField(choices=ChoiceDosen,required=False)
    dosen_penguji_1= forms.ChoiceField(choices=ChoiceDosen,required=True)
    dosen_penguji_2= forms.ChoiceField(choices=ChoiceDosen,required=True)
    # tanggal_seminar= forms.DateField(widget=DatePickerInput,required=False,initial=tanggal_seminar)
    tanggal_seminar= forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    # waktu_seminar= forms.TimeField(widget=Time24Input())
    waktu_seminar= forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    # Waktu_Seminar= forms.DateTimeField(input_formats=["%d %b %Y %H:%M:%S %Z"],required=False, default=)
    # Dosen_Penguji_2= forms.ModelChoiceField(queryset=Dosen.objects.all())1
    class Meta:
        model = jadwal_seminar
        fields = ["mahasiswa", "dosen_pembimbing_1","dosen_pembimbing_2","dosen_penguji_1","dosen_penguji_2","tahap_seminar","ruang_seminar","tanggal_seminar","waktu_seminar" ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        data_dosen =dosen.objects.all()[0:]
        ListDosen= [None]
        for fields in data_dosen:
            ListDosen += [fields]
        ChoiceDosen= list(zip(ListDosen, ListDosen))
        # print(ChoiceDosen)
        instance = kwargs.get('instance')
        # print(instance.dosen_pembimbing_1)
        if instance:
            choices = [(instance.dosen_pembimbing_1,instance.dosen_pembimbing_1 )]+ChoiceDosen
            choices = list(set(choices))
            self.fields['dosen_pembimbing_1'].choices = choices 
            
            choices = [(instance.dosen_pembimbing_2,instance.dosen_pembimbing_2 )]+ChoiceDosen
            choices = list(set(choices))
            self.fields['dosen_pembimbing_2'].choices = choices 
            
            choices = [(instance.dosen_penguji_1,instance.dosen_penguji_1 )]+ChoiceDosen
            choices = list(set(choices))
            self.fields['dosen_penguji_1'].choices = choices 
            
            choices = [(instance.dosen_penguji_2,instance.dosen_penguji_2 )]+ChoiceDosen
            choices = list(set(choices))
            self.fields['dosen_penguji_2'].choices = choices 
            
    def clean(self):
        cleaned_data = super().clean()
        dosen_pembimbing_1 = cleaned_data.get("dosen_pembimbing_1")
        dosen_pembimbing_2 = cleaned_data.get("dosen_pembimbing_2")
        dosen_penguji_1 = cleaned_data.get("dosen_penguji_1")
        dosen_penguji_2 = cleaned_data.get("dosen_penguji_2")

        # Cek duplikat antara field dosen
        if (dosen_pembimbing_1 and dosen_pembimbing_1 == dosen_pembimbing_2) or \
           (dosen_pembimbing_1 and dosen_pembimbing_1 == dosen_penguji_1) or \
           (dosen_pembimbing_1 and dosen_pembimbing_1 == dosen_penguji_2) or \
           (dosen_pembimbing_2 and dosen_pembimbing_2 == dosen_penguji_1) or \
           (dosen_pembimbing_2 and dosen_pembimbing_2 == dosen_penguji_2) or \
           (dosen_penguji_1 and dosen_penguji_1 == dosen_penguji_2):
            raise ValidationError("Dosen tidak boleh duplikat.")
        
        
        return cleaned_data
            
    
   


class JadwalSemesterForm(forms.ModelForm):
    tanggal_awal_semester= forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    tanggal_akhir_semester= forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = jadwal_semester
        fields = ["nama_semester","tanggal_awal_semester","tanggal_akhir_semester"]
