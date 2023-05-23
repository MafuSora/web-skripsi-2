# from urllib import response
# from urllib.request import Request
# from django.urls import reverse
# from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib import messages

# Import Library model data bawaan django untuk autentikasi
from django.contrib.auth.models import Group,  User

# Import Library untuk memuat halaman autentikasi seperti : login, logout
from django.contrib.auth import login as auth_login, logout, authenticate
# ,Permission
# Import Library untuk abstract class  perlu otentikasi login  dan permission role
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
# untuk mengalihkan halaman ketika tidak mendapatkan akses
from django.core.exceptions import PermissionDenied

# Import Library untuk memuat halaman
from django.shortcuts import  render, redirect
# ,get_object_or_404,

from django.contrib.contenttypes.models import ContentType

# Import file model untuk dapat dikontrol (dimanipulasi) disini  
from .models import cpmk,notifikasi,jadwal_seminar,penilaian, bimbingan, detailpenilaian, evaluasitopik, proposal, roledosen, usulantopik, dosen, kompartemen, mahasiswa, kompartemendosen, sub_cpmk, jadwal_semester

# Import file form untuk dapat dikontrol(ditampilkan) disini  
from django import forms
from .forms import JadwalFormTanpaFilter,DetailPenilaianFormBimbingan,UpdateAdminUserForm,UpdateAdminDosenForm,UpdateAdminMahasiswaForm,ProposalFormRead,ProposalFormFull,DetailPenilaianIDDosen,DetailPenilaianFormDosen,NotifikasiForm,BimbinganFormDosenUpdate, ProposalForm, RoleDosenFormUpdateSekdept, RoleDosenFormSekdept, BimbinganForm, BimbinganFormDosen, DetailPenilaianForm, EvaluasiTopikFormKompartemen, EvaluasiTopikFormSekertarisDepartemen, EvaluasiTopikFormFull, RoleDosenForm, UsulanTopikFormFull, UpdateDosenForm, KompartemenDosenForm, UpdateMahasiswaForm, NimForm, NipForm, RegistrationForm, DosenForm, MahasiswaForm, UpdateUserForm, KompartemenForm, CreateUserForm, UsulanTopikForm ,JadwalForm, JadwalSemesterForm,PenilaianForm,CPMKForm, SubCPMKForm
from django.forms import inlineformset_factory,models
# Untuk membuat field form text pada form 
from django.db.models import CharField
# ,modelformset_factory

# Function Tambahan SQL  untuk Aggregate Function 
from django.db.models import F,Count,Max,Sum,Min
# ,Prefetch
from django.db.models.functions import Substr,Cast 

# Function untuk menampilkan waktu
import time,datetime

# Function untuk mengelola email
from django.core.mail import send_mail

# IMPORT SETTING UNTUK HOST EMAIL
from django.conf import settings


from skripsi_app.decorators import role_required

#django message
from django.contrib import messages 
# Jam
tanggalan=datetime.datetime.now()
tanggal=tanggalan.strftime("%A, %d - %B - %Y")
Jam=tanggalan.strftime("%H:%M:%S")




# Create your views here.
# # 404 : Handle halamn yang tidak ditemukan (tidak tersedia) atau (salah route)
def handle_not_found(request,exception):
    return render(request,'404.html')

# # # 500 : Handle halaman error server (ada yang salah di program)
# def permission_denied(request, exception):
#     return render(request,'403.html')
# # 500 : Handle halaman error server (ada yang salah di program)
def handle_server_error(request):
    return render(request,'500.html')

# # Test Page untuk handling error 500
def test_error(request):
    mahasiswa_data=mahasiswa.objects.get(pk="abc")
    return render(request,'start.html')

# # Halaman Awal 
def start(request):
    return render(request, 'start.html')


# USER : CREATE
# Register Mahasiswa lewat halaman /register
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        form2 = NimForm(request.POST)
        # <QueryDict: {'csrfmiddlewaretoken': ['2BiEetrVP6cYf4ud73qM0OhqoxhJsrXk3SUQvvr5G5OEi7iOjN7DLrOOYza6QbCu'], 'username': ['aaa'], 'email': ['hafizhmaulana48@gmail.com'], 'first_name': ['aaa'], 'password1': ['ayaya123'], 'password2': ['ayaya123']}>
        # <WSGIRequest: POST '/skripsi_app/register/'>
        if all((form.is_valid(), form2.is_valid())):

            # add auto relation to mahasiswa table
            parent = form.save(commit=False)
            parent.save()
            child = form2.save(commit=False) 
            child.id_user=User.objects.get(username=request.POST["username"])
            child.save()
            # user = authenticate(username=username, password=password)

            # adding automate role
            this_username = User.objects.get(username=request.POST["username"])
            my_group = Group.objects.get(name='Mahasiswa')
            my_group.user_set.add(this_username)
            messages.success(request,"Akun Telah Berhasil di Buat! Silahkan Melakukan Login!")

            # auth_login(request.user)
            return redirect('/login')
    else:
        form = RegistrationForm()
        form2 = NimForm()
    return render(request, 'registration/Register.html', {"form": form, "form2": form2})

# Register Dosen, Properta, dan Admin Skripsi Skripsi  > lewat sidebar hanya bisa diakses admin dan properta
@login_required(login_url="/login")
# @permission_required("main.add_user", raise_exception=True)
@role_required(allowed_roles=['Admin','Properta'])
def user_create(request):
    user_info = user_information(request)
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        form2 = NipForm(request.POST,request.FILES)
        form = CreateUserForm(request.POST)
        # <QueryDict: {'csrfmiddlewaretoken': ['2BiEetrVP6cYf4ud73qM0OhqoxhJsrXk3SUQvvr5G5OEi7iOjN7DLrOOYza6QbCu'], 'username': ['aaa'], 'email': ['hafizhmaulana48@gmail.com'], 'first_name': ['aaa'], 'password1': ['ayaya123'], 'password2': ['ayaya123']}>
        # if all((form.is_valid(), form2.is_valid())):
        if form.is_valid() and form2.is_valid():
            parent = form.save(commit=False)
            parent.save()
            # add auto relation to dosen table
            photo_file = form2.cleaned_data['photo_file']
            child = form2.save(commit=False)
            child.photo_file = photo_file
            child.id_user = parent
            # first_kompartemen = kompartemen.objects.all()[:1].get()
            # child.id_kompartemen = first_kompartemen
            child.save()

            # adding Dosen role
            this_username = User.objects.get(username=request.POST["username"])
            my_group = Group.objects.get(name='Dosen')
            my_group.user_set.add(this_username)
            messages.success(request,"Akun Telah Berhasil di Buat!")
            return redirect('../dosenget')
    else:
        form = CreateUserForm()
        form2 = NipForm()
    return render(request, 'registration/user_create.html', {"form": form, "form2": form2, "user_info": user_info})

# Register Mahasiswa > lewat sidebar hanya bisa diakses admin dan properta
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Properta'])
def user_create_mhs(request):
    user_info = user_information(request)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        form2 = NimForm(request.POST)
        # <QueryDict: {'csrfmiddlewaretoken': ['2BiEetrVP6cYf4ud73qM0OhqoxhJsrXk3SUQvvr5G5OEi7iOjN7DLrOOYza6QbCu'], 'username': ['aaa'], 'email': ['hafizhmaulana48@gmail.com'], 'first_name': ['aaa'], 'password1': ['ayaya123'], 'password2': ['ayaya123']}>
        # <WSGIRequest: POST '/skripsi_app/register/'>
        if all((form.is_valid(), form2.is_valid())):

            # add auto relation to mahasiswa table
            parent = form.save(commit=False)
            parent.save()
            child = form2.save(commit=False)
             
            child.id_user=User.objects.get(username=request.POST["username"])
            child.save()
            # user = authenticate(username=username, password=password)

            # adding automate role
            this_username = User.objects.get(username=request.POST["username"])
            my_group = Group.objects.get(name='Mahasiswa')
            my_group.user_set.add(this_username)
            messages.success(request,"Akun Telah Berhasil di Buat!")

            # auth_login(request.user)
            return redirect('/mahasiswaget')
    else:
        form = RegistrationForm()
        form2 = NimForm()
    return render(request, 'registration/user_create_mhs.html', {"form": form, "form2": form2,"user_info": user_info})
    # return render(request, 'registration/user_create_mhs.html', {"form": form,"user_info": user_info})


# USER : READ
# Menampilkan List User Terdaftar 
@login_required(login_url="/login")
# @permission_required("auth.add_user", raise_exception=True)
@role_required(allowed_roles=['Admin','Properta'])
def user_get(request):
    user_info = user_information(request)
    users = User.objects.all()
    return render(request, 'registration/user.html', {"users": users, "user_info": user_info})

#  Menampilkan User berbentuk form berdasarkan id user 
@login_required(login_url="/login")
# @permission_required("auth.view_user", raise_exception=True)
@role_required(allowed_roles=['Admin','Properta'])
def user_read(request, id):
    user_info = user_information(request)

    if user_info[2].name == "Properta":
        # users = User.objects.get(pk=request.user.id)
        users = User.objects.get(pk=id)
    elif user_info[2].name == "Admin"  :
        # users = User.objects.get(pk=request.user.id)
        users = User.objects.get(pk=id)
    else:
        users = User.objects.get(pk=id)
    return render(request, 'registration/user_read.html', {"users": users, "user_info": user_info})

# # USER : UPDATE
# Update data User Terdaftar berdasarkan id
@login_required(login_url="/login")
# @permission_required("auth.change_user", raise_exception=True)
@role_required(allowed_roles=['Admin', 'Mahasiswa', 'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def user_update(request, id):
    user_info = user_information(request)
    if user_info[2].name == "Admin" or user_info[2].name == "Properta":
        pass
    elif request.user.id != id:
        raise PermissionDenied()
        
    if user_info[2].name == "Admin" :
        user_data = User.objects.get(pk=id)
    elif user_info[2].name == "Properta":
        user_data = User.objects.get(pk=id)
        # user_data = User.objects.get(pk=request.user.id)
    else:
        user_data = User.objects.get(pk=request.user.id)
        # user_data = User.objects.get(pk=id)
    # print(user_data)

    
    if user_info[2].name == "Admin" and request.method == 'POST':
        form = UpdateAdminUserForm(request.POST, instance=user_data)
        if form.is_valid():
            form.save()
            messages.warning(request,"Akun Telah Berhasil di Update!")
            return redirect('../userget')
    elif user_info[2].name == "Properta" and request.method == 'POST':
        form = UpdateAdminUserForm(request.POST, instance=user_data)
        if form.is_valid():
            form.save()
            messages.warning(request,"Akun Telah Berhasil di Update!")
            return redirect('../userget')
    elif request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user_data)
        if form.is_valid():
            form.save()
            messages.warning(request,"Akun Telah Berhasil di Update!")
            return redirect('../dashboard')
    elif request.method != 'POST' and user_info[2].name == "Admin" :
        form = UpdateAdminUserForm(instance=user_data)
    elif request.method != 'POST' and user_info[2].name == "Properta":
        form = UpdateAdminUserForm(instance=user_data)
    elif request.method != 'POST':
        form = UpdateUserForm(instance=user_data)
    else:
        form = UpdateUserForm(instance=user_data)
    return render(request, 'registration/user_update.html', {"form": form, "user_info": user_info})

# USER :  DELETE
# Hapus data User Terdaftar berdasarkan id
@login_required(login_url="/login")
# @permission_required("auth.delete_user", raise_exception=True)
@role_required(allowed_roles=['Admin','Properta'])
def user_delete(request, id):
    delete_data = User.objects.get(id=id)
    # print(delete_data)
    delete_data.delete()
    messages.error(request,"Akun Telah Berhasil di Hapus!")
    return redirect('../userget')

# User Group
# # USER GROUP: READ
# Menampilkan List Role Terdaftar berdasarkan user
@login_required(login_url="/login")
# @permission_required("auth.add_user", raise_exception=True)
@role_required(allowed_roles=['Admin','Properta'])
def usergroup_get(request):
    user_info = user_information(request)
    no_group = User.objects.filter(groups__isnull=True)
    usergroups = Group.objects.prefetch_related('user_set')
    return render(request, 'registration/usergroup.html', {"groups": usergroups, "nogroups": no_group, "user_info": user_info})

# USER GROUP : Update
# Update data Role Terdaftar berdasarkan id user
@login_required(login_url="/login")
# @permission_required("auth.add_user", raise_exception=True)
@role_required(allowed_roles=['Admin','Properta'])
def usergroup_update(request, id):
    user_info = user_information(request)
    group_data = Group.objects.all()
    this_username = User.objects.get(pk=id)
    this_group = this_username.groups.all()
    # print(request.POST)
    # print(len(this_group))
    if len(this_group) == 0:
        this_group = None
    else:
        this_group = list(this_group)[0]
    if request.method == 'POST':
        # print(request.POST)
        # <QueryDict: {'csrfmiddlewaretoken': ['6nJFb09tUMLtYdrq5Sbam5FDVYKVx29K5GMpDaSehN6O0zsBPkY66DvtiZpRp18c'], 'ID_Dosen': ['Mahasiswa']}>
        if this_group == None and request.POST["name"] == "":
            pass
        else:
            if this_group == None:
                pass
            else:
                delete_group = Group.objects.get(name=this_group)
                delete_group.user_set.remove(this_username)
            my_group = Group.objects.get(name=request.POST["name"])

            my_group.user_set.add(this_username)
        messages.warning(request,"Hak Akses Telah Berhasil di Ubah!")
        return redirect('../usergroupget')
    else:
        pass
    return render(request, 'registration/usergroup_update.html', {"groups": group_data, "users": this_username, "groups_ada": this_group, "user_info": user_info})

# Kompartemen
# Kompartemen : CREATE
# # Register data Kompartemen
@login_required(login_url="/login")
# @permission_required("skripsi_app.add_kompartemen", raise_exception=True)
@role_required(allowed_roles=['Admin','Properta'])
def kompartemen_create(request):
    user_info = user_information(request)
    if request.method == "POST":
        form = KompartemenForm(request.POST)
        if form.is_valid():
            create_kompartemen = form.save(commit=False)
            # post.id_dosen = request.user
            create_kompartemen.save()
            messages.success(request,"Data Kompartemen Telah Berhasil Terdaftar! ")
            return redirect("../kompartemenget")
    else:
        form = KompartemenForm()
    return render(request, 'dosen/kompartemen_create.html', {"form": form, "user_info": user_info})

# Kompartemen : GET
# Menampilkan List Kompartemen
@login_required(login_url="/login")
# @permission_required("skripsi_app.view_kompartemen", raise_exception=True)
@role_required(allowed_roles=['Admin','Properta'])
def kompartemen_get(request):
    user_info = user_information(request)
    kopartemen_data = kompartemen.objects.all()

    return render(request, 'dosen/kompartemen_get.html', {"kompartemens": kopartemen_data, "user_info": user_info})

# Kompartemen :UPDATE
# Update data Kompartemen Terdaftar berdasarkan id kompartemen
@login_required(login_url="/login")
# @permission_required("skripsi_app.change_kompartemen", raise_exception=True)
@role_required(allowed_roles=['Admin','Properta'])
def kompartemen_update(request, id):
    user_info = user_information(request)
    kompartemen_data = kompartemen.objects.get(pk=id)

    if request.method == 'POST':
        form = KompartemenForm(request.POST, instance=kompartemen_data)
        if form.is_valid():
            messages.warning(request,"Data Kompartemen Telah Berhasil Diperbarui! ")
            form.save()
            return redirect('../kompartemenget')
    else:
        form = KompartemenForm(instance=kompartemen_data)
    return render(request, 'dosen/kompartemen_update.html', {"form": form, "user_info": user_info})

# Kompartemen :DELETE
# Hapus data Kompartemen Terdaftar berdasarkan id kompartemen
@login_required(login_url="/login")
# @permission_required("skripsi_app.delete_kompartemen", raise_exception=True)
@role_required(allowed_roles=['Admin','Properta'])
def kompartemen_delete(request, id):
    delete_data = kompartemen.objects.get(id_kompartemen=id)
    messages.error(request,"Data Kompartemen Telah Berhasil Dihapus! ")
    delete_data.delete()
    return redirect('../kompartemenget')

# Mahasiswa: create : hidden
# Membuat data Mahasiswa khusus admin 
@login_required(login_url="/login")
# @permission_required("skripsi_app.add_mahasiswa", raise_exception=True)
@role_required(allowed_roles=['Admin','Properta'])
def mahasiswa_create(request):
    user_info = user_information(request)
    if request.method == "POST":
        # print(request.POST)
        form = MahasiswaForm(request.POST, request.FILES)
        if form.is_valid():
            create_mhs = form.save(commit=False)
            # post.id_dosen = request.user
            this_username = User.objects.get(pk=request.user.id)
            this_group = this_username.groups.all()
            # print(this_group)
            delete_group = Group.objects.get(name=this_group[0])
            delete_group.user_set.remove(this_username)
            my_group = Group.objects.get(name='Mahasiswa')
            my_group.user_set.add(this_username)
            
            messages.success(request,"Data Mahasiswa Telah Berhasil Terdaftar! ")
            create_mhs.save()
            return redirect("../mahasiswaget")
    else:
        form = MahasiswaForm()
    return render(request, 'mahasiswa/mahasiswa_create.html', {"form": form, "user_info": user_info})

# Mahasiswa: READ
# Menampilakan List data Mahasiswa Terdaftar
@login_required(login_url="/login")
# @permission_required("skripsi_app.add_mahasiswa", raise_exception=True)
@role_required(allowed_roles=['Admin','Properta'])
def mahasiswa_get(request):
    user_info = user_information(request)
    mahasiswas = mahasiswa.objects.all()

    return render(request, 'mahasiswa/mahasiswa_get.html', {"Mahasiswas": mahasiswas, "user_info": user_info})

# Menampilkan data progress mahasiswa berdasarkan nama 
@login_required(login_url="/login")
@role_required(allowed_roles=['Dosen','Admin', 'Kompartemen','Manajemen Departemen','Properta'])
def mahasiswa_progress_get(request):
    user_info = user_information(request)
    list_nim=[]

    # Lulus
    lulus_mhs=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim")
    lulus_list=list(bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim"))
    for i in range(len(lulus_list)):
        # print(lulus_list[i][0])
        list_nim.append(lulus_list[i][0])
    
    proposals_awal=bimbingan.objects.order_by('-tanggal_update').values("id_role_dosen").annotate(nim_count=Max('tanggal_update'))
    # print(proposals_awal)
    
    # Sudah Bimbingan
    proposals=bimbingan.objects.exclude(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update')
    proposals_list=list(bimbingan.objects.exclude(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim").distinct())
    for i in range(len(proposals_list)):
        # print(lulus_list[i][0])
        list_nim.append(proposals_list[i][0])
        # .values(NamaTahap=F("id_proposal__Nama_Tahap"),nim=F("id_proposal__nim"),status=F("Status_Bimbingan")).annotate(nim_count=Count('NIM'))
    # .annotate(nim_count=Count('id_proposal__nim'))
    
    # Sudah Bimbingan
    proposals=proposals.annotate(nim_count=Count('id_proposal__nim'))
    proposals_akhir=[]
    for id in set(proposals.values_list("id_proposal__nim", flat=True)):
        proposals_akhir.append(proposals.filter(id_proposal__nim=id).values(NamaTahap=F("id_proposal__nama_tahap"),nim=F("id_proposal__nim"),Nama=F("id_proposal__nim__id_user__first_name"),status=F("status_bimbingan")).first())
    # print(proposals_akhir)

    # Upload Proposal
    proposal_upload = proposal.objects.order_by('-tanggal_update').exclude(nim__in=list_nim)
    proposal_upload = proposal_upload.filter(id_proposal__in=proposal_upload.values('nim').annotate(max_id=Max('id_proposal')).values('max_id'))
    proposals_list2=list(proposal_upload.values_list("nim").distinct())
    for i in range (len(proposals_list2)):
        #  print(proposals_list[i])
            list_nim.append(proposals_list2[i][0])

    
    # Sudah dapat eval Topik
    evaluasitopiks=evaluasitopik.objects.exclude(id_usulan_topik__nim__in=list_nim)
    evaluasitopiks = evaluasitopiks.filter(id_evaluasi_topik__in=evaluasitopiks.values('id_usulan_topik__nim').annotate(max_id=Max('id_evaluasi_topik')).values('max_id'))
    # print(evaluasitopiks)
    evaluasitopiks_list=list(evaluasitopiks.values_list("id_usulan_topik__nim").distinct())
    # print(evaluasitopiks_list)
    for i in range (len(evaluasitopiks_list)):
        #  print(proposals_list[i])
            list_nim.append(evaluasitopiks_list[i][0])
    

    # Sudah Mengerjakan Topik
    usulantopiks=usulantopik.objects.exclude(nim__in=list_nim)
    usulantopiks = usulantopiks.filter(id_usulan_topik__in=usulantopiks.values('nim').annotate(max_id=Max('id_usulan_topik')).values('max_id'))
    # print(usulantopiks)
    usulantopiks_list=list(usulantopiks.values_list("nim").distinct())
    # print(usulantopiks_list)
    for i in range (len(usulantopiks_list)):
        #  print(proposals_list[i])
            list_nim.append(usulantopiks_list[i][0])
    # print("usul topik",list_nim)

    # Belum Buat Topik
    nim_topik=evaluasitopik.objects.exclude(id_usulan_topik__nim__in=list_nim).values_list('id_usulan_topik__nim')
    mahasiswa_topik=mahasiswa.objects.exclude(nim__in=list_nim)
    # print(mahasiswa_topik)

    # mahasiswa_topik=mahasiswa.objects.exclude(nim__in=nim_proposal).exclude(nim__in=nim_topik)
    # print(mahasiswa_topik)
    # mahasiswa_topik
    # evaluasitopikawals=evaluasitopik.objects.all()
    # print(evaluasitopikawals)
    # evaluasitopiks=evaluasitopik.objects.exclude(id_usulan_topik__nim__in=nim_proposal)
    # print(evaluasitopiks)
    # print(proposals)
    # print(nim_proposal)
    # print(mahasiswa_topik)

    return render(request, 'mahasiswa/mahasiswa_progress.html', {"proposals": proposals_akhir,
                                                                 "mahasiswa_topik":mahasiswa_topik,
                                                                  "proposal_upload":proposal_upload,
                                                                 "usulantopiks":usulantopiks,
                                                                 "lulusmhs":lulus_mhs,
                                                                 "evaluasitopiks":evaluasitopiks, 
                                                                 "user_info": user_info})

# Menampilkan data progress mahasiswa berdasarkan waktu akhir progress
@login_required(login_url="/login")
@role_required(allowed_roles=['Dosen','Admin', 'Kompartemen','Manajemen Departemen','Properta'])
def mahasiswa_waktu_get(request):
    user_info = user_information(request)
    # bimbingans = bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC")|bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir (BAB 4 - BAB 6)").filter(status_bimbingan="ACC")
    bimbingans_nim = bimbingan.objects.values_list('id_proposal__nim').filter(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)").filter(status_bimbingan="ACC").distinct()
    # |bimbingan.objects.values_list('id_proposal__nim').filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").distinct()

    bimbingans_nim_tanggal = bimbingan.objects.values(nim=F("id_proposal__nim"),TanggalUpdate=F("id_proposal__tanggal_update")).filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").order_by("id_proposal__nim").values(NIM_mhs=F("id_proposal__nim")).annotate(TanggalUpdate=Max('id_proposal__tanggal_update'))
    # bimbingans_nim_tanggal =bimbingan.objects.values(nim=F("id_proposal__nim"),TanggalUpdate=F("id_proposal__tanggal_update")).filter(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)").filter(status_bimbingan="ACC").order_by("id_proposal__nim").values(NIM_mhs=F("id_proposal__nim")).annotate(TanggalUpdate=Max('id_proposal__tanggal_update'))
    mahasiswa_topik=usulantopik.objects.order_by("nim").filter(nim__in=bimbingans_nim)
  

    return render(request, 'mahasiswa/mahasiswa_waktu.html', {"proposals": bimbingans_nim_tanggal,
                                                              "mahasiswa_topik":mahasiswa_topik, 
                                                              "user_info": user_info})


# Menampilkan data  mahasiswa berdasarkan waktu studi 
# @login_required(login_url="/login")
# def mahasiswa_progress_get(request):
#     user_info = user_information(request)
#     proposals = proposal.objects.all().order_by('-Tanggal_Buat').distinct()
#     nim_proposal = proposal.objects.values_list('NIM').distinct()
#     mahasiswa_topik=mahasiswa.objects.exclude(nim__in=nim_proposal)
#     # print(proposals)
#     # print(nim_proposal)
#     # print(mahasiswa_topik)

#     return render(request, 'mahasiswa/mahasiswa_progress.html', {"proposals": proposals,"mahasiswa_topik":mahasiswa_topik, "user_info": user_info})


# Menampilkan  data Mahasiswa Terdaftar berdasarkan id mahasiswa

@login_required(login_url="/login")
@role_required(allowed_roles=['Mahasiswa','Admin','Properta'])
def mahasiswa_read(request, id):
    user_info = user_information(request)
    if  user_info[2].name == "Properta":
        # mahasiswas = mahasiswa.objects.get(pk=user_info[0])
        mahasiswas = mahasiswa.objects.get(pk=id)
    elif user_info[2].name == "Admin" :
        mahasiswas = mahasiswa.objects.get(pk=id)
        # mahasiswas = mahasiswa.objects.get(pk=user_info[0])
    else:
        mahasiswas = mahasiswa.objects.get(pk=user_info[0])
        # mahasiswas = mahasiswa.objects.get(pk=id)
    # print(mahasiswas)
    return render(request, 'mahasiswa/mahasiswa_read.html', {"mahasiswas": mahasiswas, "user_info": user_info})

# Menampilkan Dashboard Beserta segala querynya
@login_required(login_url="/login")
@role_required(allowed_roles=['Dosen','Mahasiswa','Admin', 'Kompartemen','Manajemen Departemen','Properta'])
# @permission_required("skripsi_app.view_mahasiswa", raise_exception=True)
def dashboard(request):
    user_info = user_information(request)
    # belum assign kompartemen
    usulantopiks = usulantopik.objects.all()
    jumlah = 0
    jumlah_mhs_belum_kompartemen = 0
    for item in usulantopiks: 
        try:
            if evaluasitopik.objects.filter(
                id_usulan_topik=item).exists():
                get_object = evaluasitopik.objects.filter(
                    id_usulan_topik=item).first()
                # usulantopiks.exclude(id_usulan_topik=item.id_usulan_topik)
            else:
                get_object.id_dosen_kompartemen = "Belum Di Assign"
                jumlah_mhs_belum_kompartemen+=1
            usulantopiks[jumlah].status_dosen_Kompartemen = get_object.id_dosen_kompartemen

        except:
            usulantopiks[jumlah].status_dosen_Kompartemen = "Belum Di Assign"
            jumlah_mhs_belum_kompartemen+=1
        jumlah+=1

    # hitung dosen sempro
    cek_jumlah_sempro_dosen_sum=0
    role_dosen_filter=roledosen.objects.filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(role="Penguji Seminar Proposal 2")
    
    cek_jumlah_sempro=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC")
    
    detail_penilaian_lulus=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(status_kelulusan="Lulus")
    list_detailpenilaian_lulus=list(detail_penilaian_lulus.values_list("id_role_dosen__nim__nim",flat=True))
    
    cek_jumlah_sempro=cek_jumlah_sempro.exclude(id_proposal__nim__nim__in=list_detailpenilaian_lulus)
    
    
    detail_penilaian_tdk_lulus=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(status_kelulusan="Tidak Lulus")
    list_detailpenilaian_tdk_lulus=list(detail_penilaian_tdk_lulus.values_list("id_role_dosen__nim__nim",flat=True))
    detailpenilaian_tdk_lulus_count=detail_penilaian_tdk_lulus.values("id_role_dosen__nim__nim").annotate(nim_count=Count('id_role_dosen__nim__nim'))
    # print(detailpenilaian_tdk_lulus_count)
    
    cek_sempro_tidak_lulus=cek_jumlah_sempro.filter(id_proposal__nim__nim__in=list_detailpenilaian_tdk_lulus)
    list_cek_sempro_tidak_lulus=list(cek_sempro_tidak_lulus.values_list("id_proposal__nim__nim",flat=True))
    roledosen_tidak_lulus=role_dosen_filter.filter(nim__nim__in=list_cek_sempro_tidak_lulus)
    roledosen_data_tidak_lulus=roledosen_tidak_lulus.values("nim__nim").annotate(jumlah_role_dosen=Count('nim__nim'))
    
    
    jumlah=0
    for item in cek_sempro_tidak_lulus:
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item.id_proposal).last()
                cek_sempro_tidak_lulus[jumlah].status = get_object.status_bimbingan

            except:
                cek_sempro_tidak_lulus[jumlah].status = "Belum Diperiksa"
            jumlah += 1
            
    for item in cek_sempro_tidak_lulus: 
            # print(item.status, item.status == "ACC")
            if item.status != "ACC":
                cek_sempro_tidak_lulus=cek_sempro_tidak_lulus.exclude(id_proposal=item.id_proposal)    
            
    jumlah=0
    for item in cek_sempro_tidak_lulus:
        try : 
            abc_filtered = {d['id_role_dosen__nim__nim']: d for d in detailpenilaian_tdk_lulus_count if d['id_role_dosen__nim__nim'] == item.id_proposal.nim.nim}
            def_filtered = {d['nim__nim']: d for d in roledosen_data_tidak_lulus if d['nim__nim'] == item.id_proposal.nim.nim}
            # print(abc_filtered[item.id_proposal.nim.nim])
            # print(def_filtered[item.id_proposal.nim.nim])
            if abc_filtered and def_filtered:
                nim_count = abc_filtered[item.id_proposal.nim.nim]['nim_count']
                jumlah_role_dosen = def_filtered[item.id_proposal.nim.nim]['jumlah_role_dosen']

                if jumlah_role_dosen == (nim_count*2)+2:
                    # print("a")
                    cek_sempro_tidak_lulus[jumlah].status_dosen=f"Sudah Mencukupi : {nim_count*2} Assign Dosen"
                    # print(f"Nilai count untuk nim {filter_nim} sama.")
                else:
                    # print("b")
                    cek_sempro_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : {jumlah_role_dosen} Assign Dosen, Kurang Assign : {(nim_count*2)-jumlah_role_dosen} Dosen"
                    # print(f"Nilai count untuk nim {filter_nim} berbeda.")
            else:
                # print("c")
                cek_sempro_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : 0 Assign Dosen"
                # print(f"Nim {filter_nim} tidak ditemukan di kedua daftar.")
        except :
                cek_sempro_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : 0 Assign Dosen"
            
            
        jumlah+=1
    
    for item in cek_sempro_tidak_lulus:
        if item.status_dosen.startswith("Sudah Mencukupi"):
            pass
        else:
            cek_jumlah_sempro_dosen_sum+=1
    
    lolos_tidak_lulus=cek_jumlah_sempro.exclude(id_proposal__nim__nim__in=list_detailpenilaian_tdk_lulus)
    # print(lolos_tidak_lulus)
    # print(cek_sempro_tidak_lulus)
    # lolos_tidak_lulus=lolos_tidak_lulus.filter()
    jumlah=0
    for item in lolos_tidak_lulus:
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item.id_proposal).order_by("tanggal_update").last()
                lolos_tidak_lulus[jumlah].status = get_object.status_bimbingan

            except:
                lolos_tidak_lulus[jumlah].status = "Belum Diperiksa"
            jumlah += 1
            
    for item in lolos_tidak_lulus: 
            # print(item.status, item.status == "ACC")
            # print(item.status)
            if item.status != "ACC":
                lolos_tidak_lulus=lolos_tidak_lulus.exclude(id_proposal=item.id_proposal)
    
    jumlah=0
    for item in lolos_tidak_lulus:
        try : 
            roledosen_cek=role_dosen_filter.filter(nim=item.id_proposal.nim).count()
            if roledosen_cek==2 :
                lolos_tidak_lulus[jumlah].status_dosen="Sudah Mencukupi : 2 Assign Dosen"
            elif roledosen_cek==1 :
                lolos_tidak_lulus[jumlah].status_dosen="Belum Mencukupi : 1 Assign Dosen"
            else: 
                lolos_tidak_lulus[jumlah].status_dosen="Belum Mencukupi : 0 Assign Dosen"
                
        except :
                lolos_tidak_lulus[jumlah].status_dosen="Belum Mencukupi : 0 Assign Dosen" 
        jumlah+=1
    
    for item in lolos_tidak_lulus:
        if item.status_dosen.startswith("Sudah Mencukupi"):
            pass
        else:
            cek_jumlah_sempro_dosen_sum+=1
    
    
    # hitung dosen semhas
    cek_jumlah_semhas_dosen_sum=0
    role_dosen_filter_semhas=roledosen.objects.filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(role="Penguji Seminar Hasil 2")
    
    cek_jumlah_semhas=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC")
    
    detail_penilaian_lulus_semhas=detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(status_kelulusan="Lulus")
    list_detailpenilaian_lulus_semhas=list(detail_penilaian_lulus_semhas.values_list("id_role_dosen__nim__nim",flat=True))
    
    cek_jumlah_semhas=cek_jumlah_semhas.exclude(id_proposal__nim__nim__in=list_detailpenilaian_lulus_semhas)
    
    
    detail_penilaian_tdk_lulus_semhas=detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(status_kelulusan="Tidak Lulus")
    list_detailpenilaian_tdk_lulus_semhas=list(detail_penilaian_tdk_lulus_semhas.values_list("id_role_dosen__nim__nim",flat=True))
    detailpenilaian_tdk_lulus_count_semhas=detail_penilaian_tdk_lulus_semhas.values("id_role_dosen__nim__nim").annotate(nim_count=Count('id_role_dosen__nim__nim'))
    # print(detailpenilaian_tdk_lulus_count)
    
    cek_semhas_tidak_lulus=cek_jumlah_semhas.filter(id_proposal__nim__nim__in=list_detailpenilaian_tdk_lulus_semhas)
    list_cek_sempro_tidak_lulus_semhas=list(cek_semhas_tidak_lulus.values_list("id_proposal__nim__nim",flat=True))
    roledosen_tidak_lulus_semhas=role_dosen_filter_semhas.filter(nim__nim__in=list_cek_sempro_tidak_lulus_semhas)
    roledosen_data_tidak_lulus_semhas=roledosen_tidak_lulus_semhas.values("nim__nim").annotate(jumlah_role_dosen=Count('nim__nim'))
    
    
    jumlah=0
    for item in cek_semhas_tidak_lulus:
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item.id_proposal).order_by("tanggal_update").last()
                cek_semhas_tidak_lulus[jumlah].status = get_object.status_bimbingan

            except:
                cek_semhas_tidak_lulus[jumlah].status = "Belum Diperiksa"
            jumlah += 1
            
    for item in cek_semhas_tidak_lulus: 
            # print(item.status, item.status == "ACC")
            if item.status != "ACC":
                cek_semhas_tidak_lulus=cek_semhas_tidak_lulus.exclude(id_proposal=item.id_proposal)    
            
    jumlah=0
    for item in cek_semhas_tidak_lulus:
        try : 
            abc_filtered = {d['id_role_dosen__nim__nim']: d for d in detailpenilaian_tdk_lulus_count_semhas if d['id_role_dosen__nim__nim'] == item.id_proposal.nim.nim}
            def_filtered = {d['nim__nim']: d for d in roledosen_data_tidak_lulus_semhas if d['nim__nim'] == item.id_proposal.nim.nim}
            # print(abc_filtered[item.id_proposal.nim.nim])
            # print(def_filtered[item.id_proposal.nim.nim])
            if abc_filtered and def_filtered:
                nim_count = abc_filtered[item.id_proposal.nim.nim]['nim_count']
                jumlah_role_dosen = def_filtered[item.id_proposal.nim.nim]['jumlah_role_dosen']

                if jumlah_role_dosen == (nim_count*2)+2:
                    # print("a")
                    cek_semhas_tidak_lulus[jumlah].status_dosen=f"Sudah Mencukupi : {nim_count*2} Assign Dosen"
                    # print(f"Nilai count untuk nim {filter_nim} sama.")
                else:
                    # print("b")
                    cek_semhas_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : {jumlah_role_dosen} Assign Dosen, Kurang Assign : {(nim_count*2)-jumlah_role_dosen} Dosen"
                    # print(f"Nilai count untuk nim {filter_nim} berbeda.")
            else:
                # print("c")
                cek_semhas_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : 0 Assign Dosen"
                # print(f"Nim {filter_nim} tidak ditemukan di kedua daftar.")
        except :
                cek_semhas_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : 0 Assign Dosen"
            
            
        jumlah+=1
    
    for item in cek_semhas_tidak_lulus:
        if item.status_dosen.startswith("Sudah Mencukupi"):
            pass
        else:
            # cek_jumlah_sempro_dosen_sum+=1
            cek_jumlah_semhas_dosen_sum+=1
            
    lolos_tidak_lulus_semhas=cek_jumlah_semhas.exclude(id_proposal__nim__nim__in=list_detailpenilaian_tdk_lulus_semhas)
    # print(lolos_tidak_lulus_semhas)
    # print(cek_sempro_tidak_lulus)
    # lolos_tidak_lulus_semhas=lolos_tidak_lulus_semhas.filter()
    jumlah=0
    for item in lolos_tidak_lulus_semhas:
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item.id_proposal).order_by("tanggal_update").last()
                lolos_tidak_lulus_semhas[jumlah].status = get_object.status_bimbingan

            except:
                lolos_tidak_lulus_semhas[jumlah].status = "Belum Diperiksa"
            jumlah += 1
            
    for item in lolos_tidak_lulus_semhas: 
            # print(item.status, item.status == "ACC")
            # print(item.status)
            if item.status != "ACC":
                lolos_tidak_lulus_semhas=lolos_tidak_lulus_semhas.exclude(id_proposal=item.id_proposal)
    
    jumlah=0
    for item in lolos_tidak_lulus_semhas:
        try : 
            roledosen_cek=role_dosen_filter_semhas.filter(nim=item.id_proposal.nim).count()
            # print("ini",roledosen_cek, type(roledosen_cek))
            if roledosen_cek==2 :
                # print("a")
                lolos_tidak_lulus_semhas[jumlah].status_dosen="Sudah Mencukupi : 2 Assign Dosen"
            elif roledosen_cek==1 :
                # print("b")
                lolos_tidak_lulus_semhas[jumlah].status_dosen="Belum Mencukupi : 1 Assign Dosen"
            else: 
                # print("c")
                lolos_tidak_lulus_semhas[jumlah].status_dosen="Belum Mencukupi : 0 Assign Dosen"
                
        except :
                # print("d")
                lolos_tidak_lulus_semhas[jumlah].status_dosen="Belum Mencukupi : 0 Assign Dosen" 
        jumlah+=1
    # print("INI LOSOS",lolos_tidak_lulus_semhas)
    for item in lolos_tidak_lulus_semhas:
        if item.status_dosen.startswith("Sudah Mencukupi"):
            pass
        else:
            # cek_jumlah_sempro_dosen_sum+=1
            cek_jumlah_semhas_dosen_sum+=1
    
    
    # Hitung Semhas
    list_jadwal_semhas=list(jadwal_seminar.objects.filter(tahap_seminar="Seminar Hasil").values_list("mahasiswa",flat=True))
    list_jadwal_semhas = list(filter(lambda x: x is not None and x != '', list_jadwal_semhas))
    

    cek_nim_penilaian_semhas=list(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(status_kelulusan="Lulus").values_list("id_role_dosen__nim",flat=True))
    cek_jumlah_semhas_sum=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_semhas).exclude(id_role_dosen__nim__in=cek_nim_penilaian_semhas).count()
                
    # Hitung Sempro
    list_jadwal_sempro=list(jadwal_seminar.objects.filter(tahap_seminar="Seminar Proposal").values_list("mahasiswa",flat=True))
    list_jadwal_sempro = list(filter(lambda x: x is not None and x != '', list_jadwal_sempro))


    cek_nim_penilaian_sempro=list(detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(status_kelulusan="Lulus").values_list("id_role_dosen__nim",flat=True))
    # print(cek_nim_penilaian)
    # print(bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro).values_list("id_role_dosen__nim",flat=True))
    # print(list_jadwal_sempro)
    cek_jumlah_sempro_sum=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro).exclude(id_role_dosen__nim__in=cek_nim_penilaian_sempro).count()
    # Hitung Persebaran peserta Skripsi
    list_nim=[]
    # Lulus
    lulus_list=list(bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim"))
    lulus_list_list=list(bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim",flat=True))
    for i in range(len(lulus_list)):
        list_nim.append(lulus_list[i][0])
    print(list_nim)
    # Sudah Bimbingan
    proposals=bimbingan.objects.exclude(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update')
    proposals_list=list(bimbingan.objects.exclude(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim").distinct())
    for i in range (len(proposals_list)):
             list_nim.append(proposals_list[i][0])
    proposals=proposals.annotate(nim_count=Count('id_proposal__nim'))
    proposals_akhir=None
    for id in set(proposals.values_list("id_proposal__nim", flat=True)):
        proposals1=proposals.filter(id_proposal__nim=id).values("id_proposal__nama_tahap","id_proposal__nim","id_proposal__nim__id_user__first_name","status_bimbingan")[:1]
        if proposals_akhir==None:
            proposals_akhir=proposals1
        else:
            proposals_akhir=proposals_akhir|proposals1

    # print(list_nim)
    
    
    # Upload Proposal
    proposal_upload = proposal.objects.order_by('-tanggal_update').exclude(nim__in=list_nim)
    proposal_upload = proposal_upload.filter(id_proposal__in=proposal_upload.values('nim').annotate(max_id=Max('id_proposal')).values('max_id'))
    proposals_list2=list(proposal_upload.values_list("nim").distinct())
    for i in range (len(proposals_list2)):
            list_nim.append(proposals_list2[i][0])

    # Sudah dapat eval Topik
    evaluasitopiks=evaluasitopik.objects.exclude(id_usulan_topik__nim__in=list_nim)
    evaluasitopiks = evaluasitopiks.filter(id_evaluasi_topik__in=evaluasitopiks.values('id_usulan_topik__nim').annotate(max_id=Max('id_evaluasi_topik')).values('max_id'))
    evaluasitopiks_list=list(evaluasitopiks.values_list("id_usulan_topik__nim").distinct())
    for i in range (len(evaluasitopiks_list)):
            list_nim.append(evaluasitopiks_list[i][0])

   # Sudah Mengerjakan Topik
    usulantopiks=usulantopik.objects.exclude(nim__in=list_nim)
    usulantopiks = usulantopiks.filter(id_usulan_topik__in=usulantopiks.values('nim').annotate(max_id=Max('id_usulan_topik')).values('max_id'))
    usulantopiks_list=list(usulantopiks.values_list("nim").distinct())
    for i in range (len(usulantopiks_list)):
        #  print(proposals_list[i])
            list_nim.append(usulantopiks_list[i][0])


    # Belum Buat Topik
    mahasiswa_topik=mahasiswa.objects.exclude(nim__in=list_nim)
    mahasiswa_topiks_list=list(mahasiswa_topik.values_list("nim").distinct())
    for i in range (len(mahasiswa_topiks_list)):
        #  print(proposals_list[i])
            list_nim.append(mahasiswa_topiks_list[i][0])

    list_nim = [x for x in list_nim + lulus_list_list if (x not in list_nim) or (x not in lulus_list_list)]
    list_angkatan=[]
    list_nim=list(set(list_nim))
    test_list_nim=mahasiswa.objects.filter(nim__in=list_nim)
    # print(test_list_nim)
    for item in test_list_nim:
        # print(item)
        # print(2000+(int(str(item)[0:2])))
        list_angkatan.append(item.angkatan)
    # print(list_angkatan)
    # for item in list_nim:
    #     # print(item)
    #     # print(2000+(int(str(item)[0:2])))
    #     list_angkatan.append(2000+(int(str(item)[0:2])))
    list_angkatan_unique=list(set(list_angkatan))
    list_angkatan_unique.sort(reverse=True)
    list_jumlah_angkatan=[]
    for i in list_angkatan_unique:
        list_jumlah_angkatan.append(list_angkatan.count(i))
    # print(list_angkatan_unique)
    # print(list_jumlah_angkatan)
    total_mahasiswa=sum(list_jumlah_angkatan)



    # Jumlah Mangkrak
    list_nim=[]

    # Lulus
    lulus_mhs=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim").annotate(Tanggal_Update_Terakhir=datetime.datetime.now()-Max("tanggal_update"))
    lulus_list=list(bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim"))
    for i in range(len(lulus_list)):
        list_nim.append(lulus_list[i][0])
    # print("lulus",list_nim)


    # Sudah Bimbingan
    proposals=bimbingan.objects.exclude(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update')
    proposals_list=list(bimbingan.objects.exclude(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim").distinct())
    # print(proposals_akhir)
    for i in range(len(proposals_list)):
        list_nim.append(proposals_list[i][0])
    proposals=proposals.annotate(nim_count=Count('id_proposal__nim'))
    proposals_akhir=[]
    for id in set(proposals.values_list("id_proposal__nim", flat=True)):
        proposals_akhir.append(proposals.filter(id_proposal__nim=id).values(NamaTahap=F("id_proposal__nama_tahap"),nim=F("id_proposal__nim"),Nama=F("id_proposal__nim__id_user__first_name"),status=F("status_bimbingan")).annotate(Tanggal_Update_Terakhir=datetime.datetime.now()-Max("tanggal_update")).first())
    
    # print("sudah",list_nim)
    # Upload Proposal
    # Upload Proposal
    proposal_upload = proposal.objects.order_by('-tanggal_update').exclude(nim__in=list_nim).annotate(Tanggal_Update_Terakhir=datetime.datetime.now()-Max("tanggal_update"))
    proposal_upload = proposal_upload.filter(id_proposal__in=proposal_upload.values('nim').annotate(max_id=Max('id_proposal')).values('max_id'))
    proposals_list2=list(proposal_upload.values_list("nim").distinct())
    for i in range (len(proposals_list2)):
            list_nim.append(proposals_list2[i][0])
    
    # Sudah dapat eval Topik
    evaluasitopiks=evaluasitopik.objects.exclude(id_usulan_topik__nim__in=list_nim).annotate(Tanggal_Update_Terakhir=datetime.datetime.now()-Max("tanggal_update"))
    evaluasitopiks = evaluasitopiks.filter(id_evaluasi_topik__in=evaluasitopiks.values('id_usulan_topik__nim').annotate(max_id=Max('id_evaluasi_topik')).values('max_id'))
    evaluasitopiks_list=list(evaluasitopiks.values_list("id_usulan_topik__nim").distinct())
    # print(evaluasitopiks_list)
    for i in range (len(evaluasitopiks_list)):
            list_nim.append(evaluasitopiks_list[i][0])


    # Sudah Mengerjakan Topik
    # usulantopiks=usulantopik.objects.exclude(nim__in=list_nim).annotate(Tanggal_Update_Terakhir=datetime.datetime.now().date()-Max("tanggal_update")).distinct()
    
    usulantopiks = usulantopik.objects.exclude(nim__in=list_nim).annotate(Tanggal_Update_Terakhir=datetime.datetime.now().date() - Max("tanggal_update"))
    usulantopiks = usulantopiks.filter(id_usulan_topik__in=usulantopiks.values('nim').annotate(max_id=Max('id_usulan_topik')).values('max_id'))
    
    # print(usulantopiks)
    usulantopiks_list=list(usulantopiks.values_list("nim").distinct())
    # print(len(usulantopiks_list))
    for i in range (len(usulantopiks_list)):
            list_nim.append(usulantopiks_list[i][0])
    
    
    # proposal_upload = proposal.objects.order_by('-tanggal_update').exclude(nim__in=list_nim).annotate(Tanggal_Update_Terakhir=datetime.datetime.now()-Max("tanggal_update"))
    # # print(proposal_upload)
    # proposals_list2=list(proposal_upload.values_list("nim").distinct())
    # for i in range(len(proposals_list2)):
    #     list_nim.append(proposals_list2[i][0])
    # # print("upload",list_nim)
    # # Sudah dapat eval Topik
    # evaluasitopiks=evaluasitopik.objects.exclude(id_usulan_topik__nim__in=list_nim).annotate(Tanggal_Update_Terakhir=datetime.datetime.now()-Max("tanggal_update"))
    # evaluasitopiks_list=list(evaluasitopiks.values_list("id_usulan_topik__nim").distinct())
    # # print("ini eval topik",evaluasitopiks_list)
    # for i in range (len(evaluasitopiks_list)):
    #         list_nim.append(evaluasitopiks_list[i][0])
    # # print("eval",list_nim)

    # # Sudah Mengerjakan Topik
    # usulantopiks=usulantopik.objects.exclude(nim__in=list_nim).annotate(Tanggal_Update_Terakhir=datetime.datetime.now().date()-Max("tanggal_update"))
    # # print(usulantopiks)
    # usulantopiks = usulantopiks.filter(id_usulan_topik__in=usulantopiks.values('nim').annotate(max_id=Max('id_usulan_topik')).values('max_id'))
    # usulantopiks_list=list(usulantopiks.values_list("nim").distinct())
    # # print("ini eval topik",usulantopiks)
    # for i in range (len(usulantopiks_list)):
    #         list_nim.append(usulantopiks_list[i][0])
    # # print("ini listnim topik",list_nim)

    # Belum Buat Topik
    mahasiswa_topik=mahasiswa.objects.exclude(nim__in=list_nim).annotate(Tanggal_Update_Terakhir=datetime.datetime.now().date()-Max("id_user__date_joined"))
    
    # nim_list=[]
    if user_info[2].name != "Mahasiswa":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        nim_list=list(ambil_pembimbing.values_list("nim__nim",flat=True))
        # print("my",nim_list)
        # print("peniliannya",list_nim_penilaian)
        
    # for item in ambil_pembimbing:
    #     nim_list.append(item.nim.nim)

    update_terakhir=[]
    update_terakhir_filter_dosen=[]
    # print(proposals_akhir)
    for i in proposals_akhir:
        # print("ini i ", i)
        update_terakhir.append(i["Tanggal_Update_Terakhir"].days)
        if user_info[2].name != "Mahasiswa":
            # print(i["nim"])
            if i["nim"] in nim_list:
                # print("checknim")
                # print(i["nim"])
                update_terakhir_filter_dosen.append(i["Tanggal_Update_Terakhir"].days)
            
    for i in mahasiswa_topik:
        # print("ini i 2 ", i.nim)
        update_terakhir.append(i.Tanggal_Update_Terakhir.days)
        if user_info[2].name != "Mahasiswa":
            if i.nim in nim_list:
                # print("checknim")
                # print(i.nim)
                update_terakhir_filter_dosen.append(i.Tanggal_Update_Terakhir.days)
    for i in proposal_upload:
        update_terakhir.append(i.Tanggal_Update_Terakhir.days)
        if user_info[2].name != "Mahasiswa":
            
            if i.nim.nim in nim_list:
                # print("usulan check true")
                # print("checknim")
                # print(i.nim)
                update_terakhir_filter_dosen.append(i.Tanggal_Update_Terakhir.days)
    for i in usulantopiks:
        update_terakhir.append(i.Tanggal_Update_Terakhir.days)
        # print("proposal",i.nim)
        if user_info[2].name != "Mahasiswa":
            if i.nim.nim in nim_list:
                # print("usulan check true")
                # print("checknim")
                # print(i.nim)
                update_terakhir_filter_dosen.append(i.Tanggal_Update_Terakhir.days)
    for i in evaluasitopiks:
        # print("ini i 2 ", i.id_usulan_topik.nim.nim)
        # update_terakhir.append(i.Tanggal_Update_Terakhir.days)
        if user_info[2].name != "Mahasiswa":
            if i.id_usulan_topik.nim.nim in nim_list:
                # print("eval check true")
                # print(i.id_usulan_topik.nim.nim)
                update_terakhir_filter_dosen.append(i.Tanggal_Update_Terakhir.days)
    # print("cek",update_terakhir)
    jumlah_diatas_3_bulan=sum(i>90 for i in update_terakhir)
    # print(nim_list)
    # print(update_terakhir_filter_dosen)
    if user_info[2].name != "Mahasiswa":
        jumlah_diatas_3_bulan_dosen=sum(i>90 for i in update_terakhir_filter_dosen)
    else : 
        jumlah_diatas_3_bulan_dosen=0
    # print(jumlah_diatas_3_bulan)
    # print("dosen",jumlah_diatas_3_bulan_dosen)


    # update proposal terakhir 
    if user_info[2].name == "Mahasiswa":
        # print("nim",user_info[0])
        update_proposal_terakhir=[]
        for i in proposals_akhir:
            # print("prop",i["nim"])
            if i["nim"]==user_info[0]:
                update_proposal_terakhir.append(i["Tanggal_Update_Terakhir"].days)
        for i in proposal_upload:
            # print("p[propup",i.nim)
            if i.nim.nim==user_info[0]:
                    update_proposal_terakhir.append(i.Tanggal_Update_Terakhir.days)
        for i in evaluasitopiks:
            # print("eval",i.id_usulan_topik.nim)
            if i.id_usulan_topik.nim.nim==user_info[0]:
                update_proposal_terakhir.append(i.Tanggal_Update_Terakhir.days)
        for i in usulantopiks:
            # print("usul",i.nim)
            if i.nim.nim==user_info[0]:
                update_proposal_terakhir.append(i.Tanggal_Update_Terakhir.days)
        for i in mahasiswa_topik:
            # print("mhstopik",i.nim)
            if i.nim==user_info[0]:
                if i.Tanggal_Update_Terakhir.days < 0:
                     update_proposal_terakhir.append(0)
                else :
                    update_proposal_terakhir.append(i.Tanggal_Update_Terakhir.days)
        
        mahasiswa_last_update=update_proposal_terakhir
    else : 
        mahasiswa_last_update=[0]
    # print("last",mahasiswa_last_update)
    # Hitung Dosen Pembimbing
    roledosen_data=roledosen.objects.filter(role="Pembimbing 1").values_list("nim")|roledosen.objects.filter(role="Pembimbing 2").values_list("nim")
    # print(roledosen_data)
    roledosen_data.distinct()
    list_sudah_pembimbing=[]
    for i in range(len(roledosen_data)):
        list_sudah_pembimbing.append(roledosen_data[i][0])
    # print(list_sudah_pembimbing)
    usulantopiks = usulantopik.objects.all()
    usulantopiks=usulantopiks.exclude(nim__in=list_sudah_pembimbing)



    jumlah = 0
    for item in usulantopiks: 
        try:
            if evaluasitopik.objects.filter(status_topik="ACC").filter(
                id_usulan_topik=item.id_usulan_topik).exists():
                get_object = evaluasitopik.objects.filter(status_topik="ACC").filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
            elif evaluasitopik.objects.filter(status_topik="Revisi").filter(
                id_usulan_topik=item.id_usulan_topik).exists():
                get_object = evaluasitopik.objects.filter(status_topik="Revisi").get(
                    id_usulan_topik=item)
            elif evaluasitopik.objects.filter(status_topik="Dalam Evaluasi").filter(
                id_usulan_topik=item.id_usulan_topik).exists():
                get_object = evaluasitopik.objects.filter(status_topik="Dalam Evaluasi").get(
                    id_usulan_topik=item)
            elif evaluasitopik.objects.filter(status_topik="Dalam Revisi").filter(
                id_usulan_topik=item.id_usulan_topik).exists():
                get_object = evaluasitopik.objects.filter(status_topik="Dalam Revisi").filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
            else:
                get_object = evaluasitopik.objects.filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
            # print(get_object)
            usulantopiks[jumlah].status = get_object.status_topik

        except:
            usulantopiks[jumlah].status = "Submit"
        jumlah+=1

    for item in usulantopiks:
                    
        if item.status != "ACC":
            usulantopiks=usulantopiks.exclude(id_usulan_topik=item.id_usulan_topik)
    jumlah_belum_pembimbing=usulantopiks.count()
    # print(jumlah_belum_pembimbing)

    # Dosen
    proposal_data_acc_sempro=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC").values_list("id_proposal__nim")
    list_nim_penilaian_sempro=[]
    for i in range(len(proposal_data_acc_sempro)):
        list_nim_penilaian_sempro.append(proposal_data_acc_sempro[i][0])
    # proposal_data_acc_sempro_semhas=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC")
    proposal_data_acc_semhas=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").values_list("id_proposal__nim")
    list_nim_penilaian_semhas=[]
    for i in range(len(proposal_data_acc_semhas)):
        list_nim_penilaian_semhas.append(proposal_data_acc_semhas[i][0])
    
    # pembimbing
    # Penilaian 
    nim_list=[]
    penilaians_list=list(penilaian.objects.filter(id_detail_penilaian__id_role_dosen__role="Pembimbing 1").filter(id_detail_penilaian__nama_tahap="Bimbingan").values_list("id_detail_penilaian__id_role_dosen__id_role_dosen").distinct()|penilaian.objects.filter(id_detail_penilaian__id_role_dosen__role="Pembimbing 2").filter(id_detail_penilaian__nama_tahap="Bimbingan").values_list("id_detail_penilaian__id_role_dosen__id_role_dosen").distinct())
    list_nim_penilaian=[]
    for i in range(len(penilaians_list)):
        list_nim_penilaian.append(penilaians_list[i][0])
    if user_info[2].name == "Admin" or user_info[2].name == "Properta":
        # ambil_pembimbing=roledosen.objects.filter(nim__in=list_nim_penilaian_sempro).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nim__in=list_nim_penilaian_sempro).filter(status="Active").filter(role="Pembimbing 2")
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
    else:
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
    # print("peniliannya",list_nim_penilaian)
    
    for item in ambil_pembimbing:
        nim_list.append(item.nim)
    try:
        proposals_hitung_bimbing=proposal.objects.filter(
                nim__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        proposals_hitung_bimbing = []
    
    
    jumlah=0
    for item in proposals_hitung_bimbing:
        try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals_hitung_bimbing[jumlah].status = get_object.status_bimbingan
        except:
                proposals_hitung_bimbing[jumlah].status = "Belum Diperiksa"
                
            #         try:
            #     get_object = bimbingan.objects.filter(
            #         id_proposal=item).filter(status_bimbingan="ACC").first()
            #     proposals_hitung_bimbing[jumlah].status = get_object.status_bimbingan

            # except:
            #     proposals_hitung_bimbing[jumlah].status = "Belum Diperiksa"
            # jumlah += 1
        jumlah += 1
            
    for item in proposals_hitung_bimbing: 
            # print(item.status, item.status == "ACC")
            if item.status != "ACC":
                proposals_hitung_bimbing=proposals_hitung_bimbing.exclude(id_proposal=item.id_proposal)    
            
    
 
    jumlah_belum_dinilai_pembimbing=0
    jumlah_belum_lengkap_pembimbing=0
    # print(proposals_hitung_bimbing)
    for item in proposals_hitung_bimbing:
            # print(item.nim)
            try:
                
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                    # print("ini nim", item.nim)
                    jumlah_penilaian=list(penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).order_by().values_list("id_detail_penilaian__nama_tahap",flat=True).distinct())
                    # print(list(jumlah_penilaian))
                    if len(jumlah_penilaian)==3:
                        pass
                        # proposals_hitung_bimbing[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    elif len(jumlah_penilaian)!=3:
                        # proposals_hitung_bimbing[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                        jumlah_belum_lengkap_pembimbing+=1
                    
                    # proposals_hitung_bimbing[jumlah].tahap_penilaian = jumlah_penilaian
                else:
                    jumlah_belum_dinilai_pembimbing+=1

                
            except:
                jumlah_belum_dinilai_pembimbing+=1

    # HITUNG JUMLAH DARI SEMINAR
    id_roledosen_list=[]
    jumlah_belum_dinilai_pembimbing_seminar=0
    jumlah_belum_lengkap_pembimbing_seminar=0
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            id_roledosen_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_pembimbing_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_pembimbing_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            id_roledosen_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    # try:
    jadwal_data=jadwal_data.filter(
            dosen_pembimbing_1__in=id_roledosen_list)|jadwal_data.filter(
            dosen_pembimbing_2__in=id_roledosen_list)
        # proposals = proposal.objects.all()

    # except:
    #     jadwal_data = []
    # print(jadwal_data)
    
    # jumlah=0
    # for item in jadwal_data:
    #     if item.tahap_seminar=="Seminar Proposal":
    #         try:
    #             # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
    #             check_role= list(ambil_pembimbing.filter(
    #                 nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
    #             # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
    #             #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
    #             if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                    # jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
                    # pass
    #             else:
    #                 jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
    # jumlah_belum_dinilai_pembimbing_seminar+=1

    #         except:
    # jumlah_belum_dinilai_pembimbing_seminar+=1
    #             jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
    #     else :
    #         try:
    #             # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
    #             check_role= list(ambil_pembimbing.filter(
    #                 nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
    #             # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
    #             #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
    #             if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
    #                 jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
    # pass
    #             else:
    # jumlah_belum_dinilai_pembimbing_seminar+=1
    #                 jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

    #         except:
    # jumlah_belum_dinilai_pembimbing_seminar+=1
    #             jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
    #     jumlah += 1
    
    jumlah=0  
    for item in jadwal_data:
        try:
            # cek_pembimbing
            tahap_list=[]
            status_dosen=False
            if item.dosen_pembimbing_2==None:
                status_dosen=True
            else:
                pass
                # detailpenilaian_data=list(detailpenilaian.objects.filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).values_list("id_role_dosen",flat=True))
                # hasil= len(detailpenilaian_data)
                # if hasil==4:
                #     status_dosen=True
            # print(item.dosen_pembimbing_2)       
            # print(status_dosen)
                   
            if item.tahap_seminar=="Seminar Proposal":
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=4 and status_dosen==False :
                    # jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    # jadwal_data[jumlah].tahap_penilaian = tahap_list
                    pass
                elif len(tahap_list)>=2  and status_dosen==True :
                    # jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    # jadwal_data[jumlah].tahap_penilaian = tahap_list
                    pass
                elif len(tahap_list)>0 and len(tahap_list)<4 and status_dosen==False :
                    # jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    # jadwal_data[jumlah].tahap_penilaian = tahap_list
                    jumlah_belum_lengkap_pembimbing_seminar+=1
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    # jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    # jadwal_data[jumlah].tahap_penilaian = tahap_list
                    jumlah_belum_lengkap_pembimbing_seminar+=1
                else :
                    # jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    # jadwal_data[jumlah].tahap_penilaian = None
                    jumlah_belum_dinilai_pembimbing_seminar+=1
                # if len(tahap_list)>=2  and status_dosen==True :
                #     # jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                #     # jadwal_data[jumlah].tahap_penilaian = tahap_list
                #     pass
                # elif len(tahap_list)>=2 and status_dosen==False :
                #     # jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                #     # jadwal_data[jumlah].tahap_penilaian = tahap_list
                #     pass
                # elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==False :
                #     # jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian: Belum Ada Penilaian 2 Dosen Pembimbing"
                #     # jadwal_data[jumlah].tahap_penilaian = tahap_list
                #     jumlah_belum_lengkap_pembimbing_seminar+=1
                # elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                #     # jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                #     # jadwal_data[jumlah].tahap_penilaian = tahap_list
                #     jumlah_belum_lengkap_pembimbing_seminar+=1
                    
                # else :
                #     # jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                #     # jadwal_data[jumlah].tahap_penilaian = None
                #     jumlah_belum_dinilai_pembimbing_seminar+=1
            else : 
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=4 and status_dosen==False :
                    # jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    # jadwal_data[jumlah].tahap_penilaian = tahap_list
                    pass
                elif len(tahap_list)>=2  and status_dosen==True :
                    # jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    # jadwal_data[jumlah].tahap_penilaian = tahap_list
                    pass
                elif len(tahap_list)>0 and len(tahap_list)<4 and status_dosen==False :
                    # jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    # jadwal_data[jumlah].tahap_penilaian = tahap_list
                    jumlah_belum_lengkap_pembimbing_seminar+=1
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    # jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    # jadwal_data[jumlah].tahap_penilaian = tahap_list
                    jumlah_belum_lengkap_pembimbing_seminar+=1
                else :
                    # jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    # jadwal_data[jumlah].tahap_penilaian = None
                    jumlah_belum_dinilai_pembimbing_seminar+=1
                # if len(tahap_list)>=2  and status_dosen==True :
                #     # jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                #     # jadwal_data[jumlah].tahap_penilaian = tahap_list
                #     pass
                # elif len(tahap_list)>=2 and status_dosen==False :
                #     # jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                #     # jadwal_data[jumlah].tahap_penilaian = tahap_list
                #     pass
                # elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==False :
                #     # jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian: Belum Ada Penilaian 2 Dosen Pembimbing"
                #     # jadwal_data[jumlah].tahap_penilaian = tahap_list
                #     jumlah_belum_lengkap_pembimbing_seminar+=1
                # elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                #     # jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                #     # jadwal_data[jumlah].tahap_penilaian = tahap_list
                #     jumlah_belum_lengkap_pembimbing_seminar+=1
                # else :
                #     # jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                #     # jadwal_data[jumlah].tahap_penilaian = None
                #     jumlah_belum_dinilai_pembimbing_seminar+=1
                    
                    
        except : 
            # jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
            # jadwal_data[jumlah].tahap_penilaian = None
            jumlah_belum_dinilai_pembimbing_seminar+=1
        

        jumlah += 1
        
    
    # jumlah=0  
    # for item in jadwal_data:
    #     try:
    #         # cek_pembimbing
            
    #         status_dosen=False
    #         if item.dosen_pembimbing_2==None:
    #             status_dosen=True
    #         else:
    #             detailpenilaian_data=list(detailpenilaian.objects.filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).values_list("id_role_dosen",flat=True))
    #             hasil= len(detailpenilaian_data)
    #             if hasil==4:
    #                 status_dosen=True
                    
    #         if penilaian.objects.filter(
    #             id_detail_penilaian__id_role_dosen__nim=item.mahasiswa).exists():
                
    #             jumlah_penilaian=list(penilaian.objects.filter(
    #             id_detail_penilaian__id_role_dosen__nim=item.mahasiswa).order_by().values_list("id_detail_penilaian__nama_tahap",flat=True).distinct())
    #             # print(list(jumlah_penilaian))
    #             if len(jumlah_penilaian)==3 and status_dosen==True :
    #                 # jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
    #                 pass
    #             elif len(jumlah_penilaian)==3 and status_dosen==False :
    #                 # jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian: Belum Ada Penilaian 2 Dosen Pembimbing"
    #                 jumlah_belum_lengkap_pembimbing_seminar+=1
    #             elif len(jumlah_penilaian)!=3:
    #                 # jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
    #                 jumlah_belum_lengkap_pembimbing_seminar+=1
                
    #             # jadwal_data[jumlah].tahap_penilaian = jumlah_penilaian
    #         else:
    #             # jadwal_data[jumlah].tahap_penilaian = None
    #             # jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
    #             jumlah_belum_dinilai_pembimbing_seminar+=1
                
            
    #     except:
    #         jumlah_belum_dinilai_pembimbing_seminar+=1
    #         # jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
    #         # jadwal_data[jumlah].tahap_penilaian = None
        
    #     jumlah += 1
            
            
    
    
    # print(ambil_pembimbing)
    jumlah_pembimbing_sebagian=jumlah_belum_lengkap_pembimbing_seminar
    jumlah_pembimbing=jumlah_belum_dinilai_pembimbing_seminar
    # jumlah_pembimbing_sebagian=jumlah_belum_lengkap_pembimbing
    # jumlah_pembimbing=jumlah_belum_dinilai_pembimbing
    # ambil_pembimbing=ambil_pembimbing.exclude(nim__in=list_nim_penilaian)
    # ambil_pembimbing=ambil_pembimbing.values_list("id_role_dosen")
    # print("pembimbing",ambil_pembimbing)


    # jumlah_pembimbing=ambil_pembimbing.count()
    # print(1,jumlah_pembimbing)

    # Sempro
    # Penilaian 
    # penilaians=penilaian.objects.all()
    penilaians_list=list(penilaian.objects.filter(id_detail_penilaian__id_role_dosen__role="Penguji Seminar Proposal 1").filter(id_detail_penilaian__nama_tahap="Seminar Proposal").values_list("id_detail_penilaian__id_role_dosen__id_role_dosen").distinct()|penilaian.objects.filter(id_detail_penilaian__id_role_dosen__role="Penguji Seminar Proposal 2").filter(id_detail_penilaian__nama_tahap="Seminar Proposal").values_list("id_detail_penilaian__id_role_dosen__id_role_dosen").distinct()|penilaian.objects.filter(id_detail_penilaian__id_role_dosen__role="Pembimbing 1").filter(id_detail_penilaian__nama_tahap="Seminar Proposal").values_list("id_detail_penilaian__id_role_dosen__id_role_dosen").distinct()|penilaian.objects.filter(id_detail_penilaian__id_role_dosen__role="Pembimbing 2").filter(id_detail_penilaian__nama_tahap="Seminar Proposal").values_list("id_detail_penilaian__id_role_dosen__id_role_dosen").distinct())
    list_nim_penilaian=[]
    for i in range(len(penilaians_list)):
        list_nim_penilaian.append(penilaians_list[i][0])
    # print(list_nim_penilaian)

    if user_info[2].name == "Admin" or user_info[2].name == "Properta":
        ambil_penguji_sempro=roledosen.objects.filter(nim__in=list_nim_penilaian_sempro).filter(status="Active").filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(nim__in=list_nim_penilaian_sempro).filter(status="Active").filter(role="Penguji Seminar Proposal 2")
        
        # roledosen.objects.filter(nim__in=list_nim_penilaian_sempro).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nim__in=list_nim_penilaian_sempro).filter(status="Active").filter(role="Pembimbing 2")|
    else:
        # roledosen.objects.filter(nim__in=list_nim_penilaian_sempro).filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nim__in=list_nim_penilaian_sempro).filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")|
        ambil_penguji_sempro=roledosen.objects.filter(nim__in=list_nim_penilaian_sempro).filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(nim__in=list_nim_penilaian_sempro).filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Proposal 2")
    ambil_penguji_sempro=ambil_penguji_sempro.exclude(id_role_dosen__in=list_nim_penilaian)
    ambil_penguji_sempro=ambil_penguji_sempro.values_list("id_role_dosen")

    # list_nim_penilaian_sempro=[]
    # for i in range(len(ambil_penguji_sempro)):
    #     list_nim_penilaian_sempro.append(ambil_penguji_sempro[i][0])
    # jumlah_penguji_sempro=proposal_data_acc_sempro.filter(id_role_dosen__in=list_nim_penilaian_sempro)
    
    # Penilaiana sempro seminar
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Proposal 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_penguji_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_penguji_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Proposal 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(
                dosen_penguji_1__in=nim_list)|jadwal_data.filter(
                dosen_penguji_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
    sempro_seminar_count=0
    jumlah=0
    for item in jadwal_data:
            try:
                # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
                check_role= list(ambil_pembimbing.filter(
                    nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                    # jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
                    pass
                else:
                    # jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    sempro_seminar_count+=1

            except:
                # jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                sempro_seminar_count+=1
           
            jumlah += 1
    

    jumlah_penguji_sempro=sempro_seminar_count
    # jumlah_penguji_sempro=ambil_penguji_sempro.count()
    # print(2,jumlah_penguji_sempro)


    # Semhas
    # Penilaian 
    # penilaians=penilaian.objects.all()
    # print(user_info[2].name)
    # print(user_info[2].name != "Admin")
    # print(user_info[2] != "Admin")
    penilaians_list=list(penilaian.objects.filter(id_detail_penilaian__id_role_dosen__role="Penguji Seminar Hasil 1").filter(id_detail_penilaian__nama_tahap="Seminar Hasil").values_list("id_detail_penilaian__id_role_dosen__id_role_dosen").distinct()|penilaian.objects.filter(id_detail_penilaian__id_role_dosen__role="Penguji Seminar Hasil 2").filter(id_detail_penilaian__nama_tahap="Seminar Hasil").values_list("id_detail_penilaian__id_role_dosen__id_role_dosen").distinct()|penilaian.objects.filter(id_detail_penilaian__id_role_dosen__role="Pembimbing 1").filter(id_detail_penilaian__nama_tahap="Seminar Hasil").values_list("id_detail_penilaian__id_role_dosen__id_role_dosen").distinct()|penilaian.objects.filter(id_detail_penilaian__id_role_dosen__role="Pembimbing 2").filter(id_detail_penilaian__nama_tahap="Seminar Hasil").values_list("id_detail_penilaian__id_role_dosen__id_role_dosen").distinct())
    list_nim_penilaian=[]
    for i in range(len(penilaians_list)):
        list_nim_penilaian.append(penilaians_list[i][0])
    # print("semhas",list_nim_penilaian_semhas)
    # print("semhas",list_nim_penilaian)
    if user_info[2].name == "Admin" or user_info[2].name == "Properta":
        # print("sinikan")
        ambil_penguji_semhas=roledosen.objects.filter(nim__in=list_nim_penilaian_semhas).filter(status="Active").filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(nim__in=list_nim_penilaian_semhas).filter(status="Active").filter(role="Penguji Seminar Hasil 2")
        
        # roledosen.objects.filter(nim__in=list_nim_penilaian_semhas).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nim__in=list_nim_penilaian_semhas).filter(status="Active").filter(role="Pembimbing 2")|
    else:
        # print("koksini")
        ambil_penguji_semhas=roledosen.objects.filter(nim__in=list_nim_penilaian_semhas).filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(nim__in=list_nim_penilaian_semhas).filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Hasil 2")
        # roledosen.objects.filter(nim__in=list_nim_penilaian_semhas).filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nim__in=list_nim_penilaian_semhas).filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")|
        
    # print(ambil_penguji_semhas)

    ambil_penguji_semhas=ambil_penguji_semhas.exclude(id_role_dosen__in=list_nim_penilaian)
    ambil_penguji_semhas=ambil_penguji_semhas.values_list("id_role_dosen")
# Penilaian seminar semhas
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Hasil 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_penguji_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_penguji_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Hasil 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(
                dosen_penguji_1__in=nim_list)|jadwal_data.filter(
                dosen_penguji_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
    semhas_seminar_count=0 
    jumlah=0
    for item in jadwal_data:
        try:
            # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
            check_role= list(ambil_pembimbing.filter(
                nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
            # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
            if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                # jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
                pass
            else:
                # jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                semhas_seminar_count+=1

        except:
            semhas_seminar_count+=1
            # jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
        jumlah += 1

    # list_nim_penilaian_semhas=[]
    # for i in range(len(ambil_penguji_semhas)):
    #     list_nim_penilaian_semhas.append(ambil_penguji_semhas[i][0])
    # print("semhas",proposal_data_acc_semhas)
    # jumlah_penguji_semhas=proposal_data_acc_semhas.filter(id_role_dosen__in=list_nim_penilaian_semhas)

    jumlah_penguji_semhas=semhas_seminar_count
    # jumlah_penguji_semhas=ambil_penguji_semhas.count()
    # print(3,jumlah_penguji_semhas)


    # nim_list=[]
    # for item in ambil_pembimbing:
    #     nim_list.append(item.nim)

    # cek proposal
    if user_info[2].name == "Admin" or user_info[2].name == "Properta":
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []
        
    else:
        nim_list=[]
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []
    jumlah = 0
    for item in proposals:
        # print(item)
        try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
        except:
                proposals[jumlah].status = "Belum Diperiksa"
        
        jumlah += 1
    # print(proposals)
    for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status == "ACC" or item.status == "Revisi" :
                proposals=proposals.exclude(id_proposal=item.id_proposal)
    # print(proposals)
    jumlah_proposal=proposals.count()

    # cek eval topik
    if user_info[2].name == "Admin" or user_info[2].name == "Properta":
        usulantopiks= usulantopik.objects.all()
        # print("here")
        # jumlah_belum_evaluasi_topik= usulantopik.objects.all()
        # .exclude(status_topik="ACC").exclude(status_topik="Revisi").count()

    else :
        dosenkompartemen_list=list(evaluasitopik.objects.filter(id_dosen_kompartemen__nip=user_info[0]).values_list("id_usulan_topik",flat=True))
        # print("ini komp ",dosenkompartemen_list)
        usulantopiks= usulantopik.objects.filter(id_usulan_topik__in=dosenkompartemen_list)
        # .exclude(status_topik="ACC").exclude(status_topik="Revisi").count()
    # print(usulantopiks)
    jumlah = 0
    for item in usulantopiks: 
        try:
                
            try : 
                get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
            except: 
                class MyObject:
                    def __init__(self):
                        pass

                get_object = MyObject()
                get_object.status_topik="Submit"
                
            # print(get_object)
            usulantopiks[jumlah].status = get_object.status_topik

        except:
            usulantopiks[jumlah].status = "Submit"
        jumlah+=1
    for item in usulantopiks: 
        # print(item.status, item.status == "ACC")
        if item.status == "ACC" or item.status == "Revisi" :
            usulantopiks=usulantopiks.exclude(id_usulan_topik=item.id_usulan_topik)
    # print(usulantopiks)
    jumlah_belum_evaluasi_topik=usulantopiks.count()
    
    # cek last update usulan topik
    if user_info[2].name == "Admin" or user_info[2].name == "Properta":
        last_topik= evaluasitopik.objects.order_by("-tanggal_update").first()
        last_topik= last_topik
        # if last_topik==None:
        #     last_topik.status_topik="Belum Buat Topik"

    else : 
        last_topik= evaluasitopik.objects.filter(id_usulan_topik__nim__nim=user_info[0]).order_by("-tanggal_update").first()
        last_topik= last_topik
        # if last_topik==None:
        #     last_topik.status_topik="Belum Buat Topik"
        
    # cek last update Bimbingan
    if user_info[2].name == "Admin" or user_info[2].name == "Properta":
        last_bimbingan= bimbingan.objects.order_by("-tanggal_update").first()
        last_bimbingan= last_bimbingan

    else : 
        last_bimbingan= bimbingan.objects.filter(id_proposal__nim__nim=user_info[0]).order_by("-tanggal_update").first()

        last_bimbingan= last_bimbingan
    # Pareto
    list_nim=[]
    list_progress=[]
    list_progress_jumlah=[]
    # Lulus
    lulus_list=list(bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim"))
    for i in range(len(lulus_list)):
        list_nim.append(lulus_list[i][0])
    # print("lulus",lulus_list)

    # Sudah Bimbingan
    proposals=bimbingan.objects.exclude(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update')
    proposals_list=list(bimbingan.objects.exclude(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim").distinct())
 
    for i in range (len(proposals_list)):
             list_nim.append(proposals_list[i][0])
    # print("proposal",list_nim)
    proposals=proposals.annotate(nim_count=Count('id_proposal__nim'))
    # print(proposals)
    proposals_akhir=None
    # print(set(proposals.values_list("id_proposal__nim", flat=True)))
    for id in set(proposals.values_list("id_proposal__nim", flat=True)):
        # print(id)
        proposals1=proposals.filter(id_proposal__nim=id).values("id_proposal__nama_tahap","id_proposal__nim","id_proposal__nim__id_user__first_name","status_bimbingan")[:1]
        # proposals1=proposals1.distinct()
        # print(proposals1)
        if proposals_akhir==None:
            # print("here")
            proposals_akhir=proposals1
        else:
            proposals_akhir=proposals_akhir|proposals1
        # print(proposals_akhir)
    try:
        proposals_akhir=proposals_akhir.values("id_proposal__nama_tahap","status_bimbingan").annotate(dcount=Count("*"))
    except:
        proposals_akhir=[]
        
    # print(proposals_akhir)

    for item in proposals_akhir:
        # print(item)
        list_progress_jumlah.append(item["dcount"])
        list_progress.append(item["id_proposal__nama_tahap"] +" : "+ item["status_bimbingan"])

    # Upload Proposal
    proposal_upload = proposal.objects.order_by('-tanggal_update').exclude(nim__in=list_nim)
    proposal_upload = proposal_upload.filter(id_proposal__in=proposal_upload.values('nim').annotate(max_id=Max('id_proposal')).values('max_id'))
    proposals_list2=list(proposal_upload.values_list("nim").distinct())
    for i in range (len(proposals_list2)):
            list_nim.append(proposals_list2[i][0])

    proposal_upload=proposal_upload.values("nama_tahap").annotate(dcount=Count('nama_tahap'))
    # print("apa",proposal_upload)
    for item in proposal_upload:
        list_progress_jumlah.append(item["dcount"])
        list_progress.append(item["nama_tahap"]  +" : "+ "Belum Diperiksa Dosen")

    # Sudah dapat eval Topik
    evaluasitopiks=evaluasitopik.objects.exclude(id_usulan_topik__nim__in=list_nim)
    evaluasitopiks = evaluasitopiks.filter(id_evaluasi_topik__in=evaluasitopiks.values('id_usulan_topik__nim').annotate(max_id=Max('id_evaluasi_topik')).values('max_id'))
    evaluasitopiks_list=list(evaluasitopiks.values_list("id_usulan_topik__nim").distinct())
    for i in range (len(evaluasitopiks_list)):

            list_nim.append(evaluasitopiks_list[i][0])
    evaluasitopiks=evaluasitopiks.values("status_topik").annotate(dcount=Count('*'))

    for item in evaluasitopiks:
        list_progress_jumlah.append(item["dcount"])
        list_progress.append( "Topik : "+ item["status_topik"])
    # list_progress_jumlah.append(evaluasitopiks.filter(status_topik="ACC").count())
    # list_progress.append("Topik : ACC")
    # list_progress_jumlah.append(evaluasitopiks.filter(status_topik="Revisi").count())
    # list_progress.append("Topik : Revisi")
    # list_progress_jumlah.append(evaluasitopiks.filter(status_topik="Submit").count())
    # list_progress.append("Topik : Submit")
    # list_progress_jumlah.append(evaluasitopiks.filter(status_topik="Dalam Evaluasi").count())
    # list_progress.append("Topik : Dalam Evaluasi")

   # Sudah Mengerjakan Topik
    usulantopiks=usulantopik.objects.exclude(nim__in=list_nim)
    usulantopiks = usulantopiks.filter(id_usulan_topik__in=usulantopiks.values('nim').annotate(max_id=Max('id_usulan_topik')).values('max_id'))
    # print(usulantopiks)
    usulantopiks_list=list(usulantopiks.values_list("nim").distinct())
    # print(usulantopiks_list)
    for i in range (len(usulantopiks_list)):
        #  print(proposals_list[i])
            list_nim.append(usulantopiks_list[i][0])
    list_progress_jumlah.append(usulantopiks.count())
    list_progress.append("Topik : Sudah Submit")
   

    # Belum Buat Topik
    mahasiswa_topik=mahasiswa.objects.exclude(nim__in=list_nim).count()
    list_progress_jumlah.append(mahasiswa_topik)
    list_progress.append("Belum Membuat Topik")
    #rata rata
    bimbingans_nim = bimbingan.objects.values_list('id_proposal__nim').filter(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)").filter(status_bimbingan="ACC").distinct()
    # |bimbingan.objects.values_list('id_proposal__nim').filter(id_proposal__nama_tahap="Laporan Akhir (BAB 4 - BAB 6)").filter(status_bimbingan="ACC").distinct()
    bimbingans_nim_tanggal = bimbingan.objects.values(nim=F("id_proposal__nim"),TanggalUpdate=F("id_proposal__tanggal_update")).filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").order_by("id_proposal__nim").values(NIM_mhs=F("id_proposal__nim")).annotate(TanggalUpdate=Max('id_proposal__tanggal_update'))
    # bimbingans_nim_tanggal =bimbingan.objects.values(nim=F("id_proposal__nim"),TanggalUpdate=F("id_proposal__tanggal_update")).filter(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)").filter(status_bimbingan="ACC").order_by("id_proposal__nim").values(NIM_mhs=F("id_proposal__nim")).annotate(TanggalUpdate=Max('id_proposal__tanggal_update'))
    mahasiswa_topik_tanggal=usulantopik.objects.order_by("nim").filter(nim__in=bimbingans_nim)

    # Jadwal Data
    jadwal_data=jadwal_seminar.objects.filter(tanggal_seminar__gte=datetime.datetime.now().date())


    return render(request, 'dashboard.html', { "total_mahasiswa":total_mahasiswa,
                                              "list_angkatan_unique":list_angkatan_unique,
                                              "list_jumlah_angkatan":list_jumlah_angkatan,
                                              "jumlah_diatas_3_bulan_dosen":jumlah_diatas_3_bulan_dosen,
                                              "jumlah_diatas_3_bulan":jumlah_diatas_3_bulan,
                                              "jadwal_data":jadwal_data,
                                              "cek_jumlah_sempro_sum":cek_jumlah_sempro_sum,
                                              "cek_jumlah_sempro_dosen_sum":cek_jumlah_sempro_dosen_sum,
                                              "cek_jumlah_semhas_sum":cek_jumlah_semhas_sum,
                                              "cek_jumlah_semhas_dosen_sum":cek_jumlah_semhas_dosen_sum,
                                              "jumlah_mhs_belum_kompartemen":jumlah_mhs_belum_kompartemen,
                                              "jumlah_belum_pembimbing":jumlah_belum_pembimbing,
                                              "jumlah_pembimbing_sebagian":jumlah_pembimbing_sebagian,
                                              "jumlah_pembimbing":jumlah_pembimbing,
                                              "jumlah_penguji_sempro":jumlah_penguji_sempro,
                                              "jumlah_penguji_semhas":jumlah_penguji_semhas,
                                              "jumlah_proposal":jumlah_proposal,
                                              "jumlah_belum_evaluasi_topik":jumlah_belum_evaluasi_topik,
                                              "last_topik":last_topik,
                                              "last_bimbingan":last_bimbingan,
                                              "mahasiswa_last_update":mahasiswa_last_update,
                                              "bimbingans_nim_tanggal":bimbingans_nim_tanggal,
                                              "mahasiswa_topik_tanggal":mahasiswa_topik_tanggal,
                                              "list_progress":list_progress,
                                              "list_progress_jumlah":list_progress_jumlah,
                                              "user_info": user_info})

# Mahasiswa: UPDATE
# Update data Mahasiswa Terdaftar berdasarkan nim
@login_required(login_url="/login")
@role_required(allowed_roles=['Mahasiswa','Admin', 'Properta'])
# @permission_required("skripsi_app.change_mahasiswa", raise_exception=True)
def mahasiswa_update(request, id):
    user_info = user_information(request)
    if user_info[2].name == "Admin" or user_info[2].name == "Properta":
        pass
    elif user_info[0] != id:
        raise PermissionDenied()
    mahasiswa_data = mahasiswa.objects.get(pk=id)
    if user_info[2].name == "Admin" :
        # mahasiswa_data = mahasiswa.objects.get(pk=user_info[0])
        mahasiswa_data = mahasiswa.objects.get(pk=id)
    elif  user_info[2].name == "Properta":
        mahasiswa_data = mahasiswa.objects.get(pk=id)
    else:
        mahasiswa_data = mahasiswa.objects.get(pk=user_info[0])
        # mahasiswa_data = mahasiswa.objects.get(pk=id)
    if request.method == 'POST' and user_info[2].name == "Admin":
        form = UpdateAdminMahasiswaForm(
            request.POST, request.FILES, instance=mahasiswa_data)
        mahasiswa.objects.filter(pk=mahasiswa_data.nim).update(nim=request.POST['nim'])
        if form.is_valid():
            messages.warning(request,"Data Mahasiswa Telah Berhasil Diperbarui ! ")
            form.save()
            return redirect('../mahasiswaget')
    elif request.method == 'POST'and user_info[2].name == "Properta":
        form = UpdateAdminMahasiswaForm(
            request.POST, request.FILES, instance=mahasiswa_data)
        mahasiswa.objects.filter(pk=mahasiswa_data.nim).update(nim=request.POST['nim'])
        if form.is_valid():
            messages.warning(request,"Data Mahasiswa Telah Berhasil Diperbarui ! ")
            form.save()
            return redirect('../mahasiswaget')
    elif request.method == 'POST':
        form = UpdateMahasiswaForm(
            request.POST, request.FILES, instance=mahasiswa_data)
        if form.is_valid():
            messages.warning(request,"Foto Telah Berhasil Diperbarui ! ")
            form.save()
            return redirect('../dashboard')
    elif  user_info[2].name == "Admin":
        form = UpdateAdminMahasiswaForm(instance=mahasiswa_data)
    elif  user_info[2].name == "Properta":
        form = UpdateAdminMahasiswaForm(instance=mahasiswa_data)
    else:
        form = UpdateMahasiswaForm(instance=mahasiswa_data)
    return render(request, 'mahasiswa/mahasiswa_update.html', {"form": form,"id_user":mahasiswa_data.id_user.id, "user_info": user_info})

# Mahasiswa: delete
# Hapus data Mahasiswa Terdaftar berdasarkan nim
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Properta'])
# @permission_required("skripsi_app.delete_mahasiswa", raise_exception=True)
def mahasiswa_delete(request, id):
    delete_data = mahasiswa.objects.get(nim=id)
    messages.error(request,"Data Mahasiswa Telah Berhasil Dihapus! ")
    delete_data.delete()
    return redirect('../mahasiswaget')

#Dosen
# Dosen : Read
# Menampilakan List data Dosen Terdaftar
@login_required(login_url="/login")
@role_required(allowed_roles=['Dosen','Admin', 'Kompartemen','Manajemen Departemen','Properta'])
# @permission_required("skripsi_app.view_dosen", raise_exception=True)
def dosen_get(request):
    user_info = user_information(request)
    Dosens = dosen.objects.all()

    return render(request, 'dosen/dosen_get.html', {"dosens": Dosens, "user_info": user_info})

# Menampilakan data Dosen Terdaftar berdasarkan NIP dalam bentuk Form
@login_required(login_url="/login")
@role_required(allowed_roles=['Dosen','Admin', 'Kompartemen','Manajemen Departemen','Properta'])
# @permission_required("skripsi_app.view_dosen", raise_exception=True)
def dosen_read(request, id):
    user_info = user_information(request)
    dosens = dosen.objects.get(pk=id)
    return render(request, 'dosen/dosen_read.html', {"dosens": dosens, "user_info": user_info})

# Dosen: create : hidden
# Membuat data Dosen khusus admin 
@login_required(login_url="/login")
# @permission_required("skripsi_app.add_dosen", raise_exception=True)
@role_required(allowed_roles=['Admin','Properta'])
def dosen_create(request):
    user_info = user_information(request)
    if request.method == "POST":
        form = DosenForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.id_dosen = request.user
            messages.success(request,"Data Dosen Telah Berhasil Terdaftar! ")
            post.save()
            return redirect("../dosenget")
    else:
        form = DosenForm()
    return render(request, 'dosen/dosen_create.html', {"form": form, "user_info": user_info})

# Dosen: UPDATE
# Update data Dosen Terdaftar berdasarkan nip
@login_required(login_url="/login")
@role_required(allowed_roles=['Dosen','Admin', 'Kompartemen','Manajemen Departemen','Properta'])
# @permission_required("skripsi_app.change_dosen", raise_exception=True)
def dosen_update(request, id):
    user_info = user_information(request)
    
    if user_info[2].name == "Admin" or user_info[2].name == "Properta":
        pass
    elif user_info[0] != id:
        raise PermissionDenied()
    dosen_data = dosen.objects.get(pk=id)
    
    if user_info[2].name == "Admin" :
        # mahasiswa_data = mahasiswa.objects.get(pk=user_info[0])
        dosen_data = dosen.objects.get(pk=id)
        
    elif  user_info[2].name == "Properta":
        dosen_data = dosen.objects.get(pk=id)
    
    else:
        dosen_data = dosen.objects.get(pk=user_info[0])
        
        
    if request.method == 'POST' and user_info[2].name == "Admin":
        print(request.FILES)
        form = UpdateAdminDosenForm(
            request.POST, request.FILES, instance=dosen_data)
        dosen.objects.filter(pk=dosen_data.nip).update(nip=request.POST['nip'])
        if form.is_valid():
            
            form.save()
            messages.warning(request,"Data Dosen Telah Berhasil Diperbarui! ")
            return redirect('../dosenget')
    elif request.method == 'POST'and user_info[2].name == "Properta":
        form = UpdateAdminDosenForm(
            request.POST, request.FILES, instance=dosen_data)
        dosen.objects.filter(pk=dosen_data.nip).update(nip=request.POST['nip'])
        if form.is_valid():
            
            form.save()
            messages.warning(request,"Data Dosen Telah Berhasil Diperbarui! ")
            return redirect('../dosenget')
    elif request.method == 'POST':
        form = UpdateDosenForm(
            request.POST, request.FILES, instance=dosen_data)
        if form.is_valid():
            form.save()
            messages.warning(request,"Foto Profil Telah Berhasil Diperbarui! ")
            return redirect('../dashboard')
    elif request.method != 'POST' and user_info[2].name == "Admin":
        form = UpdateAdminDosenForm(instance=dosen_data)
    elif request.method != 'POST' and user_info[2].name == "Properta":
        form = UpdateAdminDosenForm(instance=dosen_data)
    elif request.method != 'POST':
        form = UpdateDosenForm(instance=dosen_data)
    else:
        form = UpdateDosenForm(instance=dosen_data)
        
    return render(request, 'dosen/dosen_update.html', {"form": form, "id_user":dosen_data.id_user.id, "user_info": user_info})

# Dosen: delete
# Hapus data Dosen Terdaftar berdasarkan nip
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Properta'])
# @permission_required("skripsi_app.delete_dosen", raise_exception=True)
def dosen_delete(request, id):
    delete_data = dosen.objects.get(nip=id)
    messages.error(request,"Data Dosen Telah Berhasil Dihapus! ")
    delete_data.delete()
    return redirect('../dosenget')

# Dosen Kompartemen: Create
# Membuat data assign dosen dengan kompartemen
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Properta','Manajemen Departemen'])
# @permission_required("skripsi_app.add_mahasiswa", raise_exception=True)
def kompartemendosen_create(request):
    user_info = user_information(request)
    if request.method == "POST":
        form = KompartemenDosenForm(request.POST)
        if form.is_valid():
            create_dosenkompartemen = form.save()
            create_dosenkompartemen.save()
            messages.success(request,"Data Kompartemen Dosen Telah Berhasil Disimpan! ")
            return redirect("../kompartemendosenget")
    else:
        form = KompartemenDosenForm()
    return render(request, 'dosen/kompartemendosen_create.html', {"form": form, "user_info": user_info})

# Dosen Kompartemen: read
# Menampilkan list dosen dengan kompartemen untuk evaluasi  
@login_required(login_url="/login")
@role_required(allowed_roles=['Dosen','Admin', 'Kompartemen','Manajemen Departemen','Properta'])
# @permission_required("skripsi_app.add_mahasiswa", raise_exception=True)
def kompartemendosen_get(request):
    user_info = user_information(request)
    kompartemendosens = kompartemendosen.objects.all()

    return render(request, 'dosen/kompartemendosen_get.html', {"kompartemendosens": kompartemendosens, "user_info": user_info})

# Dosen Kompartemen: Update
# mengubah data assign dosen dengan kompartemen berdasarkan id dosen kompartemen
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Properta'])
# @permission_required("skripsi_app.change_dosen", raise_exception=True)
def kompartemendosen_update(request, id):
    user_info = user_information(request)
    kompartemendosen_data = kompartemendosen.objects.get(pk=id)

    if request.method == 'POST':
        form = KompartemenDosenForm(
            request.POST, request.FILES, instance=kompartemendosen_data)
        if form.is_valid():
            form.save()
            messages.warning(request,"Data Kompartemen Dosen Telah Berhasil Diubah! ")
            return redirect('../kompartemendosenget')
    else:
        form = KompartemenDosenForm(instance=kompartemendosen_data)
    return render(request, 'dosen/kompartemendosen_update.html', {"form": form, "user_info": user_info})

# Dosen Kompartemen: delete
# menghapus data assign dosen dengan kompartemen berdasarkan id dosen kompartemen
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Manajemen Departemen','Properta'])
# @permission_required("skripsi_app.delete_dosen", raise_exception=True)
def kompartemendosen_delete(request, id):
    delete_data = kompartemendosen.objects.get(pk=id)
    messages.error(request,"Data Kompartemen Dosen Telah Berhasil Dihapus! ")
    delete_data.delete()
    return redirect('../kompartemendosenget')

# Usulan Topik
# Usulan Topik: create
# # Membuat data usulan topik oleh mahasiswa
# todo: add in notification and email 
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Mahasiswa','Properta'])
def usulantopik_create(request):
    user_info = user_information(request)
    if request.method == "POST":
        form = UsulanTopikForm(request.POST, request.FILES)
        if form.is_valid():

            create_usulantopik = form.save(commit=False)
            create_usulantopik.nim = mahasiswa.objects.get(pk=user_info[0])
            create_usulantopik.status_topik = "Submit"
            create_usulantopik.save()
            messages.success(request,"Data Usulan Topik Telah Berhasil Disimpan! ")
            # contoh : notif
            user_sekdept=list(User.objects.values_list('id').filter(groups__name='Manajemen Departemen'))
            # print(user_sekdept)
            sekdept_filter=dosen.objects.filter(id_user__in=user_sekdept)
            email_list=[]
            for i in sekdept_filter:
                notifikasi.objects.create(nip=i.nip,messages=f"Terdapat Input Usulan Topik Baru Oleh {create_usulantopik.nim} dengan judul {create_usulantopik.judul_topik} pada {tanggal} Jam {Jam}")
                # pesan=f"Terdapat Input Usulan Topik Baru Oleh {create_usulantopik.nim} pada {tanggal} Jam {Jam}"
            # send ke properta
            temp_email=list(User.objects.filter(groups__name='Properta').values_list('email'))
            for i in range(len(temp_email)):
                email_list.append(temp_email[i][0])
            # email_list=User.objects.filter(groups__name='Properta').values_list('email')
            send_mail(
                'Usulan Topik Baru',
                f"Terdapat Input Usulan Topik Baru Oleh {create_usulantopik.nim} dengan judul {create_usulantopik.judul_topik} pada {tanggal} Jam {Jam}",
                settings.EMAIL_HOST_USER,
                email_list,
                fail_silently=False,
            )
            # send ke sekdept
            email_list=[]
            # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
            temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
            for i in range(len(temp_email)):
                email_list.append(temp_email[i][0])
            send_mail(
                'Usulan Topik Baru',
                f"Terdapat Input Usulan Topik Baru Oleh {create_usulantopik.nim} dengan judul {create_usulantopik.judul_topik} pada {tanggal} Jam {Jam}",
                settings.EMAIL_HOST_USER,
                email_list,
                fail_silently=False,
            )
            return redirect("../usulantopikget")
    else:
        form = UsulanTopikForm()
    return render(request, 'mahasiswa/usulantopik_create.html', {"form": form, "user_info": user_info})
# Usulan Topik
# Usulan Topik: create
# # Membuat data usulan topik oleh mahasiswa
# todo: add in notification and email 
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Properta'])
def usulantopik_create_full(request):
    user_info = user_information(request)
    if request.method == "POST":
        form = UsulanTopikFormFull(request.POST, request.FILES)
        if form.is_valid():

            create_usulantopik = form.save(commit=False)
            # create_usulantopik.nim = mahasiswa.objects.get(pk=user_info[0])
            create_usulantopik.status_topik = "Submit"
            create_usulantopik.save()
            messages.success(request,"Data Usulan Topik Telah Berhasil Disimpan! ")
            # contoh : notif
            user_sekdept=list(User.objects.values_list('id').filter(groups__name='Manajemen Departemen'))
            # print(user_sekdept)
            sekdept_filter=dosen.objects.filter(id_user__in=user_sekdept)
            email_list=[]
            for i in sekdept_filter:
                notifikasi.objects.create(nip=i.nip,messages=f"Terdapat Input Usulan Topik Baru Oleh {create_usulantopik.nim} dengan judul {create_usulantopik.judul_topik} pada {tanggal} Jam {Jam}")
                # pesan=f"Terdapat Input Usulan Topik Baru Oleh {create_usulantopik.nim} pada {tanggal} Jam {Jam}"
            # send ke properta
            temp_email=list(User.objects.filter(groups__name='Properta').values_list('email'))
            for i in range(len(temp_email)):
                email_list.append(temp_email[i][0])
            # email_list=User.objects.filter(groups__name='Properta').values_list('email')
            send_mail(
                'Usulan Topik Baru',
                f"Terdapat Input Usulan Topik Baru Oleh {create_usulantopik.nim} dengan judul {create_usulantopik.judul_topik} pada {tanggal} Jam {Jam}",
                settings.EMAIL_HOST_USER,
                email_list,
                fail_silently=False,
            )
            # send ke sekdept
            email_list=[]
            # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
            temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
            for i in range(len(temp_email)):
                email_list.append(temp_email[i][0])
            send_mail(
                'Usulan Topik Baru',
                f"Terdapat Input Usulan Topik Baru Oleh {create_usulantopik.nim} dengan judul {create_usulantopik.judul_topik} pada {tanggal} Jam {Jam}",
                settings.EMAIL_HOST_USER,
                email_list,
                fail_silently=False,
            )
            return redirect("../usulantopikget")
    else:
        form = UsulanTopikFormFull()
    return render(request, 'mahasiswa/usulantopik_create.html', {"form": form, "user_info": user_info})

# Usulan Topik: Read
# Melihat tampilan list data Usulan Topik oleh Mahasiswa 
@login_required(login_url="/login")
@role_required(allowed_roles=['Dosen','Admin', 'Kompartemen','Manajemen Departemen','Mahasiswa','Properta'])
# @permission_required("skripsi_app.view_mahasiswa", raise_exception=True)
def usulantopik_read(request, id):
    user_info = user_information(request)
    if user_info[2].name == "Mahasiswa":
        usulantopiks = usulantopik.objects.get(pk=id, nim=user_info[0])

    else:
        usulantopiks = usulantopik.objects.get(pk=id)
    # print(usulantopiks)
    return render(request, 'mahasiswa/usulantopik_read.html', {"usulantopiks": usulantopiks,  "user_info": user_info})


# Melihat tampilan form data Usulan Topik oleh Mahasiswa 
@login_required(login_url="/login")
@role_required(allowed_roles=['Dosen','Admin', 'Kompartemen','Manajemen Departemen','Mahasiswa','Properta'])
def usulantopik_get(request):
    user_info = user_information(request)

    if user_info[2].name == "Mahasiswa":
        # try:
        usulantopiks = usulantopik.objects.filter(
            nim=mahasiswa.objects.filter(pk=user_info[0])[0])
        # print(usulantopiks)
    else:
        usulantopiks = usulantopik.objects.all()
    jumlah = 0
        
    for item in usulantopiks:
        try:
            # print(item)
            # print(evaluasitopik.objects.filter(
            #     id_usulan_topik=item).exists())
            if evaluasitopik.objects.filter(
                id_usulan_topik=item).exists():
                get_object = evaluasitopik.objects.filter(
                    id_usulan_topik=item).first()
            else:
                get_object.id_dosen_kompartemen = "Belum Di Assign"
            usulantopiks[jumlah].status_dosen_Kompartemen = get_object.id_dosen_kompartemen

        except:
            usulantopiks[jumlah].status_dosen_Kompartemen = "Belum Di Assign"
        # print(usulantopiks[jumlah].status_dosen_Kompartemen)
        try:
            # if evaluasitopik.objects.filter(status_topik="ACC").filter(
            #     id_usulan_topik=item.id_usulan_topik).exists():
            #     get_object = evaluasitopik.objects.filter(status_topik="ACC").filter(
            #         id_usulan_topik=item).latest('tanggal_update')
            # elif evaluasitopik.objects.filter(status_topik="Revisi").filter(
            #     id_usulan_topik=item.id_usulan_topik).exists():
            #     get_object = evaluasitopik.objects.filter(status_topik="Revisi").filter(
            #         id_usulan_topik=item).latest('tanggal_update')
            # elif evaluasitopik.objects.filter(status_topik="Dalam Evaluasi").filter(
            #     id_usulan_topik=item.id_usulan_topik).exists():
            #     get_object = evaluasitopik.objects.filter(status_topik="Dalam Evaluasi").filter(
            #         id_usulan_topik=item).latest('tanggal_update')
            # elif evaluasitopik.objects.filter(status_topik="Dalam Revisi").filter(
            #     id_usulan_topik=item.id_usulan_topik).exists():
            #     get_object = evaluasitopik.objects.filter(status_topik="Dalam Revisi").filter(
            #         id_usulan_topik=item).latest('tanggal_update')
            # else:
            try : 
                get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
            except: 
                class MyObject:
                    def __init__(self):
                        pass

                get_object = MyObject()
                get_object.status_topik="Submit"
                
            # print(get_object)
            usulantopiks[jumlah].status = get_object.status_topik

        except:
            usulantopiks[jumlah].status = "Submit"
        try:
            # if evaluasitopik.objects.filter(status_topik="ACC").filter(
            #     id_usulan_topik=item).exists():
            #     get_object = evaluasitopik.objects.filter(status_topik="ACC").get(
            #         id_usulan_topik=item)
            # else:
            #     get_object = evaluasitopik.objects.get(
            #     id_usulan_topik=item)
            try : 
                get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
            except: 
                class MyObject:
                    def __init__(self):
                        pass

                get_object = MyObject()
                get_object.keterangan_dosen="Belum Ada Catatan"
            usulantopiks[jumlah].keterangan_dosen = get_object.catatan
        except:
            usulantopiks[jumlah].keterangan_dosen = "Belum Ada Catatan"
        jumlah += 1

    return render(request, 'mahasiswa/usulantopik_get.html', {"usulantopiks": usulantopiks, "user_info": user_info})
# Menampilkan usulan topik dengan Filter usulan topik 1 tahun kebelakang
@login_required(login_url="/login")
@role_required(allowed_roles=['Dosen','Admin', 'Kompartemen','Manajemen Departemen','Mahasiswa','Properta'])
def usulantopik_get_1_year(request):
    user_info = user_information(request)
    get_year =datetime.datetime.now().year
    list_1_year=[]
    for item in range (2):
        list_1_year.append(get_year)
        get_year=get_year-1
    if user_info[2].name == "Mahasiswa":
        usulantopiks = usulantopik.objects.filter(tanggal_update__year__in=list_1_year).filter(
            nim=mahasiswa.objects.filter(pk=user_info[0])[0])
        jumlah = 0
        for item in usulantopiks: 
            try:
                try : 
                    get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
                except: 
                    class MyObject:
                        def __init__(self):
                            pass

                    get_object = MyObject()
                    get_object.status_topik="Submit"
                    
                # print(get_object)
                usulantopiks[jumlah].status = get_object.status_topik

            except:
                usulantopiks[jumlah].status = "Submit"
            jumlah+=1


        for item in usulantopiks: 
            # print(item.status, item.status != "ACC")
            if item.status != "ACC":
                usulantopiks=usulantopiks.exclude(id_usulan_topik=item.id_usulan_topik)
        jumlah = 0
        for item in usulantopiks:
            try:
                if evaluasitopik.objects.filter(
                    id_usulan_topik=item).exists():
                    get_object = evaluasitopik.objects.filter(
                        id_usulan_topik=item).first()
                else:
                    get_object.id_dosen_kompartemen = "Belum Di Assign"
                usulantopiks[jumlah].status_dosen_Kompartemen = get_object.id_dosen_kompartemen

            except:
                usulantopiks[jumlah].status_dosen_Kompartemen = "Belum Di Assign"

            try:
                
                try : 
                    get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
                except: 
                    class MyObject:
                        def __init__(self):
                            pass

                    get_object = MyObject()
                    get_object.status_topik="Submit"
                    
                # print(get_object)
                usulantopiks[jumlah].status = get_object.status_topik

            except:
                usulantopiks[jumlah].status = "Submit"
            try:
                if evaluasitopik.objects.filter(status_topik="ACC").filter(
                    id_usulan_topik=item).exists():
                    get_object = evaluasitopik.objects.filter(status_topik="ACC").filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
                else:
                    get_object = evaluasitopik.objects.filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
                usulantopiks[jumlah].keterangan_dosen = get_object.catatan
            except:
                usulantopiks[jumlah].keterangan_dosen = "Belum Ada Catatan"
            jumlah += 1

    else:
        usulantopiks = usulantopik.objects.filter(tanggal_update__year__in=list_1_year)
        jumlah = 0
        for item in usulantopiks: 
            try:
                try : 
                    get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
                except: 
                    class MyObject:
                        def __init__(self):
                            pass

                    get_object = MyObject()
                    get_object.status_topik="Submit"
                    
                # print(get_object)
                usulantopiks[jumlah].status = get_object.status_topik

            except:
                usulantopiks[jumlah].status = "Submit"
            jumlah+=1


        for item in usulantopiks:           
            if item.status != "ACC":
                usulantopiks=usulantopiks.exclude(id_usulan_topik=item.id_usulan_topik)
        jumlah = 0
        for item in usulantopiks:
            try:

                if evaluasitopik.objects.filter(
                    id_usulan_topik=item).exists():
                    get_object = evaluasitopik.objects.filter(
                        id_usulan_topik=item).first()
                    # usulantopiks.exclude(id_usulan_topik=item.id_usulan_topik)
                else:
                    get_object.id_dosen_kompartemen = "Belum Di Assign"
                usulantopiks[jumlah].status_dosen_Kompartemen = get_object.id_dosen_kompartemen

            except:
                usulantopiks[jumlah].status_dosen_Kompartemen = "Belum Di Assign"

            try:
                
                try : 
                    get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
                except: 
                    class MyObject:
                        def __init__(self):
                            pass

                    get_object = MyObject()
                    get_object.status_topik="Submit"
                    
                # print(get_object)
                usulantopiks[jumlah].status = get_object.status_topik

            except:
                usulantopiks[jumlah].status = "Submit"
            try:
                if evaluasitopik.objects.filter(status_topik="ACC").filter(
                    id_usulan_topik=item).exists():
                    get_object = evaluasitopik.objects.filter(status_topik="ACC").filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
                    get_object = evaluasitopik.objects.filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
                usulantopiks[jumlah].keterangan_dosen = get_object.catatan
            except:
                usulantopiks[jumlah].keterangan_dosen = "Belum Ada Catatan"
            jumlah += 1      

    return render(request, 'mahasiswa/usulantopik_get.html', {"usulantopiks": usulantopiks, "user_info": user_info})

# Menampilkan usulan topik dengan Filter belum dapat dosen kompartemen
@login_required(login_url="/login")
@role_required(allowed_roles=['Dosen','Admin', 'Kompartemen','Manajemen Departemen','Mahasiswa','Properta'])
def usulantopik_get_filter_dosen(request):
    user_info = user_information(request)

    if user_info[2].name == "Mahasiswa":
        # try:
        usulantopiks = usulantopik.objects.filter(
            nim=mahasiswa.objects.filter(pk=user_info[0])[0])
        jumlah = 0
        for item in usulantopiks: 
            try:
                if evaluasitopik.objects.filter(
                    id_usulan_topik=item).exists():
                    get_object = evaluasitopik.objects.filter(
                        id_usulan_topik=item).first()
                    # usulantopiks.exclude(id_usulan_topik=item.id_usulan_topik)
                else:
                    get_object.id_dosen_kompartemen = "Belum Di Assign"
                usulantopiks[jumlah].status_dosen_Kompartemen = get_object.id_dosen_kompartemen

            except:
                usulantopiks[jumlah].status_dosen_Kompartemen = "Belum Di Assign"
            jumlah+=1


        for item in usulantopiks: 
            # print(item.status_dosen_Kompartemen, item.status_dosen_Kompartemen != "Belum Di Assign")
            # print(usulantopiks[i].status_dosen_Kompartemen)
            if item.status_dosen_Kompartemen != "Belum Di Assign":
                usulantopiks=usulantopiks.exclude(id_usulan_topik=item.id_usulan_topik)


        jumlah = 0
        for item in usulantopiks:
            try:
                if evaluasitopik.objects.filter(
                    id_usulan_topik=item).exists():
                    get_object = evaluasitopik.objects.filter(
                        id_usulan_topik=item).first()
                else:
                    get_object.id_dosen_kompartemen = "Belum Di Assign"
                usulantopiks[jumlah].status_dosen_Kompartemen = get_object.id_dosen_kompartemen

            except:
                usulantopiks[jumlah].status_dosen_Kompartemen = "Belum Di Assign"

            try:
                
                try : 
                    get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
                except: 
                    class MyObject:
                        def __init__(self):
                            pass

                    get_object = MyObject()
                    get_object.status_topik="Submit"
                    
                # print(get_object)
                usulantopiks[jumlah].status = get_object.status_topik

            except:
                usulantopiks[jumlah].status = "Submit"
            try:
                if evaluasitopik.objects.filter(status_topik="ACC").filter(
                    id_usulan_topik=item).exists():
                    get_object = evaluasitopik.objects.filter(status_topik="ACC").filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
                    get_object = evaluasitopik.objects.filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
                usulantopiks[jumlah].keterangan_dosen = get_object.catatan
            except:
                usulantopiks[jumlah].keterangan_dosen = "Belum Ada Catatan"
            jumlah += 1

    else:
        usulantopiks = usulantopik.objects.all()
        jumlah = 0
        for item in usulantopiks: 
            try:
                if evaluasitopik.objects.filter(
                    id_usulan_topik=item).exists():
                    get_object = evaluasitopik.objects.filter(
                        id_usulan_topik=item).first()
                    # usulantopiks.exclude(id_usulan_topik=item.id_usulan_topik)
                else:
                    get_object.id_dosen_kompartemen = "Belum Di Assign"
                usulantopiks[jumlah].status_dosen_Kompartemen = get_object.id_dosen_kompartemen

            except:
                usulantopiks[jumlah].status_dosen_Kompartemen = "Belum Di Assign"
            jumlah+=1


        for item in usulantopiks: 
            # print(item.status_dosen_Kompartemen, item.status_dosen_Kompartemen != "Belum Di Assign")
            # print(usulantopiks[i].status_dosen_Kompartemen)
            if item.status_dosen_Kompartemen != "Belum Di Assign":
                # print("disini")
                usulantopiks=usulantopiks.exclude(id_usulan_topik=item.id_usulan_topik)


        jumlah = 0
        for item in usulantopiks:
            try:

                if evaluasitopik.objects.filter(
                    id_usulan_topik=item).exists():
                    get_object = evaluasitopik.objects.filter(
                        id_usulan_topik=item).first()
                    # usulantopiks.exclude(id_usulan_topik=item.id_usulan_topik)
                else:
                    get_object.id_dosen_kompartemen = "Belum Di Assign"
                usulantopiks[jumlah].status_dosen_Kompartemen = get_object.id_dosen_kompartemen

            except:
                usulantopiks[jumlah].status_dosen_Kompartemen = "Belum Di Assign"

            try:
                try : 
                    get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
                except: 
                    class MyObject:
                        def __init__(self):
                            pass

                    get_object = MyObject()
                    get_object.status_topik="Submit"
                    
                # print(get_object)
                usulantopiks[jumlah].status = get_object.status_topik

            except:
                usulantopiks[jumlah].status = "Submit"
            try:
                if evaluasitopik.objects.filter(status_topik="ACC").filter(
                    id_usulan_topik=item).exists():
                    get_object = evaluasitopik.objects.filter(status_topik="ACC").filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
                else:
                    get_object = evaluasitopik.objects.filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
                usulantopiks[jumlah].keterangan_dosen = get_object.catatan
            except:
                usulantopiks[jumlah].keterangan_dosen = "Belum Ada Catatan"
            jumlah += 1
    return render(request, 'mahasiswa/usulantopik_get.html', {"usulantopiks": usulantopiks, "user_info": user_info})
# Menampilkan usulan topik dengan Filter belum dapat dosen pembimbing
@login_required(login_url="/login")
@role_required(allowed_roles=['Dosen','Admin', 'Kompartemen','Manajemen Departemen','Mahasiswa','Properta'])
def usulantopik_get_filter_dosen_pembimbing(request):
    user_info = user_information(request)
    roledosen_data=roledosen.objects.filter(role="Pembimbing 1").values_list("nim")|roledosen.objects.filter(role="Pembimbing 2").values_list("nim")
    # print(roledosen_data)
    roledosen_data.distinct()
    list_sudah_pembimbing=[]
    for i in range(len(roledosen_data)):
        list_sudah_pembimbing.append(roledosen_data[i][0])
    # print(list_sudah_pembimbing)
    
    if user_info[2].name == "Mahasiswa":
        usulantopiks = usulantopik.objects.filter(
            nim=mahasiswa.objects.filter(pk=user_info[0])[0])
        usulantopiks=usulantopiks.exclude(nim__in=list_sudah_pembimbing)
        jumlah = 0
        for item in usulantopiks: 
            try:
                try : 
                    get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
                except: 
                    class MyObject:
                        def __init__(self):
                            pass

                    get_object = MyObject()
                    get_object.status_topik="Submit"
                    
                # print(get_object)
                usulantopiks[jumlah].status = get_object.status_topik

            except:
                usulantopiks[jumlah].status = "Submit"
            jumlah+=1


        for item in usulantopiks: 
            # print(item.status, item.status == "ACC")
            if item.status != "ACC":
                usulantopiks=usulantopiks.exclude(id_usulan_topik=item.id_usulan_topik)
        
        jumlah = 0
        for item in usulantopiks:
            try:
                if evaluasitopik.objects.filter(
                    id_usulan_topik=item).exists():
                    get_object = evaluasitopik.objects.filter(
                        id_usulan_topik=item).first()
                else:
                    get_object.id_dosen_kompartemen = "Belum Di Assign"
                usulantopiks[jumlah].status_dosen_Kompartemen = get_object.id_dosen_kompartemen

            except:
                usulantopiks[jumlah].status_dosen_Kompartemen = "Belum Di Assign"

            try:
                try : 
                    get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
                except: 
                    class MyObject:
                        def __init__(self):
                            pass

                    get_object = MyObject()
                    get_object.status_topik="Submit"
                    
                # print(get_object)
                usulantopiks[jumlah].status = get_object.status_topik

            except:
                usulantopiks[jumlah].status = "Submit"
            try:
                if evaluasitopik.objects.filter(status_topik="ACC").filter(
                    id_usulan_topik=item).exists():
                    get_object = evaluasitopik.objects.filter(status_topik="ACC").filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
                else:
                    get_object = evaluasitopik.objects.filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
                usulantopiks[jumlah].keterangan_dosen = get_object.catatan
            except:
                usulantopiks[jumlah].keterangan_dosen = "Belum Ada Catatan"
            jumlah += 1

    else:
        usulantopiks = usulantopik.objects.all()
        usulantopiks=usulantopiks.exclude(nim__in=list_sudah_pembimbing)
        jumlah = 0
        for item in usulantopiks: 
            try:
                try : 
                    get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
                except: 
                    class MyObject:
                        def __init__(self):
                            pass

                    get_object = MyObject()
                    get_object.status_topik="Submit"
                    
                # print(get_object)
                usulantopiks[jumlah].status = get_object.status_topik

            except:
                usulantopiks[jumlah].status = "Submit"
            jumlah+=1


        for item in usulantopiks:
                       
            if item.status != "ACC":
                usulantopiks=usulantopiks.exclude(id_usulan_topik=item.id_usulan_topik)
        jumlah = 0
        for item in usulantopiks:
            try:

                if evaluasitopik.objects.filter(
                    id_usulan_topik=item).exists():
                    get_object = evaluasitopik.objects.filter(
                        id_usulan_topik=item).first()
                    # usulantopiks.exclude(id_usulan_topik=item.id_usulan_topik)
                else:
                    get_object.id_dosen_kompartemen = "Belum Di Assign"
                usulantopiks[jumlah].status_dosen_Kompartemen = get_object.id_dosen_kompartemen

            except:
                usulantopiks[jumlah].status_dosen_Kompartemen = "Belum Di Assign"

            try:
                try : 
                    get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
                except: 
                    class MyObject:
                        def __init__(self):
                            pass

                    get_object = MyObject()
                    get_object.status_topik="Submit"
                    
                # print(get_object)
                usulantopiks[jumlah].status = get_object.status_topik

            except:
                usulantopiks[jumlah].status = "Submit"
            try:
                if evaluasitopik.objects.filter(status_topik="ACC").filter(
                    id_usulan_topik=item).exists():
                    get_object = evaluasitopik.objects.filter(status_topik="ACC").filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
                else:
                    get_object = evaluasitopik.objects.filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
                usulantopiks[jumlah].keterangan_dosen = get_object.catatan
            except:
                usulantopiks[jumlah].keterangan_dosen = "Belum Ada Catatan"
            jumlah += 1      
    return render(request, 'mahasiswa/usulantopik_get.html', {"usulantopiks": usulantopiks, "user_info": user_info})
# Menampilkan usulan topik dengan Filter sudah di revisi
@login_required(login_url="/login")
@role_required(allowed_roles=['Dosen','Admin', 'Kompartemen','Manajemen Departemen','Mahasiswa','Properta'])
def usulantopik_get_filter_ACC(request):
    user_info = user_information(request)

    if user_info[2].name == "Mahasiswa":
        usulantopiks = usulantopik.objects.filter(
            nim=mahasiswa.objects.filter(pk=user_info[0])[0])
        jumlah = 0
        for item in usulantopiks: 
            try:
                try : 
                    get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
                except: 
                    class MyObject:
                        def __init__(self):
                            pass

                    get_object = MyObject()
                    get_object.status_topik="Submit"
                    
                # print(get_object)
                usulantopiks[jumlah].status = get_object.status_topik

            except:
                usulantopiks[jumlah].status = "Submit"
            jumlah+=1


        for item in usulantopiks: 
            # print(item.status, item.status == "ACC")
            if item.status == "ACC" or item.status == "Revisi" or item.status == "Revisi" :
                usulantopiks=usulantopiks.exclude(id_usulan_topik=item.id_usulan_topik)
                
        jumlah = 0
        for item in usulantopiks:
            try:
                if evaluasitopik.objects.filter(
                    id_usulan_topik=item).exists():
                    get_object = evaluasitopik.objects.filter(
                        id_usulan_topik=item).first()
                else:
                    get_object.id_dosen_kompartemen = "Belum Di Assign"
                usulantopiks[jumlah].status_dosen_Kompartemen = get_object.id_dosen_kompartemen

            except:
                usulantopiks[jumlah].status_dosen_Kompartemen = "Belum Di Assign"

            try:
                try : 
                    get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
                except: 
                    class MyObject:
                        def __init__(self):
                            pass

                    get_object = MyObject()
                    get_object.status_topik="Submit"
                    
                # print(get_object)
                usulantopiks[jumlah].status = get_object.status_topik

            except:
                usulantopiks[jumlah].status = "Submit"
            try:
                if evaluasitopik.objects.filter(status_topik="ACC").filter(
                    id_usulan_topik=item).exists():
                    get_object = evaluasitopik.objects.filter(status_topik="ACC").filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
                else:
                    get_object = evaluasitopik.objects.filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
                usulantopiks[jumlah].keterangan_dosen = get_object.catatan
            except:
                usulantopiks[jumlah].keterangan_dosen = "Belum Ada Catatan"
            jumlah += 1
    
    else:
        usulantopiks = usulantopik.objects.all()
        jumlah = 0
        for item in usulantopiks: 
            try:
                try : 
                    get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
                except: 
                    class MyObject:
                        def __init__(self):
                            pass

                    get_object = MyObject()
                    get_object.status_topik="Submit"
                    
                # print(get_object)
                usulantopiks[jumlah].status = get_object.status_topik

            except:
                usulantopiks[jumlah].status = "Submit"
            jumlah+=1


        for item in usulantopiks:           
            if item.status == "ACC" or item.status == "Revisi" :
                usulantopiks=usulantopiks.exclude(id_usulan_topik=item.id_usulan_topik)
        jumlah = 0
        for item in usulantopiks:
            try:

                if evaluasitopik.objects.filter(
                    id_usulan_topik=item).exists():
                    get_object = evaluasitopik.objects.filter(
                        id_usulan_topik=item).first()
                    # usulantopiks.exclude(id_usulan_topik=item.id_usulan_topik)
                else:
                    get_object.id_dosen_kompartemen = "Belum Di Assign"
                usulantopiks[jumlah].status_dosen_Kompartemen = get_object.id_dosen_kompartemen

            except:
                usulantopiks[jumlah].status_dosen_Kompartemen = "Belum Di Assign"

            try:
                try : 
                    get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
                except: 
                    class MyObject:
                        def __init__(self):
                            pass

                    get_object = MyObject()
                    get_object.status_topik="Submit"
                    
                # print(get_object)
                usulantopiks[jumlah].status = get_object.status_topik

            except:
                usulantopiks[jumlah].status = "Submit"
            try:
                if evaluasitopik.objects.filter(status_topik="ACC").filter(
                    id_usulan_topik=item).exists():
                    get_object = evaluasitopik.objects.filter(status_topik="ACC").filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
                else:
                    get_object = evaluasitopik.objects.filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
                usulantopiks[jumlah].keterangan_dosen = get_object.catatan
            except:
                usulantopiks[jumlah].keterangan_dosen = "Belum Ada Catatan"
            jumlah += 1      
    return render(request, 'mahasiswa/usulantopik_get.html', {"usulantopiks": usulantopiks, "user_info": user_info})


# Menampilkan usulan topik dengan Filter Belum ACC untuk role kompartemen
# @permission_required(allowed_roles=['Admin', 'Kompartemen','Properta'])
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Kompartemen','Properta'])
def usulantopik_get_filter_revisi_kompartemen(request):
    user_info = user_information(request)
    evaluasitopiks_list=list(evaluasitopik.objects.filter(id_dosen_kompartemen__nip__nip=user_info[0]).values_list("id_usulan_topik",flat=True))
    usulantopiks = usulantopik.objects.filter(id_usulan_topik__in=evaluasitopiks_list)
    jumlah = 0
    for item in usulantopiks: 
        try:
            
            try : 
                get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
            except: 
                class MyObject:
                    def __init__(self):
                        pass

                get_object = MyObject()
                get_object.status_topik="Submit"
                
            # print(get_object)
            usulantopiks[jumlah].status = get_object.status_topik

        except:
            usulantopiks[jumlah].status = "Submit"
        jumlah+=1


    for item in usulantopiks: 
        print(item.status, item.status == "ACC")
        if item.status == "ACC" or item.status == "Revisi" :
            usulantopiks=usulantopiks.exclude(id_usulan_topik=item.id_usulan_topik)
            
    jumlah = 0
    for item in usulantopiks:
        try:
            if evaluasitopik.objects.filter(
                id_usulan_topik=item).exists():
                get_object = evaluasitopik.objects.filter(
                    id_usulan_topik=item).first()
            else:
                get_object.id_dosen_kompartemen = "Belum Di Assign"
            usulantopiks[jumlah].status_dosen_Kompartemen = get_object.id_dosen_kompartemen

        except:
            usulantopiks[jumlah].status_dosen_Kompartemen = "Belum Di Assign"

        try:
                
                try : 
                    get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
                except: 
                    class MyObject:
                        def __init__(self):
                            pass

                    get_object = MyObject()
                    get_object.status_topik="Submit"
                    
                # print(get_object)
                usulantopiks[jumlah].status = get_object.status_topik

        except:
                usulantopiks[jumlah].status = "Submit"
        try:
            if evaluasitopik.objects.filter(status_topik="ACC").filter(
                id_usulan_topik=item).exists():
                get_object = evaluasitopik.objects.filter(status_topik="ACC").filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
            else:
                get_object = evaluasitopik.objects.filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
            usulantopiks[jumlah].keterangan_dosen = get_object.catatan
        except:
            usulantopiks[jumlah].keterangan_dosen = "Belum Ada Catatan"
        jumlah += 1
   
    return render(request, 'mahasiswa/usulantopik_get.html', {"usulantopiks": usulantopiks, "user_info": user_info})

# Menampilkan usulan topik dengan Filter Belum ACC untuk role kompartemen
# @permission_required(allowed_roles=['Admin', 'Kompartemen','Properta'])
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Kompartemen','Properta'])
def usulantopik_get_filter_ACC_kompartemen(request):
    user_info = user_information(request)
    evaluasitopiks_list=list(evaluasitopik.objects.filter(id_dosen_kompartemen__nip__nip=user_info[0]).values_list("id_usulan_topik",flat=True))
    usulantopiks = usulantopik.objects.filter(id_usulan_topik__in=evaluasitopiks_list)
    jumlah = 0
    for item in usulantopiks: 
        try:
            
            try : 
                get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
            except: 
                class MyObject:
                    def __init__(self):
                        pass

                get_object = MyObject()
                get_object.status_topik="Submit"
                
            # print(get_object)
            usulantopiks[jumlah].status = get_object.status_topik

        except:
            usulantopiks[jumlah].status = "Submit"
        jumlah+=1


    for item in usulantopiks: 
        # print(item.status, item.status == "ACC")
        if item.status == "ACC" :
            usulantopiks=usulantopiks.exclude(id_usulan_topik=item.id_usulan_topik)
            
    jumlah = 0
    for item in usulantopiks:
        try:
            if evaluasitopik.objects.filter(
                id_usulan_topik=item).exists():
                get_object = evaluasitopik.objects.filter(
                    id_usulan_topik=item).first()
            else:
                get_object.id_dosen_kompartemen = "Belum Di Assign"
            usulantopiks[jumlah].status_dosen_Kompartemen = get_object.id_dosen_kompartemen

        except:
            usulantopiks[jumlah].status_dosen_Kompartemen = "Belum Di Assign"

        try:
                
                try : 
                    get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
                except: 
                    class MyObject:
                        def __init__(self):
                            pass

                    get_object = MyObject()
                    get_object.status_topik="Submit"
                    
                # print(get_object)
                usulantopiks[jumlah].status = get_object.status_topik

        except:
                usulantopiks[jumlah].status = "Submit"
        try:
            if evaluasitopik.objects.filter(status_topik="ACC").filter(
                id_usulan_topik=item).exists():
                get_object = evaluasitopik.objects.filter(status_topik="ACC").filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
            else:
                get_object = evaluasitopik.objects.filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
            usulantopiks[jumlah].keterangan_dosen = get_object.catatan
        except:
            usulantopiks[jumlah].keterangan_dosen = "Belum Ada Catatan"
        jumlah += 1
   
    return render(request, 'mahasiswa/usulantopik_get.html', {"usulantopiks": usulantopiks, "user_info": user_info})

# Menampilkan usulan topik dengan Filter dosen yang mengevaluasi untuk role kompartemen
# @permission_required(['Admin', 'Kompartemen','Properta'])
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Kompartemen','Properta'])
def usulantopik_get_filter_kompartemen(request):
    user_info = user_information(request)
    evaluasitopiks_list=list(evaluasitopik.objects.filter(id_dosen_kompartemen__nip__nip=user_info[0]).values_list("id_usulan_topik",flat=True))
    usulantopiks = usulantopik.objects.filter(id_usulan_topik__in=evaluasitopiks_list)

            
    jumlah = 0
    for item in usulantopiks:
        try:
            if evaluasitopik.objects.filter(
                id_usulan_topik=item).exists():
                get_object = evaluasitopik.objects.filter(
                    id_usulan_topik=item).first()
            else:
                get_object.id_dosen_kompartemen = "Belum Di Assign"
            usulantopiks[jumlah].status_dosen_Kompartemen = get_object.id_dosen_kompartemen

        except:
            usulantopiks[jumlah].status_dosen_Kompartemen = "Belum Di Assign"

        try:   
            try : 
                get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
            except: 
                class MyObject:
                    def __init__(self):
                        pass

                get_object = MyObject()
                get_object.status_topik="Submit"
                
            # print(get_object)
            usulantopiks[jumlah].status = get_object.status_topik

        except:
            usulantopiks[jumlah].status = "Submit"
        try:
            if evaluasitopik.objects.filter(status_topik="ACC").filter(
                id_usulan_topik=item).exists():
                get_object = evaluasitopik.objects.filter(status_topik="ACC").filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
            else:
                get_object = evaluasitopik.objects.filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
            usulantopiks[jumlah].keterangan_dosen = get_object.catatan
        except:
            usulantopiks[jumlah].keterangan_dosen = "Belum Ada Catatan"
        jumlah += 1
   
    return render(request, 'mahasiswa/usulantopik_get.html', {"usulantopiks": usulantopiks, "user_info": user_info})

# Menampilkan usulan topik dengan Filter mahasiswa bimbingan untuk dosen pembimbing 
@login_required(login_url="/login")
@role_required(allowed_roles=['Dosen','Admin', 'Kompartemen','Manajemen Departemen','Properta'])
# @permission_required(allowed_roles=['Dosen','Manajemen Departemen','Admin', 'Kompartemen','Properta'])
def usulantopik_getfilter_dosen(request):
    user_info = user_information(request)
    roledosen_cek=roledosen.objects.filter(status="Active").filter(role="Pembimbing 1").filter(nip__nip=user_info[0])|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2").filter(nip__nip=user_info[0])
    roledosen_list=list(roledosen_cek.values_list("nim__nim",flat=True))
    # .values_list("id_usulan_topik",flat=True)
    usulantopiks = usulantopik.objects.filter(nim__nim__in=roledosen_list)

            
    jumlah = 0
    for item in usulantopiks:
        try:
            if evaluasitopik.objects.filter(
                id_usulan_topik=item).exists():
                get_object = evaluasitopik.objects.filter(
                    id_usulan_topik=item).first()
            else:
                get_object.id_dosen_kompartemen = "Belum Di Assign"
            usulantopiks[jumlah].status_dosen_Kompartemen = get_object.id_dosen_kompartemen

        except:
            usulantopiks[jumlah].status_dosen_Kompartemen = "Belum Di Assign"
        try:  
            try : 
                get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
            except: 
                class MyObject:
                    def __init__(self):
                        pass

                get_object = MyObject()
                get_object.status_topik="Submit"
                
            # print(get_object)
            usulantopiks[jumlah].status = get_object.status_topik

        except:
            usulantopiks[jumlah].status = "Submit"
        try:
            if evaluasitopik.objects.filter(status_topik="ACC").filter(
                id_usulan_topik=item).exists():
                get_object = evaluasitopik.objects.filter(status_topik="ACC").filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
            else:
                get_object = evaluasitopik.objects.filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
            usulantopiks[jumlah].keterangan_dosen = get_object.catatan
        except:
            usulantopiks[jumlah].keterangan_dosen = "Belum Ada Catatan"
        jumlah += 1
   
    return render(request, 'mahasiswa/usulantopik_get.html', {"usulantopiks": usulantopiks, "user_info": user_info})
# Menampilkan usulan topik dengan Filter ACC mahasiswa bimbingan untuk dosen pembimbing 
@login_required(login_url="/login")
@role_required(allowed_roles=['Dosen','Admin', 'Kompartemen','Manajemen Departemen','Properta'])
def usulantopik_get_filter_ACC_dosen(request):
    user_info = user_information(request)
    roledosen_cek=roledosen.objects.filter(status="Active").filter(role="Pembimbing 1").filter(nip__nip=user_info[0])|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2").filter(nip__nip=user_info[0])
    roledosen_list=list(roledosen_cek.values_list("nim__nim",flat=True))
    # .values_list("id_usulan_topik",flat=True)
    usulantopiks = usulantopik.objects.filter(nim__nim__in=roledosen_list)
    jumlah = 0
    for item in usulantopiks: 
        try:
            try : 
                get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
            except: 
                class MyObject:
                    def __init__(self):
                        pass

                get_object = MyObject()
                get_object.status_topik="Submit"
                
            # print(get_object)
            usulantopiks[jumlah].status = get_object.status_topik

        except:
            usulantopiks[jumlah].status = "Submit"
        jumlah+=1


    for item in usulantopiks: 
        # print(item.status, item.status == "ACC")
        if item.status != "ACC" :
            usulantopiks=usulantopiks.exclude(id_usulan_topik=item.id_usulan_topik)
            
    jumlah = 0
    for item in usulantopiks:
        try:
            if evaluasitopik.objects.filter(
                id_usulan_topik=item).exists():
                get_object = evaluasitopik.objects.filter(
                    id_usulan_topik=item).first()
            else:
                get_object.id_dosen_kompartemen = "Belum Di Assign"
            usulantopiks[jumlah].status_dosen_Kompartemen = get_object.id_dosen_kompartemen

        except:
            usulantopiks[jumlah].status_dosen_Kompartemen = "Belum Di Assign"

        try:
            try : 
                get_object = evaluasitopik.objects.filter(id_usulan_topik=item).order_by('tanggal_update').last()
            except: 
                class MyObject:
                    def __init__(self):
                        pass

                get_object = MyObject()
                get_object.status_topik="Submit"
                
            # print(get_object)
            usulantopiks[jumlah].status = get_object.status_topik

        except:
            usulantopiks[jumlah].status = "Submit"
        try:
            if evaluasitopik.objects.filter(status_topik="ACC").filter(
                id_usulan_topik=item).exists():
                get_object = evaluasitopik.objects.filter(status_topik="ACC").filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
            else:
                get_object = evaluasitopik.objects.filter(
                id_usulan_topik=item).order_by("-tanggal_update").first()
            usulantopiks[jumlah].keterangan_dosen = get_object.catatan
        except:
            usulantopiks[jumlah].keterangan_dosen = "Belum Ada Catatan"
        jumlah += 1
   
    return render(request, 'mahasiswa/usulantopik_get.html', {"usulantopiks": usulantopiks, "user_info": user_info})

# Usulan Topik:Update
# Update data Usulan Topik oleh Mahasiswa  berdasarkan id usulan topik
# todo: add in notification and email
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Mahasiswa','Properta'])
# @permission_required("skripsi_app.change_dosen", raise_exception=True)
def usulantopik_update(request, id):
    user_info = user_information(request)
    if user_info[2].name == "Mahasiswa":
        usulantopik_data = usulantopik.objects.get(
            pk=id, nim=user_info[0])

        if request.method == "POST":
            form = UsulanTopikForm(
                request.POST, request.FILES, instance=usulantopik_data)
            if form.is_valid():
                create_usulantopik = form.save()
                instances = evaluasitopik.objects.filter(id_usulan_topik=usulantopik_data.id_usulan_topik).order_by('tanggal_buat')
                if instances.exists(): # Pastikan QuerySet tidak kosong
                    instances.update(status_topik='Revisi') # Mengubah status untuk semua objek

                    # Mengubah status objek pertama menjadi "Submit"
                    # print(instances)
                    # print(instances.values_list("tanggal_update"))
                    first_instance = instances.order_by('-tanggal_update').first()
                    # print(first_instance.tanggal_buat)
                    first_instance.status_topik = 'Submit'
                    first_instance.save()
                create_usulantopik.save()
                messages.warning(request,"Data Usulan Topik Telah Berhasil Diperbarui! ")
                # contoh : notif tambah if udah ada kompartemen 
                
                evaluasitopik_data=evaluasitopik.objects.filter(id_usulan_topik=usulantopik_data.id_usulan_topik).first()
                evaluasitopik_data_exist=evaluasitopik.objects.filter(id_usulan_topik=usulantopik_data.id_usulan_topik).exists()
                if evaluasitopik_data_exist==False:
                    
                    try : 
                        user_dsn=dosen.objects.filter(nip=create_usulantopik.id_dosen_kompartemen.nip.nip)
                        email_list=[]
                        # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
                        for i in user_dsn:
                            # print(i)
                            temp_email=list(User.objects.filter(pk=i.id_user.id).values_list('email'))
                            email_list.append(temp_email[0][0])
                            notifikasi.objects.create(nip=i.nip,messages=f"Terdapat Update Usulan Topik Baru Oleh {create_usulantopik.nim} dengan judul {create_usulantopik.judul_topik} pada {tanggal} Jam {Jam}")
                        # send ke mahasiswa
                        # print(user_mhs)
                        # email_list=User.objects.filter(pk=user_mhs[0].id_user.id).values_list('email',flat=True)
                        # print(email_list)
                        send_mail(
                            'Update Evaluasi Usulan Topik',
                            f"Terdapat Update Usulan Topik Baru Oleh {create_usulantopik.nim} dengan judul {create_usulantopik.judul_topik} pada {tanggal} Jam {Jam}",
                            settings.EMAIL_HOST_USER,
                            email_list,
                            fail_silently=False,
                        )
                    except :
                        pass

                    # # user_sekdept=list(User.objects.values_list('email').filter(groups__name='Manajemen Departemen'))
                    # user_sekdept=list(User.objects.values_list('id').filter(groups__name='Manajemen Departemen'))
                    # sekdept_filter=dosen.objects.filter(id_user__in=user_sekdept)
                    # for i in sekdept_filter:
                    #     notifikasi.objects.create(nip=i.nip,messages=f"Terdapat Update Usulan Topik Baru Oleh {create_usulantopik.nim} dengan judul {create_usulantopik.judul_topik} pada {tanggal} Jam {Jam}")
                    # # send ke properta
                    # # email_list=User.objects.filter(groups__name='Properta').values_list('email')
                    # email_list=[]
                    # # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    # temp_email=list(User.objects.filter(groups__name='Properta').values_list('email'))
                    # for i in range(len(temp_email)):
                    #     email_list.append(temp_email[i][0])
                    # send_mail(
                    #     'Update Usulan Topik ',
                    #     f"Terdapat Update Usulan Topik Baru Oleh {create_usulantopik.nim} dengan judul {create_usulantopik.judul_topik} pada {tanggal} Jam {Jam}",
                    #     settings.EMAIL_HOST_USER,
                    #     email_list,
                    #     fail_silently=False,
                    # )
                    # # send ke sekdept
                    # # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    # email_list=[]
                    # # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    # temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
                    # for i in range(len(temp_email)):
                    #     email_list.append(temp_email[i][0])
                    # send_mail(
                    #     'Update Usulan Topik',
                    #     f"Terdapat Update Usulan Topik Baru Oleh {create_usulantopik.nim} dengan judul {create_usulantopik.judul_topik} pada {tanggal} Jam {Jam}",
                    #     settings.EMAIL_HOST_USER,
                    #     email_list,
                    #     fail_silently=False,
                    # )
                else : 
                    # klo perlu update status klo usulan di update
                    # evaluasitopik.objects.filter(id_usulan_topik=id).update(status_topik='Dalam Evaluasi')

                    
                    try : 
                        user_dsn=dosen.objects.filter(nip=create_usulantopik.id_dosen_kompartemen.nip.nip)
                        email_list=[]
                        # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
                        for i in user_dsn:
                            # print(i)
                            temp_email=list(User.objects.filter(pk=i.id_user.id).values_list('email'))
                            email_list.append(temp_email[0][0])
                            notifikasi.objects.create(nip=i.nip,messages=f"Terdapat Update Usulan Topik Baru Oleh {create_usulantopik.nim} dengan judul {create_usulantopik.judul_topik} pada {tanggal} Jam {Jam}")
                        # send ke mahasiswa
                        # print(user_mhs)
                        # email_list=User.objects.filter(pk=user_mhs[0].id_user.id).values_list('email',flat=True)
                        # print(email_list)
                        send_mail(
                            'Update Evaluasi Usulan Topik',
                            f"Terdapat Update Usulan Topik Baru Oleh {create_usulantopik.nim} dengan judul {create_usulantopik.judul_topik} pada {tanggal} Jam {Jam}",
                            settings.EMAIL_HOST_USER,
                            email_list,
                            fail_silently=False,
                        )
                    except :
                        pass
                    # user_dosen=dosen.objects.filter(nip=evaluasitopik_data.id_dosen_kompartemen.nip.nip)

                    # # sekdept_filter=dosen.object.filter(id_user__in=userdose)
                    # for i in user_dosen:
                    #     notifikasi.objects.create(nip=i.nip,messages=f"Terdapat Update Usulan Topik Baru Oleh {create_usulantopik.nim} dengan judul {create_usulantopik.judul_topik} pada {tanggal} Jam {Jam}")
                    # # send ke properta
                    # email_list=[]
                    # # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    # temp_email=list(User.objects.filter(groups__name='Properta').values_list('email'))
                    # for i in range(len(temp_email)):
                    #     email_list.append(temp_email[i][0])
                    # # email_list=User.objects.filter(groups__name='Properta').values_list('email')
                    # send_mail(
                    #     'Update Usulan Topik ',
                    #     f"Terdapat Update Usulan Topik Baru Oleh {create_usulantopik.nim} dengan judul {create_usulantopik.judul_topik} pada {tanggal} Jam {Jam}",
                    #     settings.EMAIL_HOST_USER,
                    #     email_list,
                    #     fail_silently=False,
                    # )
                    # # send ke sekdept
                    # email_list=[]
                    # # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    # temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
                    # for i in range(len(temp_email)):
                    #     email_list.append(temp_email[i][0])
                    # # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    # send_mail(
                    #     'Update Usulan Topik',
                    #     f"Terdapat Update Usulan Topik Baru Oleh {create_usulantopik.nim} dengan judul {create_usulantopik.judul_topik} pada {tanggal} Jam {Jam}",
                    #     settings.EMAIL_HOST_USER,
                    #     email_list,
                    #     fail_silently=False,
                    # )
                return redirect("../usulantopikget")
        else:
            form = UsulanTopikForm(instance=usulantopik_data)
    else:
        usulantopik_data = usulantopik.objects.get(pk=id)
        if request.method == "POST":
            form = UsulanTopikFormFull(
                request.POST, request.FILES, instance=usulantopik_data)
            if form.is_valid():
                create_usulan = form.save(commit=False)

                instances = evaluasitopik.objects.filter(id_usulan_topik=usulantopik_data.id_usulan_topik).order_by('tanggal_buat')
                if instances.exists(): # Pastikan QuerySet tidak kosong
                    instances.update(status_topik='Revisi') # Mengubah status untuk semua objek

                    # Mengubah status objek pertama menjadi "Submit"
                    # print(instances)
                    # print(instances.values_list("tanggal_update"))
                    first_instance = instances.order_by('-tanggal_update').first()
                    # print(first_instance.tanggal_buat)
                    first_instance.status_topik = 'Submit'
                    first_instance.save()
                    
                create_usulan.save()
                messages.warning(request,"Data Usulan Topik Telah Berhasil Diperbarui! ")
                return redirect("../usulantopikget")
        else:
            form = UsulanTopikFormFull(instance=usulantopik_data)
    return render(request, 'mahasiswa/usulantopik_update.html', {"form": form, "user_info": user_info})

# tambahain notif ga
# Usulan Topik:delete
# Hapus data Usulan Topik oleh Mahasiswa berdasarkan id usulan topik 
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Mahasiswa','Properta'])
def usulantopik_delete(request, id):
    delete_data = usulantopik.objects.get(pk=id)
    messages.error(request,"Data Usulan Topik Telah Berhasil Dihapus! ")
    delete_data.delete()
    return redirect('../usulantopikget')

# Evaluasi Topik 
# Evaluasi Topik:create
# Pembuatan data Evaluasi Topik oleh DOSEN Kompartemen > Untuk Evaluasi Topik
# todo: add in notification and email
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Kompartemen','Manajemen Departemen','Properta'])
def evaluasitopik_create(request):
    user_info = user_information(request)

    if user_info[2].name == "Kompartemen":
        if request.method == "POST":
            form = EvaluasiTopikFormKompartemen(request.POST, request.FILES)
            if form.is_valid():
                create_usulan = form.save(commit=False)
                create_usulan.save()
                messages.success(request,"Data Evaluasi Topik Telah Berhasil Dibuat! ")
                 # todo notif
                user_mhs=mahasiswa.objects.filter(nim=create_usulan.id_usulan_topik.nim.nim)
                # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
                for i in user_mhs:
                    notifikasi.objects.create(nim=i.nim,messages=f"Terdapat Evaluasi Usulan Topik Baru Oleh {create_usulan.id_dosen_kompartemen.nip.id_user.first_name} pada {tanggal} Jam {Jam}")
                # send ke mahasiswa
                email_list=User.objects.filter(pk=user_mhs[0].id_user.id).values_list('email',flat=True)
                send_mail(
                    'Evaluasi Usulan Topik Baru ',
                    f"Terdapat Evaluasi Usulan Topik Baru Oleh {create_usulan.id_dosen_kompartemen.nip.id_user.first_name} pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                )
                cek_roledosen=roledosen.objects.filter(nim=create_usulan.id_usulan_topik.nim).filter(role="Pembimbing 1")|roledosen.objects.filter(nim=create_usulan.id_usulan_topik.nim).filter(role="Pembimbing 2")
                if cek_roledosen.exists():
                    pass
                else :
                    # send ke sekdept
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    email_list=[]
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
                    for i in range(len(temp_email)):
                        email_list.append(temp_email[i][0])
                    send_mail(
                        'Update Usulan Topik',
                        f"Terdapat Mahasiswa ACC Usulan Topik Baru Oleh {create_usulan.nim} dengan judul {create_usulan.judul_topik} pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                    )

                return redirect("../usulantopik_get_filter_ACC/kompartemen")
        else:
            form = EvaluasiTopikFormKompartemen()
    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        if request.method == "POST":
            form = EvaluasiTopikFormFull(request.POST, request.FILES)
            # if evaluasitopik.objects.filter(id_usulan_topik=request.id_usulan_topik).filter(role=request.role).exists():
            #     return redirect("../roledosenmax")
            if form.is_valid():
                create_usulan = form.save(commit=False)
                create_usulan.save()
                messages.success(request,"Data Evaluasi Topik Telah Berhasil Dibuat! ")
                # contoh : notif
                # todo notif
                email_list=[]
                user_mhs=mahasiswa.objects.filter(nim=create_usulan.id_usulan_topik.nim.nim)
                # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
                for i in user_mhs:
                    temp_email=list(User.objects.filter(pk=i.id_user.id).values_list('email'))
                    email_list.append(temp_email[0][0])
                    notifikasi.objects.create(nim=i.nim,messages=f"Terdapat Evaluasi Usulan Topik Baru Oleh {create_usulan.id_dosen_kompartemen.nip.id_user.first_name} pada {tanggal} Jam {Jam}")
                # send ke mahasiswa
                # email_list=User.objects.filter(pk=user_mhs[0].id_user.id).values_list('email',flat=True)
                send_mail(
                    'Evaluasi Usulan Topik Baru ',
                    f"Terdapat Evaluasi Usulan Topik Baru Oleh {create_usulan.id_dosen_kompartemen.nip.id_user.first_name} pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                )
                cek_roledosen=roledosen.objects.filter(nim=create_usulan.id_usulan_topik.nim).filter(role="Pembimbing 1")|roledosen.objects.filter(nim=create_usulan.id_usulan_topik.nim).filter(role="Pembimbing 2")
                if cek_roledosen.exists():
                    pass
                else :
                    # send ke sekdept
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    email_list=[]
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
                    for i in range(len(temp_email)):
                        email_list.append(temp_email[i][0])
                    send_mail(
                        'Update Usulan Topik',
                        f"Terdapat Mahasiswa ACC Usulan Topik Baru Oleh {create_usulan.nim} dengan judul {create_usulan.judul_topik} pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                    )
                return redirect("../evaluasitopikget")
        else:
            form = EvaluasiTopikFormFull()
    else :
        raise PermissionDenied

    return render(request, 'dosen/evaluasitopik_create.html', {"form": form, "user_info": user_info})
# Mebuat evaluasi topik berdasarkan usulan topik 
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Kompartemen', 'Manajemen Departemen','Properta'])
def evaluasitopik_create_id_usulan(request,id):
    user_info = user_information(request)
    usulantopiks=usulantopik.objects.get(id_usulan_topik=id)
    # "Menunggu Dosen Kompartemen"
    evaluasitopiks=evaluasitopik.objects.filter(id_usulan_topik=id).first()
    if user_info[2].name == "Kompartemen":
        if request.method == "POST":
            form = EvaluasiTopikFormKompartemen(request.POST, request.FILES)
            if form.is_valid():
                create_usulan = form.save(commit=False)
                create_usulan.id_usulan_topik=usulantopiks
                create_usulan.id_dosen_kompartemen=evaluasitopiks.id_dosen_kompartemen
                evaluasitopiks_delete_assign=evaluasitopik.objects.filter(id_usulan_topik=id).filter(status_topik="Menunggu Dosen Kompartemen")
                evaluasitopiks_delete_assign.delete()
                instances = evaluasitopik.objects.filter(id_usulan_topik=create_usulan.id_usulan_topik.id_usulan_topik).order_by('tanggal_buat')
                if instances.exists(): # Pastikan QuerySet tidak kosong
                    instances.update(status_topik='Revisi') # Mengubah status untuk semua objek

                    # Mengubah status objek pertama menjadi "Submit"
                    # print(instances)
                    # print(instances.values_list("tanggal_update"))
                    # first_instance = instances.order_by('-tanggal_update').first()
                    # # print(first_instance.tanggal_buat)
                    # first_instance.status_topik = 'Revisi'
                    # first_instance.save()
                create_usulan.save()
                
                messages.success(request,"Data Evaluasi Topik Telah Berhasil Dibuat! ")
                 # todo notif
                user_mhs=mahasiswa.objects.filter(nim=create_usulan.id_usulan_topik.nim.nim)
                # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
                for i in user_mhs:
                    notifikasi.objects.create(nim=i.nim,messages=f"Terdapat Evaluasi Usulan Topik Baru Oleh {create_usulan.id_dosen_kompartemen.nip.id_user.first_name} pada {tanggal} Jam {Jam}")
                # send ke mahasiswa
                # print(user_mhs[0].id_user.id)
                # email_list=User.objects.filter(pk=user_mhs[0].id_user.id).values_list('email',flat=True)
                email_list=User.objects.filter(pk=user_mhs[0].id_user.id).values_list('email',flat=True)
                # print(email_list)
                send_mail(
                    'Evaluasi Usulan Topik Baru ',
                    f"Terdapat Evaluasi Usulan Topik Baru Oleh {create_usulan.id_dosen_kompartemen.nip.id_user.first_name} pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                )
                cek_roledosen=roledosen.objects.filter(nim=create_usulan.id_usulan_topik.nim).filter(role="Pembimbing 1")|roledosen.objects.filter(nim=create_usulan.id_usulan_topik.nim).filter(role="Pembimbing 2")
                if cek_roledosen.exists():
                    pass
                else :
                    # send ke sekdept
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    email_list=[]
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
                    for i in range(len(temp_email)):
                        email_list.append(temp_email[i][0])
                    send_mail(
                        'Update Usulan Topik',
                        f"Terdapat Mahasiswa ACC Usulan Topik Baru Oleh {create_usulan.id_usulan_topik.nim} dengan judul {create_usulan.id_usulan_topik.judul_topik} pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                    )
                # "Menunggu Dosen Kompartemen"

                return redirect("../usulantopik_get_filter_ACC/kompartemen")
        else:
            form = EvaluasiTopikFormKompartemen()
    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        if request.method == "POST":
            form = EvaluasiTopikFormKompartemen(request.POST, request.FILES)
            # if evaluasitopik.objects.filter(id_usulan_topik=request.id_usulan_topik).filter(role=request.role).exists():
            #     return redirect("../roledosenmax")
            if form.is_valid():
                create_usulan = form.save(commit=False)
                create_usulan.id_usulan_topik=usulantopiks
                create_usulan.id_dosen_kompartemen=evaluasitopiks.id_dosen_kompartemen
                evaluasitopiks_delete_assign=evaluasitopik.objects.filter(id_usulan_topik=id).filter(status_topik="Menunggu Dosen Kompartemen")
                evaluasitopiks_delete_assign.delete()
                instances = evaluasitopik.objects.filter(id_usulan_topik=create_usulan.id_usulan_topik.id_usulan_topik).order_by('tanggal_buat')
                if instances.exists(): # Pastikan QuerySet tidak kosong
                    instances.update(status_topik='Revisi') # Mengubah status untuk semua objek

                    # Mengubah status objek pertama menjadi "Submit"
                    # print(instances)
                    # print(instances.values_list("tanggal_update"))
                    # first_instance = instances.order_by('-tanggal_update').first()
                    # # print(first_instance.tanggal_buat)
                    # first_instance.status_topik = 'Revisi'
                    # first_instance.save()
                create_usulan.save()
                # evaluasitopiks_delete_assign.delete()
                
                create_usulan.save()
                messages.success(request,"Data Evaluasi Topik Telah Berhasil Dibuat! ")
                # contoh : notif
                # todo notif
                email_list=[]
                user_mhs=mahasiswa.objects.filter(nim=create_usulan.id_usulan_topik.nim.nim)
                # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
                for i in user_mhs:
                    temp_email=list(User.objects.filter(pk=i.id_user.id).values_list('email'))
                    email_list.append(temp_email[0][0])
                    notifikasi.objects.create(nim=i.nim,messages=f"Terdapat Evaluasi Usulan Topik Baru Oleh {create_usulan.id_dosen_kompartemen.nip.id_user.first_name} pada {tanggal} Jam {Jam}")
                # send ke mahasiswa
                # email_list=User.objects.filter(pk=user_mhs[0].id_user.id).values_list('email',flat=True)
                send_mail(
                    'Evaluasi Usulan Topik Baru ',
                    f"Terdapat Evaluasi Usulan Topik Baru Oleh {create_usulan.id_dosen_kompartemen.nip.id_user.first_name} pada {tanggal} Jam {Jam}",
                    
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                )
                cek_roledosen=roledosen.objects.filter(nim=create_usulan.id_usulan_topik.nim).filter(role="Pembimbing 1")|roledosen.objects.filter(nim=create_usulan.id_usulan_topik.nim).filter(role="Pembimbing 2")
                if cek_roledosen.exists():
                    pass
                else :
                    # send ke sekdept
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    email_list=[]
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
                    for i in range(len(temp_email)):
                        email_list.append(temp_email[i][0])
                    send_mail(
                        'Update Usulan Topik',
                        f"Terdapat Mahasiswa ACC Usulan Topik Baru Oleh {create_usulan.id_usulan_topik.nim} dengan judul {create_usulan.id_usulan_topik.judul_topik} pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                    )
                # evaluasitopiks_delete_assign=evaluasitopik.objects.filter(id_usulan_topik=id).filter(status_topik="Menunggu Dosen Kompartemen")
                # evaluasitopiks_delete_assign.delete()
                    
                
                return redirect("../usulantopikget")
        else:
            form = EvaluasiTopikFormKompartemen()
    else :
        raise PermissionDenied

    return render(request, 'dosen/evaluasitopik_create.html', {"form": form,"file":evaluasitopiks.id_usulan_topik.file_topik ,"user_info": user_info})

# Dosen Pembimbing Topik: max reach
# handle max role dosen   
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Manajemen Departemen','Kompartemen','Properta'])
def dosenevalkompartemen_max(request):
    user_info = user_information(request)
    return render(request, 'sekdept/kompartemen_max.html', { "user_info": user_info})

# Evaluasi Topik:read
# Pembuatan data Evaluasi Topik oleh Manajemen Departemen > Assign Dosen Kompartemen 
# todo: add in notification and email
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Manajemen Departemen','Properta'])
def evaluasitopik_create_sekdept(request, id):
    user_info = user_information(request)
    usulantopik_data = usulantopik.objects.get(
        pk=id)
    # print(id)
    # print(usulantopik_data.id_usulan_topik)

    evaluasitopik_data=evaluasitopik.objects.filter(id_usulan_topik=id).first()

    try :
        file =usulantopik_data.file_topik
    except:
        file=None
    # print(evaluasitopik_data)
    if user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Admin" or user_info[2].name == "Properta" :
        
        if request.method == "POST":
            form = EvaluasiTopikFormSekertarisDepartemen(
                request.POST, request.FILES)
            if form.is_valid():
                create_usulan = form.save(commit=False)
                create_usulan.id_usulan_topik = usulantopik_data
                create_usulan.status_topik = "Menunggu Dosen Kompartemen"
                create_usulan.save()
                messages.success(request,"Data Dosen Evaluasi Topik Telah Berhasil Dibuat! ")
                evaluasitopik_data_beberapa_evaluasi=evaluasitopik.objects.filter(id_usulan_topik=id)
                for i in evaluasitopik_data_beberapa_evaluasi :
                    i.id_dosen_kompartemen=create_usulan.id_dosen_kompartemen
                    i.save()

                # todo : notif
                user_mhs=mahasiswa.objects.filter(nim=create_usulan.id_usulan_topik.nim.nim)
                email_list=[]
                email_list2=[]
                # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
                for i in user_mhs:
                    temp_email=list(User.objects.filter(pk=i.id_user.id).values_list('email'))
                    email_list.append(temp_email[0][0])
                    notifikasi.objects.create(nim=i.nim,messages=f"Dosen Evaluator anda telah ditentukan oleh Manajemen Departemen pada {tanggal} Jam {Jam}")
               
                # send ke mahasiswa
                send_mail(
                    'Berhasil mendapatkan dosen kompartemen Evaluasi Usulan Topik Baru',
                    f"Dosen Evaluator anda telah ditentukan oleh Manajemen Departemen pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                )
                # send ke Dosen Kompartemen
                notifikasi.objects.create(nip=create_usulan.id_dosen_kompartemen.nip.nip,messages=f"Anda telah ditugaskan untuk mengevaluasi {create_usulan.id_usulan_topik.judul_topik} milik {create_usulan.id_usulan_topik.nim.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}")

                temp_email2=list(User.objects.filter(pk=create_usulan.id_dosen_kompartemen.nip.id_user.id).values_list('email'))
                email_list2.append(temp_email2[0][0])
                
                send_mail(
                    'Ditugaskan untuk Evaluasi Usulan Topik Baru ',
                    f"Anda telah ditugaskan untuk mengevaluasi {create_usulan.id_usulan_topik.judul_topik} milik {create_usulan.id_usulan_topik.nim.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list2,
                    fail_silently=False,
                )
                return redirect("../usulantopik_get_filter_dosen")
        elif evaluasitopik_data!= None:
            form = EvaluasiTopikFormSekertarisDepartemen(instance=evaluasitopik_data) 
            
        else:
            form = EvaluasiTopikFormSekertarisDepartemen()
    else  : 
        raise PermissionDenied


    return render(request, 'dosen/evaluasitopik_create.html', {"form": form,"file": file, "user_info": user_info})

# Evaluasi Topik:read
# Menampilkan list data hasil evaluasi topik di klasterisasi berdasarkan role dan nomor induk 
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Mahasiswa', 'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def evaluasitopik_get(request):
    user_info = user_information(request)
    # print(user_info[2].name)
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" :
        # print("abc")
        try:
            # print(kompartemendosen.objects.filter(nip=dosen.objects.filter(pk=user_info[0])[0]))
            evaluasitopiks = evaluasitopik.objects.filter(
                    id_dosen_kompartemen=kompartemendosen.objects.filter(nip=dosen.objects.filter(pk=user_info[0])[0])[0])
        except:
            evaluasitopiks = []
        # print(evaluasitopiks)
    elif user_info[2].name == "Mahasiswa":
        try:
            evaluasitopiks = evaluasitopik.objects.filter(
                id_usulan_topik__in=usulantopik.objects.filter(nim=mahasiswa.objects.filter(pk=user_info[0])[0])).exclude(status_topik="Kosong")
        except:
            evaluasitopiks = []
    else:
        evaluasitopiks = evaluasitopik.objects.all()
    # print(usulantopiks)
    return render(request, 'dosen/evaluasitopik_get.html', {"evaluasitopiks": evaluasitopiks, "user_info": user_info})

# Evaluasi Topik:read
# Menampilkan list data hasil evaluasi topik di klasterisasi berdasarkan role dan nomor induk filter dengan ACC
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin',  'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def evaluasitopik_get_ACC(request):
    user_info = user_information(request)
    # print(user_info[2].name)
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" :
        # print("abc")
        try:
            # print(kompartemendosen.objects.filter(nip=dosen.objects.filter(pk=user_info[0])[0]))
            evaluasitopiks = evaluasitopik.objects.filter(
                    id_dosen_kompartemen=kompartemendosen.objects.filter(nip=dosen.objects.filter(pk=user_info[0])[0])[0]).exclude(status_topik="ACC").exclude(status_topik="Revisi")
        except:
            evaluasitopiks = []
        # print(evaluasitopiks)
    elif user_info[2].name == "Mahasiswa":
        raise PermissionDenied()
    else:
        evaluasitopiks = evaluasitopik.objects.all().exclude(status_topik="ACC").exclude(status_topik="Revisi")
    # print(usulantopiks)
    return render(request, 'dosen/evaluasitopik_get.html', {"evaluasitopiks": evaluasitopiks, "user_info": user_info})
# filter acc
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin',  'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def evaluasitopik_get_sudah_ACC(request):
    user_info = user_information(request)
    # print(user_info[2].name)
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" :
        # print("abc")
        try:
            # print(kompartemendosen.objects.filter(nip=dosen.objects.filter(pk=user_info[0])[0]))
            evaluasitopiks = evaluasitopik.objects.filter(
                    id_dosen_kompartemen=kompartemendosen.objects.filter(nip=dosen.objects.filter(pk=user_info[0])[0])[0]).filter(status_topik="ACC")
        except:
            evaluasitopiks = []
        # print(evaluasitopiks)
    elif user_info[2].name == "Mahasiswa":
        raise PermissionDenied()
    else:
        evaluasitopiks = evaluasitopik.objects.all().filter(status_topik="ACC")
    # print(usulantopiks)
    return render(request, 'dosen/evaluasitopik_get.html', {"evaluasitopiks": evaluasitopiks, "user_info": user_info})
# filter revisi
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin',  'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def evaluasitopik_get_sudah_revisi(request):
    user_info = user_information(request)
    # print(user_info[2].name)
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" :
        # print("abc")
        try:
            # print(kompartemendosen.objects.filter(nip=dosen.objects.filter(pk=user_info[0])[0]))
            evaluasitopiks = evaluasitopik.objects.filter(
                    id_dosen_kompartemen=kompartemendosen.objects.filter(nip=dosen.objects.filter(pk=user_info[0])[0])[0]).filter(status_topik="Revisi")
        except:
            evaluasitopiks = []
        # print(evaluasitopiks)
    elif user_info[2].name == "Mahasiswa":
        raise PermissionDenied()
    else:
        evaluasitopiks = evaluasitopik.objects.all().filter(status_topik="Revisi")
    # print(usulantopiks)
    return render(request, 'dosen/evaluasitopik_get.html', {"evaluasitopiks": evaluasitopiks, "user_info": user_info})

# filter sudah evaluasi
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin',  'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def evaluasitopik_get_sudah_evaluasi(request):
    user_info = user_information(request)
    # print(user_info[2].name)
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" :
        # print("abc")
        try:
            # print(kompartemendosen.objects.filter(nip=dosen.objects.filter(pk=user_info[0])[0]))
            evaluasitopiks = evaluasitopik.objects.filter(
                    id_dosen_kompartemen=kompartemendosen.objects.filter(nip=dosen.objects.filter(pk=user_info[0])[0])[0]).filter(status_topik__in=["ACC","Revisi"])
        except:
            evaluasitopiks = []
        # print(evaluasitopiks)
    elif user_info[2].name == "Mahasiswa":
        raise PermissionDenied()
    else:
        evaluasitopiks = evaluasitopik.objects.all().filter(status_topik__in=["ACC","Revisi"])
    # print(usulantopiks)
    return render(request, 'dosen/evaluasitopik_get.html', {"evaluasitopiks": evaluasitopiks, "user_info": user_info})

# Menampilkan form data hasil evaluasi topik  berdasarkan id evaluasi topik
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Mahasiswa', 'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def evaluasitopik_get_id_usulan(request,id):
    user_info = user_information(request)
    # check:dosen kompartemen
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" :
        try:
            list_dosen_kompartemen=[]
            temp_dosen_kompartemen=list(kompartemendosen.objects.filter(nip=dosen.objects.filter(pk=user_info[0])[0].nip).values_list('id_dosen_kompartemen'))
            # print(temp_dosen_kompartemen)
            for i in range(len(temp_dosen_kompartemen)):
                        list_dosen_kompartemen.append(temp_dosen_kompartemen[i][0])
            # print(list_dosen_kompartemen)
            evaluasitopiks = evaluasitopik.objects.filter(
                id_dosen_kompartemen__in=list_dosen_kompartemen).filter(id_usulan_topik=id)
        except:
            evaluasitopiks = []
    elif user_info[2].name == "Mahasiswa":
        try:
            list_usulan_topik=[]
            temp_usulan=list(usulantopik.objects.filter(nim=mahasiswa.objects.filter(pk=user_info[0])[0]).values_list('id_usulan_topik'))
            # print(temp_usulan)
            for i in range(len(temp_usulan)):
                        list_usulan_topik.append(temp_usulan[i][0])
            evaluasitopiks = evaluasitopik.objects.filter(
                id_usulan_topik__in=list_usulan_topik).filter(id_usulan_topik=id).exclude(status_topik="Kosong")
            # print(evaluasitopiks)
        except:
            evaluasitopiks = []
    
    elif user_info[2].name == "Manajemen Departemen"or user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        try:
            evaluasitopiks = evaluasitopik.objects.filter(id_usulan_topik=id)
        except:
            evaluasitopiks = []
    else:
        evaluasitopiks = evaluasitopik.objects.all()
    # print(usulantopiks)
    return render(request, 'dosen/evaluasitopik_get.html', {"evaluasitopiks": evaluasitopiks, "user_info": user_info})

# Evaluasi Topik:update
# Mengubah data hasil evaluasi topik di klasterisasi berdasarkan id evaluasi topik 
# todo: add in notification and email
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin',  'Manajemen Departemen','Kompartemen','Properta'])
def evaluasitopik_update(request, id):
    user_info = user_information(request)
    evaluasitopik_data = evaluasitopik.objects.get(pk=id)
   
    # try:
    #     if usulantopik.objects.filter(
    #         id_usulan_topik=evaluasitopik_data.id_usulan_topik).exists():
    #         get_object = evaluasitopik.objects.get(id_usulan_topik=evaluasitopik_data.id_usulan_topik)
    #     else:
    #         get_object = evaluasitopik.objects.get(
    #         id_usulan_topik=evaluasitopik_data.id_usulan_topik)
    #     evaluasitopik_data.file_topik = get_object.file_topik

    # except:
    #     evaluasitopik_data.file_topik = None
        
    if user_info[2].name == "Kompartemen":

        if request.method == "POST":
            form = EvaluasiTopikFormKompartemen(
                request.POST, request.FILES, instance=evaluasitopik_data)
            if form.is_valid():
                
                create_evaluasi = form.save(commit=False)
                evaluasitopiks_delete_assign=evaluasitopik.objects.filter(id_usulan_topik=create_evaluasi.id_usulan_topik.id_usulan_topik).filter(status_topik="Menunggu Dosen Kompartemen")
                evaluasitopiks_delete_assign.delete()

                instances = evaluasitopik.objects.filter(id_usulan_topik=create_evaluasi.id_usulan_topik.id_usulan_topik).order_by('tanggal_buat')
                if instances.exists(): # Pastikan QuerySet tidak kosong
                    instances.update(status_topik='Revisi') # Mengubah status untuk semua objek

                    # Mengubah status objek pertama menjadi "Submit"
                    # print(instances)
                    # print(instances.values_list("tanggal_update"))
                    # first_instance = instances.order_by('-tanggal_update').first()
                    # # print(first_instance.tanggal_buat)
                    # first_instance.status_topik = 'Revisi'
                    # first_instance.save()
                create_evaluasi.save()
                # evaluasitopiks_delete_assign.delete()
                messages.warning(request,"Data Evaluasi Topik Telah Berhasil Diubah! ")
                 # todo : notif
                user_mhs=mahasiswa.objects.filter(nim=create_evaluasi.id_usulan_topik.nim.nim)
                email_list=[]
                # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
                for i in user_mhs:
                    temp_email=list(User.objects.filter(pk=i.id_user.id).values_list('email'))
                    email_list.append(temp_email[0][0])
                    notifikasi.objects.create(nim=i.nim,messages=f"Ada perubahan terkait evaluasi topik oleh {create_evaluasi.id_dosen_kompartemen.nip.id_user.first_name} pada {tanggal} Jam {Jam}")
                # send ke mahasiswa
                # email_list=User.objects.filter(pk=user_mhs[0].id_user.id).values_list('email',flat=True)
                send_mail(
                    'Update Evaluasi Usulan Topik',
                    f"Ada perubahan terkait evaluasi topik oleh {create_evaluasi.id_dosen_kompartemen.nip.id_user.first_name} pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                )
                cek_roledosen=roledosen.objects.filter(nim=create_evaluasi.id_usulan_topik.nim.nim).filter(role="Pembimbing 1")|roledosen.objects.filter(nim=create_evaluasi.id_usulan_topik.nim.nim).filter(role="Pembimbing 2")
                if cek_roledosen.exists():
                    pass
                else :
                    # send ke sekdept
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    email_list=[]
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
                    for i in range(len(temp_email)):
                        email_list.append(temp_email[i][0])
                    send_mail(
                        'Update Usulan Topik',
                        f"Terdapat Mahasiswa ACC Usulan Topik Baru Oleh {create_evaluasi.id_usulan_topik.nim} dengan judul {create_evaluasi.id_usulan_topik.judul_topik} pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                    )
                    # notifikasi.objects.create(nip=create_usulan.id_dosen_kompartemen.nip.nip,messages=f"Anda telah ditugaskan untuk mengevaluasi {create_usulan.id_usulan_topik.judul_topik} milik {create_usulan.id_usulan_topik.nim.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}")
                
                return redirect("../evaluasitopikget")
        else:
            form = EvaluasiTopikFormKompartemen(instance=evaluasitopik_data)
    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        if request.method == "POST":
            form = EvaluasiTopikFormFull(
                request.POST, request.FILES, instance=evaluasitopik_data)
            if form.is_valid():
                create_evaluasi = form.save(commit=False)
                evaluasitopiks_delete_assign=evaluasitopik.objects.filter(id_usulan_topik=create_evaluasi.id_usulan_topik.id_usulan_topik).filter(status_topik="Menunggu Dosen Kompartemen")
                
                evaluasitopiks_delete_assign.delete()
                instances = evaluasitopik.objects.filter(id_usulan_topik=create_evaluasi.id_usulan_topik.id_usulan_topik).order_by('tanggal_buat')
                if instances.exists(): # Pastikan QuerySet tidak kosong
                    instances.update(status_topik='Revisi') # Mengubah status untuk semua objek

                    # Mengubah status objek pertama menjadi "Submit"
                    # print(instances)
                    # print(instances.values_list("tanggal_update"))
                    # first_instance = instances.order_by('-tanggal_update').first()
                    # # print(first_instance.tanggal_buat)
                    # first_instance.status_topik = 'Revisi'
                    # first_instance.save()
                create_evaluasi.save()
                messages.warning(request,"Data Evaluasi Topik Telah Berhasil Diubah! ")
                 # todo : notif
                user_mhs=mahasiswa.objects.filter(nim=create_evaluasi.id_usulan_topik.nim.nim)
                email_list=[]
                # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
                for i in user_mhs:
                    # print(i)
                    temp_email=list(User.objects.filter(pk=i.id_user.id).values_list('email'))
                    email_list.append(temp_email[0][0])
                    notifikasi.objects.create(nim=i.nim,messages=f"Ada perubahan terkait evaluasi topik oleh {create_evaluasi.id_dosen_kompartemen.nip.id_user.first_name} pada {tanggal} Jam {Jam}")
                # send ke mahasiswa
                # print(user_mhs)
                # email_list=User.objects.filter(pk=user_mhs[0].id_user.id).values_list('email',flat=True)
                # print(email_list)
                send_mail(
                    'Update Evaluasi Usulan Topik',
                    f"Ada perubahan terkait evaluasi topik oleh {create_evaluasi.id_dosen_kompartemen.nip.id_user.first_name} pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                )
                cek_roledosen=roledosen.objects.filter(nim=create_evaluasi.id_usulan_topik.nim.nim).filter(role="Pembimbing 1")|roledosen.objects.filter(nim=create_evaluasi.id_usulan_topik.nim.nim).filter(role="Pembimbing 2")
                if cek_roledosen.exists():
                    pass
                else :
                    # send ke sekdept
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    email_list=[]
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
                    for i in range(len(temp_email)):
                        email_list.append(temp_email[i][0])
                    send_mail(
                        'Update Usulan Topik',
                        f"Terdapat Mahasiswa ACC Usulan Topik Baru Oleh {create_evaluasi.id_usulan_topik.nim} dengan judul {create_evaluasi.id_usulan_topik.judul_topik} pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                    )
                
                    # notifikasi.objects.create(nip=create_usulan.id_dosen_kompartemen.nip.nip,messages=f"Anda telah ditugaskan untuk mengevaluasi {create_usulan.id_usulan_topik.judul_topik} milik {create_usulan.id_usulan_topik.nim.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}")
                return redirect("../evaluasitopikget")
        else:
            form = EvaluasiTopikFormFull(instance=evaluasitopik_data)
    elif user_info[2].name == "Manajemen Departemen":
        if request.method == "POST":
            form = EvaluasiTopikFormSekertarisDepartemen(
                request.POST, request.FILES, instance=evaluasitopik_data)
            if form.is_valid():
                create_evaluasi = form.save(commit=False)
                create_evaluasi.save()
                messages.warning(request,"Data Evaluasi Topik Telah Berhasil Diubah! ")
                 # todo : notif
                email_list=[]
                user_mhs=mahasiswa.objects.filter(nim=create_evaluasi.id_usulan_topik.nim.nim)
                # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
                for i in user_mhs:
                    temp_email=list(User.objects.filter(pk=i.id_user.id).values_list('email'))
                    email_list.append(temp_email[0][0])
                    notifikasi.objects.create(nim=i.nim,messages=f"Ada perubahan terkait evaluasi topik oleh {create_evaluasi.id_dosen_kompartemen.nip.id_user.first_name} pada {tanggal} Jam {Jam}")
                 # send ke mahasiswa
                # email_list=User.objects.filter(pk=user_mhs[0].id_user.id).values_list('email',flat=True)
                send_mail(
                    'Update Evaluasi Usulan Topik',
                    f"Ada perubahan terkait evaluasi topik oleh {create_evaluasi.id_dosen_kompartemen.nip.id_user.first_name} pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                )
                    # notifikasi.objects.create(nip=create_usulan.id_dosen_kompartemen.nip.nip,messages=f"Anda telah ditugaskan untuk mengevaluasi {create_usulan.id_usulan_topik.judul_topik} milik {create_usulan.id_usulan_topik.nim.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}")
                return redirect("../evaluasitopikget")
        else:
            form = EvaluasiTopikFormSekertarisDepartemen(
                instance=evaluasitopik_data)
    else:
        raise PermissionDenied()

    return render(request, 'dosen/evaluasitopik_update.html', {"form": form, "file": evaluasitopik_data.id_usulan_topik.file_topik, "user_info": user_info})

# Evaluasi Topik:Read
# Mengubah data hasil evaluasi topik di klasterisasi berdasarkan id evaluasi topik 
# todo: add in notification and email
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Mahasiswa', 'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def evaluasitopik_read(request, id):
    user_info = user_information(request)
    evaluasitopik_data = evaluasitopik.objects.get(pk=id)
    form = EvaluasiTopikFormFull(
                request.POST, request.FILES, instance=evaluasitopik_data)
    field = ["id_dosen_kompartemen", "id_usulan_topik",
                  "status_topik", "catatan"]
    for item in field:
        # form.field.disabled = True
        form.fields[item].disabled = True
    # form.disabled = True

    return render(request, 'dosen/evaluasitopik_read.html', {"form": form, "file": evaluasitopik_data.id_usulan_topik.file_topik, "user_info": user_info})

# Evaluasi Topik: delete
# penghapusan data Evaluasi Topik berdasarkan id evaluasi topik  
# todo: add in notification and email
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin',  'Kompartemen','Properta'])
def evaluasitopik_delete(request, id):
    delete_data = evaluasitopik.objects.get(pk=id)
    messages.error(request,"Data Evaluasi Topik Telah Berhasil Dihapus! ")
    delete_data.delete()
    return redirect('../evaluasitopikget')

# CPMK 
# CPMK:create
# Membuat data CPMK
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Properta'])
def Sub_CPMK_create(request):
    user_info = user_information(request)
    if request.method == "POST":
        form = SubCPMKForm(request.POST)
        if form.is_valid():
            create_CPMK = form.save(commit=False)

            create_CPMK.save()
            messages.success(request,"Data Sub CPMK Telah Berhasil Dibuat! ")
            return redirect("../sub_cpmk_get")
    else:
        form = SubCPMKForm()
    # print(usulantopiks)
    return render(request, 'penilaian/sub_cpmk_create.html', {"forms": form,  "user_info": user_info})

# CPMK:read
# Menampilkan List CPMK yang dibuat
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Properta'])
def Sub_CPMK_get(request):
    user_info = user_information(request)

    CPMK = sub_cpmk.objects.all()
    # print(usulantopiks)
    return render(request, 'penilaian/sub_cpmk_get.html', {"CPMK": CPMK, "user_info": user_info})

# CPMK:update
# Mengubah data CPMK berdasarkan id cpmk
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Properta'])
def Sub_CPMK_update(request,id):
    user_info = user_information(request)
    CPMK_data = sub_cpmk.objects.get(pk=id)
    if request.method == "POST":
        form = SubCPMKForm(request.POST, instance=CPMK_data)
        if form.is_valid():
            create_CPMK = form.save(commit=False)
            create_CPMK.save()
            messages.warning(request,"Data Sub CPMK Telah Berhasil Diubah! ")
            return redirect("../sub_cpmk_get")
    else:
        form = SubCPMKForm(instance=CPMK_data)
    # print(usulantopiks)
    return render(request, 'penilaian/sub_cpmk_update.html', {"forms": form,  "user_info": user_info})

# CPMK:delete
# Menghapus data CPMK berdasarkan id cpmk
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Properta'])
def Sub_CPMK_delete(request,id):
    delete_data = sub_cpmk.objects.get(pk=id)
    delete_data.delete()
    messages.error(request,"Data Sub CPMK Telah Berhasil Dihapus! ")
    return redirect('../sub_cpmk_get')

# CPMK Utama
# CPMK Utama:create
# Membuat data CPMK
@login_required(login_url="/login")
def CPMK_create(request):
    user_info = user_information(request)
    if request.method == "POST":
        form = CPMKForm(request.POST)
        if form.is_valid():
            create_CPMK = form.save(commit=False)
            create_CPMK.save()
            messages.success(request,"Data CPMK Telah Berhasil Dibuat! ")
            return redirect("../cpmk_get")
    else:
      form = CPMKForm()
    return render(request, 'penilaian/cpmk_create.html', {"forms": form,  "user_info": user_info})

# CPMK:read
# Menampilkan List CPMK yang dibuat
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Properta'])
def CPMK_get(request):
    user_info = user_information(request)
    CPMK = cpmk.objects.all()
    return render(request, 'penilaian/cpmk_get.html', {"CPMK": CPMK, "user_info": user_info})

# CPMK:update
# Mengubah data CPMK berdasarkan id cpmk
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Properta'])
def CPMK_update(request,id):
    user_info = user_information(request)
    CPMK_data = cpmk.objects.get(pk=id)
    if request.method == "POST":
        form = CPMKForm(request.POST, instance=CPMK_data)
        if form.is_valid():
            create_CPMK = form.save(commit=False)
            create_CPMK.save()
            messages.warning(request,"Data CPMK Telah Berhasil Diubah! ")
            return redirect("../cpmk_get")
    else:
        form = CPMKForm(instance=CPMK_data)
    return render(request, 'penilaian/cpmk_update.html', {"forms": form,  "user_info": user_info})

# CPMK:delete
# Menghapus data CPMK berdasarkan id cpmk
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Properta'])
def CPMK_delete(request,id):
    delete_data = cpmk.objects.get(pk=id)
    delete_data.delete()
    messages.error(request,"Data CPMK Telah Berhasil Dihapus! ")
    return redirect('../cpmk_get')

# ganti 3
# Dosen Pembimbing
# Dosen Pembimbing Topik:create
# Pembuatan data Assign Dosen Pembimbing oleh Sekdept  
# todo: add in notification and email
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen', 'Properta'])
def dosenpembimbing_create_sekdept(request, id):
    user_info = user_information(request)
    mahasiswa_data = mahasiswa.objects.get(pk=id)
    try:
        roledosen_data=roledosen.objects.filter(nim=id)    
    except:
        roledosen_data=None
    
    if request.method == "POST":
        form = RoleDosenFormSekdept(request.POST)
        # print(request.POST)
        if roledosen.objects.filter(nim=id).filter(role=request.POST["role"]).filter(status="Active").exists() and request.POST["status"] !="Finished":
            return redirect('dosenpembimbing_max', my_variable= "Role Sudah di Assign Sebelumnya")
        elif roledosen.objects.filter(nim=id).filter(nip=request.POST["nip"]).filter(status="Active").exists() and request.POST["status"] !="Finished":
            return redirect( 'dosenpembimbing_max', my_variable=  "Dosen Sudah di Assign Sebelumnya")
        else : 
            if form.is_valid():
                create_roledosen = form.save(commit=False)
                create_roledosen.nim = mahasiswa_data
                create_roledosen.save()
                messages.success(request,"Data Dosen Pembimbing Telah Berhasil Dibuat! ")
                # todo : notif
                # user_mhs=mahasiswa.objects.filter(nim=create_roledosen.nim)
                # user_mhs=mahasiswa.objects.filter(nip=create_roledosen.nip)
                    # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
                notifikasi.objects.create(nim=create_roledosen.nim.nim,messages=f"Terdapat assign dosen pendamping baru{create_roledosen.nip.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}")
                notifikasi.objects.create(nip=create_roledosen.nip.nip,messages=f"Terdapat assign mahasiswa baru {create_roledosen.nim.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}")
                        # notifikasi.objects.create(nip=create_usulan.id_dosen_kompartemen.nip.nip,messages=f"Anda telah ditugaskan untuk mengevaluasi {create_usulan.id_usulan_topik.judul_topik} milik {create_usulan.id_usulan_topik.nim.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}")
                # send ke mahasiswa
                email_list=[]
                temp_email=list(User.objects.filter(pk=create_roledosen.nim.id_user.id).values_list('email'))
                email_list.append(temp_email[0][0])
                # email_list=User.objects.filter(pk=create_roledosen.nim.id_user).values_list('email')
                send_mail(
                    'Assign Dosen Pendamping Telah Dibuat',
                    f"Terdapat assign dosen pendamping baru {create_roledosen.nip.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                    )
                # send ke Dosen
                # email_list=User.objects.filter(pk=create_roledosen.nip.id_user).values_list('email')
                email_list=[]
                temp_email=list(User.objects.filter(pk=create_roledosen.nip.id_user.id).values_list('email'))
                email_list.append(temp_email[0][0])
                send_mail(
                    'Assign Mahasiswa Telah Dibuat',
                    f"Terdapat assign mahasiswa baru {create_roledosen.nim.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                    )
                return redirect("../roledosenget")
    else:
        form = RoleDosenFormSekdept()
        data_roledosen=roledosen.objects.all()
        # test=data_roledosen.filter(role='Pembimbing 1').filter(status='Active').values('nip').annotate(count_pembimbing=Count('nip')).annotate(count_sempro=Sum(0)).annotate(count_semhas=Sum(0))
        # print(test)
        # hitung_pembimbing=
        data_pembimbing=data_roledosen.filter(role='Pembimbing 1').filter(status='Active').values("nip__id_user__first_name",'nip').annotate(count_pembimbing=Count('nip'))|data_roledosen.filter(role='Pembimbing 2').filter(status='Active').values('nip__id_user__first_name','nip').annotate(count_pembimbing=Count('nip'))
        data_sempro=data_roledosen.filter(role='Penguji Seminar Proposal 1').filter(status='Active').values("nip__id_user__first_name",'nip').annotate(count_sempro=Count('nip'))|data_roledosen.filter(role='Penguji Seminar Proposal 2').filter(status='Active').values('nip__id_user__first_name','nip').annotate(count_sempro=Count('nip'))
        data_semhas=data_roledosen.filter(role='Penguji Seminar Hasil 1').filter(status='Active').values("nip__id_user__first_name",'nip').annotate(count_semhas=Count('nip'))|data_roledosen.filter(role='Penguji Seminar Hasil 2').filter(status='Active').values('nip__id_user__first_name','nip').annotate(count_semhas=Count('nip'))
       


    return render(request, 'sekdept/roledosen_create.html', {"form": form,"roledosens":roledosen_data, "user_info": user_info,"data_pembimbing":data_pembimbing,'data_sempro':data_sempro,'data_semhas':data_semhas})
# ganti 1
# Dosen Pembimbing Topik:create
# Pembuatan data Assign Dosen Pembimbing oleh Admin  
# todo: add in notification and email
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen', 'Properta'])
def dosenpembimbing_create(request):
    user_info = user_information(request)
    
    if request.method == "POST":
        form = RoleDosenForm(request.POST)
        # print(request.POST)
        if roledosen.objects.filter(nim=request.POST["nim"]).filter(role=request.POST["role"]).filter(status="Active").exists() and request.POST["status"] !="Finished":
            return redirect('dosenpembimbing_max', my_variable= "Role Sudah di Assign Sebelumnya")
        elif roledosen.objects.filter(nim=request.POST["nim"]).filter(nip=request.POST["nip"]).filter(status="Active").exists() and request.POST["status"] !="Finished":
            return redirect( 'dosenpembimbing_max', my_variable=  "Dosen Sudah di Assign Sebelumnya")

        else : 
            # print(req)
            # count_dosen_1=roledosen.objects.filter(status="Active").filter(nip=request.POST["nip"]).filter(role="Pembimbing 1").count()
            # count_dosen_2=roledosen.objects.filter(status="Active").filter(nip=request.POST["nip"]).filter(role="Pembimbing 2").count()
            # count_dosen=count_dosen_1+count_dosen_2 
            # if count_dosen<8 : 
            if form.is_valid():
                create_roledosen = form.save()
                create_roledosen.save()
                messages.success(request,"Data Dosen Pendamping Telah Berhasil Dibuat! ")
                
                notifikasi.objects.create(nim=create_roledosen.nim.nim,messages=f"Terdapat assign dosen pendamping baru {create_roledosen.nip.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}")
                notifikasi.objects.create(nip=create_roledosen.nip.nip,messages=f"Terdapat assign mahasiswa baru {create_roledosen.nim.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}")
                        # notifikasi.objects.create(nip=create_usulan.id_dosen_kompartemen.nip.nip,messages=f"Anda telah ditugaskan untuk mengevaluasi {create_usulan.id_usulan_topik.judul_topik} milik {create_usulan.id_usulan_topik.nim.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}")
                # send ke mahasiswa
                email_list=[]
                temp_email=list(User.objects.filter(pk=create_roledosen.nim.id_user.id).values_list('email'))
                email_list.append(temp_email[0][0])
                # email_list=User.objects.filter(pk=create_roledosen.nim.id_user).values_list('email')
                send_mail(
                    'Assign Dosen Pendamping Telah Dibuat',
                    f"Terdapat assign dosen pendamping baru {create_roledosen.nip.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                    )
                # send ke Dosen
                # email_list=User.objects.filter(pk=create_roledosen.nip.id_user).values_list('email')
                email_list=[]
                temp_email=list(User.objects.filter(pk=create_roledosen.nip.id_user.id).values_list('email'))
                email_list.append(temp_email[0][0])
                send_mail(
                    'Assign Mahasiswa Telah Dibuat',
                    f"Terdapat assign mahasiswa baru  {create_roledosen.nim.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                    )    
                    
                    
                    # contoh : notif
                # user_sekdept=list(User.objects.value_list('id_user').filter(groups__name='Manajemen Departemen'))
                # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
                # for i in sekdept_filter:
                #     models.notifikasi.nip=i.nip
                #     models.notifikasi.messages=f"Terdapat Input Usulan Topik Baru Oleh {create_usulantopik.nim} pada {tanggal} Jam {Jam}"
                #     notifikasi.save()
                return redirect("../roledosenget")
            # else : 
            # return redirect("../roledosenmax")
    else:
        form = RoleDosenForm()
        data_roledosen=roledosen.objects.all()
        # test=data_roledosen.filter(role='Pembimbing 1').filter(status='Active').values('nip').annotate(count_pembimbing=Count('nip')).annotate(count_sempro=Sum(0)).annotate(count_semhas=Sum(0))
        # print(test)
        # hitung_pembimbing=
        data_pembimbing=data_roledosen.filter(role='Pembimbing 1').filter(status='Active').values("nip__id_user__first_name",'nip').annotate(count_pembimbing=Count('nip'))|data_roledosen.filter(role='Pembimbing 2').filter(status='Active').values('nip__id_user__first_name','nip').annotate(count_pembimbing=Count('nip'))
        data_sempro=data_roledosen.filter(role='Penguji Seminar Proposal 1').filter(status='Active').values("nip__id_user__first_name",'nip').annotate(count_sempro=Count('nip'))|data_roledosen.filter(role='Penguji Seminar Proposal 2').filter(status='Active').values('nip__id_user__first_name','nip').annotate(count_sempro=Count('nip'))
        data_semhas=data_roledosen.filter(role='Penguji Seminar Hasil 1').filter(status='Active').values("nip__id_user__first_name",'nip').annotate(count_semhas=Count('nip'))|data_roledosen.filter(role='Penguji Seminar Hasil 2').filter(status='Active').values('nip__id_user__first_name','nip').annotate(count_semhas=Count('nip'))
        # data_bimbingan=data_roledosen.filter(role='Pembimbing 1').filter(status='Active').values(Nama=F('nip__id_user__first_name')).annotate(count_pembimbing=F(Count('nip')),count_sempro=F(Sum(0)),count_semhas=F(Sum(0)))|data_roledosen.filter(role='Pembimbing 2').filter(status='Active').values(Nama=F('nip__id_user__first_name')).annotate(count_pembimbing=F(Count('nip')),count_sempro=F(Sum(0)),count_semhas=F(Sum(0)))
        # data_sempro=data_roledosen.filter(role='Penguji Seminar Proposal 1').filter(status='Active').values(Nama=F('nip__id_user__first_name')).annotate(count_pembimbing=Sum(0),count_sempro=Count('nip'),count_semhas=Sum(0))|data_roledosen.filter(role='Penguji Seminar Proposal 2').filter(status='Active').values(Nama=F('nip__id_user__first_name')).annotate(count_pembimbing=Sum(0),count_sempro=Count('nip'),count_semhas=Sum(0))
        # data_sempro=data_roledosen.filter(role='Penguji Seminar Proposal 1').filter(status='Active').values(Nama=F('nip__id_user__first_name')).annotate(count_pembimbing=F(Sum(0)),count_sempro=F(Count('nip')),count_semhas=F(Sum(0)))|data_roledosen.filter(role='Penguji Seminar Proposal 2').filter(status='Active').values(Nama=F('nip__id_user__first_name')).annotate(count_pembimbing=F(Sum(0)),count_sempro=F(Count('nip')),count_semhas=F(Sum(0)))
        # print(data_sempro|data_bimbingan)
        
        # test3=data_roledosen.filter(role='Penguji Seminar Hasil 1').filter(status='Active').values('nip').annotate(count_pembimbing=Sum(0)).annotate(count_sempro=Sum(0)).annotate(count_semhas=Count('nip'))|data_roledosen.filter(role='Penguji Seminar Hasil 2').filter(status='Active').values('nip').annotate(count_pembimbing=Sum(0)).annotate(count_sempro=Sum(0)).annotate(count_semhas=Count('nip'))
        # coba=data_roledosen.filter(role='Pembimbing 1').filter(status='Active').values('nip').annotate(dcount1=Count('nip'))|data_roledosen.filter(role='Pembimbing 2').filter(status='Active').values('nip').annotate(dcount1=Count('nip'))|data_roledosen.filter(role='Penguji Seminar Proposal 1').filter(status='Active').values('nip').annotate(dcount3=Count('nip'))|data_roledosen.filter(role='Penguji Seminar Proposal 2').filter(status='Active').values('nip').annotate(dcount3=Count('nip'))
        # cb_hitung2=data_roledosen.filter(role='Pembimbing 2').filter(status='Active').values('nip').annotate(dcount2=Count('nip'))
        # print(cb_hitung)
        # print(cb_hitung2)
        # print(cb_hitung3)
        # full=test1|test2|test3
        # print(full)
        # print(test1|test2)
        # print(test2)
        # print(test3)
        # abc=data_roledosen.select_related(test1,test2,test3)
        # print(data_pembimbing)

    return render(request, 'sekdept/roledosen_create.html', {"form": form, "user_info": user_info,"data_pembimbing":data_pembimbing,'data_sempro':data_sempro,'data_semhas':data_semhas})

# Dosen Pembimbing Topik: max reach
# handle max role dosen   
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen', 'Properta'])
def dosenpembimbing_max(request,my_variable):
    user_info = user_information(request)
  
    if my_variable !=None:
        my_variable = my_variable
    else:
        my_variable = None
        
    return render(request, 'sekdept/roledosen_max.html', { "user_info": user_info,"pesan":my_variable})

# Dosen Pembimbing Topik: read
# Melihat list data Assign Dosen Pembimbing, penguji seminar  
@login_required(login_url="/login")
# @role_required(allowed_roles=['Admin','Manajemen Departemen', 'Properta'])
@role_required(allowed_roles=['Admin', 'Mahasiswa', 'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def dosenpembimbing_get(request):
    user_info = user_information(request)

    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen":
        role="Dosen"
        try:
            roledosens = roledosen.objects.filter(
                nip=dosen.objects.filter(pk=user_info[0])[0])
        except:
            roledosens = []
    elif user_info[2].name == "Mahasiswa":
        role="Mahasiswa"
        try:
            roledosens = roledosen.objects.filter(
                nim=mahasiswa.objects.filter(pk=user_info[0])[0])
        except:
            roledosens = []
    elif user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        role="Manajemen Departemen"
        roledosens = roledosen.objects.all()
    return render(request, 'sekdept/roledosen_get.html', {"roledosens": roledosens, "role" : role, "user_info": user_info})

@login_required(login_url="/login")
# @role_required(allowed_roles=['Admin','Manajemen Departemen', 'Properta'])
@role_required(allowed_roles=['Admin', 'Mahasiswa', 'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def dosenpembimbing_get_sekdept(request):
    user_info = user_information(request)
    filter="sekdept"
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        role="Dosen"
        try:
            roledosens = roledosen.objects.filter(
                nip=dosen.objects.filter(pk=user_info[0])[0])
        except:
            roledosens = []
    elif user_info[2].name == "Mahasiswa":
        role="Mahasiswa"
        try:
            roledosens = roledosen.objects.filter(
                nim=mahasiswa.objects.filter(pk=user_info[0])[0])
        except:
            roledosens = []
    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        role="Manajemen Departemen"
        roledosens = roledosen.objects.all()
    return render(request, 'sekdept/roledosen_get.html', {"roledosens": roledosens, "role" : role,"filter":filter, "user_info": user_info})



# Melihat list data Assign Dosen Pembimbing serta filter dosen pembimbing  
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Mahasiswa', 'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def dosenpembimbing_get_pembimbing(request):
    user_info = user_information(request)
    role="Dosen Pembimbing"
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":

        roledosens = roledosen.objects.filter(
            nip=dosen.objects.filter(pk=user_info[0])[0]).filter(role="Pembimbing 1") | roledosen.objects.filter(
            nip=dosen.objects.filter(pk=user_info[0])[0]).filter(role="Pembimbing 2")
    elif user_info[2].name == "Mahasiswa":
        roledosens = roledosen.objects.filter(
            nim=mahasiswa.objects.filter(pk=user_info[0])[0]).filter(role="Pembimbing 1") | roledosen.objects.filter(
            nim=mahasiswa.objects.filter(pk=user_info[0])[0]).filter(role="Pembimbing 2")
    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        roledosens = roledosen.objects.all().filter(
            role="Pembimbing 2") | roledosen.objects.all().filter(role="Pembimbing 1")
    return render(request, 'sekdept/roledosen_get.html', {"roledosens": roledosens,"role":role, "user_info": user_info})

# Melihat list data Assign Dosen Pembimbing serta filter dosen pembimbing  
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin',  'Manajemen Departemen','Properta'])
def dosenpembimbing_get_active(request):
    user_info = user_information(request)
    role="Dosen Pembimbing"

    roledosens = roledosen.objects.all().filter(status="Active")
    return render(request, 'sekdept/roledosen_get.html', {"roledosens": roledosens,"role":role, "user_info": user_info})

# Melihat list data Assign Dosen Pembimbing serta filter dosen pembimbing  
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin',  'Manajemen Departemen','Properta'])
def dosenpembimbing_get_finished(request):
    user_info = user_information(request)
    role="Dosen Pembimbing"
    roledosens = roledosen.objects.all().filter(status="Finished")
    return render(request, 'sekdept/roledosen_get.html', {"roledosens": roledosens,"role":role, "user_info": user_info})

# Melihat list data Assign Dosen Pembimbing serta filter dosen pembimbing  
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Mahasiswa', 'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def dosenpembimbing_get_active_filter(request):
    user_info = user_information(request)
    role="Dosen Pembimbing"
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":

        roledosens = roledosen.objects.filter(
            nip=dosen.objects.filter(pk=user_info[0])[0]).filter(status="Active")
    elif user_info[2].name == "Mahasiswa":
        roledosens = roledosen.objects.filter(
            nim=mahasiswa.objects.filter(pk=user_info[0])[0]).filter(status="Active")
    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        roledosens = roledosen.objects.all().filter(status="Active")
    return render(request, 'sekdept/roledosen_get.html', {"roledosens": roledosens,"role":role, "user_info": user_info})

# Melihat list data Assign Dosen Pembimbing serta filter dosen pembimbing  
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Mahasiswa', 'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def dosenpembimbing_get_finished_filter(request):
    user_info = user_information(request)
    role="Dosen Pembimbing"
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":

        roledosens = roledosen.objects.filter(
            nip=dosen.objects.filter(pk=user_info[0])[0]).filter(status="Finished")
    elif user_info[2].name == "Mahasiswa":
        roledosens = roledosen.objects.filter(
            nim=mahasiswa.objects.filter(pk=user_info[0])[0]).filter(status="Finished")
    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        roledosens = roledosen.objects.all().filter(status="Finished")
    return render(request, 'sekdept/roledosen_get.html', {"roledosens": roledosens,"role":role, "user_info": user_info})


# Melihat list data Assign Dosen Penguji proposal serta filter dosen penguji proposal  
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Mahasiswa', 'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def dosenpembimbing_get_sempro(request):
    user_info = user_information(request)
    role="Dosen Seminar Proposal"
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        try:
            roledosens = roledosen.objects.filter(
                nip=dosen.objects.filter(pk=user_info[0])[0]).filter(role="Penguji Seminar Proposal 1") | roledosen.objects.filter(
                nip=dosen.objects.filter(pk=user_info[0])[0]).filter(role="Penguji Seminar Proposal 2")
        except:
            roledosens = []
        # print(roled)
    elif user_info[2].name == "Mahasiswa":
        roledosens = roledosen.objects.filter(
            nim=mahasiswa.objects.filter(pk=user_info[0])[0]).filter(role="Penguji Seminar Proposal 1") | roledosen.objects.filter(
            nim=mahasiswa.objects.filter(pk=user_info[0])[0]).filter(role="Penguji Seminar Proposal 2")
    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        roledosens = roledosen.objects.all().filter(
            role="Penguji Seminar Proposal 2") | roledosen.objects.all().filter(role="Penguji Seminar Proposal 1")
    return render(request, 'sekdept/roledosen_get.html', {"roledosens": roledosens,"role":role, "user_info": user_info})

# Melihat list data Assign Dosen Penguji hasil serta filter dosen penguji hasil  
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Mahasiswa', 'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def dosenpembimbing_get_semhas(request):
    user_info = user_information(request)
    role="Dosen Seminar Hasil"
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        try:
            roledosens = roledosen.objects.filter(
                nip=dosen.objects.filter(pk=user_info[0])[0]).filter(role="Penguji Seminar Hasil 1") | roledosen.objects.filter(
                nip=dosen.objects.filter(pk=user_info[0])[0]).filter(role="Penguji Seminar Hasil 2")
        except:
            roledosens = []
    elif user_info[2].name == "Mahasiswa":
        roledosens = roledosen.objects.filter(
            nim=mahasiswa.objects.filter(pk=user_info[0])[0]).filter(role="Penguji Seminar Hasil 1") | roledosen.objects.filter(
            nim=mahasiswa.objects.filter(pk=user_info[0])[0]).filter(role="Penguji Seminar Hasil 2")
    elif user_info[2].name == "Admin" or user_info[2].name == "Properta" :
        roledosens = roledosen.objects.all().filter(
            role="Penguji Seminar Hasil 2") | roledosen.objects.all().filter(role="Penguji Seminar Hasil 1")
    return render(request, 'sekdept/roledosen_get.html', {"roledosens": roledosens,"role":role, "user_info": user_info})
# ganti 2
# Dosen Pembimbing Topik:Update
# mengubah data Assign Dosen Penguji proposal berdasar id role dosen   
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin',  'Manajemen Departemen','Properta'])
def dosenpembimbing_update(request, id):
    user_info = user_information(request)
    dosenpembimbing_data = roledosen.objects.get(pk=id)
    try:
        list_nim_roledosen=list(roledosen.objects.filter(pk=id).values_list('nim',flat=True))
        # print(list_nim_roledosen)
        roledosen_data=roledosen.objects.filter(nim__in=list_nim_roledosen)    
    except:
        roledosen_data=None
    
    if user_info[2].name == "Dosen":
        if request.method == "POST":
            form = RoleDosenForm(request.POST, instance=dosenpembimbing_data)
            # if roledosen.objects.filter(nim=request.POST["nim"]).filter(role=request.POST["role"]).exists():
            #     return redirect("../roledosenmax")
            if roledosen.objects.filter(nim=request.POST["nim"]).filter(role=request.POST["role"]).filter(status="Active").exists() and request.POST["status"] !="Finished":
                return redirect('dosenpembimbing_max', my_variable= "Role Sudah di Assign Sebelumnya")
            elif roledosen.objects.filter(nim=request.POST["nim"]).filter(nip=request.POST["nip"]).filter(status="Active").exists() and request.POST["status"] !="Finished":
                return redirect( 'dosenpembimbing_max', my_variable=  "Dosen Sudah di Assign Sebelumnya")
            
            
            else : 
                if form.is_valid():
                    create_roledosen = form.save()
                    create_roledosen.save()
                    messages.warning(request,"Data Dosen Pendamping Telah Berhasil Diubah! ")
                    notifikasi.objects.create(nim=create_roledosen.nim.nim,messages=f"Terdapat pembaruan assign dosen pendamping {create_roledosen.nip.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}")
                    notifikasi.objects.create(nip=create_roledosen.nip.nip,messages=f"Terdapat pembaruan assign mahasiswa {create_roledosen.nim.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}")
                            # notifikasi.objects.create(nip=create_usulan.id_dosen_kompartemen.nip.nip,messages=f"Anda telah ditugaskan untuk mengevaluasi {create_usulan.id_usulan_topik.judul_topik} milik {create_usulan.id_usulan_topik.nim.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}")
                    # send ke mahasiswa
                    email_list=[]
                    temp_email=list(User.objects.filter(pk=create_roledosen.nim.id_user.id).values_list('email'))
                    email_list.append(temp_email[0][0])
                    # email_list=User.objects.filter(pk=create_roledosen.nim.id_user).values_list('email')
                    send_mail(
                        'Assign Dosen Pendamping Telah Diperbarui',
                        f"Terdapat pembaruan assign dosen pendamping {create_roledosen.nip.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                        )
                    # send ke Dosen
                    # email_list=User.objects.filter(pk=create_roledosen.nip.id_user).values_list('email')
                    email_list=[]
                    temp_email=list(User.objects.filter(pk=create_roledosen.nip.id_user.id).values_list('email'))
                    email_list.append(temp_email[0][0])
                    send_mail(
                        'Assign Mahasiswa Bimbingan Telah Diperbarui',
                        f"Terdapat pembaruan assign mahasiswa {create_roledosen.nim.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                        )
                    # contoh : notif
                # user_sekdept=list(User.objects.value_list('id_user').filter(groups__name='Manajemen Departemen'))
                # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
                # for i in sekdept_filter:
                #     models.notifikasi.nip=i.nip
                #     models.notifikasi.messages=f"Terdapat Input Usulan Topik Baru Oleh {create_usulantopik.nim} pada {tanggal} Jam {Jam}"
                #     notifikasi.save()
                    return redirect("../roledosenget")

        else:
            form = RoleDosenForm(instance=dosenpembimbing_data)
    elif user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        if request.method == "POST":
            form = RoleDosenFormUpdateSekdept(
                request.POST, instance=dosenpembimbing_data)
            if roledosen.objects.filter(nim=request.POST["nim"]).filter(role=request.POST["role"]).filter(status="Active").exists() and request.POST["status"] !="Finished":
                return redirect('dosenpembimbing_max', my_variable= "Role Sudah di Assign Sebelumnya")
            elif roledosen.objects.filter(nim=request.POST["nim"]).filter(nip=request.POST["nip"]).filter(status="Active").exists() and request.POST["status"] !="Finished":
                return redirect( 'dosenpembimbing_max', my_variable=  "Dosen Sudah di Assign Sebelumnya")
            else : 
                if form.is_valid():
                    create_roledosen = form.save()
                    create_roledosen.save()
                    messages.warning(request,"Data Dosen Pendamping Telah Berhasil Diubah! ")
                    notifikasi.objects.create(nim=create_roledosen.nim.nim,messages=f"Terdapat pembaruan assign dosen pendamping {create_roledosen.nip.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}")
                    notifikasi.objects.create(nip=create_roledosen.nip.nip,messages=f"Terdapat pembaruan assign mahasiswa {create_roledosen.nim.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}")
                            # notifikasi.objects.create(nip=create_usulan.id_dosen_kompartemen.nip.nip,messages=f"Anda telah ditugaskan untuk mengevaluasi {create_usulan.id_usulan_topik.judul_topik} milik {create_usulan.id_usulan_topik.nim.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}")
                    # send ke mahasiswa
                    email_list=[]
                    temp_email=list(User.objects.filter(pk=create_roledosen.nim.id_user.id).values_list('email'))
                    email_list.append(temp_email[0][0])
                    # email_list=User.objects.filter(pk=create_roledosen.nim.id_user).values_list('email')
                    send_mail(
                        'Assign Dosen Pendamping Telah Diperbarui',
                        f"Terdapat pembaruan assign dosen pendamping {create_roledosen.nip.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                        )
                    # send ke Dosen
                    # email_list=User.objects.filter(pk=create_roledosen.nip.id_user).values_list('email')
                    email_list=[]
                    temp_email=list(User.objects.filter(pk=create_roledosen.nip.id_user.id).values_list('email'))
                    email_list.append(temp_email[0][0])
                    send_mail(
                        'Assign Mahasiswa Bimbingan Telah Diperbarui',
                        f"Terdapat pembaruan assign mahasiswa {create_roledosen.nim.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                        )
                return redirect("../roledosenget")

        else:
            form = RoleDosenFormUpdateSekdept(instance=dosenpembimbing_data)
            data_roledosen=roledosen.objects.all()
            data_pembimbing=data_roledosen.filter(role='Pembimbing 1').filter(status='Active').values("nip__id_user__first_name",'nip').annotate(count_pembimbing=Count('nip'))|data_roledosen.filter(role='Pembimbing 2').filter(status='Active').values('nip__id_user__first_name','nip').annotate(count_pembimbing=Count('nip'))
            data_sempro=data_roledosen.filter(role='Penguji Seminar Proposal 1').filter(status='Active').values("nip__id_user__first_name",'nip').annotate(count_sempro=Count('nip'))|data_roledosen.filter(role='Penguji Seminar Proposal 2').filter(status='Active').values('nip__id_user__first_name','nip').annotate(count_sempro=Count('nip'))
            data_semhas=data_roledosen.filter(role='Penguji Seminar Hasil 1').filter(status='Active').values("nip__id_user__first_name",'nip').annotate(count_semhas=Count('nip'))|data_roledosen.filter(role='Penguji Seminar Hasil 2').filter(status='Active').values('nip__id_user__first_name','nip').annotate(count_semhas=Count('nip'))
       

    return render(request, 'sekdept/roledosen_update.html', {"form": form,"roledosens":roledosen_data, "user_info": user_info,"data_pembimbing":data_pembimbing,'data_sempro':data_sempro,'data_semhas':data_semhas, "user_info": user_info})

# Dosen Pembimbing Topik:delete
# Menghapus data Assign Dosen Penguji proposal berdasar id role dosen   
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin',  'Manajemen Departemen','Properta'])
def dosenpembimbing_delete(request, id):
    delete_data = roledosen.objects.get(pk=id)
    messages.error(request,"Data Dosen Pendamping Telah Berhasil Dihapus! ")
    notifikasi.objects.create(nim=delete_data.nim.nim,messages=f"Terdapat penghapusan assign dosen pendamping {delete_data.nip.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}")
    notifikasi.objects.create(nip=delete_data.nip.nip,messages=f"Terdapat penghapusan assign mahasiswa {delete_data.nim.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}")
            # notifikasi.objects.create(nip=create_usulan.id_dosen_kompartemen.nip.nip,messages=f"Anda telah ditugaskan untuk mengevaluasi {create_usulan.id_usulan_topik.judul_topik} milik {create_usulan.id_usulan_topik.nim.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}")
    # send ke mahasiswa
    email_list=[]
    temp_email=list(User.objects.filter(pk=delete_data.nim.id_user.id).values_list('email'))
    email_list.append(temp_email[0][0])
    # email_list=User.objects.filter(pk=create_roledosen.nim.id_user).values_list('email')
    send_mail(
        'Assign Dosen Pendamping Telah Dihapus',
        f"Terdapat penghapusan assign dosen pendamping {delete_data.nip.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}",
        settings.EMAIL_HOST_USER,
        email_list,
        fail_silently=False,
        )
    # send ke Dosen
    # email_list=User.objects.filter(pk=create_roledosen.nip.id_user).values_list('email')
    email_list=[]
    temp_email=list(User.objects.filter(pk=delete_data.nip.id_user.id).values_list('email'))
    email_list.append(temp_email[0][0])
    send_mail(
        'Assign Mahasiswa Bimbingan Telah Dihapus',
        f"Terdapat penghapusan assign mahasiswa {delete_data.nim.id_user.first_name} oleh Manajemen Departemen pada {tanggal} Jam {Jam}",
        settings.EMAIL_HOST_USER,
        email_list,
        fail_silently=False,
        )
    delete_data.delete()
    return redirect('../roledosenget')

# Bimbingan
# bimbingan:create
# # Membuat data bimbingan proposal dari scratch  
# todo: add in notification and email
# disini
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin',  'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def bimbingan_create(request):
    user_info = user_information(request)
    if user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        if request.method == "POST":
            form = BimbinganForm(request.POST)
            if form.is_valid():
                create_roledosen = form.save()
                create_roledosen.save()
                messages.success(request,"Data Bimbingan Telah Berhasil Dibuat! ")
                 # todo notif
                # user_mhs=mahasiswa.objects.filter(nim=create_usulan.id_usulan_topik.nim.nim)
                # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
                email_list=[]
                notifikasi.objects.create(nim=create_roledosen.id_proposal.nim.nim,messages=f"Terdapat Revisi Bimbingan Baru Oleh {create_roledosen.id_role_dosen.nip.id_user.first_name} pada {tanggal} Jam {Jam}")
                # send ke mahasiswa
                temp_email=list(User.objects.filter(pk=create_roledosen.id_proposal.nim.id_user.id).values_list('email'))
                email_list.append(temp_email[0][0])
                # email_list=User.objects.filter(pk=create_roledosen.id_proposal.nim.id_user).values_list('email')
                send_mail(
                    'Revisi Bimbingan Telah Dibuat Oleh Dosen',
                    f"Terdapat Revisi Bimbingan Baru Oleh {create_roledosen.id_role_dosen.nip.id_user.first_name} pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                )

                # Hitung Sempro
                list_jadwal_sempro=list(jadwal_seminar.objects.filter(tahap_seminar="Seminar Proposal").values_list("mahasiswa",flat=True))
                list_jadwal_sempro = list(filter(lambda x: x is not None and x != '', list_jadwal_sempro))
               
                cek_jumlah_sempro=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro)
                cek_jumlah_sempro_sum=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro).count()
                if cek_jumlah_sempro_sum>=3:
                    nama_nim_sempro=[]
                    for i in cek_jumlah_sempro:
                        nama_nim_sempro.append(i.id_role_dosen.nim)
                    # print(nama_nim_sempro)
                    user_sekdept=list(User.objects.values_list('id').filter(groups__name='Manajemen Departemen'))
                    # print(user_sekdept)
                    sekdept_filter=dosen.objects.filter(id_user__in=user_sekdept)
                    # email_list=[]
                    for i in sekdept_filter:
                        notifikasi.objects.create(nip=i.nip,messages=f"Terdapat {cek_jumlah_sempro_sum} Mahasiswa belum di assign majelis seminar proposal diantaranya {nama_nim_sempro}  pada {tanggal} Jam {Jam}")

                    # send ke sekdept
                    email_list=[]
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
                    for i in range(len(temp_email)):
                        email_list.append(temp_email[i][0])
                    send_mail(
                        'Terdapat Mahasiswa Belum Assign Jadwal',
                        f"Terdapat {cek_jumlah_sempro_sum} Mahasiswa belum di assign majelis seminar proposal diantaranya {nama_nim_sempro}  pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                    )
                # hitung semhas
                list_jadwal_semhas=list(jadwal_seminar.objects.filter(tahap_seminar="Seminar Hasil").values_list("mahasiswa",flat=True))
                list_jadwal_semhas = list(filter(lambda x: x is not None and x != '', list_jadwal_semhas))

                cek_jumlah_semhas=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_semhas)
                cek_jumlah_semhas_sum=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_semhas).count()
                if cek_jumlah_semhas_sum>=3:
                    nama_nim_semhas=[]
                    for i in cek_jumlah_semhas:
                        nama_nim_semhas.append(i.id_role_dosen.nim)
                    # print(nama_nim_sempro)
                    user_sekdept=list(User.objects.values_list('id').filter(groups__name='Manajemen Departemen'))
                    # print(user_sekdept)
                    sekdept_filter=dosen.objects.filter(id_user__in=user_sekdept)
                    # email_list=[]
                    for i in sekdept_filter:
                        notifikasi.objects.create(nip=i.nip,messages=f"Terdapat {cek_jumlah_semhas_sum} Mahasiswa belum di assign majelis seminar hasil diantaranya {nama_nim_semhas}  pada {tanggal} Jam {Jam}")

                    # send ke sekdept
                    email_list=[]
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
                    for i in range(len(temp_email)):
                        email_list.append(temp_email[i][0])
                    send_mail(
                        'Terdapat Mahasiswa Belum Assign Jadwal',
                        f"Terdapat {cek_jumlah_semhas_sum} Mahasiswa belum di assign majelis seminar hasil diantaranya {nama_nim_semhas}  pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                    )
                return redirect("../bimbinganget")
        else:
            form = BimbinganForm()
    else:
        if request.method == "POST":
            form = BimbinganFormDosen(request.POST)
            if form.is_valid():
                create_bimbingan = form.save(commit=False)
                #  WIP : role dosbscript
                getdosen_data=dosen.objects.get(pk=user_info[0])
                
                # print(getdosen_data)
                # create_bimbingan.id_role_dosen 
                nip_get= roledosen.objects.filter(
                    nip=getdosen_data.nip).filter(role="Pembimbing 1")|roledosen.objects.filter(
                    nip=getdosen_data.nip).filter(role="Pembimbing 2")
                create_bimbingan.id_role_dosen=nip_get[0]
                create_bimbingan.save()
                messages.success(request,"Data Bimbingan Telah Berhasil Dibuat! ")
                email_list=[]
                notifikasi.objects.create(nim=create_bimbingan.id_proposal.nim.nim,messages=f"Terdapat Revisi Bimbingan Baru Oleh {create_bimbingan.id_role_dosen.nip.id_user.first_name} pada {tanggal} Jam {Jam}")
                # send ke mahasiswa
                temp_email=list(User.objects.filter(pk=create_bimbingan.id_proposal.nim.id_user.id).values_list('email'))
                email_list.append(temp_email[0][0])
                # email_list=User.objects.filter(pk=create_bimbingan.id_proposal.nim.id_user).values_list('email')
                send_mail(
                    'Revisi Bimbingan Telah Dibuat Oleh Dosen',
                    f"Terdapat Revisi Bimbingan Baru Oleh {create_bimbingan.id_role_dosen.nip.id_user.first_name} pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                )
                  # Hitung Sempro
                list_jadwal_sempro=list(jadwal_seminar.objects.filter(tahap_seminar="Seminar Proposal").values_list("mahasiswa",flat=True))
                list_jadwal_sempro = list(filter(lambda x: x is not None and x != '', list_jadwal_sempro))

                cek_jumlah_sempro=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro)
                cek_jumlah_sempro_sum=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro).count()
                if cek_jumlah_sempro_sum>=3:
                    nama_nim_sempro=[]
                    for i in cek_jumlah_sempro:
                        nama_nim_sempro.append(i.id_role_dosen.nim)
                    # print(nama_nim_sempro)
                    user_sekdept=list(User.objects.values_list('id').filter(groups__name='Manajemen Departemen'))
                    # print(user_sekdept)
                    sekdept_filter=dosen.objects.filter(id_user__in=user_sekdept)
                    # email_list=[]
                    for i in sekdept_filter:
                        notifikasi.objects.create(nip=i.nip,messages=f"Terdapat {cek_jumlah_sempro_sum} Mahasiswa belum di assign majelis seminar proposal diantaranya {nama_nim_sempro}  pada {tanggal} Jam {Jam}")

                    # send ke sekdept
                    email_list=[]
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
                    for i in range(len(temp_email)):
                        email_list.append(temp_email[i][0])
                    send_mail(
                        'Terdapat Mahasiswa Belum Assign Jadwal',
                        f"Terdapat {cek_jumlah_sempro_sum} Mahasiswa belum di assign majelis seminar proposal diantaranya {nama_nim_sempro}  pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                    )
                # hitung semhas
                list_jadwal_semhas=list(jadwal_seminar.objects.filter(tahap_seminar="Seminar Hasil").values_list("mahasiswa",flat=True))
                list_jadwal_semhas = list(filter(lambda x: x is not None and x != '', list_jadwal_semhas))
                cek_jumlah_semhas=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro)
                cek_jumlah_semhas_sum=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro).count()
                if cek_jumlah_semhas_sum>=3:
                    nama_nim_semhas=[]
                    for i in cek_jumlah_semhas:
                        nama_nim_semhas.append(i.id_role_dosen.nim)
                    # print(nama_nim_sempro)
                    user_sekdept=list(User.objects.values_list('id').filter(groups__name='Manajemen Departemen'))
                    # print(user_sekdept)
                    sekdept_filter=dosen.objects.filter(id_user__in=user_sekdept)
                    # email_list=[]
                    for i in sekdept_filter:
                        notifikasi.objects.create(nip=i.nip,messages=f"Terdapat {cek_jumlah_semhas_sum} Mahasiswa belum di assign majelis seminar hasil diantaranya {nama_nim_semhas}  pada {tanggal} Jam {Jam}")

                    # send ke sekdept
                    email_list=[]
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
                    for i in range(len(temp_email)):
                        email_list.append(temp_email[i][0])
                    send_mail(
                        'Terdapat Mahasiswa Belum Assign Jadwal',
                        f"Terdapat {cek_jumlah_semhas_sum} Mahasiswa belum di assign majelis seminar hasil diantaranya {nama_nim_semhas}  pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                    )
                return redirect("../bimbinganget")
        else:
            form = BimbinganFormDosen()

    return render(request, 'bimbingan/bimbingan_create.html', {"form": form, "user_info": user_info})

# # Membuat data bimbingan proposal dari id proposal  
# todo: add in notification and email
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin',  'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def bimbingan_create_dosen(request, id):
    user_info = user_information(request)
    proposal_data = proposal.objects.get(pk=id)
    proposal_data_count=proposal.objects.filter(pk=id).first()
    # print(proposal_data_count)
    # proposal_data_count=
        # bimbingan_data = proposal.objects.get(pk=id)
        # print(bimbingan_data.ID_proposal.File_Proposal)
    # if proposal_data_count==0:
    #     try:
    #         bimbingan_data=bimbingan.objects.get(id_proposal=proposal_data)
    #         # bimbingan_data=bimbingan_data.ID_Proposal

    #     except:
    #         bimbingan_data=None
    # else:
    #     try:
    #         bimbingan_data=bimbingan.objects.get(id_proposal=proposal_data)
    #         # bimbingan_data=bimbingan_data.ID_Proposal

    #     except:
    #         bimbingan_data=None
    # print(bimbingan_data != None)
    # print(bimbingan_data == None)
    # print(bimbingan_data.ID_proposal.File_proposal.url)
    # print()
    # print(proposal_data.file_proposal.url)
    if request.method == "POST" :
        # print(1)
        proposal_data = proposal.objects.get(pk=id)
        
        form = BimbinganFormDosenUpdate(request.POST)
        if form.is_valid():
                create_bimbingan = form.save(commit=False)
                # create_bimbingan.id_role_dosen = roledosen.objects.filter(
                create_bimbingan.id_role_dosen = roledosen.objects.filter(
                    nip=dosen.objects.get(pk=user_info[0])).filter(nim=mahasiswa.objects.get(pk=proposal_data.nim.nim))[0]
                create_bimbingan.id_proposal = proposal_data
                instances = bimbingan.objects.filter(id_proposal=proposal_data.id_proposal).order_by('tanggal_buat')
                if instances.exists(): # Pastikan QuerySet tidak kosong
                    instances.update(status_bimbingan='Revisi') # Mengubah status untuk semua objek
                
                create_bimbingan.save()
                messages.success(request,"Data Bimbingan Telah Berhasil Dibuat! ")
                notifikasi.objects.create(nim=create_bimbingan.id_proposal.nim.nim,messages=f"Terdapat Revisi Bimbingan Baru Oleh {create_bimbingan.id_role_dosen.nip.id_user.first_name} pada {tanggal} Jam {Jam}")
                # send ke mahasiswa
                email_list=[]
                temp_email=list(User.objects.filter(pk=create_bimbingan.id_proposal.nim.id_user.id).values_list('email'))
                email_list.append(temp_email[0][0])
                send_mail(
                    'Hasil Revisi Proposal Telah Di Buat ',
                    f"Terdapat Revisi Bimbingan Baru Oleh Dosen {create_bimbingan.id_role_dosen.nip.id_user.first_name} pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                )
                  # Hitung Sempro
                list_jadwal_sempro=list(jadwal_seminar.objects.filter(tahap_seminar="Seminar Proposal").values_list("mahasiswa",flat=True))
                list_jadwal_sempro = list(filter(lambda x: x is not None and x != '', list_jadwal_sempro))
                cek_jumlah_sempro=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro)
                cek_jumlah_sempro_sum=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro).count()
                if cek_jumlah_sempro_sum>=3:
                    nama_nim_sempro=[]
                    for i in cek_jumlah_sempro:
                        nama_nim_sempro.append(i.id_role_dosen.nim)
                    # print(nama_nim_sempro)
                    user_sekdept=list(User.objects.values_list('id').filter(groups__name='Manajemen Departemen'))
                    # print(user_sekdept)
                    sekdept_filter=dosen.objects.filter(id_user__in=user_sekdept)
                    # email_list=[]
                    for i in sekdept_filter:
                        notifikasi.objects.create(nip=i.nip,messages=f"Terdapat {cek_jumlah_sempro_sum} Mahasiswa belum di assign majelis seminar proposal diantaranya {nama_nim_sempro}  pada {tanggal} Jam {Jam}")

                    # send ke sekdept
                    email_list=[]
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
                    for i in range(len(temp_email)):
                        email_list.append(temp_email[i][0])
                    send_mail(
                        'Terdapat Mahasiswa Belum Assign Jadwal',
                        f"Terdapat {cek_jumlah_sempro_sum} Mahasiswa belum di assign majelis seminar proposal diantaranya {nama_nim_sempro}  pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                    )
                # hitung semhas
                
                list_jadwal_semhas=list(jadwal_seminar.objects.filter(tahap_seminar="Seminar Hasil").values_list("mahasiswa",flat=True))
                list_jadwal_semhas = list(filter(lambda x: x is not None and x != '', list_jadwal_semhas))
             
                cek_jumlah_semhas=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_semhas)
                cek_jumlah_semhas_sum=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_semhas).count()
                if cek_jumlah_semhas_sum>=3:
                    nama_nim_semhas=[]
                    for i in cek_jumlah_semhas:
                        nama_nim_semhas.append(i.id_role_dosen.nim)
                    # print(nama_nim_sempro)
                    user_sekdept=list(User.objects.values_list('id').filter(groups__name='Manajemen Departemen'))
                    # print(user_sekdept)
                    sekdept_filter=dosen.objects.filter(id_user__in=user_sekdept)
                    # email_list=[]
                    for i in sekdept_filter:
                        notifikasi.objects.create(nip=i.nip,messages=f"Terdapat {cek_jumlah_semhas_sum} Mahasiswa belum di assign majelis seminar hasil diantaranya {nama_nim_semhas}  pada {tanggal} Jam {Jam}")

                    # send ke sekdept
                    email_list=[]
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
                    for i in range(len(temp_email)):
                        email_list.append(temp_email[i][0])
                    send_mail(
                        'Terdapat Mahasiswa Belum Assign Jadwal',
                        f"Terdapat {cek_jumlah_semhas_sum} Mahasiswa belum di assign majelis seminar hasil diantaranya {nama_nim_semhas}  pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                    )


                return redirect("../proposalget/pembimbing")
   
    else :
        # print(4)
        form = BimbinganFormDosenUpdate()
   

    return render(request, 'bimbingan/bimbingan_update.html', {"form": form, "data":proposal_data, "user_info": user_info})

# # Membuat data bimbingan proposal dari id proposal  
# todo: add in notification and email
# @login_required(login_url="/login")
# @role_required(allowed_roles=['Admin',  'Manajemen Departemen','Kompartemen','Dosen','Properta'])
# def bimbingan_create_dosen(request, id):
#     user_info = user_information(request)
#     proposal_data = proposal.objects.get(pk=id)
#     proposal_data_count=proposal.objects.filter(pk=id).count()
#     # print(proposal_data_count)
#     # proposal_data_count=
#         # bimbingan_data = proposal.objects.get(pk=id)
#         # print(bimbingan_data.ID_proposal.File_Proposal)
#     if proposal_data_count==0:
#         try:
#             bimbingan_data=bimbingan.objects.get(id_proposal=proposal_data)
#             # bimbingan_data=bimbingan_data.ID_Proposal

#         except:
#             bimbingan_data=None
#     else:
#         try:
#             bimbingan_data=bimbingan.objects.get(id_proposal=proposal_data)
#             # bimbingan_data=bimbingan_data.ID_Proposal

#         except:
#             bimbingan_data=None
#     # print(bimbingan_data != None)
#     # print(bimbingan_data == None)
#     # print(bimbingan_data.ID_proposal.File_proposal.url)
#     # print()
#     # print(proposal_data.file_proposal.url)
#     if request.method == "POST" and  bimbingan_data != None:
#         # print(1)
#         proposal_data = proposal.objects.get(pk=id)
        
#         form = BimbinganFormDosenUpdate(request.POST,instance=bimbingan_data)
#         if form.is_valid():
#                 create_bimbingan = form.save(commit=False)
#                 # create_bimbingan.id_role_dosen = roledosen.objects.filter(
#                 # create_bimbingan.id_role_dosen = roledosen.objects.filter(
#                 #     nip=dosen.objects.get(pk=user_info[0])).filter(nim=mahasiswa.objects.get(pk=proposal_data.nim.nim))[0]
#                 # create_bimbingan.ID_Proposal = proposal_data.ID_Proposal
#                 create_bimbingan.save()
#                 messages.success(request,"Data Bimbingan Telah Berhasil Dibuat! ")
#                 notifikasi.objects.create(nim=create_bimbingan.id_proposal.nim.nim,messages=f"Terdapat Revisi Bimbingan Baru Oleh {create_bimbingan.id_role_dosen.nip.id_user.first_name} pada {tanggal} Jam {Jam}")
#                 # send ke mahasiswa
#                 email_list=[]
#                 temp_email=list(User.objects.filter(pk=create_bimbingan.id_proposal.nim.id_user.id).values_list('email'))
#                 email_list.append(temp_email[0][0])
#                 send_mail(
#                     'Hasil Revisi Proposal Telah Di Buat ',
#                     f"Terdapat Revisi Bimbingan Baru Oleh Dosen {create_bimbingan.id_role_dosen.nip.id_user.first_name} pada {tanggal} Jam {Jam}",
#                     settings.EMAIL_HOST_USER,
#                     email_list,
#                     fail_silently=False,
#                 )
#                   # Hitung Sempro
#                 list_jadwal_sempro=[]
#                 cek_jumlah_seminar_proposal=jadwal_seminar.objects.filter(tahap_seminar="Seminar Proposal").values_list("mahasiswa")
#                 for i in cek_jumlah_seminar_proposal:
#                     for j in i :
#                         # print(j)
#                         if j==None or j=="":
#                             pass
#                         else :
#                             list_jadwal_sempro.append(j.split("-")[0])
#                 cek_jumlah_sempro=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro)
#                 cek_jumlah_sempro_sum=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro).count()
#                 if cek_jumlah_sempro_sum>=3:
#                     nama_nim_sempro=[]
#                     for i in cek_jumlah_sempro:
#                         nama_nim_sempro.append(i.id_role_dosen.nim)
#                     # print(nama_nim_sempro)
#                     user_sekdept=list(User.objects.values_list('id').filter(groups__name='Manajemen Departemen'))
#                     # print(user_sekdept)
#                     sekdept_filter=dosen.objects.filter(id_user__in=user_sekdept)
#                     # email_list=[]
#                     for i in sekdept_filter:
#                         notifikasi.objects.create(nip=i.nip,messages=f"Terdapat {cek_jumlah_sempro_sum} Mahasiswa belum di assign majelis seminar proposal diantaranya {nama_nim_sempro}  pada {tanggal} Jam {Jam}")

#                     # send ke sekdept
#                     email_list=[]
#                     # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
#                     temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
#                     for i in range(len(temp_email)):
#                         email_list.append(temp_email[i][0])
#                     send_mail(
#                         'Terdapat Mahasiswa Belum Assign Jadwal',
#                         f"Terdapat {cek_jumlah_sempro_sum} Mahasiswa belum di assign majelis seminar proposal diantaranya {nama_nim_sempro}  pada {tanggal} Jam {Jam}",
#                         settings.EMAIL_HOST_USER,
#                         email_list,
#                         fail_silently=False,
#                     )
#                 # hitung semhas
#                 list_jadwal_semhas=[]
#                 cek_jumlah_seminar_hasil=jadwal_seminar.objects.filter(tahap_seminar="Seminar Hasil").values_list("mahasiswa")
#                 for i in cek_jumlah_seminar_hasil:
#                     for j in i :
#                         # print(j)
#                         if j==None or j=="":
#                             pass
#                         else :
#                             list_jadwal_semhas.append(j.split("-")[0])
#                 cek_jumlah_semhas=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro)
#                 cek_jumlah_semhas_sum=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro).count()
#                 if cek_jumlah_semhas_sum>=3:
#                     nama_nim_semhas=[]
#                     for i in cek_jumlah_semhas:
#                         nama_nim_semhas.append(i.id_role_dosen.nim)
#                     # print(nama_nim_sempro)
#                     user_sekdept=list(User.objects.values_list('id').filter(groups__name='Manajemen Departemen'))
#                     # print(user_sekdept)
#                     sekdept_filter=dosen.objects.filter(id_user__in=user_sekdept)
#                     # email_list=[]
#                     for i in sekdept_filter:
#                         notifikasi.objects.create(nip=i.nip,messages=f"Terdapat {cek_jumlah_semhas_sum} Mahasiswa belum di assign majelis seminar hasil diantaranya {nama_nim_semhas}  pada {tanggal} Jam {Jam}")

#                     # send ke sekdept
#                     email_list=[]
#                     # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
#                     temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
#                     for i in range(len(temp_email)):
#                         email_list.append(temp_email[i][0])
#                     send_mail(
#                         'Terdapat Mahasiswa Belum Assign Jadwal',
#                         f"Terdapat {cek_jumlah_semhas_sum} Mahasiswa belum di assign majelis seminar hasil diantaranya {nama_nim_semhas}  pada {tanggal} Jam {Jam}",
#                         settings.EMAIL_HOST_USER,
#                         email_list,
#                         fail_silently=False,
#                     )

#                 # contoh : notif
#                     # user_sekdept=list(User.objects.value_list('id_user').filter(groups__name='Manajemen Departemen'))
#                     # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
#                     # for i in sekdept_filter:
#                     #     models.notifikasi.nip=i.nip
#                     #     models.notifikasi.messages=f"Terdapat Input Usulan Topik Baru Oleh {create_usulantopik.nim} pada {tanggal} Jam {Jam}"
#                     #     notifikasi.save()
#                 return redirect("../proposalget/pembimbing")
#     elif request.method == "POST" and  bimbingan_data == None:
#         # print(2)
#         form = BimbinganFormDosenUpdate(request.POST)
#         if form.is_valid():
#                 create_bimbingan = form.save(commit=False)
#                 # create_bimbingan.id_role_dosen = roledosen.objects.filter(
#                 create_bimbingan.id_role_dosen = roledosen.objects.filter(
#                     nip=dosen.objects.get(pk=user_info[0])).filter(nim=mahasiswa.objects.get(pk=proposal_data.nim.nim))[0]
#                 create_bimbingan.id_proposal = proposal_data
#                 create_bimbingan.save()
#                 notifikasi.objects.create(nim=create_bimbingan.id_proposal.nim.nim,messages=f"Terdapat Revisi Bimbingan Baru Oleh {create_bimbingan.id_role_dosen.nip.id_user.first_name} pada {tanggal} Jam {Jam}")
#                 # send ke mahasiswa
#                 email_list=[]
                
#                 temp_email=list(User.objects.filter(pk=create_bimbingan.id_proposal.nim.id_user.id).values_list('email'))
#                 email_list.append(temp_email[0][0])
                
#                 send_mail(
#                     'Hasil Revisi Proposal Telah Di Buat ',
#                     f"Terdapat Revisi Bimbingan Baru Oleh {create_bimbingan.id_role_dosen.nip.id_user.first_name} pada {tanggal} Jam {Jam}",
#                     settings.EMAIL_HOST_USER,
#                     email_list,
#                     fail_silently=False,
#                 )
#                   # Hitung Sempro
#                 list_jadwal_sempro=[]
#                 cek_jumlah_seminar_proposal=jadwal_seminar.objects.filter(tahap_seminar="Seminar Proposal").values_list("mahasiswa")
#                 for i in cek_jumlah_seminar_proposal:
#                     for j in i :
#                         # print(j)
#                         if j==None or j=="":
#                             pass
#                         else :
#                             list_jadwal_sempro.append(j.split("-")[0])
#                 cek_jumlah_sempro=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro)
#                 cek_jumlah_sempro_sum=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro).count()
#                 if cek_jumlah_sempro_sum>=3:
#                     nama_nim_sempro=[]
#                     for i in cek_jumlah_sempro:
#                         nama_nim_sempro.append(i.id_role_dosen.nim)
#                     # print(nama_nim_sempro)
#                     user_sekdept=list(User.objects.values_list('id').filter(groups__name='Manajemen Departemen'))
#                     # print(user_sekdept)
#                     sekdept_filter=dosen.objects.filter(id_user__in=user_sekdept)
#                     # email_list=[]
#                     for i in sekdept_filter:
#                         notifikasi.objects.create(nip=i.nip,messages=f"Terdapat {cek_jumlah_sempro_sum} Mahasiswa belum di assign majelis seminar proposal diantaranya {nama_nim_sempro}  pada {tanggal} Jam {Jam}")

#                     # send ke sekdept
#                     email_list=[]
#                     # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
#                     temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
#                     for i in range(len(temp_email)):
#                         email_list.append(temp_email[i][0])
#                     send_mail(
#                         'Terdapat Mahasiswa Belum Assign Jadwal',
#                         f"Terdapat {cek_jumlah_sempro_sum} Mahasiswa belum di assign majelis seminar proposal diantaranya {nama_nim_sempro}  pada {tanggal} Jam {Jam}",
#                         settings.EMAIL_HOST_USER,
#                         email_list,
#                         fail_silently=False,
#                     )
#                 # hitung semhas
#                 list_jadwal_semhas=[]
#                 cek_jumlah_seminar_hasil=jadwal_seminar.objects.filter(tahap_seminar="Seminar Hasil").values_list("mahasiswa")
#                 for i in cek_jumlah_seminar_hasil:
#                     for j in i :
#                         # print(j)
#                         if j==None or j=="":
#                             pass
#                         else :
#                             list_jadwal_semhas.append(j.split("-")[0])
#                 cek_jumlah_semhas=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro)
#                 cek_jumlah_semhas_sum=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro).count()
#                 if cek_jumlah_semhas_sum>=3:
#                     nama_nim_semhas=[]
#                     for i in cek_jumlah_semhas:
#                         nama_nim_semhas.append(i.id_role_dosen.nim)
#                     # print(nama_nim_sempro)
#                     user_sekdept=list(User.objects.values_list('id').filter(groups__name='Manajemen Departemen'))
#                     # print(user_sekdept)
#                     sekdept_filter=dosen.objects.filter(id_user__in=user_sekdept)
#                     # email_list=[]
#                     for i in sekdept_filter:
#                         notifikasi.objects.create(nip=i.nip,messages=f"Terdapat {cek_jumlah_semhas_sum} Mahasiswa belum di assign majelis seminar hasil diantaranya {nama_nim_semhas}  pada {tanggal} Jam {Jam}")

#                     # send ke sekdept
#                     email_list=[]
#                     # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
#                     temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
#                     for i in range(len(temp_email)):
#                         email_list.append(temp_email[i][0])
#                     send_mail(
#                         'Terdapat Mahasiswa Belum Assign Jadwal',
#                         f"Terdapat {cek_jumlah_semhas_sum} Mahasiswa belum di assign majelis seminar hasil diantaranya {nama_nim_semhas}  pada {tanggal} Jam {Jam}",
#                         settings.EMAIL_HOST_USER,
#                         email_list,
#                         fail_silently=False,
#                     )
                    

#                 # contoh : notif
#                     # user_sekdept=list(User.objects.value_list('id_user').filter(groups__name='Manajemen Departemen'))
#                     # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
#                     # for i in sekdept_filter:
#                     #     models.notifikasi.nip=i.nip
#                     #     models.notifikasi.messages=f"Terdapat Input Usulan Topik Baru Oleh {create_usulantopik.nim} pada {tanggal} Jam {Jam}"
#                     #     notifikasi.save()
#                 return redirect("../bimbinganget")
#     elif bimbingan_data == None:
#         # print(3)
#         form = BimbinganFormDosenUpdate()
#     else :
#         # print(4)
#         form = BimbinganFormDosenUpdate(instance=bimbingan_data)
   

#     return render(request, 'bimbingan/bimbingan_update.html', {"form": form, "data":proposal_data, "user_info": user_info})



# Bimbingan : Update
# # Mengubah data bimbingan proposal berdasarakan id bimbingan
# todo: add in notification and email
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin',  'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def bimbingan_update_proposal(request, id):
    user_info = user_information(request)
    proposal_data = proposal.objects.get(pk=id)
    bimbingan_data=bimbingan.objects.get(id_proposal=proposal_data)
    # print(proposal_data.file_proposal.url)
    if user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        if request.method == "POST":
            form = BimbinganForm(request.POST, instance=bimbingan_data)
            if form.is_valid():
                create_roledosen = form.save()
                create_roledosen.save()
                messages.warning(request,"Data Bimbingan Telah Berhasil Dirubah! ")
                notifikasi.objects.create(nim=create_roledosen.id_proposal.nim,messages=f"Terdapat Update Revisi Bimbingan Baru Oleh {create_roledosen.id_role_dosen.nip.id_user.first_name} pada {tanggal} Jam {Jam}")
                # send ke mahasiswa
                
                email_list=[]
                temp_email=list(User.objects.filter(pk=create_roledosen.id_proposal.nim.id_user.id).values_list('email'))
                email_list.append(temp_email[0][0])
               
                send_mail(
                    'Terdapat Update Hasil Revisi Proposal Telah Di Buat ',
                    f"Terdapat Update Revisi Bimbingan Baru Oleh {create_roledosen.id_role_dosen.nip.id_user.first_name} pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                )
                  # Hitung Sempro
                list_jadwal_sempro=list(jadwal_seminar.objects.filter(tahap_seminar="Seminar Proposal").values_list("mahasiswa",flat=True))
                list_jadwal_sempro = list(filter(lambda x: x is not None and x != '', list_jadwal_sempro))
                cek_jumlah_sempro=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro)
                cek_jumlah_sempro_sum=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro).count()
                if cek_jumlah_sempro_sum>=3:
                    nama_nim_sempro=[]
                    for i in cek_jumlah_sempro:
                        nama_nim_sempro.append(i.id_role_dosen.nim)
                    # print(nama_nim_sempro)
                    user_sekdept=list(User.objects.values_list('id').filter(groups__name='Manajemen Departemen'))
                    # print(user_sekdept)
                    sekdept_filter=dosen.objects.filter(id_user__in=user_sekdept)
                    # email_list=[]
                    for i in sekdept_filter:
                        notifikasi.objects.create(nip=i.nip,messages=f"Terdapat {cek_jumlah_sempro_sum} Mahasiswa belum di assign majelis seminar proposal diantaranya {nama_nim_sempro}  pada {tanggal} Jam {Jam}")

                    # send ke sekdept
                    email_list=[]
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
                    for i in range(len(temp_email)):
                        email_list.append(temp_email[i][0])
                    send_mail(
                        'Terdapat Mahasiswa Belum Assign Jadwal',
                        f"Terdapat {cek_jumlah_sempro_sum} Mahasiswa belum di assign majelis seminar proposal diantaranya {nama_nim_sempro}  pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                    )
                # hitung semhas
                list_jadwal_semhas=list(jadwal_seminar.objects.filter(tahap_seminar="Seminar Hasil").values_list("mahasiswa",flat=True))
                list_jadwal_semhas = list(filter(lambda x: x is not None and x != '', list_jadwal_semhas))
                cek_jumlah_semhas=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro)
                cek_jumlah_semhas_sum=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro).count()
                if cek_jumlah_semhas_sum>=3:
                    nama_nim_semhas=[]
                    for i in cek_jumlah_semhas:
                        nama_nim_semhas.append(i.id_role_dosen.nim)
                    # print(nama_nim_sempro)
                    user_sekdept=list(User.objects.values_list('id').filter(groups__name='Manajemen Departemen'))
                    # print(user_sekdept)
                    sekdept_filter=dosen.objects.filter(id_user__in=user_sekdept)
                    # email_list=[]
                    for i in sekdept_filter:
                        notifikasi.objects.create(nip=i.nip,messages=f"Terdapat {cek_jumlah_semhas_sum} Mahasiswa belum di assign majelis seminar hasil diantaranya {nama_nim_semhas}  pada {tanggal} Jam {Jam}")

                    # send ke sekdept
                    email_list=[]
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
                    for i in range(len(temp_email)):
                        email_list.append(temp_email[i][0])
                    send_mail(
                        'Terdapat Mahasiswa Belum Assign Jadwal',
                        f"Terdapat {cek_jumlah_semhas_sum} Mahasiswa belum di assign majelis seminar hasil diantaranya {nama_nim_semhas}  pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                    )

                # contoh : notif
                    # user_sekdept=list(User.objects.value_list('id_user').filter(groups__name='Manajemen Departemen'))
                    # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
                    # for i in sekdept_filter:
                    #     models.notifikasi.nip=i.nip
                    #     models.notifikasi.messages=f"Terdapat Input Usulan Topik Baru Oleh {create_usulantopik.nim} pada {tanggal} Jam {Jam}"
                    #     notifikasi.save()
                return redirect("../bimbinganget")
        else:
            form = BimbinganForm(instance=bimbingan_data)
    else:
        if request.method == "POST":
            form = BimbinganFormDosen(request.POST, instance=bimbingan_data)
            if form.is_valid():
                create_roledosen = form.save()
                create_roledosen.save()
                notifikasi.objects.create(nim=create_roledosen.id_proposal.nim,messages=f"Terdapat Update Revisi Bimbingan Baru Oleh {create_roledosen.id_role_dosen.nip.id_user.first_name} pada {tanggal} Jam {Jam}")
                # send ke mahasiswa
                email_list=[]
                
                temp_email=list(User.objects.filter(pk=create_roledosen.id_proposal.nim.id_user.id).values_list('email'))
                email_list.append(temp_email[0][0])
                
                send_mail(
                    'Terdapat Update Hasil Revisi Proposal Telah Di Buat ',
                    f"Terdapat Update Revisi Bimbingan Baru Oleh {create_roledosen.id_role_dosen.nip.id_user.first_name} pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                )

                  # Hitung Sempro
                list_jadwal_sempro=list(jadwal_seminar.objects.filter(tahap_seminar="Seminar Proposal").values_list("mahasiswa",flat=True))
                list_jadwal_sempro = list(filter(lambda x: x is not None and x != '', list_jadwal_sempro))
                cek_jumlah_sempro=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro)
                cek_jumlah_sempro_sum=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro).count()
                if cek_jumlah_sempro_sum>=3:
                    nama_nim_sempro=[]
                    for i in cek_jumlah_sempro:
                        nama_nim_sempro.append(i.id_role_dosen.nim)
                    # print(nama_nim_sempro)
                    user_sekdept=list(User.objects.values_list('id').filter(groups__name='Manajemen Departemen'))
                    # print(user_sekdept)
                    sekdept_filter=dosen.objects.filter(id_user__in=user_sekdept)
                    # email_list=[]
                    for i in sekdept_filter:
                        notifikasi.objects.create(nip=i.nip,messages=f"Terdapat {cek_jumlah_sempro_sum} Mahasiswa belum di assign majelis seminar proposal diantaranya {nama_nim_sempro}  pada {tanggal} Jam {Jam}")

                    # send ke sekdept
                    email_list=[]
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
                    for i in range(len(temp_email)):
                        email_list.append(temp_email[i][0])
                    send_mail(
                        'Terdapat Mahasiswa Belum Assign Jadwal',
                        f"Terdapat {cek_jumlah_sempro_sum} Mahasiswa belum di assign majelis seminar proposal diantaranya {nama_nim_sempro}  pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                    )
                # hitung semhas
                list_jadwal_semhas=list(jadwal_seminar.objects.filter(tahap_seminar="Seminar Hasil").values_list("mahasiswa",flat=True))
                list_jadwal_semhas = list(filter(lambda x: x is not None and x != '', list_jadwal_semhas))

                cek_jumlah_semhas=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_semhas)
                cek_jumlah_semhas_sum=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_semhas).count()
                if cek_jumlah_semhas_sum>=3:
                    nama_nim_semhas=[]
                    for i in cek_jumlah_semhas:
                        nama_nim_semhas.append(i.id_role_dosen.nim)
                    # print(nama_nim_sempro)
                    user_sekdept=list(User.objects.values_list('id').filter(groups__name='Manajemen Departemen'))
                    # print(user_sekdept)
                    sekdept_filter=dosen.objects.filter(id_user__in=user_sekdept)
                    # email_list=[]
                    for i in sekdept_filter:
                        notifikasi.objects.create(nip=i.nip,messages=f"Terdapat {cek_jumlah_semhas_sum} Mahasiswa belum di assign majelis seminar hasil diantaranya {nama_nim_semhas}  pada {tanggal} Jam {Jam}")

                    # send ke sekdept
                    email_list=[]
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
                    for i in range(len(temp_email)):
                        email_list.append(temp_email[i][0])
                    send_mail(
                        'Terdapat Mahasiswa Belum Assign Jadwal',
                        f"Terdapat {cek_jumlah_semhas_sum} Mahasiswa belum di assign majelis seminar hasil diantaranya {nama_nim_semhas}  pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                    )

                return redirect("../bimbinganget")
        else:
            form = BimbinganFormDosen(instance=bimbingan_data)
    return render(request, 'bimbingan/bimbingan_update.html', {"form": form,"data":proposal_data, "user_info": user_info})


# bimbingan:read
# Melihat list  data bimbingan bedasarkan nim untuk mahasiswa  & berdasarkan  role dosen untuk dosen 
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Mahasiswa', 'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def bimbingan_get(request):
    user_info = user_information(request)
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        bimbingans = bimbingan.objects.filter(id_role_dosen__nip=user_info[0]).filter(
            id_role_dosen__role="Pembimbing 1") | bimbingan.objects.filter(id_role_dosen__nip=user_info[0]).filter(
            id_role_dosen__role="Pembimbing 2")
        # bimbingans = []
        # bimbingan1 = bimbingan.objects.get(id_role_dosen=roledosen.objects.filter(
        #     nip=dosen.objects.filter(pk=user_info[0])[0]).filter(role="Pembimbing 1")[0])
        # bimbingan2 = bimbingan.objects.get(id_role_dosen=roledosen.objects.filter(
        #     nip=dosen.objects.filter(pk=user_info[0])[0]).filter(role="Pembimbing 2")[0])
        # bimbingans.append(bimbingan1)
        # bimbingans.append(bimbingan2)

    elif user_info[2].name == "Mahasiswa":
        bimbingans = bimbingan.objects.filter(
            id_proposal__nim=mahasiswa.objects.filter(pk=user_info[0])[0])

    else:
        bimbingans = bimbingan.objects.all()
    # print(bimbingans)
    return render(request, 'bimbingan/bimbingan_get.html', {"bimbingans": bimbingans, "user_info": user_info})
# Filter list bimbingan yang acc 
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Mahasiswa', 'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def bimbingan_get_acc(request):
    user_info = user_information(request)
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        bimbingans = bimbingan.objects.filter(id_role_dosen__nip=user_info[0]).filter(
            id_role_dosen__role="Pembimbing 1") | bimbingan.objects.filter(id_role_dosen__nip=user_info[0]).filter(
            id_role_dosen__role="Pembimbing 2")
        # bimbingans = []
        # bimbingan1 = bimbingan.objects.get(id_role_dosen=roledosen.objects.filter(
        #     nip=dosen.objects.filter(pk=user_info[0])[0]).filter(role="Pembimbing 1")[0])
        # bimbingan2 = bimbingan.objects.get(id_role_dosen=roledosen.objects.filter(
        #     nip=dosen.objects.filter(pk=user_info[0])[0]).filter(role="Pembimbing 2")[0])
        # bimbingans.append(bimbingan1)
        # bimbingans.append(bimbingan2)

    elif user_info[2].name == "Mahasiswa":
        bimbingans = bimbingan.objects.filter(
            id_proposal__nim=mahasiswa.objects.filter(pk=user_info[0])[0])

    else:
        bimbingans = bimbingan.objects.all()
    bimbingans.filter(status_bimbingan="ACC")
    # print(bimbingans)
    return render(request, 'bimbingan/bimbingan_get.html', {"bimbingans": bimbingans, "user_info": user_info})
# Filter bimbingan dengan status belum diperiksa 
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Mahasiswa', 'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def bimbingan_get_lain_lain(request):
    user_info = user_information(request)
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        bimbingans = bimbingan.objects.filter(id_role_dosen__nip=user_info[0]).filter(
            id_role_dosen__role="Pembimbing 1") | bimbingan.objects.filter(id_role_dosen__nip=user_info[0]).filter(
            id_role_dosen__role="Pembimbing 2")
        # bimbingans = []
        # bimbingan1 = bimbingan.objects.get(id_role_dosen=roledosen.objects.filter(
        #     nip=dosen.objects.filter(pk=user_info[0])[0]).filter(role="Pembimbing 1")[0])
        # bimbingan2 = bimbingan.objects.get(id_role_dosen=roledosen.objects.filter(
        #     nip=dosen.objects.filter(pk=user_info[0])[0]).filter(role="Pembimbing 2")[0])
        # bimbingans.append(bimbingan1)
        # bimbingans.append(bimbingan2)

    elif user_info[2].name == "Mahasiswa":
        bimbingans = bimbingan.objects.filter(
            id_proposal__nim=mahasiswa.objects.filter(pk=user_info[0])[0])

    else:
        bimbingans = bimbingan.objects.all()
    bimbingans.exclude(status_bimbingan="ACC").exclude(status_bimbingan="Revisi")
    # print(bimbingans)
    return render(request, 'bimbingan/bimbingan_get.html', {"bimbingans": bimbingans, "user_info": user_info})
# Filter bimbingan dengan status sudah diperiksa 
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Mahasiswa', 'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def bimbingan_get_sudah_diperiksa(request):
    user_info = user_information(request)
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        bimbingans = bimbingan.objects.filter(id_role_dosen__nip=user_info[0]).filter(
            id_role_dosen__role="Pembimbing 1") | bimbingan.objects.filter(id_role_dosen__nip=user_info[0]).filter(
            id_role_dosen__role="Pembimbing 2")
        # bimbingans = []
        # bimbingan1 = bimbingan.objects.get(id_role_dosen=roledosen.objects.filter(
        #     nip=dosen.objects.filter(pk=user_info[0])[0]).filter(role="Pembimbing 1")[0])
        # bimbingan2 = bimbingan.objects.get(id_role_dosen=roledosen.objects.filter(
        #     nip=dosen.objects.filter(pk=user_info[0])[0]).filter(role="Pembimbing 2")[0])
        # bimbingans.append(bimbingan1)
        # bimbingans.append(bimbingan2)

    elif user_info[2].name == "Mahasiswa":
        bimbingans = bimbingan.objects.filter(
            id_proposal__nim=mahasiswa.objects.filter(pk=user_info[0])[0])

    else:
        bimbingans = bimbingan.objects.all()
    bimbingans.filter(status_bimbingan__in=["Revisi","ACC"])
    # print(bimbingans)
    return render(request, 'bimbingan/bimbingan_get.html', {"bimbingans": bimbingans, "user_info": user_info})
# Filter bimbingan dengan status revisi 
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Mahasiswa', 'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def bimbingan_get_revisi(request):
    user_info = user_information(request)
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        bimbingans = bimbingan.objects.filter(id_role_dosen__nip=user_info[0]).filter(
            id_role_dosen__role="Pembimbing 1") | bimbingan.objects.filter(id_role_dosen__nip=user_info[0]).filter(
            id_role_dosen__role="Pembimbing 2")
        # bimbingans = []
        # bimbingan1 = bimbingan.objects.get(id_role_dosen=roledosen.objects.filter(
        #     nip=dosen.objects.filter(pk=user_info[0])[0]).filter(role="Pembimbing 1")[0])
        # bimbingan2 = bimbingan.objects.get(id_role_dosen=roledosen.objects.filter(
        #     nip=dosen.objects.filter(pk=user_info[0])[0]).filter(role="Pembimbing 2")[0])
        # bimbingans.append(bimbingan1)
        # bimbingans.append(bimbingan2)


    elif user_info[2].name == "Mahasiswa":
        bimbingans = bimbingan.objects.filter(
            id_proposal__nim=mahasiswa.objects.filter(pk=user_info[0])[0])

    else:
        bimbingans = bimbingan.objects.all()
    bimbingans.filter(status_bimbingan="Revisi")
    # print(bimbingans)
    return render(request, 'bimbingan/bimbingan_get.html', {"bimbingans": bimbingans, "user_info": user_info})


# CHECKPOINT : perbaikan penilaian
# menampilkan list detail penilaian aka review seminar
@login_required(login_url="/login")
@role_required(allowed_roles=[ 'Mahasiswa'])
def list_detail_penilaian(request):
    user_info = user_information(request)
    # hasil_review=detailpenilaian.objects.all()
    hasil_review=detailpenilaian.objects.filter(id_role_dosen__nim__nim=user_info[0])
    return render(request, 'penilaian/list_review_get.html', {"hasil_review": hasil_review, "user_info": user_info})
# menampilkan list detail penilaian pembimbingan
@login_required(login_url="/login")
@role_required(allowed_roles=[ 'Mahasiswa'])
def list_detail_penilaian_bimbingan(request):
    user_info = user_information(request)
    hasil_review=detailpenilaian.objects.filter(id_role_dosen__nim__nim=user_info[0]).filter(nama_tahap="Bimbingan")
    return render(request, 'penilaian/list_review_get.html', {"hasil_review": hasil_review, "user_info": user_info})
# menampilkan list detail penilaian aka review seminar proposal
@login_required(login_url="/login")
@role_required(allowed_roles=[ 'Mahasiswa'])
def list_detail_penilaian_sempro(request):
    user_info = user_information(request)
    # hasil_review=detailpenilaian.objects.all().filter(nama_tahap="Seminar Proposal")
    hasil_review=detailpenilaian.objects.filter(id_role_dosen__nim__nim=user_info[0]).filter(nama_tahap="Seminar Proposal")
    return render(request, 'penilaian/list_review_get.html', {"hasil_review": hasil_review, "user_info": user_info})
# menampilkan list detail penilaian aka review seminar hasil
@login_required(login_url="/login")
@role_required(allowed_roles=[ 'Mahasiswa'])
def list_detail_penilaian_semhas(request):
    user_info = user_information(request)
    hasil_review=detailpenilaian.objects.filter(id_role_dosen__nim__nim=user_info[0]).filter(nama_tahap="Seminar Hasil")
    return render(request, 'penilaian/list_review_get.html', {"hasil_review": hasil_review, "user_info": user_info})

# # Melihat list data bimbingan proposal  untuk dosen penguji sempro (?) 
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Mahasiswa', 'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def bimbingan_get_sempro(request):
    user_info = user_information(request)
    role="Dosen Seminar Proposal"
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        bimbingans = bimbingan.objects.filter(id_role_dosen__nip=user_info[0]).filter(
            id_role_dosen__role="Penguji Seminar Proposal 1").latest('Tanggal_Update') | bimbingan.objects.filter(id_role_dosen__nip=user_info[0]).filter(
            id_role_dosen__role="Penguji Seminar Proposal 2").latest('Tanggal_Update')

    elif user_info[2].name == "Mahasiswa":
        bimbingans = bimbingan.objects.filter(
            nim=mahasiswa.objects.filter(pk=user_info[0])[0])

    else:
        bimbingans = bimbingan.objects.all()
    # print(bimbingans)
    return render(request, 'bimbingan/bimbingan_get.html', {"bimbingans": bimbingans,"role":role, "user_info": user_info})

# # melihat data bimbingan berdasarkan id proposal  
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Mahasiswa', 'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def bimbingan_get_proposal(request,id):
    user_info = user_information(request)

    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen"or user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        bimbingans = bimbingan.objects.filter(id_role_dosen__nip=user_info[0]).filter(
            id_role_dosen__role="Pembimbing 1").filter(id_proposal=id) | bimbingan.objects.filter(id_role_dosen__nip=user_info[0]).filter(
            id_role_dosen__role="Pembimbing 2").filter(id_proposal=id)

    elif user_info[2].name == "Mahasiswa":
        bimbingans = bimbingan.objects.filter(
            nim=mahasiswa.objects.filter(pk=user_info[0])[0]).filter(id_proposal=id)

    else:
        bimbingans = bimbingan.objects.all()
    # print(bimbingans)
    status="filter proposal"
    return render(request, 'bimbingan/bimbingan_get.html', {"bimbingans": bimbingans,"status_asal":status, "user_info": user_info})

# # melihat list data bimbingan proposal berbentuk form berdasarkan id bimbingan  
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Mahasiswa', 'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def bimbingan_read(request, id):
    user_info = user_information(request)
    bimbingan_data = bimbingan.objects.get(pk=id)
    if user_info[2].name == "Mahasiswa" :
        if int(bimbingan_data.id_role_dosen.nim.nim)!=int(user_info[0]):
            raise PermissionDenied()
        else:
            pass
    # print(bimbingan_data.id_role_dosen.nim.nim==user_info[0])
    # print(user_info[0])
    form = BimbinganForm(instance=bimbingan_data)
    field = ["id_proposal","status_bimbingan", "catatan"]
    for item in form.fields:
        # form.field.disabled = True
        form.fields[item].disabled = True
    
    # form.disabled = True

    return render(request, 'bimbingan/bimbingan_read.html', {"form": form,"bimbingan_data":bimbingan_data, "user_info": user_info})


# bimbingan:update
# mengubah data bimbingan proposal berdasarkan id bimbingan  
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin',  'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def bimbingan_update(request, id):
    user_info = user_information(request)
    bimbingan_data = bimbingan.objects.get(pk=id)
    # proposal_data=proposal.objects.filter(id_proposal=bimbingan_data.id_proposal).first()
    # print(proposal_data.file_proposal.url)
    if user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        if request.method == "POST":
            form = BimbinganForm(request.POST, instance=bimbingan_data)
            if form.is_valid():
                create_roledosen = form.save()
                instances = bimbingan.objects.filter(id_proposal=bimbingan_data.id_proposal).order_by('tanggal_buat')
                if instances.exists(): # Pastikan QuerySet tidak kosong
                    instances.update(status_bimbingan='Revisi') # Mengubah status untuk semua objek
                create_roledosen.save()
                messages.warning(request,"Data Bimbingan Telah Berhasil Dirubah! ")
                notifikasi.objects.create(nim=create_roledosen.id_proposal.nim,messages=f"Terdapat Update Revisi Bimbingan Baru Oleh {create_roledosen.id_role_dosen.nip.id_user.first_name} pada {tanggal} Jam {Jam}")
                # send ke mahasiswa
                email_list=[]
                
                temp_email=list(User.objects.filter(pk=create_roledosen.id_proposal.nim.id_user.id).values_list('email'))
                email_list.append(temp_email[0][0])
                # send ke mahasiswa
                # email_list=User.objects.filter(pk=create_roledosen.id_proposal.nim.id_user).values_list('email')
                send_mail(
                    'Terdapat Update Hasil Revisi Proposal Telah Di Buat ',
                    f"Terdapat Update Revisi Bimbingan Baru Oleh {create_roledosen.id_role_dosen.nip.id_user.first_name} pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                )
                  # Hitung Sempro
                list_jadwal_sempro=list(jadwal_seminar.objects.filter(tahap_seminar="Seminar Proposal").values_list("mahasiswa",flat=True))
                list_jadwal_sempro = list(filter(lambda x: x is not None and x != '', list_jadwal_sempro))
                cek_jumlah_sempro=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro)
                cek_jumlah_sempro_sum=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro).count()
                if cek_jumlah_sempro_sum>=3:
                    nama_nim_sempro=[]
                    for i in cek_jumlah_sempro:
                        nama_nim_sempro.append(i.id_role_dosen.nim)
                    # print(nama_nim_sempro)
                    user_sekdept=list(User.objects.values_list('id').filter(groups__name='Manajemen Departemen'))
                    # print(user_sekdept)
                    sekdept_filter=dosen.objects.filter(id_user__in=user_sekdept)
                    # email_list=[]
                    for i in sekdept_filter:
                        notifikasi.objects.create(nip=i.nip,messages=f"Terdapat {cek_jumlah_sempro_sum} Mahasiswa belum di assign majelis seminar proposal diantaranya {nama_nim_sempro}  pada {tanggal} Jam {Jam}")

                    # send ke sekdept
                    email_list=[]
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
                    for i in range(len(temp_email)):
                        email_list.append(temp_email[i][0])
                    send_mail(
                        'Terdapat Mahasiswa Belum Assign Jadwal',
                        f"Terdapat {cek_jumlah_sempro_sum} Mahasiswa belum di assign majelis seminar proposal diantaranya {nama_nim_sempro}  pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                    )
                # hitung semhas
                list_jadwal_semhas=list(jadwal_seminar.objects.filter(tahap_seminar="Seminar Hasil").values_list("mahasiswa",flat=True))
                list_jadwal_semhas = list(filter(lambda x: x is not None and x != '', list_jadwal_semhas))
                cek_jumlah_semhas=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro)
                cek_jumlah_semhas_sum=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC").exclude(id_role_dosen__nim__in=list_jadwal_sempro).count()
                if cek_jumlah_semhas_sum>=3:
                    nama_nim_semhas=[]
                    for i in cek_jumlah_semhas:
                        nama_nim_semhas.append(i.id_role_dosen.nim)
                    # print(nama_nim_sempro)
                    user_sekdept=list(User.objects.values_list('id').filter(groups__name='Manajemen Departemen'))
                    # print(user_sekdept)
                    sekdept_filter=dosen.objects.filter(id_user__in=user_sekdept)
                    # email_list=[]
                    for i in sekdept_filter:
                        notifikasi.objects.create(nip=i.nip,messages=f"Terdapat {cek_jumlah_semhas_sum} Mahasiswa belum di assign majelis seminar hasil diantaranya {nama_nim_semhas}  pada {tanggal} Jam {Jam}")

                    # send ke sekdept
                    email_list=[]
                    # email_list=User.objects.filter(groups__name='Manajemen Departemen').values_list('email')
                    temp_email=list(User.objects.filter(groups__name='Manajemen Departemen').values_list('email'))
                    for i in range(len(temp_email)):
                        email_list.append(temp_email[i][0])
                    send_mail(
                        'Terdapat Mahasiswa Belum Assign Jadwal',
                        f"Terdapat {cek_jumlah_semhas_sum} Mahasiswa belum di assign majelis seminar hasil diantaranya {nama_nim_semhas}  pada {tanggal} Jam {Jam}",
                        settings.EMAIL_HOST_USER,
                        email_list,
                        fail_silently=False,
                    )


                # contoh : notif
                    # user_sekdept=list(User.objects.value_list('id_user').filter(groups__name='Manajemen Departemen'))
                    # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
                    # for i in sekdept_filter:
                    #     models.notifikasi.nip=i.nip
                    #     models.notifikasi.messages=f"Terdapat Input Usulan Topik Baru Oleh {create_usulantopik.nim} pada {tanggal} Jam {Jam}"
                    #     notifikasi.save()
                return redirect("../bimbinganget")
        else:
            form = BimbinganForm(instance=bimbingan_data)
    else:
        if request.method == "POST":
            form = BimbinganFormDosen(request.POST, instance=bimbingan_data)
            if form.is_valid():
                create_roledosen = form.save()
                instances = bimbingan.objects.filter(id_proposal=bimbingan_data.id_proposal).order_by('tanggal_buat')
                if instances.exists(): # Pastikan QuerySet tidak kosong
                    instances.update(status_bimbingan='Revisi') # Mengubah status untuk semua objek
                create_roledosen.save()
                messages.warning(request,"Data Bimbingan Telah Berhasil Dirubah! ")
                notifikasi.objects.create(nim=create_roledosen.id_proposal.nim,messages=f"Terdapat Update Revisi Bimbingan Baru Oleh {create_roledosen.id_role_dosen.nip.id_user.first_name} pada {tanggal} Jam {Jam}")
                # send ke mahasiswa
                email_list=[]
                temp_email=list(User.objects.filter(pk=create_roledosen.id_proposal.nim.id_user.id).values_list('email'))
                email_list.append(temp_email[0][0])
                send_mail(
                    'Terdapat Update Hasil Revisi Proposal Telah Di Buat ',
                    f"Terdapat Update Revisi Bimbingan Baru Oleh {create_roledosen.id_role_dosen.nip.id_user.first_name} pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                )


                # contoh : notif
                    # user_sekdept=list(User.objects.value_list('id_user').filter(groups__name='Manajemen Departemen'))
                    # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
                    # for i in sekdept_filter:
                    #     models.notifikasi.nip=i.nip
                    #     models.notifikasi.messages=f"Terdapat Input Usulan Topik Baru Oleh {create_usulantopik.nim} pada {tanggal} Jam {Jam}"
                    #     notifikasi.save()
                return redirect("../bimbinganget")
        else:
            form = BimbinganFormDosen(instance=bimbingan_data)
    return render(request, 'bimbingan/bimbingan_update.html', {"form": form,"data":bimbingan_data.id_proposal, "user_info": user_info})

# bimbingan:delete
# menghapus data bimbingan berdasarkan id bimbingan
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin', 'Manajemen Departemen','Kompartemen','Dosen','Properta'])
def bimbingan_delete(request, id):
    delete_data = bimbingan.objects.get(pk=id)
    messages.error(request,"Data Bimbingan Telah Berhasil Dihapus! ")
    delete_data.delete()
    return redirect('../bimbinganget')

# Detail Penilaian 
# detailpenilaian:create
# Untuk Membuat Komentar Skripsi(data detail penilaian ) saja > ga kepake sih 
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def detailpenilaian_create(request):
    user_info = user_information(request)
    if user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        if request.method == "POST":
            form = DetailPenilaianForm(request.POST)
            if form.is_valid():
                create_roledosen = form.save()
                create_roledosen.save()
                messages.success(request,"Data Detail Penilaian Telah Berhasil Dibuat! ")
                return redirect("../bimbinganget")
        else:
            form = DetailPenilaianForm()
    else:
        if request.method == "POST":
            form = DetailPenilaianForm(request.POST)
            if form.is_valid():
                create_roledosen = form.save(commit=False)
                create_roledosen.id_role_dosen = dosen.objects.get(
                    pk=user_info[0])
                create_roledosen.save()
                messages.success(request,"Data Detail Penilaian Telah Berhasil Dibuat! ")
                return redirect("../bimbinganget")
        else:
            form = DetailPenilaianForm()
    return render(request, 'dosen/detailpenilaian_create.html', {"form": form, "user_info": user_info})

# Detail Penilaian: Read

# Detail Penilaian:update


# @login_required(login_url="/login")
# def detailpenilaian_create(request, id):
#     user_info = user_information(request)
#     detailpenilaian_data = detailpenilaian.objects.get(pk=id)
#     if user_info[2].name == "Admin":
#         if request.method == "POST":
#             form = DetailPenilaianForm(
#                 request.POST, instance=detailpenilaian_data)
#             if form.is_valid():
#                 create_roledosen = form.save()
#                 create_roledosen.save()
#                 return redirect("../bimbinganget")
#         else:
#             form = DetailPenilaianForm(instance=detailpenilaian_data)
#     else:
#         if request.method == "POST":
#             form = DetailPenilaianForm(
#                 request.POST, instance=detailpenilaian_data)
#             if form.is_valid():
#                 create_roledosen = form.save(commit=False)
#                 create_roledosen.id_role_dosen = dosen.objects.get(
#                     pk=user_info[0])
#                 create_roledosen.save()
#                 return redirect("../bimbinganget")
#         else:
#             form = DetailPenilaianForm(instance=detailpenilaian_data)
#     return render(request, 'dosen/detailpenilaian_create.html', {"form": form, "user_info": user_info})


# Detail Penilaian:delete
# # Untuk Menghapus Komentar Skripsi(data detail penilaian) > ga kepake sih 
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def detailpenilaian_delete(request):
    delete_data = detailpenilaian.objects.get(pk=id)
    delete_data.delete()
    messages.error(request,"Data Detail Penilaian Telah Berhasil Dihapus! ")
    return redirect('../detailpenilaianget')

# Penilaian
# penilaian:create
# Untuk membuat penilaian > Tidak Terpakai karena nanti digabung detail penilaian
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def penilaian_create(request):
    user_info = user_information(request)
    cpmk_list=sub_cpmk.objects.all()
    # penilaian_data = penilaian.objects.get(pk=id)
    if user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        if request.method == "POST":
            form = PenilaianForm(
                request.POST)
            if form.is_valid():
                create_roledosen = form.save()
                create_roledosen.save()
                messages.success(request,"Data Penilaian Telah Berhasil Dibuat! ")
                
                return redirect("../bimbinganget")
        else:
            form = PenilaianForm()
    else:
        if request.method == "POST":
            form = PenilaianForm(
                request.POST)
            if form.is_valid():
                create_roledosen = form.save(commit=False)
                create_roledosen.id_role_dosen = dosen.objects.get(
                    pk=user_info[0])
                create_roledosen.save()
                messages.success(request,"Data Penilaian Telah Berhasil Dibuat! ")
                return redirect("../bimbinganget")
        else:
            form = PenilaianForm()
    return render(request, 'dosen/penilaian_update.html', {"form": form, "user_info": user_info,"cpmk":cpmk_list})
# penilaian:read
# Untuk list data penilaian > Tidak Terpakai karena nanti digabung detail penilaian
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def penilaian_get(request):
    user_info = user_information(request)

    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        try:
            penilaians = penilaian.objects.filter(
                pk=dosen.objects.filter(pk=user_info[0])[0])
        except:
            bimbingans = []
    elif user_info[2].name == "Mahasiswa":
        try:
            bimbingans = bimbingan.objects.filter(
                id_detail_penilaian=mahasiswa.objects.filter(pk=user_info[0])[0])
        except:
            bimbingans = []
    else:
        bimbingans = bimbingan.objects.all()
    return render(request, 'bimbingan/bimbingan_get.html', {"bimbingans": bimbingans, "user_info": user_info})


# penilaian:read
# Untuk menampilkan list penilaian sempro berdasarkan nim
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def nilai_sempro_get(request,nim):
    user_info = user_information(request)
    if user_info[2].name == "Mahasiswa" and nim !=user_info[0]:
        raise PermissionDenied()
    else : 
        pass
    data_penilaians=[]
    data_penilaian=None
    data_penilaians.append(detailpenilaian.objects.filter(status_kelulusan="Lulus").filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # data_penilaians.append(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # data_penilaians.append(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # data_penilaians.append(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # print(data_penilaians)
    data_penilaians.append(detailpenilaian.objects.filter(status_kelulusan="Lulus").filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 2').first())
    # print(data_penilaians)
    data_penilaians.append(detailpenilaian.objects.filter(status_kelulusan="Lulus").filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Penguji Seminar Proposal 1').first())
    # print(data_penilaians)
    data_penilaians.append(detailpenilaian.objects.filter(status_kelulusan="Lulus").filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Penguji Seminar Proposal 2').first())
    # print(data_penilaians)
    res = []
    for val in data_penilaians:
        if val != None :
            res.append(val)
   
    data_penilaian=res
    # print("last",data_penilaian)
    try:  
        roledosen_data=roledosen.objects.filter(nim=nim).filter(role='Pembimbing 1').first()                              
        # print(1,roledosen_data.id_role_dosen)
        nilai_data_pembimbing1=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__id_role_dosen__nim=nim).filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__status_kelulusan="Lulus")
        nilai_data_pembimbing1_checker=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__id_role_dosen__nim=nim).filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__status_kelulusan="Lulus").exists()
    except:
        nilai_data_pembimbing1=None
        nilai_data_pembimbing1_checker=False

    try:  
        roledosen_data=roledosen.objects.filter(nim=nim).filter(role='Pembimbing 2').first()                              
        # print(2,roledosen_data.id_role_dosen)
        nilai_data_pembimbing2=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__id_role_dosen__nim=nim).filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__status_kelulusan="Lulus")
        nilai_data_pembimbing2_checker=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__id_role_dosen__nim=nim).filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__status_kelulusan="Lulus").exists()
    except:
        nilai_data_pembimbing2=None
        nilai_data_pembimbing2_checker=False
    try:  
        roledosen_data=roledosen.objects.filter(nim=nim).filter(role='Penguji Seminar Proposal 1').first()                              
        # print(3,roledosen_data.id_role_dosen)
        nilai_data_penguji1=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__id_role_dosen__nim=nim).filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__status_kelulusan="Lulus")
        nilai_data_penguji1_checker=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__id_role_dosen__nim=nim).filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__status_kelulusan="Lulus").exists()
    except:
        nilai_data_penguji1=None
        nilai_data_penguji1_checker=False
    try:  
        roledosen_data=roledosen.objects.filter(nim=nim).filter(role='Penguji Seminar Proposal 2').first()                              
        # print(4,roledosen_data.id_role_dosen)
        nilai_data_penguji2=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__id_role_dosen__nim=nim).filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__status_kelulusan="Lulus")
        nilai_data_penguji2_checker=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__id_role_dosen__nim=nim).filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__status_kelulusan="Lulus").exists()
    except:
        nilai_data_penguji2=None
        nilai_data_penguji2_checker=False
    # print(nilai_data_pembimbing1_checker)
    # print(nilai_data_pembimbing2_checker)
    # print(nilai_data_pembimbing1)
    # print(nilai_data_pembimbing2)
    # print(nilai_data_penguji1_checker)
    # print(nilai_data_penguji2_checker)
    # print(nilai_data_penguji2)
    lst_isi=[]
    lst_nilai=[]
    if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
        lst_isi.append("Pembimbing 1")
        lst_nilai.append(nilai_data_pembimbing1)
    # if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
    #     lst_isi.append("Pembimbing 1")
    #     lst_nilai.append(nilai_data_pembimbing1)
    # if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
    #     lst_isi.append("Pembimbing 1")
    #     lst_nilai.append(nilai_data_pembimbing1)
    # if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
    #     lst_isi.append("Pembimbing 1")
        # lst_nilai.append(nilai_data_pembimbing1)
    if nilai_data_pembimbing2!=None and nilai_data_pembimbing2_checker==True:
        lst_isi.append("Pembimbing 2")
        lst_nilai.append(nilai_data_pembimbing2)
    if nilai_data_penguji1!=None and nilai_data_penguji1_checker==True:
        lst_isi.append("Penguji Sempro 1")
        lst_nilai.append(nilai_data_penguji1)
    if nilai_data_penguji2!=None and nilai_data_penguji2_checker==True:
        lst_isi.append("Penguji Sempro 2")
        lst_nilai.append(nilai_data_penguji2)

    # print(lst_nilai)
    # print(lst_isi)
    # abc=nilai_data_pembimbing1,nilai_data_pembimbing1
    # ziplist=zip(lst_nilai)
    # print(type(abc))
    # ziplist=zip(nilai_data_pembimbing1, nilai_data_pembimbing2,nilai_data_penguji1,nilai_data_penguji2)
    return render(request, 'penilaian/penilaian_sempro.html', {"nilai_list": lst_nilai,"isi_list":lst_isi
                                                               ,"data_penilaian":data_penilaian
                                                               , "user_info": user_info})
# penilaian:read
# Untuk menampilkan list penilaian semhas berdasarkan nim
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def nilai_semhas_get(request,nim):
    user_info = user_information(request)
    if user_info[2].name == "Mahasiswa" and nim !=user_info[0]:
        raise PermissionDenied()
    else : 
        pass
    data_penilaians=[]
    data_penilaian=None
    data_penilaians.append(detailpenilaian.objects.filter(status_kelulusan="Lulus").filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # data_penilaians.append(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # data_penilaians.append(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # data_penilaians.append(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # print(data_penilaians)
    data_penilaians.append(detailpenilaian.objects.filter(status_kelulusan="Lulus").filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 2').first())
    # print(data_penilaians)
    data_penilaians.append(detailpenilaian.objects.filter(status_kelulusan="Lulus").filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Penguji Seminar Hasil 1').first())
    # print(data_penilaians)
    data_penilaians.append(detailpenilaian.objects.filter(status_kelulusan="Lulus").filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Penguji Seminar Hasil 2').first())
    # print(data_penilaians)
    res = []
    for val in data_penilaians:
        if val != None :
            res.append(val)
   
    data_penilaian=res
    # print("last",data_penilaian)
    try:  
        roledosen_data=roledosen.objects.filter(nim=nim).filter(role='Pembimbing 1').first()                              
        # print(1,roledosen_data.id_role_dosen)
        nilai_data_pembimbing1=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__id_role_dosen__nim=nim).filter(id_detail_penilaian__nama_tahap="Seminar Hasil").filter(id_detail_penilaian__status_kelulusan="Lulus")
        nilai_data_pembimbing1_checker=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__id_role_dosen__nim=nim).filter(id_detail_penilaian__nama_tahap="Seminar Hasil").filter(id_detail_penilaian__status_kelulusan="Lulus").exists()
        # print(1,nilai_data_pembimbing1_checker)
    except:
        nilai_data_pembimbing1=None
        nilai_data_pembimbing1_checker=False

    try:  
        roledosen_data=roledosen.objects.filter(nim=nim).filter(role='Pembimbing 2').first()                              
        # print(2,roledosen_data.id_role_dosen)
        nilai_data_pembimbing2=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__id_role_dosen__nim=nim).filter(id_detail_penilaian__nama_tahap="Seminar Hasil").filter(id_detail_penilaian__status_kelulusan="Lulus")
        nilai_data_pembimbing2_checker=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__id_role_dosen__nim=nim).filter(id_detail_penilaian__nama_tahap="Seminar Hasil").filter(id_detail_penilaian__status_kelulusan="Lulus").exists()
        # print(2,nilai_data_pembimbing2_checker)
    except:
        nilai_data_pembimbing2=None
        nilai_data_pembimbing2_checker=False
    try:  
        roledosen_data=roledosen.objects.filter(nim=nim).filter(role='Penguji Seminar Hasil 1').first()                              
        # print(3,roledosen_data.id_role_dosen)
        nilai_data_penguji1=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__id_role_dosen__nim=nim).filter(id_detail_penilaian__nama_tahap="Seminar Hasil").filter(id_detail_penilaian__status_kelulusan="Lulus")
        nilai_data_penguji1_checker=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__id_role_dosen__nim=nim).filter(id_detail_penilaian__nama_tahap="Seminar Hasil").exists()
        # print(3,nilai_data_penguji1_checker)
    except:
        nilai_data_penguji1=None
        nilai_data_penguji1_checker=False
    try:  
        roledosen_data=roledosen.objects.filter(nim=nim).filter(role='Penguji Seminar Hasil 2').first()                              
        # print(4,roledosen_data.id_role_dosen)
        nilai_data_penguji2=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__id_role_dosen__nim=nim).filter(id_detail_penilaian__nama_tahap="Seminar Hasil").filter(id_detail_penilaian__status_kelulusan="Lulus")
        nilai_data_penguji2_checker=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__id_role_dosen__nim=nim).filter(id_detail_penilaian__nama_tahap="Seminar Hasil").filter(id_detail_penilaian__status_kelulusan="Lulus").exists()
    except:
        nilai_data_penguji2=None
        nilai_data_penguji2_checker=False
    # print(nilai_data_pembimbing1_checker)
    # print(nilai_data_pembimbing2_checker)
    # print(nilai_data_pembimbing1)
    # print(nilai_data_pembimbing2)
    # print(nilai_data_penguji1_checker)
    # print(nilai_data_penguji2_checker)
    # print(nilai_data_penguji2)
    lst_isi=[]
    lst_nilai=[]
    if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
        lst_isi.append("Pembimbing 1")
        lst_nilai.append(nilai_data_pembimbing1)
    # if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
    #     lst_isi.append("Pembimbing 1")
    #     lst_nilai.append(nilai_data_pembimbing1)
    # if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
    #     lst_isi.append("Pembimbing 1")
    #     lst_nilai.append(nilai_data_pembimbing1)
    # if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
    #     lst_isi.append("Pembimbing 1")
    #     lst_nilai.append(nilai_data_pembimbing1)
    if nilai_data_pembimbing2!=None and nilai_data_pembimbing2_checker==True:
        lst_isi.append("Pembimbing 2")
        lst_nilai.append(nilai_data_pembimbing2)
    if nilai_data_penguji1!=None and nilai_data_penguji1_checker==True:
        lst_isi.append("Penguji Semhas 1")
        lst_nilai.append(nilai_data_penguji1)
    if nilai_data_penguji2!=None and nilai_data_penguji2_checker==True:
        lst_isi.append("Penguji Semhas 2")
        lst_nilai.append(nilai_data_penguji2)

    # print(lst_nilai)
    # print(lst_isi)
    # abc=nilai_data_pembimbing1,nilai_data_pembimbing1
    # ziplist=zip(lst_nilai)
    # print(type(abc))
    # ziplist=zip(nilai_data_pembimbing1, nilai_data_pembimbing2,nilai_data_penguji1,nilai_data_penguji2)
    return render(request, 'penilaian/penilaian_semhas.html', {"nilai_list": lst_nilai,"isi_list":lst_isi, 
                                                               "data_penilaian":data_penilaian, 
                                                               "user_info": user_info})


# penilaian:read
# Untuk menampilkan list penilaian sempro berdasarkan nim
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def nilai_sempro_get_seminar(request,id_jadwal_seminar):
    jadwal_seminar_data=jadwal_seminar.objects.get(pk=id_jadwal_seminar)
    user_info = user_information(request)
    if user_info[2].name == "Mahasiswa" :
        raise PermissionDenied()
    else : 
        pass
    data_penilaians=[]
    
    data_penilaians.append(detailpenilaian.objects.filter(id_jadwal_seminar=jadwal_seminar_data.id_jadwal_seminar).filter(id_role_dosen__nim=jadwal_seminar_data.mahasiswa.nim).filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__role='Pembimbing 1').first())
    # data_penilaians.append(detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # data_penilaians.append(detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # data_penilaians.append(detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    print(data_penilaians)
    data_penilaians.append(detailpenilaian.objects.filter(id_jadwal_seminar=jadwal_seminar_data.id_jadwal_seminar).filter(id_role_dosen__nim=jadwal_seminar_data.mahasiswa.nim).filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__role='Pembimbing 2').first())
    print(data_penilaians)
    data_penilaians.append(detailpenilaian.objects.filter(id_jadwal_seminar=jadwal_seminar_data.id_jadwal_seminar).filter(id_role_dosen__nim=jadwal_seminar_data.mahasiswa.nim).filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__role='Penguji Seminar Proposal 1').first())
    print(data_penilaians)
    data_penilaians.append(detailpenilaian.objects.filter(id_jadwal_seminar=jadwal_seminar_data.id_jadwal_seminar).filter(id_role_dosen__nim=jadwal_seminar_data.mahasiswa.nim).filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__role='Penguji Seminar Proposal 2').first())
    print(data_penilaians)
   
    res = []
    for val in data_penilaians:
        if val != None :
            res.append(val)
   
    data_penilaian=res
    # print("last",data_penilaian)
    try:  
        roledosen_data=roledosen.objects.filter(pk=jadwal_seminar_data.dosen_pembimbing_1.id_role_dosen).filter(role='Pembimbing 1').first()                              
        # print(1,roledosen_data.id_role_dosen)
        nilai_data_pembimbing1=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__nama_tahap="Seminar Proposal")
        nilai_data_pembimbing1_checker=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__nama_tahap="Seminar Proposal").exists()
        # print(1,nilai_data_pembimbing1_checker)
    except:
        nilai_data_pembimbing1=None
        nilai_data_pembimbing1_checker=False

    try:  
        roledosen_data=roledosen.objects.filter(pk=jadwal_seminar_data.dosen_pembimbing_2.id_role_dosen).filter(role='Pembimbing 2').first()                              
        # print(2,roledosen_data.id_role_dosen)
        nilai_data_pembimbing2=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__nama_tahap="Seminar Proposal")
        nilai_data_pembimbing2_checker=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__nama_tahap="Seminar Proposal").exists()
        # print(2,nilai_data_pembimbing2_checker)
    except:
        nilai_data_pembimbing2=None
        nilai_data_pembimbing2_checker=False
    try:  
        roledosen_data=roledosen.objects.filter(pk=jadwal_seminar_data.dosen_penguji_1.id_role_dosen).filter(role='Penguji Seminar Proposal 1').first()                              
        # print(3,roledosen_data.id_role_dosen)
        nilai_data_penguji1=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__nama_tahap="Seminar Proposal")
        nilai_data_penguji1_checker=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__nama_tahap="Seminar Proposal").exists()
    except:
        nilai_data_penguji1=None
        nilai_data_penguji1_checker=False
    try:  
        roledosen_data=roledosen.objects.filter(pk=jadwal_seminar_data.dosen_penguji_2.id_role_dosen).filter(role='Penguji Seminar Proposal 2').first()                              
        # print(4,roledosen_data.id_role_dosen)
        nilai_data_penguji2=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__nama_tahap="Seminar Proposal")
        nilai_data_penguji2_checker=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__nama_tahap="Seminar Proposal").exists()
    except:
        nilai_data_penguji2=None
        nilai_data_penguji2_checker=False
    # print(nilai_data_pembimbing1_checker)
    # print(nilai_data_pembimbing2_checker)
    # print(nilai_data_pembimbing1)
    # print(nilai_data_pembimbing2)
    # print(nilai_data_penguji1_checker)
    # print(nilai_data_penguji2_checker)
    # print(nilai_data_penguji2)
    lst_isi=[]
    lst_nilai=[]
    if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
        lst_isi.append("Pembimbing 1")
        lst_nilai.append(nilai_data_pembimbing1)
    # if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
    #     lst_isi.append("Pembimbing 1")
    #     lst_nilai.append(nilai_data_pembimbing1)
    # if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
    #     lst_isi.append("Pembimbing 1")
    #     lst_nilai.append(nilai_data_pembimbing1)
    # if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
    #     lst_isi.append("Pembimbing 1")
        # lst_nilai.append(nilai_data_pembimbing1)
    if nilai_data_pembimbing2!=None and nilai_data_pembimbing2_checker==True:
        lst_isi.append("Pembimbing 2")
        lst_nilai.append(nilai_data_pembimbing2)
    if nilai_data_penguji1!=None and nilai_data_penguji1_checker==True:
        lst_isi.append("Penguji Sempro 1")
        lst_nilai.append(nilai_data_penguji1)
    if nilai_data_penguji2!=None and nilai_data_penguji2_checker==True:
        lst_isi.append("Penguji Sempro 2")
        lst_nilai.append(nilai_data_penguji2)

    # print(lst_nilai)
    # print(lst_isi)
    # abc=nilai_data_pembimbing1,nilai_data_pembimbing1
    # ziplist=zip(lst_nilai)
    # print(type(abc))
    # ziplist=zip(nilai_data_pembimbing1, nilai_data_pembimbing2,nilai_data_penguji1,nilai_data_penguji2)
    return render(request, 'penilaian/penilaian_sempro.html', {"nilai_list": lst_nilai,"isi_list":lst_isi
                                                               ,"data_penilaian":data_penilaian
                                                               , "user_info": user_info})
    
# penilaian:read
# Untuk menampilkan list penilaian semhas berdasarkan nim
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def nilai_semhas_get_seminar(request,id_jadwal_seminar):
    user_info = user_information(request)
    jadwal_seminar_data=jadwal_seminar.objects.get(pk=id_jadwal_seminar)
    if user_info[2].name == "Mahasiswa" :
        raise PermissionDenied()
    else : 
        pass
    data_penilaians=[]
    data_penilaian=None
    data_penilaians.append(detailpenilaian.objects.filter(id_jadwal_seminar=jadwal_seminar_data.id_jadwal_seminar).filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__role='Pembimbing 1').first())
    # data_penilaians.append(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # data_penilaians.append(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # data_penilaians.append(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # print(data_penilaians)
    data_penilaians.append(detailpenilaian.objects.filter(id_jadwal_seminar=jadwal_seminar_data.id_jadwal_seminar).filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__role='Pembimbing 2').first())
    # print(data_penilaians)
    data_penilaians.append(detailpenilaian.objects.filter(id_jadwal_seminar=jadwal_seminar_data.id_jadwal_seminar).filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__role='Penguji Seminar Hasil 1').first())
    # print(data_penilaians)
    data_penilaians.append(detailpenilaian.objects.filter(id_jadwal_seminar=jadwal_seminar_data.id_jadwal_seminar).filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__role='Penguji Seminar Hasil 2').first())
    # print(data_penilaians)
    res = []
    for val in data_penilaians:
        if val != None :
            res.append(val)
   
    data_penilaian=res
    # print("last",data_penilaian)
    try:  
        roledosen_data=roledosen.objects.filter(pk=jadwal_seminar_data.dosen_pembimbing_1.id_role_dosen).filter(role='Pembimbing 1').first()                              
        # print(1,roledosen_data.id_role_dosen)
        nilai_data_pembimbing1=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__nama_tahap="Seminar Hasil")
        nilai_data_pembimbing1_checker=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__nama_tahap="Seminar Hasil").exists()
        # print(1,nilai_data_pembimbing1_checker)
    except:
        nilai_data_pembimbing1=None
        nilai_data_pembimbing1_checker=False

    try:  
        roledosen_data=roledosen.objects.filter(pk=jadwal_seminar_data.dosen_pembimbing_2.id_role_dosen).filter(role='Pembimbing 2').first()                              
        # print(2,roledosen_data.id_role_dosen)
        nilai_data_pembimbing2=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__nama_tahap="Seminar Hasil")
        nilai_data_pembimbing2_checker=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__nama_tahap="Seminar Hasil").exists()
        # print(2,nilai_data_pembimbing2_checker)
    except:
        nilai_data_pembimbing2=None
        nilai_data_pembimbing2_checker=False
    try:  
        roledosen_data=roledosen.objects.filter(pk=jadwal_seminar_data.dosen_penguji_1.id_role_dosen).filter(role='Penguji Seminar Hasil 1').first()                              
        # print(3,roledosen_data.id_role_dosen)
        nilai_data_penguji1=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__nama_tahap="Seminar Hasil")
        nilai_data_penguji1_checker=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__nama_tahap="Seminar Hasil").exists()
        # print(3,nilai_data_penguji1_checker)
    except:
        nilai_data_penguji1=None
        nilai_data_penguji1_checker=False
    try:  
        roledosen_data=roledosen.objects.filter(pk=jadwal_seminar_data.dosen_penguji_2.id_role_dosen).filter(role='Penguji Seminar Hasil 2').first()                              
        # print(4,roledosen_data.id_role_dosen)
        nilai_data_penguji2=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__nama_tahap="Seminar Hasil")
        nilai_data_penguji2_checker=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__nama_tahap="Seminar Hasil").exists()
    except:
        nilai_data_penguji2=None
        nilai_data_penguji2_checker=False
    # print(nilai_data_pembimbing1_checker)
    # print(nilai_data_pembimbing2_checker)
    # print(nilai_data_pembimbing1)
    # print(nilai_data_pembimbing2)
    # print(nilai_data_penguji1_checker)
    # print(nilai_data_penguji2_checker)
    # print(nilai_data_penguji2)
    lst_isi=[]
    lst_nilai=[]
    if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
        lst_isi.append("Pembimbing 1")
        lst_nilai.append(nilai_data_pembimbing1)
    # if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
    #     lst_isi.append("Pembimbing 1")
    #     lst_nilai.append(nilai_data_pembimbing1)
    # if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
    #     lst_isi.append("Pembimbing 1")
    #     lst_nilai.append(nilai_data_pembimbing1)
    # if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
    #     lst_isi.append("Pembimbing 1")
    #     lst_nilai.append(nilai_data_pembimbing1)
    if nilai_data_pembimbing2!=None and nilai_data_pembimbing2_checker==True:
        lst_isi.append("Pembimbing 2")
        lst_nilai.append(nilai_data_pembimbing2)
    if nilai_data_penguji1!=None and nilai_data_penguji1_checker==True:
        lst_isi.append("Penguji Semhas 1")
        lst_nilai.append(nilai_data_penguji1)
    if nilai_data_penguji2!=None and nilai_data_penguji2_checker==True:
        lst_isi.append("Penguji Semhas 2")
        lst_nilai.append(nilai_data_penguji2)

    # print(lst_nilai)
    # print(lst_isi)
    # abc=nilai_data_pembimbing1,nilai_data_pembimbing1
    # ziplist=zip(lst_nilai)
    # print(type(abc))
    # ziplist=zip(nilai_data_pembimbing1, nilai_data_pembimbing2,nilai_data_penguji1,nilai_data_penguji2)
    return render(request, 'penilaian/penilaian_semhas.html', {"nilai_list": lst_nilai,"isi_list":lst_isi, 
                                                               "data_penilaian":data_penilaian, 
                                                               "user_info": user_info})   

# penilaian:read
# Untuk menampilkan list penilaian bimbingan berdasarkan nim
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def nilai_bimbingan_get_seminar(request,id_jadwal_seminar):
    user_info = user_information(request)
    jadwal_seminar_data=jadwal_seminar.objects.get(pk=id_jadwal_seminar)
    if user_info[2].name == "Mahasiswa":
        raise PermissionDenied()
    else : 
        pass
    # data_penilaian=penilaian.objects.filter(id_detail_penilaian__id_role_dosen__nim=nim)
    data_penilaians=[]
    data_penilaian=None
    data_penilaians.append(detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=jadwal_seminar_data.mahasiswa.nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # data_penilaians.append(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # data_penilaians.append(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # data_penilaians.append(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # print(data_penilaians)
    data_penilaians.append(detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=jadwal_seminar_data.mahasiswa.nim).filter(id_role_dosen__role='Pembimbing 2').first())
    # print(data_penilaians)
   
    res = []
    for val in data_penilaians:
        if val != None :
            res.append(val)
   
    data_penilaian=res
    # print("last",data_penilaian)
    
    try:  
        roledosen_data=roledosen.objects.filter(pk=jadwal_seminar_data.dosen_pembimbing_1.id_role_dosen).filter(role='Pembimbing 1').first()  
                                    
        # print(1,roledosen_data.id_role_dosen)
        nilai_data_pembimbing1=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__nama_tahap="Bimbingan")
        nilai_data_pembimbing1_checker=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__nama_tahap="Bimbingan").exists()
    except:
        nilai_data_pembimbing1=None
        nilai_data_pembimbing1_checker=False

    try:  
        roledosen_data=roledosen.objects.filter(pk=jadwal_seminar_data.dosen_pembimbing_2.id_role_dosen).filter(role='Pembimbing 2').first()     
        # print(roledosen_data)                         
        # print(2,roledosen_data.id_role_dosen)
        nilai_data_pembimbing2=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__nama_tahap="Bimbingan")
        # print(nilai_data_pembimbing2)                         
        nilai_data_pembimbing2_checker=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__nama_tahap="Bimbingan").exists()
        # print(nilai_data_pembimbing2_checker)                         
    except:
        nilai_data_pembimbing2=None
        nilai_data_pembimbing2_checker=False
    
    
    lst_isi=[]
    lst_nilai=[]
    if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
        lst_isi.append("Pembimbing 1")
        lst_nilai.append(nilai_data_pembimbing1)
    # if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
    #     lst_isi.append("Pembimbing 1")
    #     lst_nilai.append(nilai_data_pembimbing1)
    # if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
    #     lst_isi.append("Pembimbing 1")
    #     lst_nilai.append(nilai_data_pembimbing1)
    # if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
    #     lst_isi.append("Pembimbing 1")
    #     lst_nilai.append(nilai_data_pembimbing1)
    if nilai_data_pembimbing2!=None and nilai_data_pembimbing2_checker==True:
        lst_isi.append("Pembimbing 2")
        lst_nilai.append(nilai_data_pembimbing2)
    

    # print(lst_nilai)
    # abc=nilai_data_pembimbing1,nilai_data_pembimbing1
    # ziplist=zip(lst_nilai)
    # print(type(abc))
    # ziplist=zip(nilai_data_pembimbing1, nilai_data_pembimbing2,nilai_data_penguji1,nilai_data_penguji2)
    return render(request, 'penilaian/penilaian_dosen.html', {"nilai_list": lst_nilai,"isi_list":lst_isi, 
                                                              "data_penilaian":data_penilaian,
                                                               "user_info": user_info})





# penilaian:read
# Untuk menampilkan list penilaian bimbingan berdasarkan nim
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def nilai_bimbingan_get(request,nim):
    user_info = user_information(request)
    if user_info[2].name == "Mahasiswa" and nim !=user_info[0]:
        raise PermissionDenied()
    else : 
        pass
    # data_penilaian=penilaian.objects.filter(id_detail_penilaian__id_role_dosen__nim=nim)
    data_penilaians=[]
    data_penilaian=None
    data_penilaians.append(detailpenilaian.objects.filter(status_kelulusan="Lulus").filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # data_penilaians.append(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # data_penilaians.append(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # data_penilaians.append(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 1').first())
    # print(data_penilaians)
    data_penilaians.append(detailpenilaian.objects.filter(status_kelulusan="Lulus").filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=nim).filter(id_role_dosen__role='Pembimbing 2').first())
    # print(data_penilaians)
   
    res = []
    for val in data_penilaians:
        if val != None :
            res.append(val)
   
    data_penilaian=res
    # print("last",data_penilaian)
    
    try:  
        roledosen_data=roledosen.objects.filter(nim=nim).filter(role='Pembimbing 1').first()  
                                    
        # print(1,roledosen_data.id_role_dosen)
        nilai_data_pembimbing1=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__id_role_dosen__nim=nim).filter(id_detail_penilaian__nama_tahap="Bimbingan").filter(id_detail_penilaian__status_kelulusan="Lulus")
        nilai_data_pembimbing1_checker=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__id_role_dosen__nim=nim).filter(id_detail_penilaian__nama_tahap="Bimbingan").filter(id_detail_penilaian__status_kelulusan="Lulus").exists()
    except:
        nilai_data_pembimbing1=None
        nilai_data_pembimbing1_checker=False

    try:  
        roledosen_data=roledosen.objects.filter(nim=nim).filter(role='Pembimbing 2').first()     
        # print(roledosen_data)                         
        # print(2,roledosen_data.id_role_dosen)
        nilai_data_pembimbing2=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__id_role_dosen__nim=nim).filter(id_detail_penilaian__nama_tahap="Bimbingan").filter(id_detail_penilaian__status_kelulusan="Lulus")
        # print(nilai_data_pembimbing2)                         
        nilai_data_pembimbing2_checker=penilaian.objects.filter(id_detail_penilaian__id_role_dosen=roledosen_data).filter(id_detail_penilaian__id_role_dosen__nim=nim).filter(id_detail_penilaian__nama_tahap="Bimbingan").filter(id_detail_penilaian__status_kelulusan="Lulus").exists()
        # print(nilai_data_pembimbing2_checker)                         
    except:
        nilai_data_pembimbing2=None
        nilai_data_pembimbing2_checker=False
    
    
    lst_isi=[]
    lst_nilai=[]
    if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
        lst_isi.append("Pembimbing 1")
        lst_nilai.append(nilai_data_pembimbing1)
    # if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
    #     lst_isi.append("Pembimbing 1")
    #     lst_nilai.append(nilai_data_pembimbing1)
    # if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
    #     lst_isi.append("Pembimbing 1")
    #     lst_nilai.append(nilai_data_pembimbing1)
    # if nilai_data_pembimbing1!=None and nilai_data_pembimbing1_checker==True :
    #     lst_isi.append("Pembimbing 1")
    #     lst_nilai.append(nilai_data_pembimbing1)
    if nilai_data_pembimbing2!=None and nilai_data_pembimbing2_checker==True:
        lst_isi.append("Pembimbing 2")
        lst_nilai.append(nilai_data_pembimbing2)
    

    # print(lst_nilai)
    # abc=nilai_data_pembimbing1,nilai_data_pembimbing1
    # ziplist=zip(lst_nilai)
    # print(type(abc))
    # ziplist=zip(nilai_data_pembimbing1, nilai_data_pembimbing2,nilai_data_penguji1,nilai_data_penguji2)
    return render(request, 'penilaian/penilaian_dosen.html', {"nilai_list": lst_nilai,"isi_list":lst_isi, 
                                                              "data_penilaian":data_penilaian,
                                                               "user_info": user_info})

# penilaian dan detail penilaian:create & update
# Untuk pembuatan dan update data penilaian dan detail penilaian seminar proposal berdasarkan id proposal
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def penilaian_sempro_dosen_1(request, id_jadwal_seminar):
    user_info = user_information(request)
    jadwal_seminar_data=jadwal_seminar.objects.get(pk=id_jadwal_seminar)
    # print(jadwal_seminar_data)
    mahasiswa_data=mahasiswa.objects.get(nim=jadwal_seminar_data.mahasiswa.nim)

    # list_cpmk_sempro=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    list_cpmk_sempro=list(sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_sempro=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    # print(list_cpmk_sempro)
    bimbingan_filter=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(id_proposal__nim=mahasiswa_data.nim).filter(status_bimbingan="ACC").order_by("-tanggal_update").first()
    # .filter(status_bimbingan="ACC")
    try : 
        proposal_data=proposal.objects.get(pk=bimbingan_filter.id_proposal.id_proposal)
    except:
        proposal_data=None
    # print(proposal_data)
    # list1=list_cpmk_sempro
    # list(list_cpmk_sempro.values_list("id_sub_cpmk",flat=True))
    # list2=["1A","1B","1C", "2A","3A","3B","3C","5A","5B","6A","7A"]
    # for elemen in list1:
    #     if elemen in list2:
    #         print(elemen, "ditemukan dalam kedua list")
    #     else:
    #         print(elemen, "tidak ditemukan dalam kedua list")
    
    
    # list_cpmk_semhas=["1A","1C", "2A","2B","2C","2D","3D","4A","5A","5B","7A","8A"]
    # list_cpmk_pembimbing=["1A","2A","2B", "2C","3A","3D","4A","5A","5B","6B","8B"]
    
    # cpmk_data=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0)
    cpmk_data=sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_sempro=0)
    roledosen_get=roledosen.objects.get(pk=jadwal_seminar_data.dosen_penguji_1.id_role_dosen)

    # print(roledosen_get)
    # # roledosen_checker=roledosen.objects.filter(pk=roledosen_data.id_role_dosen).exists()
    
    # print(roledosen_data.id_role_dosen)
    detailpenilaian_data=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Seminar Proposal").filter(id_jadwal_seminar=jadwal_seminar_data).first()
    detailpenilaian_checker=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Seminar Proposal").filter(id_jadwal_seminar=jadwal_seminar_data).exists()
    penilaian_first=penilaian.objects.filter(id_detail_penilaian=detailpenilaian_data).first()

    PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=0,can_delete=False)

    if request.method == 'POST':
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None

        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        else :
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST)
        
            # form.initial[]
        # print(penilaianset_form.is_valid())
        if all((detailpenilaian_form.is_valid(), penilaianset_form.is_valid())):
                # print(2,penilaianset_form)
                if detailpenilaian_checker==False:
                    detailpenilaian_form=detailpenilaian(
                        id_role_dosen = roledosen_get,
                        hasil_review = request.POST["hasil_review"],
                        id_jadwal_seminar=jadwal_seminar_data,
                        status_kelulusan = request.POST["status_kelulusan"],
                        nama_tahap= "Seminar Proposal",
                    )

                else :
                    detailpenilaian_form=detailpenilaian.objects.get(pk=detailpenilaian_data.id_detail_penilaian)
                    detailpenilaian_form.hasil_review=request.POST["hasil_review"]
                    detailpenilaian_form.status_kelulusan=request.POST["status_kelulusan"]

                detailpenilaian_form.save()
                # print(detailpenilaian_form)
                detailpenilaianfilter=detailpenilaian.objects.filter(id_role_dosen = roledosen_get).filter(hasil_review = request.POST["hasil_review"]).first()
                detailpenilaiandata=detailpenilaian.objects.get(pk=detailpenilaianfilter.id_detail_penilaian)
                penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaiandata)

                if penilaianset_form.is_valid():
                
                   penilaianset_form.save()
                messages.success(request,"Data Penilaian Telah Berhasil Dibuat! ")
                return redirect('/jadwal_sempro/belum')
        else :
            counter_cpmk=0
            for form in penilaianset_form:
            
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_sempro[counter_cpmk])
                    counter_cpmk+=1
            

    else :
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None
        
        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormDosen()
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_sempro),can_delete=False)  
            penilaianset_form=PenilaianFormSet()

            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_sempro[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_sempro[counter_cpmk])
                    counter_cpmk+=1
            # print(1)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_sempro),can_delete=False)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            # print(detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_sempro[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_sempro[counter_cpmk])
                    counter_cpmk+=1
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
               
                    form.initial["id_sub_cpmk"]=list_cpmk_sempro[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_sempro[counter_cpmk])
                    counter_cpmk+=1
            # print(3)
        else :
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet()
            # print(4)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_sempro[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_sempro[counter_cpmk])
                    counter_cpmk+=1
    # detailpenilaian_form=None 
    # penilaianset_form=None
    # cpmk_data=None
    # proposal_data=None
    return render(request, 'dosen/penilaian_update.html', {"detailpenilaianform":detailpenilaian_form,"form_nilai":penilaianset_form,"proposal_data":proposal_data,"cpmk_data":cpmk_data, "user_info": user_info})


# penilaian dan detail penilaian:create & update
# Untuk pembuatan dan update data penilaian dan detail penilaian seminar proposal berdasarkan id proposal
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def penilaian_sempro_dosen_2(request, id_jadwal_seminar):
    user_info = user_information(request)
    jadwal_seminar_data=jadwal_seminar.objects.get(pk=id_jadwal_seminar)
    # print(jadwal_seminar_data)
    mahasiswa_data=mahasiswa.objects.get(nim=jadwal_seminar_data.mahasiswa.nim)

    # list_cpmk_sempro=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    list_cpmk_sempro=list(sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_sempro=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    # print(list_cpmk_sempro)
    bimbingan_filter=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(id_proposal__nim=mahasiswa_data.nim).filter(status_bimbingan="ACC").order_by("-tanggal_update").first()
    # .filter(status_bimbingan="ACC")
    try : 
        proposal_data=proposal.objects.get(pk=bimbingan_filter.id_proposal.id_proposal)
    except:
        proposal_data=None
    # print(proposal_data)
    # list1=list_cpmk_sempro
    # list(list_cpmk_sempro.values_list("id_sub_cpmk",flat=True))
    # list2=["1A","1B","1C", "2A","3A","3B","3C","5A","5B","6A","7A"]
    # for elemen in list1:
    #     if elemen in list2:
    #         print(elemen, "ditemukan dalam kedua list")
    #     else:
    #         print(elemen, "tidak ditemukan dalam kedua list")
    
    
    # list_cpmk_semhas=["1A","1C", "2A","2B","2C","2D","3D","4A","5A","5B","7A","8A"]
    # list_cpmk_pembimbing=["1A","2A","2B", "2C","3A","3D","4A","5A","5B","6B","8B"]
    
    # cpmk_data=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0)
    cpmk_data=sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_sempro=0)
    roledosen_get=roledosen.objects.get(pk=jadwal_seminar_data.dosen_penguji_2.id_role_dosen)

    # print(roledosen_get)
    # # roledosen_checker=roledosen.objects.filter(pk=roledosen_data.id_role_dosen).exists()
    
    # print(roledosen_data.id_role_dosen)
    detailpenilaian_data=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Seminar Proposal").filter(id_jadwal_seminar=jadwal_seminar_data).first()
    detailpenilaian_checker=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Seminar Proposal").filter(id_jadwal_seminar=jadwal_seminar_data).exists()
    penilaian_first=penilaian.objects.filter(id_detail_penilaian=detailpenilaian_data).first()

    PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=0,can_delete=False)

    if request.method == 'POST':
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None

        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        else :
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST)
        
            # form.initial[]
        # print(penilaianset_form.is_valid())
        if all((detailpenilaian_form.is_valid(), penilaianset_form.is_valid())):
                # print(2,penilaianset_form)
                if detailpenilaian_checker==False:
                    detailpenilaian_form=detailpenilaian(
                        id_role_dosen = roledosen_get,
                        hasil_review = request.POST["hasil_review"],
                        id_jadwal_seminar=jadwal_seminar_data,
                        status_kelulusan = request.POST["status_kelulusan"],
                        nama_tahap= "Seminar Proposal",
                    )

                else :
                    detailpenilaian_form=detailpenilaian.objects.get(pk=detailpenilaian_data.id_detail_penilaian)
                    detailpenilaian_form.hasil_review=request.POST["hasil_review"]
                    detailpenilaian_form.status_kelulusan=request.POST["status_kelulusan"]

                detailpenilaian_form.save()
                # print(detailpenilaian_form)
                detailpenilaianfilter=detailpenilaian.objects.filter(id_role_dosen = roledosen_get).filter(hasil_review = request.POST["hasil_review"]).first()
                detailpenilaiandata=detailpenilaian.objects.get(pk=detailpenilaianfilter.id_detail_penilaian)
                penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaiandata)

                if penilaianset_form.is_valid():
                
                   penilaianset_form.save()
                messages.success(request,"Data Penilaian Telah Berhasil Dibuat! ")
                return redirect('/jadwal_sempro/belum')
        else :
            counter_cpmk=0
            for form in penilaianset_form:
            
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_sempro[counter_cpmk])
                    counter_cpmk+=1
            

    else :
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None
        
        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormDosen()
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_sempro),can_delete=False)  
            penilaianset_form=PenilaianFormSet()

            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_sempro[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_sempro[counter_cpmk])
                    counter_cpmk+=1
            # print(1)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_sempro),can_delete=False)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            # print(detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_sempro[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_sempro[counter_cpmk])
                    counter_cpmk+=1
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
               
                    form.initial["id_sub_cpmk"]=list_cpmk_sempro[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_sempro[counter_cpmk])
                    counter_cpmk+=1
            # print(3)
        else :
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet()
            # print(4)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_sempro[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_sempro[counter_cpmk])
                    counter_cpmk+=1
    # detailpenilaian_form=None 
    # penilaianset_form=None
    # cpmk_data=None
    # proposal_data=None
    return render(request, 'dosen/penilaian_update.html', {"detailpenilaianform":detailpenilaian_form,"form_nilai":penilaianset_form,"proposal_data":proposal_data,"cpmk_data":cpmk_data, "user_info": user_info})

# penilaian dan detail penilaian:create & update
# Untuk pembuatan dan update data penilaian dan detail penilaian seminar proposal berdasarkan id proposal
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def penilaian_sempro_dosen_pembimbing_1(request, id_jadwal_seminar):
    user_info = user_information(request)
    jadwal_seminar_data=jadwal_seminar.objects.get(pk=id_jadwal_seminar)
    # print(jadwal_seminar_data)
    mahasiswa_data=mahasiswa.objects.get(nim=jadwal_seminar_data.mahasiswa.nim)

    # list_cpmk_sempro=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    list_cpmk_sempro=list(sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_sempro=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    # print(list_cpmk_sempro)
    bimbingan_filter=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(id_proposal__nim=mahasiswa_data.nim).filter(status_bimbingan="ACC").order_by("-tanggal_update").first()
    # .filter(status_bimbingan="ACC")
    try : 
        proposal_data=proposal.objects.get(pk=bimbingan_filter.id_proposal.id_proposal)
    except:
        proposal_data=None
    # print(proposal_data)
    # list1=list_cpmk_sempro
    # list(list_cpmk_sempro.values_list("id_sub_cpmk",flat=True))
    # list2=["1A","1B","1C", "2A","3A","3B","3C","5A","5B","6A","7A"]
    # for elemen in list1:
    #     if elemen in list2:
    #         print(elemen, "ditemukan dalam kedua list")
    #     else:
    #         print(elemen, "tidak ditemukan dalam kedua list")
    
    
    # list_cpmk_semhas=["1A","1C", "2A","2B","2C","2D","3D","4A","5A","5B","7A","8A"]
    # list_cpmk_pembimbing=["1A","2A","2B", "2C","3A","3D","4A","5A","5B","6B","8B"]
    
    # cpmk_data=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0)
    cpmk_data=sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_sempro=0)
    roledosen_get=roledosen.objects.get(pk=jadwal_seminar_data.dosen_pembimbing_1.id_role_dosen)

    # print(roledosen_get)
    # # roledosen_checker=roledosen.objects.filter(pk=roledosen_data.id_role_dosen).exists()
    
    # print(roledosen_data.id_role_dosen)
    detailpenilaian_data=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Seminar Proposal").filter(id_jadwal_seminar=jadwal_seminar_data).first()
    detailpenilaian_checker=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Seminar Proposal").filter(id_jadwal_seminar=jadwal_seminar_data).exists()
    penilaian_first=penilaian.objects.filter(id_detail_penilaian=detailpenilaian_data).first()

    PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=0,can_delete=False)

    if request.method == 'POST':
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None

        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        else :
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST)
        
            # form.initial[]
        # print(penilaianset_form.is_valid())
        if all((detailpenilaian_form.is_valid(), penilaianset_form.is_valid())):
                # print(2,penilaianset_form)
                if detailpenilaian_checker==False:
                    detailpenilaian_form=detailpenilaian(
                        id_role_dosen = roledosen_get,
                        hasil_review = request.POST["hasil_review"],
                        id_jadwal_seminar=jadwal_seminar_data,
                        status_kelulusan = request.POST["status_kelulusan"],
                        nama_tahap= "Seminar Proposal",
                    )

                else :
                    detailpenilaian_form=detailpenilaian.objects.get(pk=detailpenilaian_data.id_detail_penilaian)
                    detailpenilaian_form.hasil_review=request.POST["hasil_review"]
                    detailpenilaian_form.status_kelulusan=request.POST["status_kelulusan"]

                detailpenilaian_form.save()
                # print(detailpenilaian_form)
                detailpenilaianfilter=detailpenilaian.objects.filter(id_role_dosen = roledosen_get).filter(hasil_review = request.POST["hasil_review"]).first()
                detailpenilaiandata=detailpenilaian.objects.get(pk=detailpenilaianfilter.id_detail_penilaian)
                penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaiandata)

                if penilaianset_form.is_valid():
                
                   penilaianset_form.save()
                messages.success(request,"Data Penilaian Telah Berhasil Dibuat! ")
                return redirect('/jadwal_bimbingan/belum')
        else :
            counter_cpmk=0
            for form in penilaianset_form:
            
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_sempro[counter_cpmk])
                    counter_cpmk+=1
            

    else :
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None
        
        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormDosen()
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_sempro),can_delete=False)  
            penilaianset_form=PenilaianFormSet()

            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_sempro[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_sempro[counter_cpmk])
                    counter_cpmk+=1
            # print(1)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_sempro),can_delete=False)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            # print(detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_sempro[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_sempro[counter_cpmk])
                    counter_cpmk+=1
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
               
                    form.initial["id_sub_cpmk"]=list_cpmk_sempro[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_sempro[counter_cpmk])
                    counter_cpmk+=1
            # print(3)
        else :
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet()
            # print(4)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_sempro[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_sempro[counter_cpmk])
                    counter_cpmk+=1
    # detailpenilaian_form=None 
    # penilaianset_form=None
    # cpmk_data=None
    # proposal_data=None
    return render(request, 'dosen/penilaian_update.html', {"detailpenilaianform":detailpenilaian_form,"form_nilai":penilaianset_form,"proposal_data":proposal_data,"cpmk_data":cpmk_data, "user_info": user_info})

# penilaian dan detail penilaian:create & update
# Untuk pembuatan dan update data penilaian dan detail penilaian seminar proposal berdasarkan id proposal
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def penilaian_sempro_dosen_pembimbing_2(request, id_jadwal_seminar):
    user_info = user_information(request)
    jadwal_seminar_data=jadwal_seminar.objects.get(pk=id_jadwal_seminar)
    # print(jadwal_seminar_data)
    mahasiswa_data=mahasiswa.objects.get(nim=jadwal_seminar_data.mahasiswa.nim)

    # list_cpmk_sempro=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    list_cpmk_sempro=list(sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_sempro=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    # print(list_cpmk_sempro)
    bimbingan_filter=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(id_proposal__nim=mahasiswa_data.nim).filter(status_bimbingan="ACC").order_by("-tanggal_update").first()
    # .filter(status_bimbingan="ACC")
    try : 
        proposal_data=proposal.objects.get(pk=bimbingan_filter.id_proposal.id_proposal)
    except:
        proposal_data=None
    # print(proposal_data)
    # list1=list_cpmk_sempro
    # list(list_cpmk_sempro.values_list("id_sub_cpmk",flat=True))
    # list2=["1A","1B","1C", "2A","3A","3B","3C","5A","5B","6A","7A"]
    # for elemen in list1:
    #     if elemen in list2:
    #         print(elemen, "ditemukan dalam kedua list")
    #     else:
    #         print(elemen, "tidak ditemukan dalam kedua list")
    
    
    # list_cpmk_semhas=["1A","1C", "2A","2B","2C","2D","3D","4A","5A","5B","7A","8A"]
    # list_cpmk_pembimbing=["1A","2A","2B", "2C","3A","3D","4A","5A","5B","6B","8B"]
    
    # cpmk_data=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0)
    cpmk_data=sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_sempro=0)
    roledosen_get=roledosen.objects.get(pk=jadwal_seminar_data.dosen_pembimbing_2.id_role_dosen)

    # print(roledosen_get)
    # # roledosen_checker=roledosen.objects.filter(pk=roledosen_data.id_role_dosen).exists()
    
    # print(roledosen_data.id_role_dosen)
    detailpenilaian_data=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Seminar Proposal").filter(id_jadwal_seminar=jadwal_seminar_data).first()
    detailpenilaian_checker=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Seminar Proposal").filter(id_jadwal_seminar=jadwal_seminar_data).exists()
    penilaian_first=penilaian.objects.filter(id_detail_penilaian=detailpenilaian_data).first()

    PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=0,can_delete=False)

    if request.method == 'POST':
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None

        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        else :
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST)
        
            # form.initial[]
        # print(penilaianset_form.is_valid())
        if all((detailpenilaian_form.is_valid(), penilaianset_form.is_valid())):
                # print(2,penilaianset_form)
                if detailpenilaian_checker==False:
                    detailpenilaian_form=detailpenilaian(
                        id_role_dosen = roledosen_get,
                        hasil_review = request.POST["hasil_review"],
                        id_jadwal_seminar=jadwal_seminar_data,
                        status_kelulusan = request.POST["status_kelulusan"],
                        nama_tahap= "Seminar Proposal",
                    )

                else :
                    detailpenilaian_form=detailpenilaian.objects.get(pk=detailpenilaian_data.id_detail_penilaian)
                    detailpenilaian_form.hasil_review=request.POST["hasil_review"]
                    detailpenilaian_form.status_kelulusan=request.POST["status_kelulusan"]

                detailpenilaian_form.save()
                # print(detailpenilaian_form)
                detailpenilaianfilter=detailpenilaian.objects.filter(id_role_dosen = roledosen_get).filter(hasil_review = request.POST["hasil_review"]).first()
                detailpenilaiandata=detailpenilaian.objects.get(pk=detailpenilaianfilter.id_detail_penilaian)
                penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaiandata)

                if penilaianset_form.is_valid():
                
                   penilaianset_form.save()
                messages.success(request,"Data Penilaian Telah Berhasil Dibuat! ")
                return redirect('/jadwal_bimbingan/belum')
        else :
            counter_cpmk=0
            for form in penilaianset_form:
            
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_sempro[counter_cpmk])
                    counter_cpmk+=1
            

    else :
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None
        
        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormDosen()
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_sempro),can_delete=False)  
            penilaianset_form=PenilaianFormSet()

            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_sempro[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_sempro[counter_cpmk])
                    counter_cpmk+=1
            # print(1)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_sempro),can_delete=False)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            # print(detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_sempro[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_sempro[counter_cpmk])
                    counter_cpmk+=1
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
               
                    form.initial["id_sub_cpmk"]=list_cpmk_sempro[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_sempro[counter_cpmk])
                    counter_cpmk+=1
            # print(3)
        else :
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet()
            # print(4)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_sempro[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_sempro[counter_cpmk])
                    counter_cpmk+=1
    # detailpenilaian_form=None 
    # penilaianset_form=None
    # cpmk_data=None
    # proposal_data=None
    return render(request, 'dosen/penilaian_update.html', {"detailpenilaianform":detailpenilaian_form,"form_nilai":penilaianset_form,"proposal_data":proposal_data,"cpmk_data":cpmk_data, "user_info": user_info})

# penilaian dan detail penilaian:create & update
# Untuk pembuatan dan update data penilaian dan detail penilaian bimbingan berdasarkan id proposal
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def penilaian_bimbingan_dosen_1_by_nim(request, nim):
    user_info = user_information(request)
    # jadwal_seminar_data=jadwal_seminar.objects.get(pk=id_jadwal_seminar)
    # print(jadwal_seminar_data)
    mahasiswa_data=mahasiswa.objects.get(nim=nim)

    # list_cpmk_pembimbing=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    list_cpmk_pembimbing=list(sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_pembimbing=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    # print(list_cpmk_sempro)
    # bimbingan_filter=bimbingan.objects.filter(id_proposal__nim=mahasiswa_data.nim).filter(status_bimbingan="ACC").order_by("-tanggal_update").first()
    # # .filter(status_bimbingan="ACC")
    #     try : 
    #     proposal_data=proposal.objects.get(pk=bimbingan_filter.id_proposal.id_proposal)
    # except:
    #     proposal_data=None
    # print(proposal_data)
    # list1=list(sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_pembimbing=0).values_list("id_sub_cpmk",flat=True))
    # # list(list_cpmk_pembimbing.values_list("id_sub_cpmk",flat=True))
    # list2=["1A","2A","2B", "2C","3A","3D","4A","5A","5B","6B","8B"]
    # for elemen in list1:
    #     if elemen in list2:
    #         print(elemen, "ditemukan dalam kedua list")
    #     else:
    #         print(elemen, "tidak ditemukan dalam kedua list")
    
    
    # list_cpmk_semhas=["1A","1C", "2A","2B","2C","2D","3D","4A","5A","5B","7A","8A"]
    # list_cpmk_pembimbing=["1A","2A","2B", "2C","3A","3D","4A","5A","5B","6B","8B"]
    
    # cpmk_data=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0)
    cpmk_data=sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_pembimbing=0)
    roledosen_get=roledosen.objects.filter(nim__nim=nim).filter(status="Active").filter(role="Pembimbing 1").first()


    detailpenilaian_data=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Bimbingan").first()
    detailpenilaian_checker=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Bimbingan").exists()
    penilaian_first=penilaian.objects.filter(id_detail_penilaian=detailpenilaian_data).first()

    PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=0,can_delete=False)

    if request.method == 'POST':
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None

        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormBimbingan(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormBimbingan(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormBimbingan(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        else :
            detailpenilaian_form=DetailPenilaianFormBimbingan(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST)
        
            # form.initial[]
        # print(penilaianset_form.is_valid())
        if all((detailpenilaian_form.is_valid(), penilaianset_form.is_valid())):
                # print(2,penilaianset_form)
                if detailpenilaian_checker==False:
                    detailpenilaian_form=detailpenilaian(
                        id_role_dosen = roledosen_get,
                        hasil_review = request.POST["hasil_review"],
                        id_jadwal_seminar=None,
                        status_kelulusan = request.POST["status_kelulusan"],
                        nama_tahap= "Bimbingan",

                    )

                else :
                    detailpenilaian_form=detailpenilaian.objects.get(pk=detailpenilaian_data.id_detail_penilaian)
                    detailpenilaian_form.hasil_review=request.POST["hasil_review"]
                    detailpenilaian_form.status_kelulusan=request.POST["status_kelulusan"]

                detailpenilaian_form.save()
                # print(detailpenilaian_form)
                detailpenilaianfilter=detailpenilaian.objects.filter(id_role_dosen = roledosen_get).filter(hasil_review = request.POST["hasil_review"]).first()
                detailpenilaiandata=detailpenilaian.objects.get(pk=detailpenilaianfilter.id_detail_penilaian)
                penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaiandata)

                if penilaianset_form.is_valid():
                   penilaianset_form.save()
                messages.success(request,"Data Penilaian Telah Berhasil Dibuat! ")
                return redirect('/tabulasi_penilaian')
        else : 
            counter_cpmk=0
            for form in penilaianset_form.forms:
                    # print(form)
                    # form.fields["id_sub_cpmk_"].widget.attrs['disabled'] = False
                    # form.initial["id_tabel_sub_cpmk_"]=sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    # form.fields["id_tabel_sub_cpmk_"].initial=sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    # form.fields["id_sub_cpmk_"].widget.attrs['disabled'] = True
                    counter_cpmk+=1

    else :
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None
        
        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormBimbingan()
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_pembimbing),can_delete=False)  
            penilaianset_form=PenilaianFormSet()

            counter_cpmk=0
            for form in penilaianset_form:
                # print(1)
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_pembimbing[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    # form.fields["id_sub_cpmk_"].widget.attrs['disabled'] = False
                    # form.fields["id_sub_cpmk_"].widget.attrs['value'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    # form.fields["id_sub_cpmk_"].widget.attrs['disabled'] = True
                    counter_cpmk+=1
            # print(1)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormBimbingan(instance=detailpenilaian_data)
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_pembimbing),can_delete=False)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            # print(detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_pembimbing[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    counter_cpmk+=1
            # print(2)
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormBimbingan(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
               
                    form.initial["id_sub_cpmk"]=list_cpmk_pembimbing[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    counter_cpmk+=1
            # print(3)
        else :
            detailpenilaian_form=DetailPenilaianFormBimbingan(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet()
            # print(4)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_pembimbing[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    counter_cpmk+=1
    return render(request, 'dosen/penilaian_update.html', {"detailpenilaianform":detailpenilaian_form,"form_nilai":penilaianset_form,"cpmk_data":cpmk_data, "user_info": user_info})


# penilaian dan detail penilaian:create & update
# Untuk pembuatan dan update data penilaian dan detail penilaian bimbingan berdasarkan id proposal
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def penilaian_bimbingan_dosen_2_by_nim(request, nim):
    user_info = user_information(request)
    # jadwal_seminar_data=jadwal_seminar.objects.get(pk=id_jadwal_seminar)
    # print(jadwal_seminar_data)
    mahasiswa_data=mahasiswa.objects.get(nim=nim)

    # list_cpmk_pembimbing=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    list_cpmk_pembimbing=list(sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_pembimbing=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    # print(list_cpmk_sempro)
    # bimbingan_filter=bimbingan.objects.filter(id_proposal__nim=mahasiswa_data.nim).filter(status_bimbingan="ACC").order_by("-tanggal_update").first()
    # # .filter(status_bimbingan="ACC")
    #     try : 
    #     proposal_data=proposal.objects.get(pk=bimbingan_filter.id_proposal.id_proposal)
    # except:
    #     proposal_data=None
    # print(proposal_data)
    # list1=list(sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_pembimbing=0).values_list("id_sub_cpmk",flat=True))
    # # list(list_cpmk_pembimbing.values_list("id_sub_cpmk",flat=True))
    # list2=["1A","2A","2B", "2C","3A","3D","4A","5A","5B","6B","8B"]
    # for elemen in list1:
    #     if elemen in list2:
    #         print(elemen, "ditemukan dalam kedua list")
    #     else:
    #         print(elemen, "tidak ditemukan dalam kedua list")
    
    
    # list_cpmk_semhas=["1A","1C", "2A","2B","2C","2D","3D","4A","5A","5B","7A","8A"]
    # list_cpmk_pembimbing=["1A","2A","2B", "2C","3A","3D","4A","5A","5B","6B","8B"]
    
    # cpmk_data=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0)
    cpmk_data=sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_pembimbing=0)
    roledosen_get=roledosen.objects.filter(nim__nim=nim).filter(status="Active").filter(role="Pembimbing 2").first()


    detailpenilaian_data=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Bimbingan").first()
    detailpenilaian_checker=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Bimbingan").exists()
    penilaian_first=penilaian.objects.filter(id_detail_penilaian=detailpenilaian_data).first()

    PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=0,can_delete=False)

    if request.method == 'POST':
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None

        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormBimbingan(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormBimbingan(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormBimbingan(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        else :
            detailpenilaian_form=DetailPenilaianFormBimbingan(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST)
        
            # form.initial[]
        # print(penilaianset_form.is_valid())
        if all((detailpenilaian_form.is_valid(), penilaianset_form.is_valid())):
                # print(2,penilaianset_form)
                if detailpenilaian_checker==False:
                    detailpenilaian_form=detailpenilaian(
                        id_role_dosen = roledosen_get,
                        hasil_review = request.POST["hasil_review"],
                        id_jadwal_seminar=None,
                        status_kelulusan = request.POST["status_kelulusan"],
                        nama_tahap= "Bimbingan",

                    )

                else :
                    detailpenilaian_form=detailpenilaian.objects.get(pk=detailpenilaian_data.id_detail_penilaian)
                    detailpenilaian_form.hasil_review=request.POST["hasil_review"]
                    detailpenilaian_form.status_kelulusan=request.POST["status_kelulusan"]

                detailpenilaian_form.save()
                # print(detailpenilaian_form)
                detailpenilaianfilter=detailpenilaian.objects.filter(id_role_dosen = roledosen_get).filter(hasil_review = request.POST["hasil_review"]).first()
                detailpenilaiandata=detailpenilaian.objects.get(pk=detailpenilaianfilter.id_detail_penilaian)
                penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaiandata)

                if penilaianset_form.is_valid():
                   penilaianset_form.save()
                messages.success(request,"Data Penilaian Telah Berhasil Dibuat! ")
                return redirect('/tabulasi_penilaian')
        else : 
            counter_cpmk=0
            for form in penilaianset_form.forms:
                    # print(form)
                    # form.fields["id_sub_cpmk_"].widget.attrs['disabled'] = False
                    # form.initial["id_tabel_sub_cpmk_"]=sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    # form.fields["id_tabel_sub_cpmk_"].initial=sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    # form.fields["id_sub_cpmk_"].widget.attrs['disabled'] = True
                    counter_cpmk+=1

    else :
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None
        
        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormBimbingan()
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_pembimbing),can_delete=False)  
            penilaianset_form=PenilaianFormSet()

            counter_cpmk=0
            for form in penilaianset_form:
                # print(1)
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_pembimbing[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    # form.fields["id_sub_cpmk_"].widget.attrs['disabled'] = False
                    # form.fields["id_sub_cpmk_"].widget.attrs['value'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    # form.fields["id_sub_cpmk_"].widget.attrs['disabled'] = True
                    counter_cpmk+=1
            # print(1)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormBimbingan(instance=detailpenilaian_data)
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_pembimbing),can_delete=False)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            # print(detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_pembimbing[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    counter_cpmk+=1
            # print(2)
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormBimbingan(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
               
                    form.initial["id_sub_cpmk"]=list_cpmk_pembimbing[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    counter_cpmk+=1
            # print(3)
        else :
            detailpenilaian_form=DetailPenilaianFormBimbingan(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet()
            # print(4)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_pembimbing[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    counter_cpmk+=1
    return render(request, 'dosen/penilaian_update.html', {"detailpenilaianform":detailpenilaian_form,"form_nilai":penilaianset_form,"cpmk_data":cpmk_data, "user_info": user_info})


# penilaian dan detail penilaian:create & update
# Untuk pembuatan dan update data penilaian dan detail penilaian bimbingan berdasarkan id proposal
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def penilaian_bimbingan_dosen_1(request, id_jadwal_seminar):
    user_info = user_information(request)
    jadwal_seminar_data=jadwal_seminar.objects.get(pk=id_jadwal_seminar)
    # print(jadwal_seminar_data)
    mahasiswa_data=mahasiswa.objects.get(nim=jadwal_seminar_data.mahasiswa.nim)

    # list_cpmk_pembimbing=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    list_cpmk_pembimbing=list(sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_pembimbing=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    # print(list_cpmk_sempro)
    # bimbingan_filter=bimbingan.objects.filter(id_proposal__nim=mahasiswa_data.nim).filter(status_bimbingan="ACC").order_by("-tanggal_update").first()
    # # .filter(status_bimbingan="ACC")
    #     try : 
    #     proposal_data=proposal.objects.get(pk=bimbingan_filter.id_proposal.id_proposal)
    # except:
    #     proposal_data=None
    # print(proposal_data)
    # list1=list(sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_pembimbing=0).values_list("id_sub_cpmk",flat=True))
    # # list(list_cpmk_pembimbing.values_list("id_sub_cpmk",flat=True))
    # list2=["1A","2A","2B", "2C","3A","3D","4A","5A","5B","6B","8B"]
    # for elemen in list1:
    #     if elemen in list2:
    #         print(elemen, "ditemukan dalam kedua list")
    #     else:
    #         print(elemen, "tidak ditemukan dalam kedua list")
    
    
    # list_cpmk_semhas=["1A","1C", "2A","2B","2C","2D","3D","4A","5A","5B","7A","8A"]
    # list_cpmk_pembimbing=["1A","2A","2B", "2C","3A","3D","4A","5A","5B","6B","8B"]
    
    # cpmk_data=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0)
    cpmk_data=sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_pembimbing=0)
    roledosen_get=roledosen.objects.get(pk=jadwal_seminar_data.dosen_pembimbing_1.id_role_dosen)


    detailpenilaian_data=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Bimbingan").first()
    detailpenilaian_checker=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Bimbingan").exists()
    penilaian_first=penilaian.objects.filter(id_detail_penilaian=detailpenilaian_data).first()

    PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=0,can_delete=False)

    if request.method == 'POST':
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None

        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormBimbingan(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormBimbingan(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormBimbingan(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        else :
            detailpenilaian_form=DetailPenilaianFormBimbingan(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST)
        
            # form.initial[]
        # print(penilaianset_form.is_valid())
        if all((detailpenilaian_form.is_valid(), penilaianset_form.is_valid())):
                # print(2,penilaianset_form)
                if detailpenilaian_checker==False:
                    detailpenilaian_form=detailpenilaian(
                        id_role_dosen = roledosen_get,
                        hasil_review = request.POST["hasil_review"],
                        id_jadwal_seminar=None,
                        status_kelulusan = request.POST["status_kelulusan"],
                        nama_tahap= "Bimbingan",

                    )

                else :
                    detailpenilaian_form=detailpenilaian.objects.get(pk=detailpenilaian_data.id_detail_penilaian)
                    detailpenilaian_form.hasil_review=request.POST["hasil_review"]
                    detailpenilaian_form.status_kelulusan=request.POST["status_kelulusan"]

                detailpenilaian_form.save()
                # print(detailpenilaian_form)
                detailpenilaianfilter=detailpenilaian.objects.filter(id_role_dosen = roledosen_get).filter(hasil_review = request.POST["hasil_review"]).first()
                detailpenilaiandata=detailpenilaian.objects.get(pk=detailpenilaianfilter.id_detail_penilaian)
                penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaiandata)

                if penilaianset_form.is_valid():
                   penilaianset_form.save()
                messages.success(request,"Data Penilaian Telah Berhasil Dibuat! ")
                return redirect('/jadwal_bimbingan/belum')
        else : 
            counter_cpmk=0
            for form in penilaianset_form.forms:
                    # print(form)
                    # form.fields["id_sub_cpmk_"].widget.attrs['disabled'] = False
                    # form.initial["id_tabel_sub_cpmk_"]=sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    # form.fields["id_tabel_sub_cpmk_"].initial=sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    # form.fields["id_sub_cpmk_"].widget.attrs['disabled'] = True
                    counter_cpmk+=1

    else :
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None
        
        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormBimbingan()
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_pembimbing),can_delete=False)  
            penilaianset_form=PenilaianFormSet()

            counter_cpmk=0
            for form in penilaianset_form:
                # print(1)
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_pembimbing[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    # form.fields["id_sub_cpmk_"].widget.attrs['disabled'] = False
                    # form.fields["id_sub_cpmk_"].widget.attrs['value'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    # form.fields["id_sub_cpmk_"].widget.attrs['disabled'] = True
                    counter_cpmk+=1
            # print(1)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormBimbingan(instance=detailpenilaian_data)
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_pembimbing),can_delete=False)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            # print(detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_pembimbing[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    counter_cpmk+=1
            # print(2)
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormBimbingan(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
               
                    form.initial["id_sub_cpmk"]=list_cpmk_pembimbing[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    counter_cpmk+=1
            # print(3)
        else :
            detailpenilaian_form=DetailPenilaianFormBimbingan(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet()
            # print(4)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_pembimbing[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    counter_cpmk+=1
    return render(request, 'dosen/penilaian_update.html', {"detailpenilaianform":detailpenilaian_form,"form_nilai":penilaianset_form,"cpmk_data":cpmk_data, "user_info": user_info})

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def penilaian_bimbingan_dosen_2(request, id_jadwal_seminar):
    user_info = user_information(request)
    jadwal_seminar_data=jadwal_seminar.objects.get(pk=id_jadwal_seminar)
    # print(jadwal_seminar_data)
    mahasiswa_data=mahasiswa.objects.get(nim=jadwal_seminar_data.mahasiswa.nim)

    # list_cpmk_pembimbing=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    list_cpmk_pembimbing=list(sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_pembimbing=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    # print(list_cpmk_sempro)
    # bimbingan_filter=bimbingan.objects.filter(id_proposal__nim=mahasiswa_data.nim).filter(status_bimbingan="ACC").order_by("-tanggal_update").first()
    # # .filter(status_bimbingan="ACC")
    #     try : 
    #     proposal_data=proposal.objects.get(pk=bimbingan_filter.id_proposal.id_proposal)
    # except:
    #     proposal_data=None
    # print(proposal_data)
    # list1=list(sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_pembimbing=0).values_list("id_sub_cpmk",flat=True))
    # # list(list_cpmk_pembimbing.values_list("id_sub_cpmk",flat=True))
    # list2=["1A","2A","2B", "2C","3A","3D","4A","5A","5B","6B","8B"]
    # for elemen in list1:
    #     if elemen in list2:
    #         print(elemen, "ditemukan dalam kedua list")
    #     else:
    #         print(elemen, "tidak ditemukan dalam kedua list")
    
    
    # list_cpmk_semhas=["1A","1C", "2A","2B","2C","2D","3D","4A","5A","5B","7A","8A"]
    # list_cpmk_pembimbing=["1A","2A","2B", "2C","3A","3D","4A","5A","5B","6B","8B"]
    
    # cpmk_data=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0)
    cpmk_data=sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_pembimbing=0)
    roledosen_get=roledosen.objects.get(pk=jadwal_seminar_data.dosen_pembimbing_2.id_role_dosen)


    detailpenilaian_data=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Bimbingan").first()
    detailpenilaian_checker=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Bimbingan").exists()
    penilaian_first=penilaian.objects.filter(id_detail_penilaian=detailpenilaian_data).first()

    PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=0,can_delete=False)

    if request.method == 'POST':
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None

        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormBimbingan(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormBimbingan(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormBimbingan(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        else :
            detailpenilaian_form=DetailPenilaianFormBimbingan(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST)
        
            # form.initial[]
        # print(penilaianset_form.is_valid())
        if all((detailpenilaian_form.is_valid(), penilaianset_form.is_valid())):
                # print(2,penilaianset_form)
                if detailpenilaian_checker==False:
                    detailpenilaian_form=detailpenilaian(
                        id_role_dosen = roledosen_get,
                        hasil_review = request.POST["hasil_review"],
                        id_jadwal_seminar=None,
                        status_kelulusan = request.POST["status_kelulusan"],
                        nama_tahap= "Bimbingan",

                    )

                else :
                    detailpenilaian_form=detailpenilaian.objects.get(pk=detailpenilaian_data.id_detail_penilaian)
                    detailpenilaian_form.hasil_review=request.POST["hasil_review"]
                    detailpenilaian_form.status_kelulusan=request.POST["status_kelulusan"]

                detailpenilaian_form.save()
                # print(detailpenilaian_form)
                detailpenilaianfilter=detailpenilaian.objects.filter(id_role_dosen = roledosen_get).filter(hasil_review = request.POST["hasil_review"]).first()
                detailpenilaiandata=detailpenilaian.objects.get(pk=detailpenilaianfilter.id_detail_penilaian)
                penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaiandata)

                if penilaianset_form.is_valid():
                   penilaianset_form.save()
                messages.success(request,"Data Penilaian Telah Berhasil Dibuat! ")
                return redirect('/jadwal_bimbingan/belum')
        else : 
            counter_cpmk=0
            for form in penilaianset_form.forms:
                    # print(form)
                    # form.fields["id_sub_cpmk_"].widget.attrs['disabled'] = False
                    # form.initial["id_tabel_sub_cpmk_"]=sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    # form.fields["id_tabel_sub_cpmk_"].initial=sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    # form.fields["id_sub_cpmk_"].widget.attrs['disabled'] = True
                    counter_cpmk+=1

    else :
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None
        
        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormBimbingan()
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_pembimbing),can_delete=False)  
            penilaianset_form=PenilaianFormSet()

            counter_cpmk=0
            for form in penilaianset_form:
                # print(1)
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_pembimbing[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    # form.fields["id_sub_cpmk_"].widget.attrs['disabled'] = False
                    # form.fields["id_sub_cpmk_"].widget.attrs['value'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    # form.fields["id_sub_cpmk_"].widget.attrs['disabled'] = True
                    counter_cpmk+=1
            # print(1)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormBimbingan(instance=detailpenilaian_data)
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_pembimbing),can_delete=False)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            # print(detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_pembimbing[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    counter_cpmk+=1
            # print(2)
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormBimbingan(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
               
                    form.initial["id_sub_cpmk"]=list_cpmk_pembimbing[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    counter_cpmk+=1
            # print(3)
        else :
            detailpenilaian_form=DetailPenilaianFormBimbingan(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet()
            # print(4)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_pembimbing[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_pembimbing[counter_cpmk])
                    counter_cpmk+=1
    return render(request, 'dosen/penilaian_update.html', {"detailpenilaianform":detailpenilaian_form,"form_nilai":penilaianset_form,
                                                        #    "proposal_data":proposal_data,
                                                        "cpmk_data":cpmk_data, "user_info": user_info})


# penilaian dan detail penilaian:create & update
# Untuk pembuatan dan update data penilaian dan detail penilaian seminar hasil berdasarkan id proposal
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def penilaian_semhas_dosen_1(request, id_jadwal_seminar):
    user_info = user_information(request)
    jadwal_seminar_data=jadwal_seminar.objects.get(pk=id_jadwal_seminar)
    # print(jadwal_seminar_data)
    mahasiswa_data=mahasiswa.objects.get(nim=jadwal_seminar_data.mahasiswa.nim)

    # list_cpmk_pembimbing=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    list_cpmk_semhas=list(sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_semhas=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    # print(list_cpmk_sempro)
    bimbingan_filter=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(id_proposal__nim=mahasiswa_data.nim).filter(status_bimbingan="ACC").order_by("-tanggal_update").first()
    # .filter(status_bimbingan="ACC")
    try : 
        proposal_data=proposal.objects.get(pk=bimbingan_filter.id_proposal.id_proposal)
    except:
        proposal_data=None
    # print(proposal_data)
    # list1=list(sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_semhas=0).values_list("id_sub_cpmk",flat=True))
    # # list(list_cpmk_semhas.values_list("id_sub_cpmk",flat=True))
    # list2=["1A","1C", "2A","2B","2C","2D","3D","4A","5A","5B","7A","8A"]
    # for elemen in list1:
    #     if elemen in list2:
    #         print(elemen, "ditemukan dalam kedua list")
    #     else:
    #         print(elemen, "tidak ditemukan dalam kedua list")
    
    
    # list_cpmk_semhas=["1A","1C", "2A","2B","2C","2D","3D","4A","5A","5B","7A","8A"]
    # list_cpmk_pembimbing=["1A","2A","2B", "2C","3A","3D","4A","5A","5B","6B","8B"]
    
    # cpmk_data=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0)
    cpmk_data=sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_semhas=0)
    roledosen_get=roledosen.objects.get(pk=jadwal_seminar_data.dosen_penguji_1.id_role_dosen)

    
    # print(roledosen_data.id_role_dosen)
    detailpenilaian_data=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Seminar Hasil").filter(id_jadwal_seminar=jadwal_seminar_data).first()
    detailpenilaian_checker=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Seminar Hasil").filter(id_jadwal_seminar=jadwal_seminar_data).exists()
    penilaian_first=penilaian.objects.filter(id_detail_penilaian=detailpenilaian_data).first()

    PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=0,can_delete=False)

    if request.method == 'POST':
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None

        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        else :
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST)
        
            # form.initial[]
        # print(penilaianset_form.is_valid())
        if all((detailpenilaian_form.is_valid(), penilaianset_form.is_valid())):
                # print(2,penilaianset_form)
                if detailpenilaian_checker==False:
                    detailpenilaian_form=detailpenilaian(
                        id_role_dosen = roledosen_get,
                        hasil_review = request.POST["hasil_review"],
                        id_jadwal_seminar=jadwal_seminar_data,
                        status_kelulusan = request.POST["status_kelulusan"],
                        nama_tahap= "Seminar Hasil",

                    )

                else :
                    detailpenilaian_form=detailpenilaian.objects.get(pk=detailpenilaian_data.id_detail_penilaian)
                    detailpenilaian_form.hasil_review=request.POST["hasil_review"]
                    detailpenilaian_form.status_kelulusan=request.POST["status_kelulusan"]

                detailpenilaian_form.save()
                # print(detailpenilaian_form)
                detailpenilaianfilter=detailpenilaian.objects.filter(id_role_dosen = roledosen_get).filter(hasil_review = request.POST["hasil_review"]).first()
                detailpenilaiandata=detailpenilaian.objects.get(pk=detailpenilaianfilter.id_detail_penilaian)
                penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaiandata)

                if penilaianset_form.is_valid():
                   penilaianset_form.save()
                messages.success(request,"Data Penilaian Telah Berhasil Dibuat! ")
                return redirect('/jadwal_semhas/belum')
        else :
            counter_cpmk=0
            for form in penilaianset_form:
            
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_semhas[counter_cpmk])
                    counter_cpmk+=1

    else :
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None
        
        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormDosen()
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_semhas),can_delete=False)  
            penilaianset_form=PenilaianFormSet()

            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_semhas[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_semhas[counter_cpmk])
                    # form.initial["id_tabel_sub_cpmk_"]=list_cpmk_semhas[counter_cpmk]
                    counter_cpmk+=1
            # print(1)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_semhas),can_delete=False)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            # print(detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_semhas[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_semhas[counter_cpmk])
                    counter_cpmk+=1
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
               
                    # form.initial["id_sub_cpmk"]=list_cpmk_pembimbing[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_semhas[counter_cpmk])
                    counter_cpmk+=1
            # print(3)
        else :
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet()
            # print(4)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_semhas[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_semhas[counter_cpmk])
                    counter_cpmk+=1
    return render(request, 'dosen/penilaian_update.html', {"detailpenilaianform":detailpenilaian_form,"form_nilai":penilaianset_form,"cpmk_data":cpmk_data,"proposal_data":proposal_data, "user_info": user_info})

# penilaian dan detail penilaian:create & update
# Untuk pembuatan dan update data penilaian dan detail penilaian seminar hasil berdasarkan id proposal
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def penilaian_semhas_dosen_2(request, id_jadwal_seminar):
    user_info = user_information(request)
    jadwal_seminar_data=jadwal_seminar.objects.get(pk=id_jadwal_seminar)
    # print(jadwal_seminar_data)
    mahasiswa_data=mahasiswa.objects.get(nim=jadwal_seminar_data.mahasiswa.nim)

    # list_cpmk_pembimbing=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    list_cpmk_semhas=list(sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_semhas=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    # print(list_cpmk_sempro)
    bimbingan_filter=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(id_proposal__nim=mahasiswa_data.nim).filter(status_bimbingan="ACC").order_by("-tanggal_update").first()
    # .filter(status_bimbingan="ACC")
    try : 
        proposal_data=proposal.objects.get(pk=bimbingan_filter.id_proposal.id_proposal)
    except:
        proposal_data=None
    # print(proposal_data)
    # list1=list(sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_semhas=0).values_list("id_sub_cpmk",flat=True))
    # # list(list_cpmk_semhas.values_list("id_sub_cpmk",flat=True))
    # list2=["1A","1C", "2A","2B","2C","2D","3D","4A","5A","5B","7A","8A"]
    # for elemen in list1:
    #     if elemen in list2:
    #         print(elemen, "ditemukan dalam kedua list")
    #     else:
    #         print(elemen, "tidak ditemukan dalam kedua list")
    
    
    # list_cpmk_semhas=["1A","1C", "2A","2B","2C","2D","3D","4A","5A","5B","7A","8A"]
    # list_cpmk_pembimbing=["1A","2A","2B", "2C","3A","3D","4A","5A","5B","6B","8B"]
    
    # cpmk_data=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0)
    cpmk_data=sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_semhas=0)
    roledosen_get=roledosen.objects.get(pk=jadwal_seminar_data.dosen_penguji_2.id_role_dosen)

    
    # print(roledosen_data.id_role_dosen)
    detailpenilaian_data=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Seminar Hasil").filter(id_jadwal_seminar=jadwal_seminar_data).first()
    detailpenilaian_checker=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Seminar Hasil").filter(id_jadwal_seminar=jadwal_seminar_data).exists()
    penilaian_first=penilaian.objects.filter(id_detail_penilaian=detailpenilaian_data).first()

    PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=0,can_delete=False)

    if request.method == 'POST':
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None

        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        else :
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST)
        
            # form.initial[]
        # print(penilaianset_form.is_valid())
        if all((detailpenilaian_form.is_valid(), penilaianset_form.is_valid())):
                # print(2,penilaianset_form)
                if detailpenilaian_checker==False:
                    detailpenilaian_form=detailpenilaian(
                        id_role_dosen = roledosen_get,
                        hasil_review = request.POST["hasil_review"],
                        id_jadwal_seminar=jadwal_seminar_data,
                        status_kelulusan = request.POST["status_kelulusan"],
                        nama_tahap= "Seminar Hasil",

                    )

                else :
                    detailpenilaian_form=detailpenilaian.objects.get(pk=detailpenilaian_data.id_detail_penilaian)
                    detailpenilaian_form.hasil_review=request.POST["hasil_review"]
                    detailpenilaian_form.status_kelulusan=request.POST["status_kelulusan"]

                detailpenilaian_form.save()
                # print(detailpenilaian_form)
                detailpenilaianfilter=detailpenilaian.objects.filter(id_role_dosen = roledosen_get).filter(hasil_review = request.POST["hasil_review"]).first()
                detailpenilaiandata=detailpenilaian.objects.get(pk=detailpenilaianfilter.id_detail_penilaian)
                penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaiandata)

                if penilaianset_form.is_valid():
                   penilaianset_form.save()
                messages.success(request,"Data Penilaian Telah Berhasil Dibuat! ")
                return redirect('/jadwal_semhas/belum')
        else :
            counter_cpmk=0
            for form in penilaianset_form:
            
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_semhas[counter_cpmk])
                    counter_cpmk+=1

    else :
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None
        
        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormDosen()
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_semhas),can_delete=False)  
            penilaianset_form=PenilaianFormSet()

            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_semhas[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_semhas[counter_cpmk])
                    # form.initial["id_tabel_sub_cpmk_"]=list_cpmk_semhas[counter_cpmk]
                    counter_cpmk+=1
            # print(1)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_semhas),can_delete=False)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            # print(detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_semhas[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_semhas[counter_cpmk])
                    counter_cpmk+=1
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
               
                    # form.initial["id_sub_cpmk"]=list_cpmk_pembimbing[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_semhas[counter_cpmk])
                    counter_cpmk+=1
            # print(3)
        else :
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet()
            # print(4)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_semhas[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_semhas[counter_cpmk])
                    counter_cpmk+=1
    return render(request, 'dosen/penilaian_update.html', {"detailpenilaianform":detailpenilaian_form,"form_nilai":penilaianset_form,"cpmk_data":cpmk_data,"proposal_data":proposal_data, "user_info": user_info})

# penilaian dan detail penilaian:create & update
# Untuk pembuatan dan update data penilaian dan detail penilaian seminar hasil berdasarkan id proposal
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def penilaian_semhas_dosen_pembimbing_1(request, id_jadwal_seminar):
    user_info = user_information(request)
    jadwal_seminar_data=jadwal_seminar.objects.get(pk=id_jadwal_seminar)
    # print(jadwal_seminar_data)
    mahasiswa_data=mahasiswa.objects.get(nim=jadwal_seminar_data.mahasiswa.nim)

    # list_cpmk_pembimbing=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    list_cpmk_semhas=list(sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_semhas=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    # print(list_cpmk_sempro)
    bimbingan_filter=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(id_proposal__nim=mahasiswa_data.nim).filter(status_bimbingan="ACC").order_by("-tanggal_update").first()
    # .filter(status_bimbingan="ACC")
    try : 
        proposal_data=proposal.objects.get(pk=bimbingan_filter.id_proposal.id_proposal)
    except:
        proposal_data=None
    # print(proposal_data)
    # list1=list(sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_semhas=0).values_list("id_sub_cpmk",flat=True))
    # # list(list_cpmk_semhas.values_list("id_sub_cpmk",flat=True))
    # list2=["1A","1C", "2A","2B","2C","2D","3D","4A","5A","5B","7A","8A"]
    # for elemen in list1:
    #     if elemen in list2:
    #         print(elemen, "ditemukan dalam kedua list")
    #     else:
    #         print(elemen, "tidak ditemukan dalam kedua list")
    
    
    # list_cpmk_semhas=["1A","1C", "2A","2B","2C","2D","3D","4A","5A","5B","7A","8A"]
    # list_cpmk_pembimbing=["1A","2A","2B", "2C","3A","3D","4A","5A","5B","6B","8B"]
    
    # cpmk_data=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0)
    cpmk_data=sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_semhas=0)
    roledosen_get=roledosen.objects.get(pk=jadwal_seminar_data.dosen_pembimbing_1.id_role_dosen)

    
    # print(roledosen_data.id_role_dosen)
    detailpenilaian_data=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Seminar Hasil").filter(id_jadwal_seminar=jadwal_seminar_data).first()
    detailpenilaian_checker=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Seminar Hasil").filter(id_jadwal_seminar=jadwal_seminar_data).exists()
    penilaian_first=penilaian.objects.filter(id_detail_penilaian=detailpenilaian_data).first()

    PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=0,can_delete=False)

    if request.method == 'POST':
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None

        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        else :
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST)
        
            # form.initial[]
        # print(penilaianset_form.is_valid())
        if all((detailpenilaian_form.is_valid(), penilaianset_form.is_valid())):
                # print(2,penilaianset_form)
                if detailpenilaian_checker==False:
                    detailpenilaian_form=detailpenilaian(
                        id_role_dosen = roledosen_get,
                        hasil_review = request.POST["hasil_review"],
                        id_jadwal_seminar=jadwal_seminar_data,
                        status_kelulusan = request.POST["status_kelulusan"],
                        nama_tahap= "Seminar Hasil",

                    )

                else :
                    detailpenilaian_form=detailpenilaian.objects.get(pk=detailpenilaian_data.id_detail_penilaian)
                    detailpenilaian_form.hasil_review=request.POST["hasil_review"]
                    detailpenilaian_form.status_kelulusan=request.POST["status_kelulusan"]

                detailpenilaian_form.save()
                # print(detailpenilaian_form)
                detailpenilaianfilter=detailpenilaian.objects.filter(id_role_dosen = roledosen_get).filter(hasil_review = request.POST["hasil_review"]).first()
                detailpenilaiandata=detailpenilaian.objects.get(pk=detailpenilaianfilter.id_detail_penilaian)
                penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaiandata)

                if penilaianset_form.is_valid():
                   penilaianset_form.save()
                messages.success(request,"Data Penilaian Telah Berhasil Dibuat! ")
                return redirect('/jadwal_bimbingan/belum')
        else :
            counter_cpmk=0
            for form in penilaianset_form:
            
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_semhas[counter_cpmk])
                    counter_cpmk+=1

    else :
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None
        
        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormDosen()
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_semhas),can_delete=False)  
            penilaianset_form=PenilaianFormSet()

            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_semhas[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_semhas[counter_cpmk])
                    # form.initial["id_tabel_sub_cpmk_"]=list_cpmk_semhas[counter_cpmk]
                    counter_cpmk+=1
            # print(1)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_semhas),can_delete=False)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            # print(detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_semhas[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_semhas[counter_cpmk])
                    counter_cpmk+=1
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
               
                    # form.initial["id_sub_cpmk"]=list_cpmk_pembimbing[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_semhas[counter_cpmk])
                    counter_cpmk+=1
            # print(3)
        else :
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet()
            # print(4)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_semhas[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_semhas[counter_cpmk])
                    counter_cpmk+=1
    return render(request, 'dosen/penilaian_update.html', {"detailpenilaianform":detailpenilaian_form,"form_nilai":penilaianset_form,"cpmk_data":cpmk_data,"proposal_data":proposal_data, "user_info": user_info})

# penilaian dan detail penilaian:create & update
# Untuk pembuatan dan update data penilaian dan detail penilaian seminar hasil berdasarkan id proposal
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def penilaian_semhas_dosen_pembimbing_2(request, id_jadwal_seminar):
    user_info = user_information(request)
    jadwal_seminar_data=jadwal_seminar.objects.get(pk=id_jadwal_seminar)
    # print(jadwal_seminar_data)
    mahasiswa_data=mahasiswa.objects.get(nim=jadwal_seminar_data.mahasiswa.nim)

    # list_cpmk_pembimbing=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    list_cpmk_semhas=list(sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_semhas=0).order_by("id_sub_cpmk").values_list("id_tabel_sub_cpmk",flat=True))
    # print(list_cpmk_sempro)
    bimbingan_filter=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(id_proposal__nim=mahasiswa_data.nim).filter(status_bimbingan="ACC").order_by("-tanggal_update").first()
    # .filter(status_bimbingan="ACC")
    try : 
        proposal_data=proposal.objects.get(pk=bimbingan_filter.id_proposal.id_proposal)
    except:
        proposal_data=None
    # print(proposal_data)
    # list1=list(sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_semhas=0).values_list("id_sub_cpmk",flat=True))
    # # list(list_cpmk_semhas.values_list("id_sub_cpmk",flat=True))
    # list2=["1A","1C", "2A","2B","2C","2D","3D","4A","5A","5B","7A","8A"]
    # for elemen in list1:
    #     if elemen in list2:
    #         print(elemen, "ditemukan dalam kedua list")
    #     else:
    #         print(elemen, "tidak ditemukan dalam kedua list")
    
    
    # list_cpmk_semhas=["1A","1C", "2A","2B","2C","2D","3D","4A","5A","5B","7A","8A"]
    # list_cpmk_pembimbing=["1A","2A","2B", "2C","3A","3D","4A","5A","5B","6B","8B"]
    
    # cpmk_data=sub_cpmk.objects.filter(id_nama_semester=mahasiswa_data.semester_daftar_skripsi).exclude(bobot_sempro=0)
    cpmk_data=sub_cpmk.objects.filter(tahun_angkatan=mahasiswa_data.angkatan).exclude(bobot_semhas=0)
    roledosen_get=roledosen.objects.get(pk=jadwal_seminar_data.dosen_pembimbing_2.id_role_dosen)

    
    # print(roledosen_data.id_role_dosen)
    detailpenilaian_data=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Seminar Hasil").filter(id_jadwal_seminar=jadwal_seminar_data).first()
    detailpenilaian_checker=detailpenilaian.objects.filter(id_role_dosen=roledosen_get).filter(nama_tahap="Seminar Hasil").filter(id_jadwal_seminar=jadwal_seminar_data).exists()
    penilaian_first=penilaian.objects.filter(id_detail_penilaian=detailpenilaian_data).first()

    PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=0,can_delete=False)

    if request.method == 'POST':
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None

        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaian_data)
        else :
            detailpenilaian_form=DetailPenilaianFormDosen(request.POST,instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(request.POST)
        
            # form.initial[]
        # print(penilaianset_form.is_valid())
        if all((detailpenilaian_form.is_valid(), penilaianset_form.is_valid())):
                # print(2,penilaianset_form)
                if detailpenilaian_checker==False:
                    detailpenilaian_form=detailpenilaian(
                        id_role_dosen = roledosen_get,
                        hasil_review = request.POST["hasil_review"],
                        id_jadwal_seminar=jadwal_seminar_data,
                        status_kelulusan = request.POST["status_kelulusan"],
                        nama_tahap= "Seminar Hasil",

                    )

                else :
                    detailpenilaian_form=detailpenilaian.objects.get(pk=detailpenilaian_data.id_detail_penilaian)
                    detailpenilaian_form.hasil_review=request.POST["hasil_review"]
                    detailpenilaian_form.status_kelulusan=request.POST["status_kelulusan"]

                detailpenilaian_form.save()
                # print(detailpenilaian_form)
                detailpenilaianfilter=detailpenilaian.objects.filter(id_role_dosen = roledosen_get).filter(hasil_review = request.POST["hasil_review"]).first()
                detailpenilaiandata=detailpenilaian.objects.get(pk=detailpenilaianfilter.id_detail_penilaian)
                penilaianset_form=PenilaianFormSet(request.POST,instance=detailpenilaiandata)

                if penilaianset_form.is_valid():
                   penilaianset_form.save()
                messages.success(request,"Data Penilaian Telah Berhasil Dibuat! ")
                return redirect('/jadwal_bimbingan/belum')
        else :
            counter_cpmk=0
            for form in penilaianset_form:
            
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_semhas[counter_cpmk])
                    counter_cpmk+=1

    else :
        try :
            penilaian_data=penilaian.objects.get(pk=penilaian_first.id_penilaian)
        except :
            penilaian_data=None
        
        if penilaian_data==None and detailpenilaian_checker==False:
            detailpenilaian_form=DetailPenilaianFormDosen()
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_semhas),can_delete=False)  
            penilaianset_form=PenilaianFormSet()

            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_semhas[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_semhas[counter_cpmk])
                    # form.initial["id_tabel_sub_cpmk_"]=list_cpmk_semhas[counter_cpmk]
                    counter_cpmk+=1
            # print(1)
        elif penilaian_data==None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            PenilaianFormSet = inlineformset_factory(detailpenilaian, penilaian,form=PenilaianForm, extra=len(list_cpmk_semhas),can_delete=False)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            # print(detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_semhas[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_semhas[counter_cpmk])
                    counter_cpmk+=1
        elif penilaian_data!=None and detailpenilaian_checker==True:
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet(instance=detailpenilaian_data)
            counter_cpmk=0
            for form in penilaianset_form:
               
                    # form.initial["id_sub_cpmk"]=list_cpmk_pembimbing[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_semhas[counter_cpmk])
                    counter_cpmk+=1
            # print(3)
        else :
            detailpenilaian_form=DetailPenilaianFormDosen(instance=detailpenilaian_data)
            penilaianset_form=PenilaianFormSet()
            # print(4)
            counter_cpmk=0
            for form in penilaianset_form:
                if "id_tabel_sub_cpmk" not in form.initial:
                    form.initial["id_sub_cpmk"]=list_cpmk_semhas[counter_cpmk]
                    # print(form.initial["id_sub_cpmk"])
                    form.fields["id_sub_cpmk_"].widget.attrs['placeholder'] = sub_cpmk.objects.get(pk=list_cpmk_semhas[counter_cpmk])
                    counter_cpmk+=1
    return render(request, 'dosen/penilaian_update.html', {"detailpenilaianform":detailpenilaian_form,"form_nilai":penilaianset_form,"cpmk_data":cpmk_data,"proposal_data":proposal_data, "user_info": user_info})


# Penilaian Dosen Pembimbing
# @login_required(login_url="/login")
# def penilaian_update(request, id):
#     user_info = user_information(request)
#     penilaian_data = penilaian.objects.get(pk=id)
#     if user_info[2].name == "Admin":
#         if request.method == "POST":
#             form = PenilaianForm(
#                 request.POST, instance=penilaian_data)
#             if form.is_valid():
#                 create_roledosen = form.save()
#                 create_roledosen.save()
#                 return redirect("../bimbinganget")
#         else:
#             form = PenilaianForm(instance=penilaian_data)
#     else:
#         if request.method == "POST":
#             form = PenilaianForm(
#                 request.POST, instance=penilaian_data)
#             form_penilaian= ParameterPenilaianForm(initial={"id_tabel_sub_cpmk":["3A","3B","3C"]})
#             form_set_nilai=inlineformset_factory(CPMK,ParameterPenilaian,fields=())
#             if form.is_valid():
#                 create_roledosen = form.save(commit=False)
#                 create_roledosen.id_role_dosen = dosen.objects.get(
#                     pk=user_info[0])
#                 create_roledosen.save()
#                 return redirect("../bimbinganget")
#         else:
#             form = PenilaianForm(instance=penilaian_data)
#     return render(request, 'dosen/penilaian_update.html', {"form": form, "user_info": user_info})


# penilaian:delete
# Menghapus data penilaian 
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def penilaian_delete(request, id):
    delete_data = penilaian.objects.get(pk=id)
    messages.error(request,"Data Penilaian Telah Berhasil Dihapus! ")
    delete_data.delete()
    return redirect('../penilaianget')

# todo : bug hapus data detail penilaian dan penilaian 

# Proposal 
# Proposal: Create
# Untuk Membuat Proposal Skripsi  
# todo: add in notification and email
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Mahasiswa','Properta'])
def proposal_create_full(request):
    user_info = user_information(request)
    if request.method == "POST":
        form = ProposalFormFull(request.POST, request.FILES)
        if form.is_valid():
            create_proposal = form.save(commit=False)
            create_proposal.save()
            messages.success(request,"Data Proposal Telah Berhasil Dibuat! ")
             # todo notif
            roledosen_data=roledosen.objects.filter(role="Pembimbing 1").filter(nim=create_proposal.nim)|roledosen.objects.filter(role="Pembimbing 2").filter(nim=create_proposal.nim)
            email_list=[]
            # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
            for i in roledosen_data:
                temp_email=list(User.objects.filter(pk=i.nip.id_user.id).values_list('email'))
                email_list.append(temp_email[0][0])
                notifikasi.objects.create(nip=i.nip,messages=f"Terdapat Proposal Baru Oleh {create_proposal.nim.id_user.first_name} Untuk diperiksa pada {tanggal} Jam {Jam}")
            # roledosen_data=roledosen.objects.filter(role="Pembimbing 1").filter(nim=create_proposal.nim)|roledosen.objects.filter(role="Pembimbing 2").filter(nim=create_proposal.nim)
            # send ke mahasiswa
            # email_list=roledosen.objects.filter(role="Pembimbing 1").filter(nim=create_proposal.nim).values_list('email')|roledosen.objects.filter(role="Pembimbing 2").filter(nim=create_proposal.nim).values_list('email')
            # User.objects.filter(pk=create_roledosen.id_proposal.nim.id_user).values_list('email')
            send_mail(
                'Terdapat Update Hasil Revisi Proposal Telah Di Buat ',
                f"Terdapat Proposal Baru Oleh {create_proposal.nim.id_user.first_name} Untuk diperiksa pada {tanggal} Jam {Jam}",
                settings.EMAIL_HOST_USER,
                email_list,
                fail_silently=False,
            )

            return redirect("../proposalget")
    else:
        form = ProposalFormFull()
    return render(request, 'bimbingan/proposal_create.html', {"form": form, "user_info": user_info})
# Proposal 
# Proposal: Create
# Untuk Membuat Proposal Skripsi  
# todo: add in notification and email
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Mahasiswa','Properta'])
def proposal_create(request):
    user_info = user_information(request)
    if request.method == "POST":
        form = ProposalForm(request.POST, request.FILES)
        if form.is_valid():

            create_proposal = form.save(commit=False)
            create_proposal.nim = mahasiswa.objects.get(pk=user_info[0])
            # create_proposal.nim = mahasiswa.objects.get(pk=user_info[0])
            create_proposal.save()
            messages.success(request,"Data Proposal Telah Berhasil Dibuat! ")
             # todo notif
            roledosen_data=roledosen.objects.filter(role="Pembimbing 1").filter(nim=create_proposal.nim)|roledosen.objects.filter(role="Pembimbing 2").filter(nim=create_proposal.nim)
            email_list=[]
            # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
            for i in roledosen_data:
                temp_email=list(User.objects.filter(pk=i.nip.id_user.id).values_list('email'))
                email_list.append(temp_email[0][0])
                notifikasi.objects.create(nip=i.nip,messages=f"Terdapat Proposal Baru Oleh {create_proposal.nim.id_user.first_name} Untuk diperiksa pada {tanggal} Jam {Jam}")
            # roledosen_data=roledosen.objects.filter(role="Pembimbing 1").filter(nim=create_proposal.nim)|roledosen.objects.filter(role="Pembimbing 2").filter(nim=create_proposal.nim)
            # send ke mahasiswa
            # email_list=roledosen.objects.filter(role="Pembimbing 1").filter(nim=create_proposal.nim).values_list('email')|roledosen.objects.filter(role="Pembimbing 2").filter(nim=create_proposal.nim).values_list('email')
            # User.objects.filter(pk=create_roledosen.id_proposal.nim.id_user).values_list('email')
            send_mail(
                'Terdapat Update Hasil Revisi Proposal Telah Di Buat ',
                f"Terdapat Proposal Baru Oleh {create_proposal.nim.id_user.first_name} Untuk diperiksa pada {tanggal} Jam {Jam}",
                settings.EMAIL_HOST_USER,
                email_list,
                fail_silently=False,
            )

            return redirect("../proposalget")
    else:
        form = ProposalForm()
    return render(request, 'bimbingan/proposal_create.html', {"form": form, "user_info": user_info})
# checkpoint :proposal  read

# Proposal:read
# Proposal Untuk data 5 tahun kebelakang tanpa filter
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_5_years(request):
    user_info = user_information(request)
    get_year =datetime.datetime.now().year
    list_5_year=[]
    for item in range (5):
        list_5_year.append(get_year)
        get_year=get_year-1
    # print(list_5_year)
    if user_info[2].name == "Mahasiswa":
        try:
            proposals = proposal.objects.filter(tanggal_update__year__in=list_5_year).filter(
                nim=mahasiswa.objects.filter(pk=user_info[0])[0])
        except:
            proposals = []
        jumlah = 0
        for item in proposals:
            # print(item)
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
            jumlah += 1
        for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status != "ACC":
                proposals=proposals.exclude(id_proposal=item.id_proposal)

    else:
        proposals = proposal.objects.filter(tanggal_update__year__in=list_5_year)
        jumlah = 0
        for item in proposals:
            # print(item)
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
           
            jumlah += 1
        for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status != "ACC":
                proposals=proposals.exclude(id_proposal=item.id_proposal)
    jumlah=0
    for item in proposals:
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                    proposals[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    proposals[jumlah].status_nilai = "Belum Di Nilai"

            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1
   
        # for i in proposals:
        #     print(i.status)
    # print(usulantopiks)
    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals, "user_info": user_info})
# Proposal Untuk data 5 tahun kebelakang dengan filter proposal awal
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_5_years_proposal(request):
    user_info = user_information(request)
    get_year =datetime.datetime.now().year
    list_5_year=[]
    for item in range (5):
        list_5_year.append(get_year)
        get_year=get_year-1
    # print(list_5_year)
    if user_info[2].name == "Mahasiswa":
        try:
            proposals = proposal.objects.filter(nama_tahap="Proposal Awal (Revisi Seminar Proposal)").filter(tanggal_update__year__in=list_5_year).filter(
                nim=mahasiswa.objects.filter(pk=user_info[0])[0])
        except:
            proposals = []
        jumlah = 0
        for item in proposals:
            # print(item)
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
           
            jumlah += 1
        for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status != "ACC":
                proposals=proposals.exclude(id_proposal=item.id_proposal)

    else:
        proposals = proposal.objects.filter(nama_tahap="Proposal Awal (Revisi Seminar Proposal)").filter(tanggal_update__year__in=list_5_year)
        jumlah = 0
        for item in proposals:
            # print(item)
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
           
            jumlah += 1
        for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status != "ACC":
                proposals=proposals.exclude(id_proposal=item.id_proposal)
    jumlah=0
    for item in proposals:
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                    proposals[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    proposals[jumlah].status_nilai = "Belum Di Nilai"

            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1
   
        # for i in proposals:
        #     print(i.status)
    # print(usulantopiks)
    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals, "user_info": user_info})

# Proposal Untuk data 5 tahun kebelakang dengan filter Laporan Akhir
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_5_years_hasil(request):
    user_info = user_information(request)
    get_year =datetime.datetime.now().year
    list_5_year=[]
    for item in range (5):
        list_5_year.append(get_year)
        get_year=get_year-1
    # print(list_5_year)
    if user_info[2].name == "Mahasiswa":
        try:
            proposals = proposal.objects.filter(nama_tahap="Laporan Akhir (Revisi Seminar Hasil)").filter(tanggal_update__year__in=list_5_year).filter(
                nim=mahasiswa.objects.filter(pk=user_info[0])[0])
        except:
            proposals = []
        jumlah = 0
        for item in proposals:
            # print(item)
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
           
            jumlah += 1
        for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status != "ACC":
                proposals=proposals.exclude(id_proposal=item.id_proposal)

    else:
        proposals = proposal.objects.filter(nama_tahap="Laporan Akhir (Revisi Seminar Hasil)").filter(tanggal_update__year__in=list_5_year)
        jumlah = 0
        for item in proposals:
            # print(item)
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
           
            jumlah += 1
        for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status != "ACC":
                proposals=proposals.exclude(id_proposal=item.id_proposal)
    jumlah=0
    for item in proposals:
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                    proposals[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    proposals[jumlah].status_nilai = "Belum Di Nilai"

            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1
   
        # for i in proposals:
        #     print(i.status)
    # print(usulantopiks)
    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals, "user_info": user_info})

# Proposal tanpa filter
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Mahasiswa','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get(request):
    user_info = user_information(request)

    if user_info[2].name == "Mahasiswa":
        try:
            proposals = proposal.objects.filter(
                nim=mahasiswa.objects.filter(pk=user_info[0])[0])
        except:
            proposals = []
        jumlah = 0
        for item in proposals:
            # print(item)
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
           
            jumlah += 1

    else:
        proposals = proposal.objects.all()
        jumlah = 0
        for item in proposals:
            # print(item)
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
           
            jumlah += 1
    jumlah=0
    for item in proposals:
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                    proposals[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    proposals[jumlah].status_nilai = "Belum Di Nilai"

            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1
    
        # for i in proposals:
        #     print(i.status)
    # print(usulantopiks)
    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals, "user_info": user_info})



# newtodo
# Proposal:read
# Untuk melihat list proposal difilter   acc dari nim untuk mhasiswa 
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Mahasiswa','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_filter_ACC(request):
    user_info = user_information(request)

    if user_info[2].name == "Mahasiswa":
        try:
            proposals = proposal.objects.filter(
                nim=mahasiswa.objects.filter(pk=user_info[0])[0])
        except:
            proposals = []
        jumlah = 0
        for item in proposals:
            # print(item)
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item).last()
                proposals[jumlah].status = get_object.status_bimbingan

            except:
                proposals[jumlah].status = "Belum Diperiksa"
           
            jumlah += 1

    else:
        proposals = proposal.objects.all()
        jumlah = 0
        for item in proposals:
            # print(item)
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item).last()
                proposals[jumlah].status = get_object.status_bimbingan

            except:
                proposals[jumlah].status = "Belum Diperiksa"
           
            jumlah += 1
    for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status != "ACC":
                proposals=proposals.exclude(id_proposal=item.id_proposal)
                
    jumlah=0
    for item in proposals:
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                    proposals[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    proposals[jumlah].status_nilai = "Belum Di Nilai"

            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item).last()
                proposals[jumlah].status = get_object.status_bimbingan

            except:
                proposals[jumlah].status = "Belum Diperiksa"
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1
            

    

        # for i in proposals:
        #     print(i.status)
    # print(usulantopiks)
    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals, "user_info": user_info})
# Proposal  dengan filter proposal awal
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_filter_sempro(request):
    user_info = user_information(request)
    tabel="Seminar Proposal"
    
    list_jadwal_sempro=list(jadwal_seminar.objects.filter(tahap_seminar="Seminar Proposal").values_list("mahasiswa",flat=True))
    list_jadwal_sempro = list(filter(lambda x: x is not None and x != '', list_jadwal_sempro))

    role_dosen_filter=roledosen.objects.filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(role="Penguji Seminar Proposal 2")
    
    cek_jumlah_sempro=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC")
    
    detail_penilaian_lulus=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(status_kelulusan="Lulus")
    list_detailpenilaian_lulus=list(detail_penilaian_lulus.values_list("id_role_dosen__nim__nim",flat=True))
    
    cek_jumlah_sempro=cek_jumlah_sempro.exclude(id_proposal__nim__nim__in=list_detailpenilaian_lulus)
    
    
    detail_penilaian_tdk_lulus=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(status_kelulusan="Tidak Lulus")
    list_detailpenilaian_tdk_lulus=list(detail_penilaian_tdk_lulus.values_list("id_role_dosen__nim__nim",flat=True))
    detailpenilaian_tdk_lulus_count=detail_penilaian_tdk_lulus.values("id_role_dosen__nim__nim").annotate(nim_count=Count('id_role_dosen__nim__nim'))
    # print(detailpenilaian_tdk_lulus_count)
    
    cek_sempro_tidak_lulus=cek_jumlah_sempro.filter(id_proposal__nim__nim__in=list_detailpenilaian_tdk_lulus)
    list_cek_sempro_tidak_lulus=list(cek_sempro_tidak_lulus.values_list("id_proposal__nim__nim",flat=True))
    roledosen_tidak_lulus=role_dosen_filter.filter(nim__nim__in=list_cek_sempro_tidak_lulus)
    roledosen_data_tidak_lulus=roledosen_tidak_lulus.values("nim__nim").annotate(jumlah_role_dosen=Count('nim__nim'))
    
    
    jumlah=0
    for item in cek_sempro_tidak_lulus:
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item.id_proposal).last()
                cek_sempro_tidak_lulus[jumlah].status = get_object.status_bimbingan

            except:
                cek_sempro_tidak_lulus[jumlah].status = "Belum Diperiksa"
            jumlah += 1
            
    for item in cek_sempro_tidak_lulus: 
            # print(item.status, item.status == "ACC")
            if item.status != "ACC":
                cek_sempro_tidak_lulus=cek_sempro_tidak_lulus.exclude(id_proposal=item.id_proposal)    
            
    jumlah=0
    for item in cek_sempro_tidak_lulus:
        try : 
            abc_filtered = {d['id_role_dosen__nim__nim']: d for d in detailpenilaian_tdk_lulus_count if d['id_role_dosen__nim__nim'] == item.id_proposal.nim.nim}
            def_filtered = {d['nim__nim']: d for d in roledosen_data_tidak_lulus if d['nim__nim'] == item.id_proposal.nim.nim}
            # print(abc_filtered[item.id_proposal.nim.nim])
            # print(def_filtered[item.id_proposal.nim.nim])
            if abc_filtered and def_filtered:
                nim_count = abc_filtered[item.id_proposal.nim.nim]['nim_count']
                jumlah_role_dosen = def_filtered[item.id_proposal.nim.nim]['jumlah_role_dosen']

                if jumlah_role_dosen == (nim_count*2)+2:
                    # print("a")
                    cek_sempro_tidak_lulus[jumlah].status_dosen=f"Sudah Mencukupi : {nim_count*2} Assign Dosen"
                    # print(f"Nilai count untuk nim {filter_nim} sama.")
                else:
                    # print("b")
                    cek_sempro_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : {jumlah_role_dosen} Assign Dosen, Kurang Assign : {(nim_count*2)-jumlah_role_dosen} Dosen"
                    # print(f"Nilai count untuk nim {filter_nim} berbeda.")
            else:
                # print("c")
                cek_sempro_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : 0 Assign Dosen"
                # print(f"Nim {filter_nim} tidak ditemukan di kedua daftar.")
        except :
                cek_sempro_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : 0 Assign Dosen"
            
            
        jumlah+=1
    
    for item in cek_sempro_tidak_lulus:
        if item.status_dosen.startswith("Sudah Mencukupi"):
            cek_sempro_tidak_lulus=cek_sempro_tidak_lulus.exclude(id_proposal=item.id_proposal)
    
    jumlah=0
    for item in cek_sempro_tidak_lulus:
            try : 
                abc_filtered = {d['id_role_dosen__nim__nim']: d for d in detailpenilaian_tdk_lulus_count if d['id_role_dosen__nim__nim'] == item.id_proposal.nim.nim}
                def_filtered = {d['nim__nim']: d for d in roledosen_data_tidak_lulus if d['nim__nim'] == item.id_proposal.nim.nim}
                # print(abc_filtered[item.id_proposal.nim.nim])
                # print(def_filtered[item.id_proposal.nim.nim])
                if abc_filtered and def_filtered:
                    nim_count = abc_filtered[item.id_proposal.nim.nim]['nim_count']
                    jumlah_role_dosen = def_filtered[item.id_proposal.nim.nim]['jumlah_role_dosen']

                    if jumlah_role_dosen == (nim_count*2)+2:
                        # print("a")
                        cek_sempro_tidak_lulus[jumlah].status_dosen=f"Sudah Mencukupi : {nim_count*2} Assign Dosen"
                        # print(f"Nilai count untuk nim {filter_nim} sama.")
                    else:
                        # print("b")
                        cek_sempro_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : {jumlah_role_dosen} Assign Dosen, Kurang Assign : {((nim_count*2)+2)-jumlah_role_dosen} Dosen"
                        # print(f"Nilai count untuk nim {filter_nim} berbeda.")
                else:
                    # print("c")
                    cek_sempro_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : 0 Assign Dosen"
                    # print(f"Nim {filter_nim} tidak ditemukan di kedua daftar.")
            except :
                    cek_sempro_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : 0 Assign Dosen"
            
            try:
                if item.id_proposal.nim.nim in list_jadwal_sempro:
                    cek_sempro_tidak_lulus[jumlah].status_jadwal="Sudah Assign Jadwal"
                else :
                    cek_sempro_tidak_lulus[jumlah].status_jadwal="Belum Assign Jadwal"
            except :     
                    cek_sempro_tidak_lulus[jumlah].status_jadwal="Belum Assign Jadwal"
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.id_proposal.nim).exists():
                    cek_sempro_tidak_lulus[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    cek_sempro_tidak_lulus[jumlah].status_nilai = "Belum Di Nilai"

            except:
                cek_sempro_tidak_lulus[jumlah].status_nilai = "Belum Di Nilai"
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item.id_proposal).last()
                cek_sempro_tidak_lulus[jumlah].status = get_object.status_bimbingan

            except:
                cek_sempro_tidak_lulus[jumlah].status = "Belum Diperiksa"
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                cek_sempro_tidak_lulus[jumlah].keterangan_dosen = get_object.catatan
            except:
                cek_sempro_tidak_lulus[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = proposal.objects.filter(nim=item.id_proposal.nim).filter(
                    nama_tahap="Proposal Awal").count()
                # print(get_object)
                cek_sempro_tidak_lulus[jumlah].jumlah_sempro = get_object
            except:
                cek_sempro_tidak_lulus[jumlah].jumlah_sempro = 0
            try:
                get_object = proposal.objects.filter(nim=item.id_proposal.nim).filter(
                    nama_tahap="Laporan Akhir").count()
                # print(get_object)
                cek_sempro_tidak_lulus[jumlah].jumlah_semhas = get_object
            except:
                cek_sempro_tidak_lulus[jumlah].jumlah_semhas = 0
            jumlah += 1
    
    
    lolos_tidak_lulus=cek_jumlah_sempro.exclude(id_proposal__nim__nim__in=list_detailpenilaian_tdk_lulus)
    # print(lolos_tidak_lulus)
    # print(cek_sempro_tidak_lulus)
    # lolos_tidak_lulus=lolos_tidak_lulus.filter()
    jumlah=0
    for item in lolos_tidak_lulus:
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item.id_proposal).last()
                lolos_tidak_lulus[jumlah].status = get_object.status_bimbingan

            except:
                lolos_tidak_lulus[jumlah].status = "Belum Diperiksa"
            jumlah += 1
            
    for item in lolos_tidak_lulus: 
            # print(item.status, item.status == "ACC")
            # print(item.status)
            if item.status != "ACC":
                lolos_tidak_lulus=lolos_tidak_lulus.exclude(id_proposal=item.id_proposal)
    
    jumlah=0
    for item in lolos_tidak_lulus:
        try : 
            roledosen_cek=role_dosen_filter.filter(nim=item.id_proposal.nim).count()
            if roledosen_cek==2 :
                lolos_tidak_lulus[jumlah].status_dosen="Sudah Mencukupi : 2 Assign Dosen"
            elif roledosen_cek==1 :
                lolos_tidak_lulus[jumlah].status_dosen="Belum Mencukupi : 1 Assign Dosen"
            else: 
                lolos_tidak_lulus[jumlah].status_dosen="Belum Mencukupi : 0 Assign Dosen"
                
        except :
                lolos_tidak_lulus[jumlah].status_dosen="Belum Mencukupi : 0 Assign Dosen" 
        jumlah+=1
    
    for item in lolos_tidak_lulus:
        if item.status_dosen.startswith("Sudah Mencukupi"):
            lolos_tidak_lulus=lolos_tidak_lulus.exclude(id_proposal=item.id_proposal)
    
    
    jumlah=0
    for item in lolos_tidak_lulus:
            try : 
                roledosen_cek=role_dosen_filter.filter(nim=item.id_proposal.nim).count()
                if roledosen_cek==2 :
                    lolos_tidak_lulus[jumlah].status_dosen="Sudah Mencukupi : 2 Assign Dosen"
                elif roledosen_cek==1 :
                    lolos_tidak_lulus[jumlah].status_dosen="Belum Mencukupi : 1 Assign Dosen"
                else: 
                    lolos_tidak_lulus[jumlah].status_dosen="Belum Mencukupi : 0 Assign Dosen"
                    
            except :
                    lolos_tidak_lulus[jumlah].status_dosen="Belum Mencukupi : 0 Assign Dosen" 
                    
            try:
                if item.id_proposal.nim.nim in list_jadwal_sempro:
                    lolos_tidak_lulus[jumlah].status_jadwal="Sudah Assign Jadwal"
                else :
                    lolos_tidak_lulus[jumlah].status_jadwal="Belum Assign Jadwal"
            except :     
                    lolos_tidak_lulus[jumlah].status_jadwal="Belum Assign Jadwal"
                    
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.id_proposal.nim).exists():
                    lolos_tidak_lulus[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    lolos_tidak_lulus[jumlah].status_nilai = "Belum Di Nilai"

            except:
                lolos_tidak_lulus[jumlah].status_nilai = "Belum Di Nilai"
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item.id_proposal).last()
                lolos_tidak_lulus[jumlah].status = get_object.status_bimbingan

            except:
                lolos_tidak_lulus[jumlah].status = "Belum Diperiksa"
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                lolos_tidak_lulus[jumlah].keterangan_dosen = get_object.catatan
            except:
                lolos_tidak_lulus[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = proposal.objects.filter(nim=item.id_proposal.nim).filter(
                    nama_tahap="Proposal Awal").count()
                # print(get_object)
                lolos_tidak_lulus[jumlah].jumlah_sempro = get_object
            except:
                lolos_tidak_lulus[jumlah].jumlah_sempro = 0
            try:
                get_object = proposal.objects.filter(nim=item.id_proposal.nim).filter(
                    nama_tahap="Laporan Akhir").count()
                # print(get_object)
                lolos_tidak_lulus[jumlah].jumlah_semhas = get_object
            except:
                lolos_tidak_lulus[jumlah].jumlah_semhas = 0
            jumlah += 1
            

    
    # print(lolos_tidak_lulus)
    # print(cek_sempro_tidak_lulus)
        # for i in proposals:
        #     print(i.status)
    # print(usulantopiks)
    return render(request, 'bimbingan/filter_seminar.html', {"proposals": lolos_tidak_lulus,"proposals2": cek_sempro_tidak_lulus, "user_info": user_info,"tabel":tabel})


# Proposal Untuk filter beluma ada jadwal seminar proposal awal
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_filter_sempro_jadwal(request):
    user_info = user_information(request)
    tabel="Seminar Proposal"
    
    list_jadwal_sempro=list(jadwal_seminar.objects.filter(tahap_seminar="Seminar Proposal").values_list("mahasiswa",flat=True))
    print(list_jadwal_sempro)
    list_jadwal_sempro = list(filter(lambda x: x is not None and x != '', list_jadwal_sempro))
    role_dosen_filter=roledosen.objects.filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(role="Penguji Seminar Proposal 2")
    
    cek_jumlah_sempro=bimbingan.objects.filter(id_proposal__nama_tahap="Proposal Awal").filter(status_bimbingan="ACC")
    detail_penilaian_lulus=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(status_kelulusan="Lulus")
    list_detailpenilaian_lulus=list(detail_penilaian_lulus.values_list("id_role_dosen__nim__nim",flat=True))
    # print(detail_penilaian_lulus)
    
    cek_jumlah_sempro=cek_jumlah_sempro.exclude(id_proposal__nim__nim__in=list_detailpenilaian_lulus)
    
    
    detail_penilaian_tdk_lulus=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(status_kelulusan="Tidak Lulus")
    list_detailpenilaian_tdk_lulus=list(detail_penilaian_tdk_lulus.values_list("id_role_dosen__nim__nim",flat=True))
    detailpenilaian_tdk_lulus_count=detail_penilaian_tdk_lulus.values("id_role_dosen__nim__nim").annotate(nim_count=Count('id_role_dosen__nim__nim'))
    # print(detailpenilaian_tdk_lulus_count)
    
    cek_sempro_tidak_lulus=cek_jumlah_sempro.filter(id_proposal__nim__nim__in=list_detailpenilaian_tdk_lulus)
    list_cek_sempro_tidak_lulus=list(cek_sempro_tidak_lulus.values_list("id_proposal__nim__nim",flat=True))
    roledosen_tidak_lulus=role_dosen_filter.filter(nim__nim__in=list_cek_sempro_tidak_lulus)
    roledosen_data_tidak_lulus=roledosen_tidak_lulus.values("nim__nim").annotate(jumlah_role_dosen=Count('nim__nim'))
    # print(cek_sempro_tidak_lulus)
    jumlah=0
    for item in cek_sempro_tidak_lulus:
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item.id_proposal).last()
                cek_sempro_tidak_lulus[jumlah].status = get_object.status_bimbingan

            except:
                cek_sempro_tidak_lulus[jumlah].status = "Belum Diperiksa"
            jumlah += 1
            
    for item in cek_sempro_tidak_lulus: 
            # print(item.status, item.status == "ACC")
            if item.status != "ACC":
                cek_sempro_tidak_lulus=cek_sempro_tidak_lulus.exclude(id_proposal=item.id_proposal) 
    jumlah=0
    for item in cek_sempro_tidak_lulus:
        try:
            if item.id_proposal.nim.nim in list_jadwal_sempro:
                cek_sempro_tidak_lulus[jumlah].status_jadwal="Sudah Assign Jadwal"
            else :
                cek_sempro_tidak_lulus[jumlah].status_jadwal="Belum Assign Jadwal"
        except :     
                cek_sempro_tidak_lulus[jumlah].status_jadwal="Belum Assign Jadwal"
            
            
        jumlah+=1
    
    for item in cek_sempro_tidak_lulus:
        if item.status_jadwal=="Sudah Assign Jadwal":
            cek_sempro_tidak_lulus=cek_sempro_tidak_lulus.exclude(id_proposal=item.id_proposal)
    
    jumlah=0
    for item in cek_sempro_tidak_lulus:
            try : 
                abc_filtered = {d['id_role_dosen__nim__nim']: d for d in detailpenilaian_tdk_lulus_count if d['id_role_dosen__nim__nim'] == item.id_proposal.nim.nim}
                def_filtered = {d['nim__nim']: d for d in roledosen_data_tidak_lulus if d['nim__nim'] == item.id_proposal.nim.nim}
                # print(abc_filtered[item.id_proposal.nim.nim])
                # print(def_filtered[item.id_proposal.nim.nim])
                if abc_filtered and def_filtered:
                    nim_count = abc_filtered[item.id_proposal.nim.nim]['nim_count']
                    jumlah_role_dosen = def_filtered[item.id_proposal.nim.nim]['jumlah_role_dosen']

                    if jumlah_role_dosen == (nim_count*2)+2:
                        # print("a")
                        cek_sempro_tidak_lulus[jumlah].status_dosen=f"Sudah Mencukupi : {nim_count*2} Assign Dosen"
                        # print(f"Nilai count untuk nim {filter_nim} sama.")
                    else:
                        # print("b")
                        cek_sempro_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : {jumlah_role_dosen} Assign Dosen, Kurang Assign : {((nim_count*2)+2)-jumlah_role_dosen} Dosen"
                        # print(f"Nilai count untuk nim {filter_nim} berbeda.")
                else:
                    # print("c")
                    cek_sempro_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : 0 Assign Dosen"
                    # print(f"Nim {filter_nim} tidak ditemukan di kedua daftar.")
            except :
                    cek_sempro_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : 0 Assign Dosen"
            
            try:
                if item.id_proposal.nim.nim in list_jadwal_sempro:
                    cek_sempro_tidak_lulus[jumlah].status_jadwal="Sudah Assign Jadwal"
                else :
                    cek_sempro_tidak_lulus[jumlah].status_jadwal="Belum Assign Jadwal"
            except :     
                    cek_sempro_tidak_lulus[jumlah].status_jadwal="Belum Assign Jadwal"
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.id_proposal.nim).exists():
                    cek_sempro_tidak_lulus[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    cek_sempro_tidak_lulus[jumlah].status_nilai = "Belum Di Nilai"

            except:
                cek_sempro_tidak_lulus[jumlah].status_nilai = "Belum Di Nilai"
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item.id_proposal).last()
                cek_sempro_tidak_lulus[jumlah].status = get_object.status_bimbingan

            except:
                cek_sempro_tidak_lulus[jumlah].status = "Belum Diperiksa"
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                cek_sempro_tidak_lulus[jumlah].keterangan_dosen = get_object.catatan
            except:
                cek_sempro_tidak_lulus[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = proposal.objects.filter(nim=item.id_proposal.nim).filter(
                    nama_tahap="Proposal Awal").count()
                # print(get_object)
                cek_sempro_tidak_lulus[jumlah].jumlah_sempro = get_object
            except:
                cek_sempro_tidak_lulus[jumlah].jumlah_sempro = 0
            try:
                get_object = proposal.objects.filter(nim=item.id_proposal.nim).filter(
                    nama_tahap="Laporan Akhir").count()
                # print(get_object)
                cek_sempro_tidak_lulus[jumlah].jumlah_semhas = get_object
            except:
                cek_sempro_tidak_lulus[jumlah].jumlah_semhas = 0
            jumlah += 1
    
    
    lolos_tidak_lulus=cek_jumlah_sempro.exclude(id_proposal__nim__nim__in=list_detailpenilaian_tdk_lulus)
    # print(lolos_tidak_lulus)
    jumlah=0
    for item in lolos_tidak_lulus:

            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item.id_proposal).last()
                lolos_tidak_lulus[jumlah].status = get_object.status_bimbingan

            except:
                # print("a")
                lolos_tidak_lulus[jumlah].status = "Belum Diperiksa"
            jumlah += 1
            
    for item in lolos_tidak_lulus: 
            # print(item.status, item.status == "ACC")
            # print(item.status)
            if item.status != "ACC":
                lolos_tidak_lulus=lolos_tidak_lulus.exclude(id_proposal=item.id_proposal)
    # lolos_tidak_lulus=lolos_tidak_lulus.filter()
    jumlah=0
    for item in lolos_tidak_lulus:
        try:

            if item.id_proposal.nim.nim in list_jadwal_sempro:
                lolos_tidak_lulus[jumlah].status_jadwal="Sudah Assign Jadwal"
            else :
                lolos_tidak_lulus[jumlah].status_jadwal="Belum Assign Jadwal"
        except :     
        #         lolos_tidak_lulus[jumlah].status_jadwal="Belum Assign Jadwal"
            jumlah+=1
    
    for item in lolos_tidak_lulus:
        if item.status_jadwal=="Sudah Assign Jadwal":
            lolos_tidak_lulus=lolos_tidak_lulus.exclude(id_proposal=item.id_proposal)
    
    # print(lolos_tidak_lulus)
    jumlah=0
    for item in lolos_tidak_lulus:
            try : 
                roledosen_cek=role_dosen_filter.filter(nim=item.id_proposal.nim).count()
                if roledosen_cek==2 :
                    lolos_tidak_lulus[jumlah].status_dosen="Sudah Mencukupi : 2 Assign Dosen"
                elif roledosen_cek==1 :
                    lolos_tidak_lulus[jumlah].status_dosen="Belum Mencukupi : 1 Assign Dosen"
                else: 
                    lolos_tidak_lulus[jumlah].status_dosen="Belum Mencukupi : 0 Assign Dosen"
                    
            except :
                    lolos_tidak_lulus[jumlah].status_dosen="Belum Mencukupi : 0 Assign Dosen" 
                    
            try:
                if item.id_proposal.nim.nim in list_jadwal_sempro:
                    lolos_tidak_lulus[jumlah].status_jadwal="Sudah Assign Jadwal"
                else :
                    lolos_tidak_lulus[jumlah].status_jadwal="Belum Assign Jadwal"
            except :     
                    lolos_tidak_lulus[jumlah].status_jadwal="Belum Assign Jadwal"
                    
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.id_proposal.nim).exists():
                    lolos_tidak_lulus[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    lolos_tidak_lulus[jumlah].status_nilai = "Belum Di Nilai"

            except:
                lolos_tidak_lulus[jumlah].status_nilai = "Belum Di Nilai"
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item.id_proposal).last()
                lolos_tidak_lulus[jumlah].status = get_object.status_bimbingan

            except:
                lolos_tidak_lulus[jumlah].status = "Belum Diperiksa"
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                lolos_tidak_lulus[jumlah].keterangan_dosen = get_object.catatan
            except:
                lolos_tidak_lulus[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = proposal.objects.filter(nim=item.id_proposal.nim).filter(
                    nama_tahap="Proposal Awal").count()
                # print(get_object)
                lolos_tidak_lulus[jumlah].jumlah_sempro = get_object
            except:
                lolos_tidak_lulus[jumlah].jumlah_sempro = 0
            try:
                get_object = proposal.objects.filter(nim=item.id_proposal.nim).filter(
                    nama_tahap="Laporan Akhir").count()
                # print(get_object)
                lolos_tidak_lulus[jumlah].jumlah_semhas = get_object
            except:
                lolos_tidak_lulus[jumlah].jumlah_semhas = 0
            jumlah += 1
            

    

        # for i in proposals:
        #     print(i.status)
    # print(usulantopiks)
    return render(request, 'bimbingan/filter_seminar.html', {"proposals": lolos_tidak_lulus,"proposals2": cek_sempro_tidak_lulus, "user_info": user_info,"tabel":tabel})

# Proposal  dengan filter Laporan Akhir
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_filter_semhas(request):
    user_info = user_information(request)
    tabel="Seminar Hasil"
    
    list_jadwal_semhas=list(jadwal_seminar.objects.filter(tahap_seminar="Seminar Hasil").values_list("mahasiswa",flat=True))
    list_jadwal_semhas = list(filter(lambda x: x is not None and x != '', list_jadwal_semhas))
    role_dosen_filter_semhas=roledosen.objects.filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(role="Penguji Seminar Hasil 2")
    
    cek_jumlah_semhas=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC")
    
    detail_penilaian_lulus_semhas=detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(status_kelulusan="Lulus")
    list_detailpenilaian_lulus_semhas=list(detail_penilaian_lulus_semhas.values_list("id_role_dosen__nim__nim",flat=True))
    
    cek_jumlah_semhas=cek_jumlah_semhas.exclude(id_proposal__nim__nim__in=list_detailpenilaian_lulus_semhas)
    
    
    detail_penilaian_tdk_lulus_semhas=detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(status_kelulusan="Tidak Lulus")
    list_detailpenilaian_tdk_lulus_semhas=list(detail_penilaian_tdk_lulus_semhas.values_list("id_role_dosen__nim__nim",flat=True))
    detailpenilaian_tdk_lulus_count_semhas=detail_penilaian_tdk_lulus_semhas.values("id_role_dosen__nim__nim").annotate(nim_count=Count('id_role_dosen__nim__nim'))
    # print(detailpenilaian_tdk_lulus_count)
    
    cek_semhas_tidak_lulus=cek_jumlah_semhas.filter(id_proposal__nim__nim__in=list_detailpenilaian_tdk_lulus_semhas)
    list_cek_sempro_tidak_lulus_semhas=list(cek_semhas_tidak_lulus.values_list("id_proposal__nim__nim",flat=True))
    roledosen_tidak_lulus_semhas=role_dosen_filter_semhas.filter(nim__nim__in=list_cek_sempro_tidak_lulus_semhas)
    roledosen_data_tidak_lulus_semhas=roledosen_tidak_lulus_semhas.values("nim__nim").annotate(jumlah_role_dosen=Count('nim__nim'))
    
    
    jumlah=0
    for item in cek_semhas_tidak_lulus:
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item.id_proposal).last()
                cek_semhas_tidak_lulus[jumlah].status = get_object.status_bimbingan

            except:
                cek_semhas_tidak_lulus[jumlah].status = "Belum Diperiksa"
            jumlah += 1
            
    for item in cek_semhas_tidak_lulus: 
            # print(item.status, item.status == "ACC")
            if item.status != "ACC":
                cek_semhas_tidak_lulus=cek_semhas_tidak_lulus.exclude(id_proposal=item.id_proposal)    
            
    jumlah=0
    for item in cek_semhas_tidak_lulus:
        try : 
            abc_filtered = {d['id_role_dosen__nim__nim']: d for d in detailpenilaian_tdk_lulus_count_semhas if d['id_role_dosen__nim__nim'] == item.id_proposal.nim.nim}
            def_filtered = {d['nim__nim']: d for d in roledosen_data_tidak_lulus_semhas if d['nim__nim'] == item.id_proposal.nim.nim}
            # print(abc_filtered[item.id_proposal.nim.nim])
            # print(def_filtered[item.id_proposal.nim.nim])
            if abc_filtered and def_filtered:
                nim_count = abc_filtered[item.id_proposal.nim.nim]['nim_count']
                jumlah_role_dosen = def_filtered[item.id_proposal.nim.nim]['jumlah_role_dosen']

                if jumlah_role_dosen == (nim_count*2)+2:
                    # print("a")
                    cek_semhas_tidak_lulus[jumlah].status_dosen=f"Sudah Mencukupi : {nim_count*2} Assign Dosen"
                    # print(f"Nilai count untuk nim {filter_nim} sama.")
                else:
                    # print("b")
                    cek_semhas_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : {jumlah_role_dosen} Assign Dosen, Kurang Assign : {(nim_count*2)-jumlah_role_dosen} Dosen"
                    # print(f"Nilai count untuk nim {filter_nim} berbeda.")
            else:
                # print("c")
                cek_semhas_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : 0 Assign Dosen"
                # print(f"Nim {filter_nim} tidak ditemukan di kedua daftar.")
        except :
                cek_semhas_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : 0 Assign Dosen"
            
            
        jumlah+=1
    
    for item in cek_semhas_tidak_lulus:
        if item.status_dosen.startswith("Sudah Mencukupi"):
            cek_semhas_tidak_lulus=cek_semhas_tidak_lulus.exclude(id_proposal=item.id_proposal)
    
    jumlah=0
    for item in cek_semhas_tidak_lulus:
            try : 
                abc_filtered = {d['id_role_dosen__nim__nim']: d for d in detailpenilaian_tdk_lulus_count_semhas if d['id_role_dosen__nim__nim'] == item.id_proposal.nim.nim}
                def_filtered = {d['nim__nim']: d for d in roledosen_data_tidak_lulus_semhas if d['nim__nim'] == item.id_proposal.nim.nim}
                # print(abc_filtered[item.id_proposal.nim.nim])
                # print(def_filtered[item.id_proposal.nim.nim])
                if abc_filtered and def_filtered:
                    nim_count = abc_filtered[item.id_proposal.nim.nim]['nim_count']
                    jumlah_role_dosen = def_filtered[item.id_proposal.nim.nim]['jumlah_role_dosen']

                    if jumlah_role_dosen == (nim_count*2)+2:
                        # print("a")
                        cek_semhas_tidak_lulus[jumlah].status_dosen=f"Sudah Mencukupi : {nim_count*2} Assign Dosen"
                        # print(f"Nilai count untuk nim {filter_nim} sama.")
                    else:
                        # print("b")
                        cek_semhas_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : {jumlah_role_dosen} Assign Dosen, Kurang Assign : {((nim_count*2)+2)-jumlah_role_dosen} Dosen"
                        # print(f"Nilai count untuk nim {filter_nim} berbeda.")
                else:
                    # print("c")
                    cek_semhas_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : 0 Assign Dosen"
                    # print(f"Nim {filter_nim} tidak ditemukan di kedua daftar.")
            except :
                    cek_semhas_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : 0 Assign Dosen"
            
            try:
                if item.id_proposal.nim.nim in list_jadwal_semhas:
                    cek_semhas_tidak_lulus[jumlah].status_jadwal="Sudah Assign Jadwal"
                else :
                    cek_semhas_tidak_lulus[jumlah].status_jadwal="Belum Assign Jadwal"
            except :     
                    cek_semhas_tidak_lulus[jumlah].status_jadwal="Belum Assign Jadwal"
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.id_proposal.nim).exists():
                    cek_semhas_tidak_lulus[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    cek_semhas_tidak_lulus[jumlah].status_nilai = "Belum Di Nilai"

            except:
                cek_semhas_tidak_lulus[jumlah].status_nilai = "Belum Di Nilai"
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item.id_proposal).last()
                cek_semhas_tidak_lulus[jumlah].status = get_object.status_bimbingan

            except:
                cek_semhas_tidak_lulus[jumlah].status = "Belum Diperiksa"
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                cek_semhas_tidak_lulus[jumlah].keterangan_dosen = get_object.catatan
            except:
                cek_semhas_tidak_lulus[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = proposal.objects.filter(nim=item.id_proposal.nim).filter(
                    nama_tahap="Proposal Awal").count()
                # print(get_object)
                cek_semhas_tidak_lulus[jumlah].jumlah_sempro = get_object
            except:
                cek_semhas_tidak_lulus[jumlah].jumlah_sempro = 0
            try:
                get_object = proposal.objects.filter(nim=item.id_proposal.nim).filter(
                    nama_tahap="Laporan Akhir").count()
                # print(get_object)
                cek_semhas_tidak_lulus[jumlah].jumlah_semhas = get_object
            except:
                cek_semhas_tidak_lulus[jumlah].jumlah_semhas = 0
            jumlah += 1
    
    
    lolos_tidak_lulus_semhas=cek_jumlah_semhas.exclude(id_proposal__nim__nim__in=list_detailpenilaian_tdk_lulus_semhas)
    # print(lolos_tidak_lulus_semhas)
    # print(cek_sempro_tidak_lulus)
    # lolos_tidak_lulus_semhas=lolos_tidak_lulus_semhas.filter()
    jumlah=0
    for item in lolos_tidak_lulus_semhas:
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item.id_proposal).last()
                lolos_tidak_lulus_semhas[jumlah].status = get_object.status_bimbingan

            except:
                lolos_tidak_lulus_semhas[jumlah].status = "Belum Diperiksa"
            jumlah += 1
            
    for item in lolos_tidak_lulus_semhas: 
            # print(item.status, item.status == "ACC")
            # print(item.status)
            if item.status != "ACC":
                lolos_tidak_lulus_semhas=lolos_tidak_lulus_semhas.exclude(id_proposal=item.id_proposal)
    
    jumlah=0
    for item in lolos_tidak_lulus_semhas:
        try : 
            roledosen_cek=role_dosen_filter_semhas.filter(nim=item.id_proposal.nim).count()
            # print("ini",roledosen_cek, type(roledosen_cek))
            if roledosen_cek==2 :
                # print("a")
                lolos_tidak_lulus_semhas[jumlah].status_dosen="Sudah Mencukupi : 2 Assign Dosen"
            elif roledosen_cek==1 :
                # print("b")
                lolos_tidak_lulus_semhas[jumlah].status_dosen="Belum Mencukupi : 1 Assign Dosen"
            else: 
                # print("c")
                lolos_tidak_lulus_semhas[jumlah].status_dosen="Belum Mencukupi : 0 Assign Dosen"
                
        except :
                # print("d")
                lolos_tidak_lulus_semhas[jumlah].status_dosen="Belum Mencukupi : 0 Assign Dosen" 
        jumlah+=1
    
    for item in lolos_tidak_lulus_semhas:
        if item.status_dosen.startswith("Sudah Mencukupi"):
            lolos_tidak_lulus_semhas=lolos_tidak_lulus_semhas.exclude(id_proposal=item.id_proposal)
    
    
    jumlah=0
    for item in lolos_tidak_lulus_semhas:
            try : 
                roledosen_cek=role_dosen_filter_semhas.filter(nim=item.id_proposal.nim).count()
                if roledosen_cek==2 :
                    lolos_tidak_lulus_semhas[jumlah].status_dosen="Sudah Mencukupi : 2 Assign Dosen"
                elif roledosen_cek==1 :
                    lolos_tidak_lulus_semhas[jumlah].status_dosen="Belum Mencukupi : 1 Assign Dosen"
                else: 
                    lolos_tidak_lulus_semhas[jumlah].status_dosen="Belum Mencukupi : 0 Assign Dosen"
                    
            except :
                    lolos_tidak_lulus_semhas[jumlah].status_dosen="Belum Mencukupi : 0 Assign Dosen" 
                    
            try:
                if item.id_proposal.nim.nim in list_jadwal_semhas:
                    lolos_tidak_lulus_semhas[jumlah].status_jadwal="Sudah Assign Jadwal"
                else :
                    lolos_tidak_lulus_semhas[jumlah].status_jadwal="Belum Assign Jadwal"
            except :     
                    lolos_tidak_lulus_semhas[jumlah].status_jadwal="Belum Assign Jadwal"
                    
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.id_proposal.nim).exists():
                    lolos_tidak_lulus_semhas[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    lolos_tidak_lulus_semhas[jumlah].status_nilai = "Belum Di Nilai"

            except:
                lolos_tidak_lulus_semhas[jumlah].status_nilai = "Belum Di Nilai"
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item.id_proposal).last()
                lolos_tidak_lulus_semhas[jumlah].status = get_object.status_bimbingan

            except:
                lolos_tidak_lulus_semhas[jumlah].status = "Belum Diperiksa"
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                lolos_tidak_lulus_semhas[jumlah].keterangan_dosen = get_object.catatan
            except:
                lolos_tidak_lulus_semhas[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = proposal.objects.filter(nim=item.id_proposal.nim).filter(
                    nama_tahap="Laporan Akhir").count()
                # print(get_object)
                lolos_tidak_lulus_semhas[jumlah].jumlah_sempro = get_object
            except:
                lolos_tidak_lulus_semhas[jumlah].jumlah_sempro = 0
            try:
                get_object = proposal.objects.filter(nim=item.id_proposal.nim).filter(
                    nama_tahap="Laporan Akhir").count()
                # print(get_object)
                lolos_tidak_lulus_semhas[jumlah].jumlah_semhas = get_object
            except:
                lolos_tidak_lulus_semhas[jumlah].jumlah_semhas = 0
            jumlah += 1
            

    
    # print(lolos_tidak_lulus)
    # print(cek_sempro_tidak_lulus)
        # for i in proposals:
        #     print(i.status)
    # print(usulantopiks)
    return render(request, 'bimbingan/filter_seminar.html', {"proposals": lolos_tidak_lulus_semhas,"proposals2": cek_semhas_tidak_lulus, "user_info": user_info,"tabel":tabel})


# Proposal Untuk  filter belum ada jadwal seminar Laporan Akhir
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_filter_semhas_jadwal(request):
    user_info = user_information(request)
    tabel="Seminar Hasil"
    
    list_jadwal_semhas=list(jadwal_seminar.objects.filter(tahap_seminar="Seminar Hasil").values_list("mahasiswa",flat=True))
    list_jadwal_semhas = list(filter(lambda x: x is not None and x != '', list_jadwal_semhas))
    role_dosen_filter_semhas=roledosen.objects.filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(role="Penguji Seminar Hasil 2")
    
    cek_jumlah_semhas=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir").filter(status_bimbingan="ACC")
    
    detail_penilaian_lulus_semhas=detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(status_kelulusan="Lulus")
    list_detailpenilaian_lulus_semhas=list(detail_penilaian_lulus_semhas.values_list("id_role_dosen__nim__nim",flat=True))
    
    cek_jumlah_semhas=cek_jumlah_semhas.exclude(id_proposal__nim__nim__in=list_detailpenilaian_lulus_semhas)
    
    
    detail_penilaian_tdk_lulus_semhas=detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(status_kelulusan="Tidak Lulus")
    list_detailpenilaian_tdk_lulus_semhas=list(detail_penilaian_tdk_lulus_semhas.values_list("id_role_dosen__nim__nim",flat=True))
    detailpenilaian_tdk_lulus_count_semhas=detail_penilaian_tdk_lulus_semhas.values("id_role_dosen__nim__nim").annotate(nim_count=Count('id_role_dosen__nim__nim'))
    # print(detailpenilaian_tdk_lulus_count)
    
    cek_semhas_tidak_lulus=cek_jumlah_semhas.filter(id_proposal__nim__nim__in=list_detailpenilaian_tdk_lulus_semhas)
    list_cek_sempro_tidak_lulus_semhas=list(cek_semhas_tidak_lulus.values_list("id_proposal__nim__nim",flat=True))
    roledosen_tidak_lulus_semhas=role_dosen_filter_semhas.filter(nim__nim__in=list_cek_sempro_tidak_lulus_semhas)
    roledosen_data_tidak_lulus_semhas=roledosen_tidak_lulus_semhas.values("nim__nim").annotate(jumlah_role_dosen=Count('nim__nim'))
    
    
    jumlah=0
    for item in cek_semhas_tidak_lulus:
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item.id_proposal).last()
                cek_semhas_tidak_lulus[jumlah].status = get_object.status_bimbingan

            except:
                cek_semhas_tidak_lulus[jumlah].status = "Belum Diperiksa"
            jumlah += 1
            
    for item in cek_semhas_tidak_lulus: 
            # print(item.status, item.status == "ACC")
            if item.status != "ACC":
                cek_semhas_tidak_lulus=cek_semhas_tidak_lulus.exclude(id_proposal=item.id_proposal)    
            
    jumlah=0
    for item in cek_semhas_tidak_lulus:
        try:
            if item.id_proposal.nim.nim in list_jadwal_semhas:
                cek_semhas_tidak_lulus[jumlah].status_jadwal="Sudah Assign Jadwal"
            else :
                cek_semhas_tidak_lulus[jumlah].status_jadwal="Belum Assign Jadwal"
        except :     
                cek_semhas_tidak_lulus[jumlah].status_jadwal="Belum Assign Jadwal"
            
            
        jumlah+=1
    
    for item in cek_semhas_tidak_lulus:
        if item.status_jadwal=="Sudah Assign Jadwal":
            cek_semhas_tidak_lulus=cek_semhas_tidak_lulus.exclude(id_proposal=item.id_proposal)
    jumlah=0
    for item in cek_semhas_tidak_lulus:
            try : 
                abc_filtered = {d['id_role_dosen__nim__nim']: d for d in detailpenilaian_tdk_lulus_count_semhas if d['id_role_dosen__nim__nim'] == item.id_proposal.nim.nim}
                def_filtered = {d['nim__nim']: d for d in roledosen_data_tidak_lulus_semhas if d['nim__nim'] == item.id_proposal.nim.nim}
                # print(abc_filtered[item.id_proposal.nim.nim])
                # print(def_filtered[item.id_proposal.nim.nim])
                if abc_filtered and def_filtered:
                    nim_count = abc_filtered[item.id_proposal.nim.nim]['nim_count']
                    jumlah_role_dosen = def_filtered[item.id_proposal.nim.nim]['jumlah_role_dosen']

                    if jumlah_role_dosen == (nim_count*2)+2:
                        # print("a")
                        cek_semhas_tidak_lulus[jumlah].status_dosen=f"Sudah Mencukupi : {nim_count*2} Assign Dosen"
                        # print(f"Nilai count untuk nim {filter_nim} sama.")
                    else:
                        # print("b")
                        cek_semhas_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : {jumlah_role_dosen} Assign Dosen, Kurang Assign : {((nim_count*2)+2)-jumlah_role_dosen} Dosen"
                        # print(f"Nilai count untuk nim {filter_nim} berbeda.")
                else:
                    # print("c")
                    cek_semhas_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : 0 Assign Dosen"
                    # print(f"Nim {filter_nim} tidak ditemukan di kedua daftar.")
            except :
                    cek_semhas_tidak_lulus[jumlah].status_dosen=f"Belum Mencukupi : 0 Assign Dosen"
            
            try:
                if item.id_proposal.nim.nim in list_jadwal_semhas:
                    cek_semhas_tidak_lulus[jumlah].status_jadwal="Sudah Assign Jadwal"
                else :
                    cek_semhas_tidak_lulus[jumlah].status_jadwal="Belum Assign Jadwal"
            except :     
                    cek_semhas_tidak_lulus[jumlah].status_jadwal="Belum Assign Jadwal"
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.id_proposal.nim).exists():
                    cek_semhas_tidak_lulus[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    cek_semhas_tidak_lulus[jumlah].status_nilai = "Belum Di Nilai"

            except:
                cek_semhas_tidak_lulus[jumlah].status_nilai = "Belum Di Nilai"
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item.id_proposal).last()
                cek_semhas_tidak_lulus[jumlah].status = get_object.status_bimbingan

            except:
                cek_semhas_tidak_lulus[jumlah].status = "Belum Diperiksa"
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                cek_semhas_tidak_lulus[jumlah].keterangan_dosen = get_object.catatan
            except:
                cek_semhas_tidak_lulus[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = proposal.objects.filter(nim=item.id_proposal.nim).filter(
                    nama_tahap="Laporan Akhir").count()
                # print(get_object)
                cek_semhas_tidak_lulus[jumlah].jumlah_sempro = get_object
            except:
                cek_semhas_tidak_lulus[jumlah].jumlah_sempro = 0
            try:
                get_object = proposal.objects.filter(nim=item.id_proposal.nim).filter(
                    nama_tahap="Laporan Akhir").count()
                # print(get_object)
                cek_semhas_tidak_lulus[jumlah].jumlah_semhas = get_object
            except:
                cek_semhas_tidak_lulus[jumlah].jumlah_semhas = 0
            jumlah += 1
    
    
    lolos_tidak_lulus_semhas=cek_jumlah_semhas.exclude(id_proposal__nim__nim__in=list_detailpenilaian_tdk_lulus_semhas)
    # print(lolos_tidak_lulus_semhas)
    # print(cek_sempro_tidak_lulus)
    # lolos_tidak_lulus_semhas=lolos_tidak_lulus_semhas.filter()
    jumlah=0
    for item in lolos_tidak_lulus_semhas:
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item.id_proposal).last()
                lolos_tidak_lulus_semhas[jumlah].status = get_object.status_bimbingan

            except:
                lolos_tidak_lulus_semhas[jumlah].status = "Belum Diperiksa"
            jumlah += 1
            
    for item in lolos_tidak_lulus_semhas: 
            # print(item.status, item.status == "ACC")
            # print(item.status)
            if item.status != "ACC":
                lolos_tidak_lulus_semhas=lolos_tidak_lulus_semhas.exclude(id_proposal=item.id_proposal)
    
    jumlah=0
    for item in lolos_tidak_lulus_semhas:
        try:
            if item.id_proposal.nim.nim in list_jadwal_semhas:
                lolos_tidak_lulus_semhas[jumlah].status_jadwal="Sudah Assign Jadwal"
            else :
                lolos_tidak_lulus_semhas[jumlah].status_jadwal="Belum Assign Jadwal"
        except :     
                lolos_tidak_lulus_semhas[jumlah].status_jadwal="Belum Assign Jadwal"
        jumlah+=1
    
    for item in lolos_tidak_lulus_semhas:
        if item.status_jadwal=="Sudah Assign Jadwal":
            lolos_tidak_lulus_semhas=lolos_tidak_lulus_semhas.exclude(id_proposal=item.id_proposal)
    
    jumlah=0
    for item in lolos_tidak_lulus_semhas:
            try : 
                roledosen_cek=role_dosen_filter_semhas.filter(nim=item.id_proposal.nim).count()
                if roledosen_cek==2 :
                    lolos_tidak_lulus_semhas[jumlah].status_dosen="Sudah Mencukupi : 2 Assign Dosen"
                elif roledosen_cek==1 :
                    lolos_tidak_lulus_semhas[jumlah].status_dosen="Belum Mencukupi : 1 Assign Dosen"
                else: 
                    lolos_tidak_lulus_semhas[jumlah].status_dosen="Belum Mencukupi : 0 Assign Dosen"
                    
            except :
                    lolos_tidak_lulus_semhas[jumlah].status_dosen="Belum Mencukupi : 0 Assign Dosen" 
                    
            try:
                if item.id_proposal.nim.nim in list_jadwal_semhas:
                    lolos_tidak_lulus_semhas[jumlah].status_jadwal="Sudah Assign Jadwal"
                else :
                    lolos_tidak_lulus_semhas[jumlah].status_jadwal="Belum Assign Jadwal"
            except :     
                    lolos_tidak_lulus_semhas[jumlah].status_jadwal="Belum Assign Jadwal"
                    
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.id_proposal.nim).exists():
                    lolos_tidak_lulus_semhas[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    lolos_tidak_lulus_semhas[jumlah].status_nilai = "Belum Di Nilai"

            except:
                lolos_tidak_lulus_semhas[jumlah].status_nilai = "Belum Di Nilai"
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item.id_proposal).last()
                lolos_tidak_lulus_semhas[jumlah].status = get_object.status_bimbingan

            except:
                lolos_tidak_lulus_semhas[jumlah].status = "Belum Diperiksa"
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                lolos_tidak_lulus_semhas[jumlah].keterangan_dosen = get_object.catatan
            except:
                lolos_tidak_lulus_semhas[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = proposal.objects.filter(nim=item.id_proposal.nim).filter(
                    nama_tahap="Proposal Awal").count()
                # print(get_object)
                lolos_tidak_lulus_semhas[jumlah].jumlah_sempro = get_object
            except:
                lolos_tidak_lulus_semhas[jumlah].jumlah_sempro = 0
            try:
                get_object = proposal.objects.filter(nim=item.id_proposal.nim).filter(
                    nama_tahap="Laporan Akhir").count()
                # print(get_object)
                lolos_tidak_lulus_semhas[jumlah].jumlah_semhas = get_object
            except:
                lolos_tidak_lulus_semhas[jumlah].jumlah_semhas = 0
            jumlah += 1
            

    
    # print(lolos_tidak_lulus)
    # print(cek_sempro_tidak_lulus)
        # for i in proposals:
        #     print(i.status)
    # print(usulantopiks)
    return render(request, 'bimbingan/filter_seminar.html', {"proposals": lolos_tidak_lulus_semhas,"proposals2": cek_semhas_tidak_lulus, "user_info": user_info,"tabel":tabel})

# Proposal Untuk  filter proposal revisi
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Mahasiswa','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_filter_revisi(request):
    user_info = user_information(request)

    if user_info[2].name == "Mahasiswa":
        try:
            proposals = proposal.objects.filter(
                nim=mahasiswa.objects.filter(pk=user_info[0])[0])
        except:
            proposals = []
        jumlah = 0
        for item in proposals:
            # print(item)
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item).last()
                proposals[jumlah].status = get_object.status_bimbingan

            except:
                proposals[jumlah].status = "Belum Diperiksa"
           
            jumlah += 1

    else:
        proposals = proposal.objects.all()
        jumlah = 0
        for item in proposals:
            # print(item)
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item).last()
                proposals[jumlah].status = get_object.status_bimbingan

            except:
                proposals[jumlah].status = "Belum Diperiksa"
           
            jumlah += 1
    for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status != "Revisi":
                proposals=proposals.exclude(id_proposal=item.id_proposal)
                
    jumlah=0
    for item in proposals:
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                    proposals[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    proposals[jumlah].status_nilai = "Belum Di Nilai"

            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item).last()
                proposals[jumlah].status = get_object.status_bimbingan

            except:
                proposals[jumlah].status = "Belum Diperiksa"
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1
            

    

        # for i in proposals:
        #     print(i.status)
    # print(usulantopiks)
    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals, "user_info": user_info})

# Proposal Untuk  filter proposal belum diperiksa
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Mahasiswa','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_filter_belum_diperiksa(request):
    user_info = user_information(request)

    if user_info[2].name == "Mahasiswa":
        try:
            proposals = proposal.objects.filter(
                nim=mahasiswa.objects.filter(pk=user_info[0])[0])
        except:
            proposals = []
        jumlah = 0
        for item in proposals:
            # print(item)
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item).last()
                proposals[jumlah].status = get_object.status_bimbingan

            except:
                proposals[jumlah].status = "Belum Diperiksa"
           
            jumlah += 1

    else:
        proposals = proposal.objects.all()
        jumlah = 0
        for item in proposals:
            # print(item)
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item).last()
                proposals[jumlah].status = get_object.status_bimbingan

            except:
                proposals[jumlah].status = "Belum Diperiksa"
           
            jumlah += 1
    for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status == "Revisi" or item.status == "ACC":
                proposals=proposals.exclude(id_proposal=item.id_proposal)
                
    jumlah=0
    for item in proposals:
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                    proposals[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    proposals[jumlah].status_nilai = "Belum Di Nilai"

            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
            try:
                get_object = bimbingan.objects.filter(
                    id_proposal=item).last()
                proposals[jumlah].status = get_object.status_bimbingan

            except:
                proposals[jumlah].status = "Belum Diperiksa"
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1
            

    

        # for i in proposals:
        #     print(i.status)
    # print(usulantopiks)
    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals, "user_info": user_info})

# Proposal Untuk  filter proposal sudah dinilai
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Mahasiswa','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_filter_dinilai(request):
    user_info = user_information(request)

    if user_info[2].name == "Mahasiswa":
        try:
            proposals = proposal.objects.filter(
                nim=mahasiswa.objects.filter(pk=user_info[0])[0])
        except:
            proposals = []
        jumlah = 0
        for item in proposals:
            # print(item)
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                    proposals[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    proposals[jumlah].status_nilai = "Belum Di Nilai"

            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
           
            jumlah += 1
        for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status_nilai == "Belum Di Nilai":
                proposals=proposals.exclude(id_proposal=item.id_proposal)

    else:
        proposals = proposal.objects.all()
        jumlah = 0
        for item in proposals:
            # print(item)
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                    proposals[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    proposals[jumlah].status_nilai = "Belum Di Nilai"

            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
           
            jumlah += 1
        for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status_nilai == "Belum Di Nilai":
                proposals=proposals.exclude(id_proposal=item.id_proposal)
       
    jumlah=0
    for item in proposals:
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                    proposals[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    proposals[jumlah].status_nilai = "Belum Di Nilai"

            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1
    

    

        # for i in proposals:
        #     print(i.status)
    # print(usulantopiks)
    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals, "user_info": user_info})

# Proposal Untuk  filter proposal belum dinilai
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Mahasiswa','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_filter_belum_dinilai(request):
    user_info = user_information(request)

    if user_info[2].name == "Mahasiswa":
        try:
            proposals = proposal.objects.filter(
                nim=mahasiswa.objects.filter(pk=user_info[0])[0])
        except:
            proposals = []
        jumlah = 0
        for item in proposals:
            # print(item)
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                    proposals[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    proposals[jumlah].status_nilai = "Belum Di Nilai"

            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
           
            jumlah += 1
        for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status_nilai != "Belum Di Nilai":
                proposals=proposals.exclude(id_proposal=item.id_proposal)

    else:
        proposals = proposal.objects.all()
        jumlah = 0
        for item in proposals:
            # print(item)
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                    proposals[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    proposals[jumlah].status_nilai = "Belum Di Nilai"

            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
           
            jumlah += 1
        for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status_nilai != "Belum Di Nilai":
                proposals=proposals.exclude(id_proposal=item.id_proposal)
       
    jumlah=0
    for item in proposals:
            try:
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                    proposals[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    proposals[jumlah].status_nilai = "Belum Di Nilai"

            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1
    

    

        # for i in proposals:
        #     print(i.status)
    # print(usulantopiks)
    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals, "user_info": user_info})


# Proposal :Read 
# Mmelihat data  proposal mahasiswa yang di filter berdasarkan id proposal dalam bentuk form 

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Mahasiswa','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def bimbingan_get_id_proposal(request,id):
    user_info = user_information(request)
    # print(id)
    # print(mahasiswa.objects.get(pk=user_info[0]).nim)
    if user_info[2].name == "Mahasiswa":
        try:
            proposals=proposal.objects.get(pk=id)
        except:
            return redirect("../bimbinganget")
        # print(proposals.nim.nim)
        # print(user_info[0])
        if proposals.nim.nim != user_info[0]:
            raise PermissionDenied()
        else :     
        # if proposal.nim
        # print(proposals)
        # print(proposals)
            try : 
                bimbingans = bimbingan.objects.filter(id_proposal=proposals)
            except :
                bimbingans = []
            
        # .filter(id_proposal__nim__nim=mahasiswa.objects.get(pk=user_info[0]).nim)
        # print(bimbingans)
        # except:
            # bimbingans = []

    else:
        bimbingans = bimbingan.objects.filter(id_proposal=id)
    # print(usulantopiks)
    return render(request, 'bimbingan/bimbingan_get.html', {"bimbingans": bimbingans, "user_info": user_info})

# Proposal :Read 
# Mentabulasi list proposal mahasiswa  yang di filter berdasarkan peran dosen sebagai pembimbing

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_dosen_filter_acc(request):
    user_info = user_information(request)
    nim_list=[]
    role="Dosen Pembimbing"
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []
        


    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta" :
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []
    else:
        raise PermissionDenied()
    # print(nim_list)
    # usulantopiks = usulantopik.objects.filter(
    #         nim=mahasiswa.objects.filter(pk=user_info[0])[0])
    jumlah=0
    for item in proposals:  
        try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
        except:
                proposals[jumlah].status = "Belum Diperiksa"
        jumlah+=1
           
    for item in proposals: 
            # print(item.status, item.status == "ACC")
            # print(item.nim.nim,"-",item.status )
            if item.status == "ACC" or item.status == "Revisi":
                proposals=proposals.exclude(id_proposal=item.id_proposal)
    
    jumlah=0
    for item in proposals:
            try:
                
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                   
                    jumlah_penilaian=list(penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).order_by().values_list("id_detail_penilaian__nama_tahap",flat=True).distinct())
                    # print(list(jumlah_penilaian))
                    if len(jumlah_penilaian)==3:
                        proposals[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    elif len(jumlah_penilaian)!=3:
                        proposals[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    
                    proposals[jumlah].tahap_penilaian = jumlah_penilaian
                else:
                    proposals[jumlah].tahap_penilaian = None
                    proposals[jumlah].status_nilai = "Belum Di Nilai"
                
            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
                proposals[jumlah].tahap_penilaian = None
            
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                proposals[jumlah].status = "Belum Diperiksa"
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1

    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals,"role":role, "user_info": user_info})

# filter proposal sudah diperiksa
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_dosen_filter_sudah_periksa(request):
    user_info = user_information(request)
    nim_list=[]
    role="Dosen Pembimbing"
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []
        


    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta" :
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []
    else:
        raise PermissionDenied()
    # print(nim_list)
    # usulantopiks = usulantopik.objects.filter(
    #         nim=mahasiswa.objects.filter(pk=user_info[0])[0])
    jumlah=0
    for item in proposals:  
        try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
        except:
                proposals[jumlah].status = "Belum Diperiksa"
        jumlah+=1
           
    for item in proposals: 
            # print(item.status, item.status == "ACC")
            if  item.status == "Revisi" or item.status == "ACC":
                pass
            else:
                proposals=proposals.exclude(id_proposal=item.id_proposal)
    jumlah=0
    for item in proposals:
            try:
                
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                   
                    jumlah_penilaian=list(penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).order_by().values_list("id_detail_penilaian__nama_tahap",flat=True).distinct())
                    # print(list(jumlah_penilaian))
                    if len(jumlah_penilaian)==3:
                        proposals[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    elif len(jumlah_penilaian)!=3:
                        proposals[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    
                    proposals[jumlah].tahap_penilaian = jumlah_penilaian
                else:
                    proposals[jumlah].tahap_penilaian = None
                    proposals[jumlah].status_nilai = "Belum Di Nilai"
                
            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
                proposals[jumlah].tahap_penilaian = None
            
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                proposals[jumlah].status = "Belum Diperiksa"
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1

    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals,"role":role, "user_info": user_info})

# filter proposal revisi
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_dosen_filter_revisi(request):
    user_info = user_information(request)
    nim_list=[]
    role="Dosen Pembimbing"
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []
        


    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta" :
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []
    else:
        raise PermissionDenied()
    # print(nim_list)
    # usulantopiks = usulantopik.objects.filter(
    #         nim=mahasiswa.objects.filter(pk=user_info[0])[0])
    jumlah=0
    for item in proposals:  
        try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
        except:
                proposals[jumlah].status = "Belum Diperiksa"
        jumlah+=1
           
    for item in proposals: 
            # print(item.status, item.status == "ACC")
            if  item.status != "Revisi":
                proposals=proposals.exclude(id_proposal=item.id_proposal)
    jumlah=0
    for item in proposals:
            try:
                
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                   
                    jumlah_penilaian=list(penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).order_by().values_list("id_detail_penilaian__nama_tahap",flat=True).distinct())
                    # print(list(jumlah_penilaian))
                    if len(jumlah_penilaian)==3:
                        proposals[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    elif len(jumlah_penilaian)!=3:
                        proposals[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    
                    proposals[jumlah].tahap_penilaian = jumlah_penilaian
                else:
                    proposals[jumlah].tahap_penilaian = None
                    proposals[jumlah].status_nilai = "Belum Di Nilai"
                
            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
                proposals[jumlah].tahap_penilaian = None
            
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                proposals[jumlah].status = "Belum Diperiksa"
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1

    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals,"role":role, "user_info": user_info})

# filter proposal sudah acc
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_dosen_filter_sudah_acc(request):
    user_info = user_information(request)
    nim_list=[]
    role="Dosen Pembimbing"
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []
        


    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta" :
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []
    else:
        raise PermissionDenied()
    # print(nim_list)
    # usulantopiks = usulantopik.objects.filter(
    #         nim=mahasiswa.objects.filter(pk=user_info[0])[0])
    jumlah=0
    for item in proposals:  
        try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
        except:
                proposals[jumlah].status = "Belum Diperiksa"
        jumlah+=1
           
    for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status != "ACC":
                proposals=proposals.exclude(id_proposal=item.id_proposal)
    jumlah=0
    for item in proposals:
            try:
                
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                   
                    jumlah_penilaian=list(penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).order_by().values_list("id_detail_penilaian__nama_tahap",flat=True).distinct())
                    # print(list(jumlah_penilaian))
                    if len(jumlah_penilaian)==3:
                        proposals[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    elif len(jumlah_penilaian)!=3:
                        proposals[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    
                    proposals[jumlah].tahap_penilaian = jumlah_penilaian
                else:
                    proposals[jumlah].tahap_penilaian = None
                    proposals[jumlah].status_nilai = "Belum Di Nilai"
                
            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
                proposals[jumlah].tahap_penilaian = None
            
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                proposals[jumlah].status = "Belum Diperiksa"
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1

    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals,"role":role, "user_info": user_info})
# Proposal :Read 
# Mentabulasi list proposal mahasiswa  yang di filter berdasarkan peran dosen sebagai pembimbing

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_dosen(request):
    user_info = user_information(request)
    nim_list=[]
    role="Dosen Pembimbing"
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []

    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta" :
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []
    else:
        raise PermissionDenied()
    # print(nim_list)
    # usulantopiks = usulantopik.objects.filter(
    #         nim=mahasiswa.objects.filter(pk=user_info[0])[0])
    jumlah=0
    for item in proposals:
            try:
                
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                   
                    jumlah_penilaian=list(penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).order_by().values_list("id_detail_penilaian__nama_tahap",flat=True).distinct())
                    # print(list(jumlah_penilaian))
                    if len(jumlah_penilaian)==3:
                        proposals[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    elif len(jumlah_penilaian)!=3:
                        proposals[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    
                    proposals[jumlah].tahap_penilaian = jumlah_penilaian
                else:
                    proposals[jumlah].tahap_penilaian = None
                    proposals[jumlah].status_nilai = "Belum Di Nilai"
                
            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
                proposals[jumlah].tahap_penilaian = None
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1

    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals,"role":role, "user_info": user_info})
# Proposal :Read 
# Mentabulasi list proposal mahasiswa  yang di filter berdasarkan proposal yang sudah dinilai
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_dosen_sudah_dinilai(request):
    user_info = user_information(request)
    nim_list=[]
    role="Dosen Pembimbing"
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []

    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta" :
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []
    else:
        raise PermissionDenied()
    # print(nim_list)
    # usulantopiks = usulantopik.objects.filter(
    #         nim=mahasiswa.objects.filter(pk=user_info[0])[0])
    jumlah=0
    for item in proposals:
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
            jumlah += 1
            
    for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status != "ACC":
                proposals=proposals.exclude(id_proposal=item.id_proposal)    
            
    jumlah=0
    for item in proposals:
            try:
                
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                   
                    jumlah_penilaian=list(penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).order_by().values_list("id_detail_penilaian__nama_tahap",flat=True).distinct())
                    # print(list(jumlah_penilaian))
                    if len(jumlah_penilaian)==3:
                        proposals[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    elif len(jumlah_penilaian)!=3:
                        proposals[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    
                    proposals[jumlah].tahap_penilaian = jumlah_penilaian
                else:
                    proposals[jumlah].tahap_penilaian = None
                    proposals[jumlah].status_nilai = "Belum Di Nilai"
                
            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
                proposals[jumlah].tahap_penilaian = None
            
            jumlah += 1
    for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status_nilai == "Sudah Ada Seluruh Penilaian" :
                proposals=proposals.exclude(id_proposal=item.id_proposal)
    jumlah=0
    for item in proposals:
            try: 
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                   
                    jumlah_penilaian=list(penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).order_by().values_list("id_detail_penilaian__nama_tahap",flat=True).distinct())
                    # print(list(jumlah_penilaian))
                    if len(jumlah_penilaian)==3:
                        proposals[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    elif len(jumlah_penilaian)!=3:
                        proposals[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    
                    proposals[jumlah].tahap_penilaian = jumlah_penilaian
                else:
                    proposals[jumlah].tahap_penilaian = None
                    proposals[jumlah].status_nilai = "Belum Di Nilai"
                
            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
                proposals[jumlah].tahap_penilaian = None
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = proposals.filter(id_proposal__nim=item.nim).filter(
                    nama_tahap="Proposal Awal").count()
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = proposals.filter(id_proposal__nim=item.nim).filter(
                    nama_tahap="Laporan Akhir").count()
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1

    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals,"role":role, "user_info": user_info})


# Mentabulasi list proposal mahasiswa  yang di filter berdasarkan proposal yang sudah dinilai
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_dosen_lengkap_penilaian(request):
    user_info = user_information(request)
    nim_list=[]
    role="Dosen Pembimbing"
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []

    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta" :
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []
    else:
        raise PermissionDenied()
    # print(nim_list)
    # usulantopiks = usulantopik.objects.filter(
    #         nim=mahasiswa.objects.filter(pk=user_info[0])[0])
    jumlah=0
    for item in proposals:
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
            jumlah += 1
            
    for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status != "ACC":
                proposals=proposals.exclude(id_proposal=item.id_proposal)    
            
    jumlah=0
    for item in proposals:
            try:
                
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                   
                    jumlah_penilaian=list(penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).order_by().values_list("id_detail_penilaian__nama_tahap",flat=True).distinct())
                    # print(list(jumlah_penilaian))
                    if len(jumlah_penilaian)==3:
                        proposals[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    elif len(jumlah_penilaian)!=3:
                        proposals[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    
                    proposals[jumlah].tahap_penilaian = jumlah_penilaian
                else:
                    proposals[jumlah].tahap_penilaian = None
                    proposals[jumlah].status_nilai = "Belum Di Nilai"
                
            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
                proposals[jumlah].tahap_penilaian = None
            
            jumlah += 1
    for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status_nilai != "Sudah Ada Seluruh Penilaian" :
                proposals=proposals.exclude(id_proposal=item.id_proposal)
    jumlah=0
    for item in proposals:
            try: 
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                   
                    jumlah_penilaian=list(penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).order_by().values_list("id_detail_penilaian__nama_tahap",flat=True).distinct())
                    # print(list(jumlah_penilaian))
                    if len(jumlah_penilaian)==3:
                        proposals[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    elif len(jumlah_penilaian)!=3:
                        proposals[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    
                    proposals[jumlah].tahap_penilaian = jumlah_penilaian
                else:
                    proposals[jumlah].tahap_penilaian = None
                    proposals[jumlah].status_nilai = "Belum Di Nilai"
                
            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
                proposals[jumlah].tahap_penilaian = None
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = proposals.filter(id_proposal__nim=item.nim).filter(
                    nama_tahap="Proposal Awal").count()
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = proposals.filter(id_proposal__nim=item.nim).filter(
                    nama_tahap="Laporan Akhir").count()
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1

    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals,"role":role, "user_info": user_info})

# Proposal :Read 
# Mentabulasi list proposal mahasiswa  yang di filter berdasarkan proposal yang belum dinilai
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_dosen_belum_dinilai(request):
    user_info = user_information(request)
    nim_list=[]
    role="Dosen Pembimbing"
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []

    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta" :
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []
    else:
        raise PermissionDenied()
    # print(nim_list)
    # usulantopiks = usulantopik.objects.filter(
    #         nim=mahasiswa.objects.filter(pk=user_info[0])[0])
    jumlah=0
    for item in proposals:
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
            jumlah += 1
            
    for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status != "ACC":
                proposals=proposals.exclude(id_proposal=item.id_proposal)    
            
    jumlah=0
    for item in proposals:
            try:
                
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                   
                    jumlah_penilaian=list(penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).order_by().values_list("id_detail_penilaian__nama_tahap",flat=True).distinct())
                    # print(list(jumlah_penilaian))
                    if len(jumlah_penilaian)==3:
                        proposals[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    elif len(jumlah_penilaian)!=3:
                        proposals[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    
                    proposals[jumlah].tahap_penilaian = jumlah_penilaian
                else:
                    proposals[jumlah].tahap_penilaian = None
                    proposals[jumlah].status_nilai = "Belum Di Nilai"
                
            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
                proposals[jumlah].tahap_penilaian = None
            
            jumlah += 1
    for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status_nilai != "Belum Di Nilai" :
                proposals=proposals.exclude(id_proposal=item.id_proposal)
    jumlah=0
    for item in proposals:
            try: 
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                   
                    jumlah_penilaian=list(penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).order_by().values_list("id_detail_penilaian__nama_tahap",flat=True).distinct())
                    # print(list(jumlah_penilaian))
                    if len(jumlah_penilaian)==3:
                        proposals[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    elif len(jumlah_penilaian)!=3:
                        proposals[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    
                    proposals[jumlah].tahap_penilaian = jumlah_penilaian
                else:
                    proposals[jumlah].tahap_penilaian = None
                    proposals[jumlah].status_nilai = "Belum Di Nilai"
                
            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
                proposals[jumlah].tahap_penilaian = None
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = proposals.filter(id_proposal__nim=item.nim).filter(
                    nama_tahap="Proposal Awal").count()
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = proposals.filter(id_proposal__nim=item.nim).filter(
                    nama_tahap="Laporan Akhir").count()
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1

    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals,"role":role, "user_info": user_info})

# Proposal :Read 
# Mentabulasi list proposal mahasiswa  yang di filter berdasarkan proposal yang sudah  dinilai sebagian
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_dosen_sudah_dinilai_sebagian(request):
    user_info = user_information(request)
    nim_list=[]
    role="Dosen Pembimbing"
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []

    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta" :
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []
    else:
        raise PermissionDenied()
    # print(nim_list)
    # usulantopiks = usulantopik.objects.filter(
    #         nim=mahasiswa.objects.filter(pk=user_info[0])[0])
    jumlah=0
    for item in proposals:
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
            jumlah += 1
            
    for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status != "ACC":
                proposals=proposals.exclude(id_proposal=item.id_proposal)    
            
    jumlah=0
    for item in proposals:
            try:
                
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                   
                    jumlah_penilaian=list(penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).order_by().values_list("id_detail_penilaian__nama_tahap",flat=True).distinct())
                    # print(list(jumlah_penilaian))
                    if len(jumlah_penilaian)==3:
                        proposals[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    elif len(jumlah_penilaian)!=3:
                        proposals[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    
                    proposals[jumlah].tahap_penilaian = jumlah_penilaian
                else:
                    proposals[jumlah].tahap_penilaian = None
                    proposals[jumlah].status_nilai = "Belum Di Nilai"
                
            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
                proposals[jumlah].tahap_penilaian = None
            
            jumlah += 1
    for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status_nilai != "Sudah Ada Sebagian Penilaian" :
                proposals=proposals.exclude(id_proposal=item.id_proposal)
    jumlah=0
    for item in proposals:
            try: 
                if penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                   
                    jumlah_penilaian=list(penilaian.objects.filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).order_by().values_list("id_detail_penilaian__nama_tahap",flat=True).distinct())
                    # print(list(jumlah_penilaian))
                    if len(jumlah_penilaian)==3:
                        proposals[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    elif len(jumlah_penilaian)!=3:
                        proposals[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    
                    proposals[jumlah].tahap_penilaian = jumlah_penilaian
                else:
                    proposals[jumlah].tahap_penilaian = None
                    proposals[jumlah].status_nilai = "Belum Di Nilai"
                
            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
                proposals[jumlah].tahap_penilaian = None
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = proposals.filter(id_proposal__nim=item.nim).filter(
                    nama_tahap="Proposal Awal").count()
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = proposals.filter(id_proposal__nim=item.nim).filter(
                    nama_tahap="Laporan Akhir").count()
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1

    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals,"role":role, "user_info": user_info})

# Proposal :Read 
# Mentabulasi list proposal mahasiswa  yang di filter berdasarkan peran dosen sebagai penguji seminar proposal
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def proposal_get_sempro(request):
    user_info = user_information(request)
    nim_list=[]
    role="Dosen Seminar Proposal"
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Proposal 2")
        # print(ambil_pembimbing)
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(nama_tahap="Proposal Awal (BAB 1 - BAB 3)").filter(
                    nim__in=nim_list)|proposal.objects.filter(nama_tahap="Proposal Awal").filter(
                    nim__in=nim_list)
        except:    
            proposals=[]
        # print(proposals)
        lst_proposals=[]
        for item in proposals:
            lst_proposals.append(item.id_proposal)
        try:
            bimbingans=bimbingan.objects.filter(status_bimbingan="ACC").filter(id_proposal__in=lst_proposals)
        except:
            bimbingans= []
        # print(bimbingans)
        lst_proposal_acc=[]
        for item in bimbingans:
            lst_proposal_acc.append(item.id_proposal.id_proposal)
        # print(lst_proposal_acc)
        try:
            proposals=proposal.objects.filter(
                    id_proposal__in=lst_proposal_acc)
        except:
            proposals=[]
    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Proposal 2")
        # |roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
        # print(ambil_pembimbing)
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(nama_tahap="Proposal Awal (BAB 1 - BAB 3)").filter(
                    nim__in=nim_list)|proposal.objects.filter(nama_tahap="Proposal Awal").filter(
                    nim__in=nim_list)
        except:    
            proposals=[]
        # print(proposals)
        lst_proposals=[]
        for item in proposals:
            lst_proposals.append(item.id_proposal)
        try:
            bimbingans=bimbingan.objects.filter(status_bimbingan="ACC").filter(id_proposal__in=lst_proposals)
        except:
            bimbingans= []
        # print(bimbingans)
        lst_proposal_acc=[]
        for item in bimbingans:
            lst_proposal_acc.append(item.id_proposal.id_proposal)
        # print(lst_proposal_acc)
        try:
            proposals=proposal.objects.filter(
                    id_proposal__in=lst_proposal_acc)
        except:
            proposals=[]
    else:
        raise PermissionDenied()
    jumlah=0
    for item in proposals:
            try:
                check_role= list(ambil_pembimbing.filter(
                    nim=item.nim).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                    proposals[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    proposals[jumlah].status_nilai = "Belum Di Nilai"

            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1

    # print(proposals.ID_Proposal)
    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals,"role":role, "user_info": user_info})
# Mentabulasi list proposal mahasiswa  yang di filter berdasarkan penilaian yang sudah dinilai
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])

def proposal_get_sempro_sudah_nilai(request):
    user_info = user_information(request)
    nim_list=[]
    role="Dosen Seminar Proposal"
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Proposal 2")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        # print(ambil_pembimbing)
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(nama_tahap="Proposal Awal (BAB 1 - BAB 3)").filter(
                    nim__in=nim_list)|proposal.objects.filter(nama_tahap="Proposal Awal").filter(
                    nim__in=nim_list)
        except:    
            proposals=[]
        # print(proposals)
        lst_proposals=[]
        for item in proposals:
            lst_proposals.append(item.id_proposal)
        try:
            bimbingans=bimbingan.objects.filter(status_bimbingan="ACC").filter(id_proposal__in=lst_proposals)
        except:
            bimbingans= []
        # print(bimbingans)
        lst_proposal_acc=[]
        for item in bimbingans:
            lst_proposal_acc.append(item.id_proposal.id_proposal)
        # print(lst_proposal_acc)
        try:
            proposals=proposal.objects.filter(
                    id_proposal__in=lst_proposal_acc)
        except:
            proposals=[]
    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Proposal 2")
        # |roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
        # print(ambil_pembimbing)
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(nama_tahap="Proposal Awal (BAB 1 - BAB 3)").filter(
                    nim__in=nim_list)|proposal.objects.filter(nama_tahap="Proposal Awal").filter(
                    nim__in=nim_list)
        except:    
            proposals=[]
        # print(proposals)
        lst_proposals=[]
        for item in proposals:
            lst_proposals.append(item.id_proposal)
        try:
            bimbingans=bimbingan.objects.filter(status_bimbingan="ACC").filter(id_proposal__in=lst_proposals)
        except:
            bimbingans= []
        # print(bimbingans)
        lst_proposal_acc=[]
        for item in bimbingans:
            lst_proposal_acc.append(item.id_proposal.id_proposal)
        # print(lst_proposal_acc)
        try:
            proposals=proposal.objects.filter(
                    id_proposal__in=lst_proposal_acc)
        except:
            proposals=[]
    else:
        raise PermissionDenied()
    jumlah=0
    for item in proposals:
            try:
                check_role= list(ambil_pembimbing.filter(
                    nim=item.nim).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                    proposals[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    proposals[jumlah].status_nilai = "Belum Di Nilai"

            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
           
            jumlah += 1
    for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status_nilai != "Belum Di Nilai":
                proposals=proposals.exclude(id_proposal=item.id_proposal)
    jumlah=0
    for item in proposals:
            try:
                check_role= list(ambil_pembimbing.filter(
                    nim=item.nim).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                    proposals[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    proposals[jumlah].status_nilai = "Belum Di Nilai"

            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1

    # print(proposals.ID_Proposal)
    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals,"role":role, "user_info": user_info})
# Proposal :Read 
# Mentabulasi list proposal mahasiswa  yang di filter berdasarkan peran dosen sebagai penguji seminar hasil 
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])   
def proposal_get_semhas(request):
    user_info = user_information(request)
    role="Dosen Seminar Hasil"
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Hasil 2")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(nama_tahap="Laporan Akhir").filter(
                    nim__in=nim_list)
            
        except:    
            proposals=[]
        lst_proposals=[]
        for item in proposals:
            lst_proposals.append(item.id_proposal)
        try:
            bimbingans=bimbingan.objects.filter(status_bimbingan="ACC").filter(id_proposal__in=lst_proposals)
        except:
            bimbingans= []
        # print(bimbingans)
        lst_proposal_acc=[]
        for item in bimbingans:
            lst_proposal_acc.append(item.id_proposal.id_proposal)
        # print(lst_proposal_acc)
        try:
            proposals=proposal.objects.filter(
                    id_proposal__in=lst_proposal_acc)
        except:
            proposals=[]
        # try:
            
        #     proposals=proposal.objects.filter(
        #             nim__in=nim_list).last("tanggal_update")
        #     # proposals = proposal.objects.all()

        # except:
        #     proposals = []
    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Hasil 2")
        # |roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(nama_tahap="Laporan Akhir").filter(
                    nim__in=nim_list)
            
        except:    
            proposals=[]
        lst_proposals=[]
        for item in proposals:
            lst_proposals.append(item.id_proposal)
        try:
            bimbingans=bimbingan.objects.filter(status_bimbingan="ACC").filter(id_proposal__in=lst_proposals)
        except:
            bimbingans= []
        # print(bimbingans)
        lst_proposal_acc=[]
        for item in bimbingans:
            lst_proposal_acc.append(item.id_proposal.id_proposal)
        # print(lst_proposal_acc)
        try:
            proposals=proposal.objects.filter(
                    id_proposal__in=lst_proposal_acc)
        except:
            proposals=[]
            # proposals = proposal.objects.all()
    else:
        raise PermissionDenied()

    jumlah=0
    for item in proposals:
            try:
                check_role= list(ambil_pembimbing.filter(
                    nim=item.nim).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Hasil").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                    proposals[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    proposals[jumlah].status_nilai = "Belum Di Nilai"

            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1
    # print(nim_list)
    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals,"role":role, "user_info": user_info})

# Proposal :Read 
# Mentabulasi list proposal mahasiswa  yang di filter berdasarkan peran dosen sebagai penguji seminar hasil dansudah dinilai
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])   
def proposal_get_semhas_sudah_dinilai(request):
    user_info = user_information(request)
    role="Dosen Seminar Hasil"
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Hasil 2")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(nama_tahap="Laporan Akhir").filter(
                    nim__in=nim_list)
            
        except:    
            proposals=[]
        lst_proposals=[]
        for item in proposals:
            lst_proposals.append(item.id_proposal)
        try:
            bimbingans=bimbingan.objects.filter(status_bimbingan="ACC").filter(id_proposal__in=lst_proposals)
        except:
            bimbingans= []
        # print(bimbingans)
        lst_proposal_acc=[]
        for item in bimbingans:
            lst_proposal_acc.append(item.id_proposal.id_proposal)
        # print(lst_proposal_acc)
        try:
            proposals=proposal.objects.filter(
                    id_proposal__in=lst_proposal_acc)
        except:
            proposals=[]
        # try:
            
        #     proposals=proposal.objects.filter(
        #             nim__in=nim_list).last("tanggal_update")
        #     # proposals = proposal.objects.all()

        # except:
        #     proposals = []
    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta":
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Hasil 2")
        # |roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(nama_tahap="Laporan Akhir").filter(
                    nim__in=nim_list)
            
        except:    
            proposals=[]
        lst_proposals=[]
        for item in proposals:
            lst_proposals.append(item.id_proposal)
        try:
            bimbingans=bimbingan.objects.filter(status_bimbingan="ACC").filter(id_proposal__in=lst_proposals)
        except:
            bimbingans= []
        # print(bimbingans)
        lst_proposal_acc=[]
        for item in bimbingans:
            lst_proposal_acc.append(item.id_proposal.id_proposal)
        # print(lst_proposal_acc)
        try:
            proposals=proposal.objects.filter(
                    id_proposal__in=lst_proposal_acc)
        except:
            proposals=[]
            # proposals = proposal.objects.all()
    else:
        raise PermissionDenied()

    jumlah=0
    for item in proposals:
            try:
                check_role= list(ambil_pembimbing.filter(
                    nim=item.nim).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Hasil").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                    proposals[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    proposals[jumlah].status_nilai = "Belum Di Nilai"

            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
            jumlah += 1
    for item in proposals: 
            # print(item.status, item.status == "ACC")
            if item.status_nilai != "Belum Di Nilai":
                proposals=proposals.exclude(id_proposal=item.id_proposal)
    jumlah=0
    for item in proposals:
            try:
                check_role= list(ambil_pembimbing.filter(
                    nim=item.nim).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Hasil").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                    id_detail_penilaian__id_role_dosen__nim=item.nim).exists():
                    proposals[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    proposals[jumlah].status_nilai = "Belum Di Nilai"

            except:
                proposals[jumlah].status_nilai = "Belum Di Nilai"
            try:  
                get_object = bimbingan.objects.filter(
                    id_proposal=item).order_by("tanggal_update").last()
                proposals[jumlah].status = get_object.status_bimbingan
            except:
                    proposals[jumlah].status = "Belum Diperiksa"
           
            try:
                get_object = bimbingan.objects.get(
                    id_proposal=item)
                proposals[jumlah].keterangan_dosen = get_object.catatan
            except:
                proposals[jumlah].keterangan_dosen = "Belum Ada Catatan"
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Proposal Awal").count()
                # print(get_object)
                proposals[jumlah].jumlah_sempro = get_object
            except:
                proposals[jumlah].jumlah_sempro = 0
            try:
                get_object = bimbingan.objects.filter(id_proposal=item.id_proposal).filter(
                    id_proposal__nama_tahap="Laporan Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1
    # print(nim_list)
    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals,"role":role, "user_info": user_info})

# Proposal : Read
# Membaca data proposal berbentuk form berdasarkan id proposal
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])   
def proposal_read(request, id):
    user_info = user_information(request)
    proposal_data = proposal.objects.filter(pk=id)

    form = ProposalFormRead(instance=proposal_data[0])
    form.fields["file_proposal"].widget = forms.HiddenInput()
    field = ["nim",  "nama_tahap", "judul_proposal",
             "file_proposal", "keterangan"
]
    for item in field:
        # form.field.disabled = True
        form.fields[item].disabled = True
    # print(form)
    return render(request, 'bimbingan/proposal_read.html', {"form": form, "proposal": proposal_data[0].file_proposal, "user_info": user_info})

# check point : proposal read
# Proposal : Update
# Mengupdate data proposal berdasarkan id proposal
# todo: add in notification and email

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Mahasiswa','Properta'])   
def proposal_update(request, id):
    user_info = user_information(request)
    proposal_data = proposal.objects.get(pk=id)
    if user_info[2].name == "Mahasiswa" and request.method == "POST":
            form = ProposalForm(request.POST, request.FILES,
                                instance=proposal_data)
            if form.is_valid():

                create_proposal = form.save(commit=False)
                create_proposal.nim = mahasiswa.objects.get(pk=user_info[0])
                # instances = evaluasitopik.objects.filter(id_usulan_topik=usulantopik_data.id_usulan_topik).order_by('tanggal_buat')
                # if instances.exists(): # Pastikan QuerySet tidak kosong
                #     instances.update(status_topik='Revisi') # Mengubah status untuk semua objek

                #     # Mengubah status objek pertama menjadi "Submit"
                #     # print(instances)
                #     # print(instances.values_list("tanggal_update"))
                #     first_instance = instances.order_by('-tanggal_buat').first()
                #     # print(first_instance.tanggal_buat)
                #     first_instance.status_topik = 'Submit'
                #     first_instance.save()
                instances = bimbingan.objects.filter(id_proposal=proposal_data.id_proposal).order_by('tanggal_buat')
                if instances.exists(): # Pastikan QuerySet tidak kosong
                    instances.update(status_bimbingan='Revisi') # Mengubah status untuk semua objek

                    # Mengubah status objek pertama menjadi "Submit"
                    first_instance = instances.order_by('-tanggal_update').first()
                    first_instance.status_bimbingan = 'Submit'
                    first_instance.save()
                create_proposal.save()
                messages.warning(request,"Data Proposal Telah Berhasil Diperbaharui! ")
                roledosen_data=roledosen.objects.filter(role="Pembimbing 1").filter(nim=create_proposal.nim)|roledosen.objects.filter(role="Pembimbing 2").filter(nim=create_proposal.nim)
                email_list=[]
                    # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
                for i in roledosen_data:
                    temp_email=list(User.objects.filter(pk=i.nip.id_user.id).values_list('email'))
                    email_list.append(temp_email[0][0])
                    notifikasi.objects.create(nip=i.nip,messages=f"Terdapat Update Proposal dilakukan Oleh {create_proposal.nim.id_user.first_name} Untuk diperiksa pada {tanggal} Jam {Jam}")
                # email_list=User.objects.filter(pk=i.nip.id_user).values_list('email')
                send_mail(
                    'Terdapat Update Proposal Telah Di Buat ',
                    f"Terdapat Proposal Baru Oleh {create_proposal.nim.id_user.first_name} Untuk diperiksa pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                )

                return redirect("../proposalget")
    elif (user_info[2].name == "Admin" or user_info[2].name == "Properta") and request.method == "POST":
            form = ProposalFormFull(request.POST, request.FILES,
                                instance=proposal_data)
            if form.is_valid():

                create_proposal = form.save(commit=False)
                # create_proposal.nim = mahasiswa.objects.get(pk=user_info[0])
                instances = bimbingan.objects.filter(id_proposal=proposal_data.id_proposal).order_by('tanggal_buat')
                if instances.exists(): # Pastikan QuerySet tidak kosong
                    instances.update(status_bimbingan='Revisi') # Mengubah status untuk semua objek

                    # Mengubah status objek pertama menjadi "Submit"
                    first_instance = instances.first()
                    first_instance.status_bimbingan = 'Submit'
                    first_instance.save()
                create_proposal.save()
                messages.warning(request,"Data Proposal Telah Berhasil Diperbaharui! ")
                roledosen_data=roledosen.objects.filter(role="Pembimbing 1").filter(nim=create_proposal.nim)|roledosen.objects.filter(role="Pembimbing 2").filter(nim=create_proposal.nim)
                email_list=[]
                # sekdept_filter=dosen.object.filter(id_user__in=user_sekdept)
                for i in roledosen_data:
                    temp_email=list(User.objects.filter(pk=i.nip.id_user.id).values_list('email'))
                    email_list.append(temp_email[0][0])
                    notifikasi.objects.create(nip=i.nip,messages=f"Terdapat Update Proposal dilakukan Oleh {create_proposal.nim.id_user.first_name} Untuk diperiksa pada {tanggal} Jam {Jam}")
                # email_list=User.objects.filter(pk=i.nip.id_user).values_list('email')
                # User.objects.filter(pk=create_roledosen.id_proposal.nim.id_user).values_list('email')
                send_mail(
                    'Terdapat Update Proposal Telah Di Buat ',
                    f"Terdapat Update Proposal dilakukan Oleh {create_proposal.nim.id_user.first_name} Untuk diperiksa pada {tanggal} Jam {Jam}",
                    settings.EMAIL_HOST_USER,
                    email_list,
                    fail_silently=False,
                )
                return redirect("../proposalget")
    elif user_info[2].name == "Admin"  or user_info[2].name == "Properta" :
            form = ProposalFormFull(instance=proposal_data)
    else :
            form = ProposalForm(instance=proposal_data)
    return render(request, 'bimbingan/proposal_create.html', {"form": form, "user_info": user_info})

# proposal : delete
# Menghapus data proposal berdasarkan id proposal
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Mahasiswa','Properta'])   
def proposal_delete(request, id):
    delete_data = proposal.objects.get(pk=id)
    messages.error(request,"Data Proposal Telah Berhasil Dihapus! ")
    delete_data.delete()
    return redirect('../proposalget')

# userinfo : Read 
# Memberikan Informasi dasar user untuk profil pengguna
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Mahasiswa','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def user_information(request):


    notifikasi_filter=notifikasi.objects.filter(nip=None).filter(nim=None)|notifikasi.objects.filter(nip="").filter(nim=None)|notifikasi.objects.filter(nip=None).filter(nim="")|notifikasi.objects.filter(nip="").filter(nim="")
    for i in notifikasi_filter:
        i.delete()
    try:
        role = request.user.groups.all()[0]
        try:
            role2 = role.name
        except:
            pass
    except:
        role = ""
        role2 = "Admin"
    # print(role2)
    
    if role2 != "Mahasiswa":
        try:
            dosendata = dosen.objects.get(id_user=request.user.pk)
            # print(dosendata)
        except:
            dosendata = ""
        try:
            Nomor = dosendata.nip
        except:
            Nomor = ""
        try:
            photo = dosendata.photo_file.url
        except:
            photo = ""
    else:
        # print("test")
        try:
            mhs = mahasiswa.objects.get(id_user=request.user)
        except:
            mhs = ""

        try:
            Nomor = mhs.nim
        except:
            Nomor = ""
        try:
            photo = mhs.photo_file.url
        except:
            photo = ""
    # notiifikasi_data=models.notifikasi.objects.filter(nim=Nomor)|models.notifikasi.objects.filter(nip=Nomor)
    notiifikasi_data= notifikasi.objects.filter(nim=Nomor)|notifikasi.objects.filter(nip=Nomor)|notifikasi.objects.filter(nim__startswith=Nomor)|notifikasi.objects.filter(nip__endswith=Nomor)
    # print(notiifikasi_data)
    if notiifikasi_data.exists():
        pass
    else :
        notiifikasi_data=None
    if request.method == "POST":
        formnotif = NotifikasiForm(request.POST)
        # print(formnotif)
        if formnotif.is_valid():
            create_proposal = formnotif.save(commit=False)
            create_proposal.save() 
   
    else : 
        formnotif = NotifikasiForm()
    # print(notiifikasi_data.exists())
    try : 
        count_notif=notiifikasi_data.count()
    except :
        count_notif=0

    return Nomor, photo, role,notiifikasi_data,count_notif,{"formnotif":formnotif}
# Menghapus Notifikasi 
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Mahasiswa','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def notifikasi_delete(request,id):
    delete_data = notifikasi.objects.get(pk=id)
    messages.error(request,"Data Notifikasi Telah Berhasil Dihapus! ")
    delete_data.delete()
    return redirect('../dashboard')
# sampe sini 
# Tampilan Awal masing masing role 
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Mahasiswa','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def home(request):
    user_info = user_information(request)
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        bimbingans = bimbingan.objects.filter(id_role_dosen__nip=user_info[0]).filter(
            id_role_dosen__role="Pembimbing 1") | bimbingan.objects.filter(id_role_dosen__nip=user_info[0]).filter(
            id_role_dosen__role="Pembimbing 2")
        # bimbingans = []
        # bimbingan1 = bimbingan.objects.get(id_role_dosen=roledosen.objects.filter(
        #     nip=dosen.objects.filter(pk=user_info[0])[0]).filter(role="Pembimbing 1")[0])
        # bimbingan2 = bimbingan.objects.get(id_role_dosen=roledosen.objects.filter(
        #     nip=dosen.objects.filter(pk=user_info[0])[0]).filter(role="Pembimbing 2")[0])
        # bimbingans.append(bimbingan1)
        # bimbingans.append(bimbingan2)
    elif user_info[2].name == "Mahasiswa":
        bimbingans = bimbingan.objects.filter(
            id_proposal__nim=mahasiswa.objects.filter(pk=user_info[0])[0])

    else:
        bimbingans = bimbingan.objects.all()
        # dosens = dosen.objects.all() 
        # if request.method == "post":
        #     id_dosen = request.POST.get("dosen-id").first()
        #     dosen = dosen.object.filter(id_dosen=id_dosen)
        #     if dosen and dosen.author == request.user:
        #         dosen.delete()

    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" :
        try:
            # print(kompartemendosen.objects.filter(nip=dosen.objects.filter(pk=user_info[0])[0]))
            evaluasitopiks = evaluasitopik.objects.filter(
                    id_dosen_kompartemen=kompartemendosen.objects.filter(nip=dosen.objects.filter(pk=user_info[0])[0])[0])
        except:
            evaluasitopiks = []
        # print(evaluasitopiks)
    elif user_info[2].name == "Mahasiswa":
        try:
            evaluasitopiks = evaluasitopik.objects.filter(
                id_usulan_topik=usulantopik.objects.filter(pk=mahasiswa.objects.filter(pk=user_info[0])[0]))
        except:
            evaluasitopiks = []
    else:
        evaluasitopiks = evaluasitopik.objects.all()
    # print(usulantopiks)

    nim_list=[]
    # role="Dosen Pembimbing"
    if user_info[2].name == "Dosen" or user_info[2].name == "Kompartemen" or user_info[2].name == "Manajemen Departemen":
        
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.nim)
        try:
            proposals=proposal.objects.filter(
                    nim__in=nim_list)
            # proposals = proposal.objects.all()

        except:
            proposals = []
    else:
            proposals = []

    return render(request, 'home.html', {"bimbingans": bimbingans,"evaluasitopiks":evaluasitopiks,"proposals":proposals, "user_info": user_info})

# Fungsi Testing : Merubah User berdasarkan nama yang dicantumkan ketika ada  
@login_required(login_url="/login")
# @role_required(allowed_roles=['Admin','Properta'])
def change_user(request, id):
    # id_dosen = request.POST.get("name").first()
    # print(request.user.id)
    if id=="Sekertaris_Departemen":
        id="Manajemen Departemen"
        
    this_username = User.objects.get(pk=request.user.id)
    this_group = this_username.groups.all()
    # print(this_group[0].name)
    check_group = Group.objects.filter(name=id)
    if not check_group.exists():
        pass 
    else : 
        if this_group.exists():
            delete_group = Group.objects.get(name=this_group[0].name)
            delete_group.user_set.remove(this_username)
        id = id.replace("_", " ")
        my_group = Group.objects.get(name=id)
        my_group.user_set.add(this_username)
    messages.success(request,"Berhasil Merubah Hak Akses User! ")
    return redirect('../usergroupget')
# Jadwal Seminar
# jadwal: Create
# Membuat data Jadwal Seminar
# todo: add in notification and email
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Properta'])
def jadwal_create(request):
    user_info = user_information(request)
    role_dosen_data=roledosen.objects.filter(status="Active")
    # jadwal_data=Jadwal.objects.get()
    if request.method == "POST":
        form = JadwalForm(request.POST)
        if form.is_valid():
            # post.id_dosen = request.user
            form = form.save(commit=False)
            form.save()
            # print(form)
            # todo notif
            notifikasi.objects.create(nim=form.mahasiswa,messages=f"Anda sudah diassign untuk melakukan jadwal seminar sebagai peserta seminar pada tanggal {form.tanggal_seminar} dan jam {form.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
            notifikasi.objects.create(nip=form.dosen_pembimbing_1,messages=f"Anda sudah diassign untuk melakukan jadwal seminar sebagai pembimbing 1 mahasiswa {form.mahasiswa} pada tanggal {form.tanggal_seminar} dan jam {form.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
            notifikasi.objects.create(nip=form.dosen_pembimbing_2,messages=f"Anda sudah diassign untuk melakukan jadwal seminar sebagai pembimbing 2 mahasiswa {form.mahasiswa} pada tanggal {form.tanggal_seminar} dan jam {form.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
            notifikasi.objects.create(nip=form.dosen_penguji_1,messages=f"Anda sudah diassign untuk melakukan jadwal seminar sebagai penguji 1 mahasiswa {form.mahasiswa} pada tanggal {form.tanggal_seminar} dan jam {form.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
            notifikasi.objects.create(nip=form.dosen_penguji_2,messages=f"Anda sudah diassign untuk melakukan jadwal seminar sebagai penguji 2 mahasiswa {form.mahasiswa} pada tanggal {form.tanggal_seminar} dan jam {form.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
            # email_list=User.objects.filter(pk=form.nim.id_user).values_list('email')
            email_list=[]

            temp_email=list(User.objects.filter(pk=mahasiswa.objects.get(pk=form.mahasiswa.nim).id_user.id).values_list('email',flat=True))
            email_list=email_list+temp_email

            temp_email=list(User.objects.filter(pk=dosen.objects.get(pk=form.dosen_pembimbing_1.nip.nip).id_user.id).values_list('email',flat=True))
            email_list=email_list+temp_email



            try : 
                temp_email=list(User.objects.filter(pk=dosen.objects.get(pk=form.dosen_pembimbing_2.nip.nip).id_user.id).values_list('email',flat=True))
                email_list=email_list+temp_email
            except:
                pass

            temp_email=list(User.objects.filter(pk=dosen.objects.get(pk=form.dosen_penguji_1.nip.nip).id_user.id).values_list('email',flat=True))
            email_list=email_list+temp_email

            temp_email=list(User.objects.filter(pk=dosen.objects.get(pk=form.dosen_penguji_2.nip.nip).id_user.id).values_list('email',flat=True))
            email_list=email_list+temp_email
            
            # User.objects.filter(pk=form.nim.id_user).values_list('email')
            send_mail(
                'Terdapat Assign Jadwal Seminar',
                f"Anda sudah diassign untuk melakukan jadwal seminar {form.mahasiswa} pada tanggal {form.tanggal_seminar} dan jam {form.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}",
                settings.EMAIL_HOST_USER,
                email_list,
                fail_silently=False,
            )
            messages.success(request,"Data Jadwal Seminar Telah Berhasil Dibuat! ")
            return redirect("../jadwalget/nomorinduk")
    # elif jadwal_data!=None:
        #  form = JadwalForm(instance=jadwal_data)
    else:
        form = JadwalForm()
    return render(request, 'dosen/jadwal_create.html', {"form": form, "user_info": user_info,"role_dosen_data":role_dosen_data})

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Properta'])
def jadwal_create_tanpa_filter(request):
    user_info = user_information(request)
    role_dosen_data=roledosen.objects.all()
    # jadwal_data=Jadwal.objects.get()
    if request.method == "POST":
        form = JadwalFormTanpaFilter(request.POST)
        if form.is_valid():
            # post.id_dosen = request.user
            form = form.save(commit=False)
            form.save()
            # print(form)
            # todo notif
            notifikasi.objects.create(nim=form.mahasiswa,messages=f"Anda sudah diassign untuk melakukan jadwal seminar sebagai peserta seminar pada tanggal {form.tanggal_seminar} dan jam {form.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
            notifikasi.objects.create(nip=form.dosen_pembimbing_1,messages=f"Anda sudah diassign untuk melakukan jadwal seminar sebagai pembimbing 1 mahasiswa {form.mahasiswa} pada tanggal {form.tanggal_seminar} dan jam {form.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
            notifikasi.objects.create(nip=form.dosen_pembimbing_2,messages=f"Anda sudah diassign untuk melakukan jadwal seminar sebagai pembimbing 2 mahasiswa {form.mahasiswa} pada tanggal {form.tanggal_seminar} dan jam {form.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
            notifikasi.objects.create(nip=form.dosen_penguji_1,messages=f"Anda sudah diassign untuk melakukan jadwal seminar sebagai penguji 1 mahasiswa {form.mahasiswa} pada tanggal {form.tanggal_seminar} dan jam {form.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
            notifikasi.objects.create(nip=form.dosen_penguji_2,messages=f"Anda sudah diassign untuk melakukan jadwal seminar sebagai penguji 2 mahasiswa {form.mahasiswa} pada tanggal {form.tanggal_seminar} dan jam {form.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
            # email_list=User.objects.filter(pk=form.nim.id_user).values_list('email')
            email_list=[]

            temp_email=list(User.objects.filter(pk=mahasiswa.objects.get(pk=form.mahasiswa.nim).id_user.id).values_list('email',flat=True))
            email_list=email_list+temp_email

            temp_email=list(User.objects.filter(pk=dosen.objects.get(pk=form.dosen_pembimbing_1.nip.nip).id_user.id).values_list('email',flat=True))
            email_list=email_list+temp_email



            try : 
                temp_email=list(User.objects.filter(pk=dosen.objects.get(pk=form.dosen_pembimbing_2.nip.nip).id_user.id).values_list('email',flat=True))
                email_list=email_list+temp_email
            except:
                pass

            temp_email=list(User.objects.filter(pk=dosen.objects.get(pk=form.dosen_penguji_1.nip.nip).id_user.id).values_list('email',flat=True))
            email_list=email_list+temp_email

            temp_email=list(User.objects.filter(pk=dosen.objects.get(pk=form.dosen_penguji_2.nip.nip).id_user.id).values_list('email',flat=True))
            email_list=email_list+temp_email
            
            # User.objects.filter(pk=form.nim.id_user).values_list('email')
            send_mail(
                'Terdapat Assign Jadwal Seminar',
                f"Anda sudah diassign untuk melakukan jadwal seminar {form.mahasiswa} pada tanggal {form.tanggal_seminar} dan jam {form.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}",
                settings.EMAIL_HOST_USER,
                email_list,
                fail_silently=False,
            )
            messages.success(request,"Data Jadwal Seminar Telah Berhasil Dibuat! ")
            return redirect("../jadwalget/nomorinduk")
    # elif jadwal_data!=None:
        #  form = JadwalForm(instance=jadwal_data)
    else:
        form = JadwalFormTanpaFilter()
    return render(request, 'dosen/jadwal_create.html', {"form": form, "user_info": user_info,"role_dosen_data":role_dosen_data})


# Jadwal Seminar : Update
# Mengubah data Jadwal Seminar berdasarkan id seminar 
# todo: add in notification and email
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Properta'])
def jadwal_update(request,id):
    user_info = user_information(request)
    jadwal_data=jadwal_seminar.objects.get(pk=id)
    role_dosen_data=roledosen.objects.all()
    print(jadwal_data.dosen_penguji_1)
    print(jadwal_data.dosen_penguji_2)
    # print(jadwal_data.waktu_seminar)
    # print(jadwal_data.tanggal_seminar)
    if request.method == "POST":
        form = JadwalForm(request.POST,instance=jadwal_data)

        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            messages.warning(request,"Data Jadwal Seminar Telah Berhasil Diperbarui! ")
            # print(jadwal_data.mahasiswa.split("-")[0])
            # todo : notif
            email_list=[]
            notifikasi.objects.create(nim=jadwal_data.mahasiswa,messages=f"Terdapat perubahan Jadwal untuk anda melakukan jadwal seminar sebagai peserta seminar pada tanggal {jadwal_data.tanggal_seminar} dan jam {jadwal_data.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
            notifikasi.objects.create(nip=jadwal_data.dosen_pembimbing_1,messages=f"Terdapat perubahan Jadwal untuk anda melakukan jadwal seminar sebagai pembimbing 1 mahasiswa {jadwal_data.mahasiswa} pada tanggal {jadwal_data.tanggal_seminar} dan jam {jadwal_data.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
            notifikasi.objects.create(nip=jadwal_data.dosen_pembimbing_2,messages=f"Terdapat perubahan Jadwal untuk anda melakukan jadwal seminar sebagai pembimbing 2 mahasiswa {jadwal_data.mahasiswa} pada tanggal {jadwal_data.tanggal_seminar} dan jam {jadwal_data.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
            notifikasi.objects.create(nip=jadwal_data.dosen_penguji_1,messages=f"Terdapat perubahan Jadwal untuk anda melakukan jadwal seminar sebagai penguji 1 mahasiswa {jadwal_data.mahasiswa} pada tanggal {jadwal_data.tanggal_seminar} dan jam {jadwal_data.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
            notifikasi.objects.create(nip=jadwal_data.dosen_penguji_2,messages=f"Terdapat perubahan Jadwal untuk anda melakukan jadwal seminar sebagai penguji 2 mahasiswa {jadwal_data.mahasiswa} pada tanggal {jadwal_data.tanggal_seminar} dan jam {jadwal_data.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
            email_list=[]

            temp_email=list(User.objects.filter(pk=mahasiswa.objects.get(pk=form.mahasiswa.nim).id_user.id).values_list('email',flat=True))
            email_list=email_list+temp_email

            temp_email=list(User.objects.filter(pk=dosen.objects.get(pk=form.dosen_pembimbing_1.nip.nip).id_user.id).values_list('email',flat=True))
            email_list=email_list+temp_email

            try : 
                temp_email=list(User.objects.filter(pk=dosen.objects.get(pk=form.dosen_pembimbing_2.nip.nip).id_user.id).values_list('email',flat=True))
                email_list=email_list+temp_email
            except:
                pass

            temp_email=list(User.objects.filter(pk=dosen.objects.get(pk=form.dosen_penguji_1.nip.nip).id_user.id).values_list('email',flat=True))
            email_list=email_list+temp_email

            temp_email=list(User.objects.filter(pk=dosen.objects.get(pk=form.dosen_penguji_2.nip.nip).id_user.id).values_list('email',flat=True))
            email_list=email_list+temp_email
                            # User.objects.filter(pk=dosen.objects.get(pk=jadwal_data.dosen_pembimbing_1.nip).id_user.id).values_list('email')|
                            # User.objects.filter(pk=jadwal_data.dosen_pembimbing_2.nip).values_list('email'))
                            # |User.objects.filter(pk=dosen.objects.get(pk=jadwal_data.dosen_penguji_1.nip).id_user.id).values_list('email'))
                            # |User.objects.filter(pk=dosen.objects.get(pk=jadwal_data.dosen_penguji_2.nip).id_user.id).values_list('email'))
            # |User.objects.filter(pk=dosen.objects.get(pk=jadwal_data.dosen_pembimbing_2.nip).id_user.id).values_list('email')
            # 
            # print(email_list)
            # masi error
            # |User.objects.filter(pk=jadwal_data.dosen_penguji_1.id_user.id).values_list('email')|User.objects.filter(pk=jadwal_data.dosen_penguji_2.id_user.id).values_list('email')
            # mahasiswa.objects.get(pk=jadwal_data.mahasiswa.split("-")[0])
            # print(email_list)
            # User.objects.filter(pk=jadwal_data.nim.id_user).values_list('email')
            send_mail(
                'Terdapat Assign Jadwal Seminar ',
                f"Anda sudah diassign untuk melakukan jadwal seminar {jadwal_data.mahasiswa} pada tanggal {jadwal_data.tanggal_seminar} dan jam {jadwal_data.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}",
                settings.EMAIL_HOST_USER,
                email_list,
                fail_silently=False,
            )
            return redirect("../jadwalget/nomorinduk")
    else:
        form = JadwalForm(instance=jadwal_data)
    return render(request, 'dosen/jadwal_create.html', {"form": form, "user_info": user_info,"role_dosen_data":role_dosen_data})

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Properta'])
def jadwal_update_tanpa_filter(request,id):
    user_info = user_information(request)
    jadwal_data=jadwal_seminar.objects.get(pk=id)
    role_dosen_data=roledosen.objects.all()
    # print(jadwal_data.dosen_pembimbing_1)
    # print(jadwal_data.waktu_seminar)
    # print(jadwal_data.tanggal_seminar)
    if request.method == "POST":
        form = JadwalFormTanpaFilter(request.POST,instance=jadwal_data)

        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            messages.warning(request,"Data Jadwal Seminar Telah Berhasil Diperbarui! ")
            # print(jadwal_data.mahasiswa.split("-")[0])
            # todo : notif
            email_list=[]
            notifikasi.objects.create(nim=jadwal_data.mahasiswa,messages=f"Terdapat perubahan Jadwal untuk anda melakukan jadwal seminar sebagai peserta seminar pada tanggal {jadwal_data.tanggal_seminar} dan jam {jadwal_data.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
            notifikasi.objects.create(nip=jadwal_data.dosen_pembimbing_1,messages=f"Terdapat perubahan Jadwal untuk anda melakukan jadwal seminar sebagai pembimbing 1 mahasiswa {jadwal_data.mahasiswa} pada tanggal {jadwal_data.tanggal_seminar} dan jam {jadwal_data.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
            notifikasi.objects.create(nip=jadwal_data.dosen_pembimbing_2,messages=f"Terdapat perubahan Jadwal untuk anda melakukan jadwal seminar sebagai pembimbing 2 mahasiswa {jadwal_data.mahasiswa} pada tanggal {jadwal_data.tanggal_seminar} dan jam {jadwal_data.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
            notifikasi.objects.create(nip=jadwal_data.dosen_penguji_1,messages=f"Terdapat perubahan Jadwal untuk anda melakukan jadwal seminar sebagai penguji 1 mahasiswa {jadwal_data.mahasiswa} pada tanggal {jadwal_data.tanggal_seminar} dan jam {jadwal_data.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
            notifikasi.objects.create(nip=jadwal_data.dosen_penguji_2,messages=f"Terdapat perubahan Jadwal untuk anda melakukan jadwal seminar sebagai penguji 2 mahasiswa {jadwal_data.mahasiswa} pada tanggal {jadwal_data.tanggal_seminar} dan jam {jadwal_data.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
            email_list=[]

            temp_email=list(User.objects.filter(pk=mahasiswa.objects.get(pk=form.mahasiswa.nim).id_user.id).values_list('email',flat=True))
            email_list=email_list+temp_email

            temp_email=list(User.objects.filter(pk=dosen.objects.get(pk=form.dosen_pembimbing_1.nip.nip).id_user.id).values_list('email',flat=True))
            email_list=email_list+temp_email

            try : 
                temp_email=list(User.objects.filter(pk=dosen.objects.get(pk=form.dosen_pembimbing_2.nip.nip).id_user.id).values_list('email',flat=True))
                email_list=email_list+temp_email
            except:
                pass

            temp_email=list(User.objects.filter(pk=dosen.objects.get(pk=form.dosen_penguji_1.nip.nip).id_user.id).values_list('email',flat=True))
            email_list=email_list+temp_email

            temp_email=list(User.objects.filter(pk=dosen.objects.get(pk=form.dosen_penguji_2.nip.nip).id_user.id).values_list('email',flat=True))
            email_list=email_list+temp_email
                            # User.objects.filter(pk=dosen.objects.get(pk=jadwal_data.dosen_pembimbing_1.nip).id_user.id).values_list('email')|
                            # User.objects.filter(pk=jadwal_data.dosen_pembimbing_2.nip).values_list('email'))
                            # |User.objects.filter(pk=dosen.objects.get(pk=jadwal_data.dosen_penguji_1.nip).id_user.id).values_list('email'))
                            # |User.objects.filter(pk=dosen.objects.get(pk=jadwal_data.dosen_penguji_2.nip).id_user.id).values_list('email'))
            # |User.objects.filter(pk=dosen.objects.get(pk=jadwal_data.dosen_pembimbing_2.nip).id_user.id).values_list('email')
            # 
            # print(email_list)
            # masi error
            # |User.objects.filter(pk=jadwal_data.dosen_penguji_1.id_user.id).values_list('email')|User.objects.filter(pk=jadwal_data.dosen_penguji_2.id_user.id).values_list('email')
            # mahasiswa.objects.get(pk=jadwal_data.mahasiswa.split("-")[0])
            # print(email_list)
            # User.objects.filter(pk=jadwal_data.nim.id_user).values_list('email')
            send_mail(
                'Terdapat Assign Jadwal Seminar ',
                f"Anda sudah diassign untuk melakukan jadwal seminar {jadwal_data.mahasiswa} pada tanggal {jadwal_data.tanggal_seminar} dan jam {jadwal_data.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}",
                settings.EMAIL_HOST_USER,
                email_list,
                fail_silently=False,
            )
            return redirect("../jadwalget/nomorinduk")
    else:
        form = JadwalFormTanpaFilter(instance=jadwal_data,initial={"tanggal_seminar":jadwal_data.tanggal_seminar.strftime('%Y-%m-%d'),"waktu_seminar":jadwal_data.waktu_seminar.strftime('%H:%M')})
    return render(request, 'dosen/jadwal_create.html', {"form": form, "user_info": user_info,"role_dosen_data":role_dosen_data})



# Jadwal Seminar : Delete
# menghapus  data Jadwal Seminar berdasarkan id jadwal 
# todo: add in notification and email
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Properta'])
def jadwal_delete(request,id):
    
    jadwal_data=jadwal_seminar.objects.get(pk=id)
    email_list=[]

    temp_email=list(User.objects.filter(pk=mahasiswa.objects.get(pk=jadwal_data.mahasiswa.nim).id_user.id).values_list('email',flat=True))
    email_list=email_list+temp_email

    temp_email=list(User.objects.filter(pk=dosen.objects.get(pk=jadwal_data.dosen_pembimbing_1.nip.nip).id_user.id).values_list('email',flat=True))
    email_list=email_list+temp_email

    try : 
        temp_email=list(User.objects.filter(pk=dosen.objects.get(pk=jadwal_data.dosen_pembimbing_2.nip.nip).id_user.id).values_list('email',flat=True))
        email_list=email_list+temp_email
    except:
        pass

    temp_email=list(User.objects.filter(pk=dosen.objects.get(pk=jadwal_data.dosen_penguji_1.nip.nip).id_user.id).values_list('email',flat=True))
    email_list=email_list+temp_email

    temp_email=list(User.objects.filter(pk=dosen.objects.get(pk=jadwal_data.dosen_penguji_2.nip.nip).id_user.id).values_list('email',flat=True))
    email_list=email_list+temp_email
    send_mail(
        'Jadwal Seminar Dihapus ',
        f"Anda Dihapus Dari Jadwal Seminar pada tanggal { jadwal_data.tanggal_seminar} dan jam {jadwal_data.waktu_seminar}  telah di hapus pada {tanggal} Jam {Jam}",
        settings.EMAIL_HOST_USER,
        email_list,
        fail_silently=
        False,
    )

    notifikasi.objects.create(nim=jadwal_data.mahasiswa.nim,messages=f"Terdapat penghapusan Jadwal untuk anda melakukan jadwal seminar sebagai peserta seminar pada tanggal {jadwal_data.tanggal_seminar} dan jam {jadwal_data.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
    notifikasi.objects.create(nip=jadwal_data.dosen_pembimbing_1.nip,messages=f"Terdapat penghapusan Jadwal untuk anda melakukan jadwal seminar sebagai pembimbing 1 mahasiswa {jadwal_data.mahasiswa} pada tanggal {jadwal_data.tanggal_seminar} dan jam {jadwal_data.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
    notifikasi.objects.create(nip=jadwal_data.dosen_pembimbing_2.nip,messages=f"Terdapat penghapusan Jadwal untuk anda melakukan jadwal seminar sebagai pembimbing 2 mahasiswa {jadwal_data.mahasiswa} pada tanggal {jadwal_data.tanggal_seminar} dan jam {jadwal_data.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
    notifikasi.objects.create(nip=jadwal_data.dosen_penguji_1.nip,messages=f"Terdapat penghapusan Jadwal untuk anda melakukan jadwal seminar sebagai penguji 1 mahasiswa {jadwal_data.mahasiswa} pada tanggal {jadwal_data.tanggal_seminar} dan jam {jadwal_data.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
    notifikasi.objects.create(nip=jadwal_data.dosen_penguji_2.nip,messages=f"Terdapat penghapusan Jadwal untuk anda melakukan jadwal seminar sebagai penguji 2 mahasiswa {jadwal_data.mahasiswa} pada tanggal {jadwal_data.tanggal_seminar} dan jam {jadwal_data.waktu_seminar}  telah di update pada {tanggal} Jam {Jam}")
    jadwal_data.delete()
    messages.error(request,"Data Jadwal Seminar Telah Berhasil Dihapus! ")
    return redirect('../jadwalget/nomorinduk')

# Jadwal Seminar : Read 
# Mengambil data Jadwal Seminar
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Mahasiswa','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_get(request):
    user_info = user_information(request)
    jadwal_data=jadwal_seminar.objects.all()
    return render(request, 'dosen/jadwal.html', {"jadwals": jadwal_data, "user_info": user_info})

# Jadwal Seminar : Read 
# Mengambil data Jadwal Seminar hari ini
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Mahasiswa','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_get_today(request):
    user_info = user_information(request)
    jadwal_data=jadwal_seminar.objects.filter(tanggal_seminar__gte=datetime.datetime.now().date())
    
    return render(request, 'dosen/jadwal.html', {"jadwals": jadwal_data, "user_info": user_info})

# checkpoint: check
# todo :  Jadwal Seminar masih bug untuk ditampilkan setelah hari inii 
# Jadwal Seminar : Read 
# Menampilkan list jadwal seminar dengan filter nomor induk
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Mahasiswa','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_mhs_dosen_get(request):
    user_info = user_information(request)
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        jadwal_data=jadwal_seminar.objects.filter(dosen_pembimbing_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_pembimbing_2__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_penguji_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_penguji_2__nip=user_info[0])
    elif user_info[2].name == "Mahasiswa":
        jadwal_data=jadwal_seminar.objects.filter(mahasiswa__nim=user_info[0])
    else:
        jadwal_data=jadwal_seminar.objects.all()
    return render(request, 'dosen/jadwal.html', {"jadwals": jadwal_data, "user_info": user_info})



@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Mahasiswa','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_mhs_dosen_get_all(request):
    user_info = user_information(request)
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        jadwal_data=jadwal_seminar.objects.filter(dosen_pembimbing_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_pembimbing_2__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_penguji_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_penguji_2__nip=user_info[0])
    else:
        jadwal_data=jadwal_seminar.objects.all()
    return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info})

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_dosen_bimbingan_tanpa_filter(request):
    user_info = user_information(request)
    role="Dosen Pembimbing"
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_pembimbing_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_pembimbing_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(role="Pembimbing 1")|roledosen.objects.filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(
                dosen_pembimbing_1__in=nim_list)|jadwal_data.filter(
                dosen_pembimbing_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
        
    # jumlah=0
    # for item in jadwal_data:
    #     if item.tahap_seminar=="Seminar Proposal":
    #         try:
    #             # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
    #             check_role= list(ambil_pembimbing.filter(
    #                 nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
    #             # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
    #             #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
    #             if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
    #                 jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
    #             else:
    #                 jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

    #         except:
    #             jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
    #     else :
    #         try:
    #             # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
    #             check_role= list(ambil_pembimbing.filter(
    #                 nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
    #             # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
    #             #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
    #             if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
    #                 jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
    #             else:
    #                 jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

    #         except:
    #             jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
    #     jumlah += 1

  

    jumlah=0  
    for item in jadwal_data:
        try:
            # cek_pembimbing
            tahap_list=[]
            status_dosen=False
            if item.dosen_pembimbing_2==None:
                status_dosen=True
            else:
                pass
                # detailpenilaian_data=list(detailpenilaian.objects.filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).values_list("id_role_dosen",flat=True))
                # hasil= len(detailpenilaian_data)
                # if hasil==4:
                #     status_dosen=True
            # print(item.dosen_pembimbing_2)       
            # print(status_dosen)
                   
            if item.tahap_seminar=="Seminar Proposal":
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=2  and status_dosen==True :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>=2 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian: Belum Ada Penilaian 2 Dosen Pembimbing"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                else :
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    jadwal_data[jumlah].tahap_penilaian = None
            else : 
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=2  and status_dosen==True :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>=2 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian: Belum Ada Penilaian 2 Dosen Pembimbing"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                else :
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    jadwal_data[jumlah].tahap_penilaian = None
        except : 
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
            jadwal_data[jumlah].tahap_penilaian = None
        
        if item.tahap_seminar=="Seminar Proposal":
            try:
                # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
                check_role= list(ambil_pembimbing.filter(
                    nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                    jadwal_data[jumlah].status_nilai1 = "Sudah Ada Penilaian"
                else:
                    jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"

            except:
                jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"
        else :
            try:
                # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
                check_role= list(ambil_pembimbing.filter(
                    nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                    jadwal_data[jumlah].status_nilai1 = "Sudah Ada Penilaian"
                else:
                    jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"

            except:
                jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"
        

        jumlah += 1
    # for item in jadwal_data: 
    #     # print(item.status, item.status == "ACC")
    #     if item.status_nilai != "Belum Di Nilai" :
    #         jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
            
            
    return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info,"role":role})
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Properta'])
def tabulasi_penilaian_no_filter(request):
    user_info = user_information(request)
    # role=""
    nim_list=[]
    role_dosen_list=[]
    
    ambil_pembimbing=roledosen.objects.filter(role="Pembimbing 1")|roledosen.objects.filter(role="Pembimbing 2")
    for item in ambil_pembimbing:
        role_dosen_list.append(item.id_role_dosen)
        nim_list.append(item.nim.nim)
        
    jadwal_data=jadwal_seminar.objects.all()
     
    try:
        mahasiswa_data=mahasiswa.objects.filter(nim__in=nim_list)
        jadwal_data=jadwal_data.filter(
                dosen_pembimbing_1__in=role_dosen_list)|jadwal_data.filter(
                dosen_pembimbing_2__in=role_dosen_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
    jumlah=0
    for item in mahasiswa_data:
        mahasiswa_data[jumlah].status_dosen_pembimbing="Admin"
        cek_pembimbing=roledosen.objects.filter(nim=item.nim).filter(role="Pembimbing 1")|roledosen.objects.filter(nim=item.nim).filter(role="Pembimbing 2")
        if cek_pembimbing.count() == 2:
            jumlah_penilaian_pembimbing=2
        else:
            jumlah_penilaian_pembimbing=1
        # print(jumlah_penilaian_pembimbing)
        # try :    
        detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus")
        if detailpenilaian_data.count() == jumlah_penilaian_pembimbing :
            mahasiswa_data[jumlah].status_bimbingan="Penilaian Bimbingan Sudah Lengkap"
            detailpenilaian_data_list=list(detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus").values_list("id_role_dosen__role",flat=True))
            mahasiswa_data[jumlah].tahap_bimbingan=detailpenilaian_data_list
            # mahasiswa_data[jumlah].tahap_bimbingan=None
        else:
            mahasiswa_data[jumlah].status_bimbingan="Penilaian Bimbingan Belum Lengkap"
            detailpenilaian_data_list=list(detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus").values_list("id_role_dosen__role",flat=True))
            mahasiswa_data[jumlah].tahap_bimbingan=detailpenilaian_data_list
        # except:

        
            
        cek_data_sempro=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus")
        if cek_data_sempro.count()==4 and cek_pembimbing.count() == 2:
            mahasiswa_data[jumlah].status_sempro="Penilaian Seminar Proposal Sudah Lengkap"
            detailpenilaian_data_list=list(detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus").values_list("id_role_dosen__role",flat=True))
            mahasiswa_data[jumlah].tahap_sempro=detailpenilaian_data_list
        elif cek_data_sempro.count()==3 and cek_pembimbing.count() ==1:
            mahasiswa_data[jumlah].status_sempro="Penilaian Seminar Proposal Sudah Lengkap"
            detailpenilaian_data_list=list(detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus").values_list("id_role_dosen__role",flat=True))
            mahasiswa_data[jumlah].tahap_sempro=detailpenilaian_data_list
        else:
            mahasiswa_data[jumlah].status_sempro="Penilaian Seminar Proposal Belum Lengkap"
            detailpenilaian_data_list=list(detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus").values_list("id_role_dosen__role",flat=True))
            mahasiswa_data[jumlah].tahap_sempro=detailpenilaian_data_list
        
        cek_data_semhas=detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus")
        if cek_data_semhas.count()==4 and cek_pembimbing.count() == 2:
            mahasiswa_data[jumlah].status_semhas="Penilaian Seminar Hasil Sudah Lengkap"
            detailpenilaian_data_list=list(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus").values_list("id_role_dosen__role",flat=True))
            mahasiswa_data[jumlah].tahap_semhas=detailpenilaian_data_list
        elif cek_data_semhas.count()==3 and cek_pembimbing.count() ==1:
            mahasiswa_data[jumlah].status_semhas="Penilaian Seminar Hasil Sudah Lengkap"
            detailpenilaian_data_list=list(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus").values_list("id_role_dosen__role",flat=True))
            mahasiswa_data[jumlah].tahap_semhas=detailpenilaian_data_list
        else:
            mahasiswa_data[jumlah].status_semhas="Penilaian Seminar Hasil Belum Lengkap"
            detailpenilaian_data_list=list(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus").values_list("id_role_dosen__role",flat=True))
            mahasiswa_data[jumlah].tahap_semhas=detailpenilaian_data_list
        jumlah+=1        
            
            
    return render(request, 'mahasiswa/mahasiswa_penilaian.html', {"mahasiswa_data": mahasiswa_data, "user_info": user_info})

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def tabulasi_penilaian(request):
    user_info = user_information(request)
    # role=""
    nim_list=[]
    role_dosen_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            role_dosen_list.append(item.id_role_dosen)
            nim_list.append(item.nim.nim)
        jadwal_data=jadwal_seminar.objects.filter(dosen_pembimbing_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_pembimbing_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            role_dosen_list.append(item.id_role_dosen)
            nim_list.append(item.nim.nim)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        mahasiswa_data=mahasiswa.objects.filter(nim__in=nim_list)
        jadwal_data=jadwal_data.filter(
                dosen_pembimbing_1__in=role_dosen_list)|jadwal_data.filter(
                dosen_pembimbing_2__in=role_dosen_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
    jumlah=0
    for item in mahasiswa_data:
        cek_pembimbing=roledosen.objects.filter(nim=item.nim).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nim=item.nim).filter(status="Active").filter(role="Pembimbing 2")
        if cek_pembimbing.count() == 2:
            jumlah_penilaian_pembimbing=2
        else:
            jumlah_penilaian_pembimbing=1
            
        if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
            ambil_pembimbing=roledosen.objects.filter(nim=item.nim).filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nim=item.nim).filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
            mahasiswa_data[jumlah].status_dosen_pembimbing=str(ambil_pembimbing.first().role)
        else:
            ambil_pembimbing=roledosen.objects.filter(nim=item.nim).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nim=item.nim).filter(status="Active").filter(role="Pembimbing 2")
            mahasiswa_data[jumlah].status_dosen_pembimbing="Admin"
                
        print(jumlah_penilaian_pembimbing)
        # try :    
        detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus")
        if detailpenilaian_data.count() == jumlah_penilaian_pembimbing :
            mahasiswa_data[jumlah].status_bimbingan="Penilaian Bimbingan Sudah Lengkap"
            detailpenilaian_data_list=list(detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus").values_list("id_role_dosen__role",flat=True))
            mahasiswa_data[jumlah].tahap_bimbingan=detailpenilaian_data_list
            # mahasiswa_data[jumlah].tahap_bimbingan=None
        else:
            mahasiswa_data[jumlah].status_bimbingan="Penilaian Bimbingan Belum Lengkap"
            detailpenilaian_data_list=list(detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus").values_list("id_role_dosen__role",flat=True))
            mahasiswa_data[jumlah].tahap_bimbingan=detailpenilaian_data_list
        # except:

        
            
        cek_data_sempro=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus")
        if cek_data_sempro.count()==4 and cek_pembimbing.count() == 2:
            mahasiswa_data[jumlah].status_sempro="Penilaian Seminar Proposal Sudah Lengkap"
            detailpenilaian_data_list=list(detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus").values_list("id_role_dosen__role",flat=True))
            mahasiswa_data[jumlah].tahap_sempro=detailpenilaian_data_list
        elif cek_data_sempro.count()==3 and cek_pembimbing.count() ==1:
            mahasiswa_data[jumlah].status_sempro="Penilaian Seminar Proposal Sudah Lengkap"
            detailpenilaian_data_list=list(detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus").values_list("id_role_dosen__role",flat=True))
            mahasiswa_data[jumlah].tahap_sempro=detailpenilaian_data_list
        else:
            mahasiswa_data[jumlah].status_sempro="Penilaian Seminar Proposal Belum Lengkap"
            detailpenilaian_data_list=list(detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus").values_list("id_role_dosen__role",flat=True))
            mahasiswa_data[jumlah].tahap_sempro=detailpenilaian_data_list
        
        cek_data_semhas=detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus")
        if cek_data_semhas.count()==4 and cek_pembimbing.count() == 2:
            mahasiswa_data[jumlah].status_semhas="Penilaian Seminar Hasil Sudah Lengkap"
            detailpenilaian_data_list=list(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus").values_list("id_role_dosen__role",flat=True))
            mahasiswa_data[jumlah].tahap_semhas=detailpenilaian_data_list
        elif cek_data_semhas.count()==3 and cek_pembimbing.count() ==1:
            mahasiswa_data[jumlah].status_semhas="Penilaian Seminar Hasil Sudah Lengkap"
            detailpenilaian_data_list=list(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus").values_list("id_role_dosen__role",flat=True))
            mahasiswa_data[jumlah].tahap_semhas=detailpenilaian_data_list
        else:
            mahasiswa_data[jumlah].status_semhas="Penilaian Seminar Hasil Belum Lengkap"
            detailpenilaian_data_list=list(detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__nim=item.nim).filter(status_kelulusan="Lulus").values_list("id_role_dosen__role",flat=True))
            mahasiswa_data[jumlah].tahap_semhas=detailpenilaian_data_list
        jumlah+=1        
            
            
    return render(request, 'mahasiswa/mahasiswa_penilaian.html', {"mahasiswa_data": mahasiswa_data, "user_info": user_info})

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Properta'])
def jadwal_dosen_bimbingan_no_filter_nim(request,nim):
    user_info = user_information(request)
    role="Dosen Pembimbing"
    nim_list=[]
   
    ambil_pembimbing=roledosen.objects.filter(role="Pembimbing 1")|roledosen.objects.filter(role="Pembimbing 2")
    for item in ambil_pembimbing:
        nim_list.append(item.id_role_dosen)
        
    jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(mahasiswa=nim).filter(
                dosen_pembimbing_1__in=nim_list)|jadwal_data.filter(
                dosen_pembimbing_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
        
    # jumlah=0
    # for item in jadwal_data:
    #     if item.tahap_seminar=="Seminar Proposal":
    #         try:
    #             # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
    #             check_role= list(ambil_pembimbing.filter(
    #                 nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
    #             # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
    #             #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
    #             if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
    #                 jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
    #             else:
    #                 jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

    #         except:
    #             jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
    #     else :
    #         try:
    #             # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
    #             check_role= list(ambil_pembimbing.filter(
    #                 nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
    #             # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
    #             #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
    #             if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
    #                 jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
    #             else:
    #                 jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

    #         except:
    #             jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
    #     jumlah += 1


    jumlah=0  
    for item in jadwal_data:
        try:
            # cek_pembimbing
            tahap_list=[]
            status_dosen=False
            if item.dosen_pembimbing_2==None:
                status_dosen=True
            else:
                pass
                # detailpenilaian_data=list(detailpenilaian.objects.filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).values_list("id_role_dosen",flat=True))
                # hasil= len(detailpenilaian_data)
                # if hasil==4:
                #     status_dosen=True
            # print(item.dosen_pembimbing_2)       
            # print(status_dosen)
                   
            if item.tahap_seminar=="Seminar Proposal":
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>=2  and status_dosen==True :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                else :
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    jadwal_data[jumlah].tahap_penilaian = None
            else : 
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>=2  and status_dosen==True :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                else :
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    jadwal_data[jumlah].tahap_penilaian = None
        except : 
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
            jadwal_data[jumlah].tahap_penilaian = None
        
        if item.tahap_seminar=="Seminar Proposal":
            try:
                # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
                check_role= list(ambil_pembimbing.filter(
                    nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                    jadwal_data[jumlah].status_nilai1 = "Sudah Ada Penilaian"
                else:
                    jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"

            except:
                jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"
        else :
            try:
                # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
                check_role= list(ambil_pembimbing.filter(
                    nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                    jadwal_data[jumlah].status_nilai1 = "Sudah Ada Penilaian"
                else:
                    jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"

            except:
                jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"
        

        jumlah += 1
            
    # for item in jadwal_data: 
    #     # print(item.status, item.status == "ACC")
    #     if item.status_nilai != "Belum Di Nilai" :
    #         jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
            
            
    return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info,"role":role})

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_dosen_bimbingan_filter_nim(request,nim):
    user_info = user_information(request)
    role="Dosen Pembimbing"
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_pembimbing_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_pembimbing_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(role="Pembimbing 1")|roledosen.objects.filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(mahasiswa=nim).filter(
                dosen_pembimbing_1__in=nim_list)|jadwal_data.filter(
                dosen_pembimbing_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
        
    # jumlah=0
    # for item in jadwal_data:
    #     if item.tahap_seminar=="Seminar Proposal":
    #         try:
    #             # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
    #             check_role= list(ambil_pembimbing.filter(
    #                 nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
    #             # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
    #             #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
    #             if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
    #                 jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
    #             else:
    #                 jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

    #         except:
    #             jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
    #     else :
    #         try:
    #             # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
    #             check_role= list(ambil_pembimbing.filter(
    #                 nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
    #             # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
    #             #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
    #             if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
    #                 jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
    #             else:
    #                 jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

    #         except:
    #             jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
    #     jumlah += 1


    jumlah=0  
    for item in jadwal_data:
        try:
            # cek_pembimbing
            tahap_list=[]
            status_dosen=False
            if item.dosen_pembimbing_2==None:
                status_dosen=True
            else:
                pass
                # detailpenilaian_data=list(detailpenilaian.objects.filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).values_list("id_role_dosen",flat=True))
                # hasil= len(detailpenilaian_data)
                # if hasil==4:
                #     status_dosen=True
            # print(item.dosen_pembimbing_2)       
            # print(status_dosen)
                   
            if item.tahap_seminar=="Seminar Proposal":
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>=2  and status_dosen==True :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                else :
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    jadwal_data[jumlah].tahap_penilaian = None
            else : 
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>=2  and status_dosen==True :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                else :
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    jadwal_data[jumlah].tahap_penilaian = None
        except : 
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
            jadwal_data[jumlah].tahap_penilaian = None
        
        if item.tahap_seminar=="Seminar Proposal":
            try:
                # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
                check_role= list(ambil_pembimbing.filter(
                    nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                    jadwal_data[jumlah].status_nilai1 = "Sudah Ada Penilaian"
                else:
                    jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"

            except:
                jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"
        else :
            try:
                # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
                check_role= list(ambil_pembimbing.filter(
                    nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                    jadwal_data[jumlah].status_nilai1 = "Sudah Ada Penilaian"
                else:
                    jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"

            except:
                jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"
        

        jumlah += 1
            
    # for item in jadwal_data: 
    #     # print(item.status, item.status == "ACC")
    #     if item.status_nilai != "Belum Di Nilai" :
    #         jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
            
            
    return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info,"role":role})


@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_dosen_bimbingan(request):
    user_info = user_information(request)
    role="Dosen Pembimbing"
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_pembimbing_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_pembimbing_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(
                dosen_pembimbing_1__in=nim_list)|jadwal_data.filter(
                dosen_pembimbing_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
    
    # jumlah=0
    # for item in jadwal_data:
    #     if item.tahap_seminar=="Seminar Proposal":
    #         try:
    #             # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
    #             check_role= list(ambil_pembimbing.filter(
    #                 nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
    #             # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
    #             #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
    #             if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
    #                 jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
    #             else:
    #                 jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

    #         except:
    #             jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
    #     else :
    #         try:
    #             # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
    #             check_role= list(ambil_pembimbing.filter(
    #                 nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
    #             # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
    #             #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
    #             if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
    #                 jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
    #             else:
    #                 jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

    #         except:
    #             jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
    #     jumlah += 1

  
    
    jumlah=0  
    for item in jadwal_data:
        # try:
            # cek_pembimbing
            tahap_list=[]
            status_dosen=False
            if item.dosen_pembimbing_2==None:
                status_dosen=True
            else:
                pass
                # detailpenilaian_data=list(detailpenilaian.objects.filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).values_list("id_role_dosen",flat=True))
                # hasil= len(detailpenilaian_data)
                # if hasil==4:
                #     status_dosen=True
            # print(item.dosen_pembimbing_2)       
            # print(status_dosen)
                   
            if item.tahap_seminar=="Seminar Proposal":
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                # print(status_dosen,item.id_jadwal_seminar)
                if len(tahap_list)>=4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>=2  and status_dosen==True :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                else :
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    jadwal_data[jumlah].tahap_penilaian = None
            else : 
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>=2  and status_dosen==True :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                else :
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    jadwal_data[jumlah].tahap_penilaian = None
                
            # if penilaian.objects.filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.mahasiswa).exists():
                
            #     jumlah_penilaian=list(penilaian.objects.filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.mahasiswa).order_by().values_list("id_detail_penilaian__nama_tahap",flat=True).distinct())
                
            #     # print(list(jumlah_penilaian))
            #     if len(jumlah_penilaian)==3  and status_dosen==True :
            #         jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
            #     elif len(jumlah_penilaian)==3 and status_dosen==False :
            #         jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian: Belum Ada Penilaian 2 Dosen Pembimbing"
            #     elif len(jumlah_penilaian)!=3:
            #         jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                
            #     jadwal_data[jumlah].tahap_penilaian = jumlah_penilaian
            # else:
            #     jadwal_data[jumlah].tahap_penilaian = None
            #     jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
            
        # except:
        #     jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        #     jadwal_data[jumlah].tahap_penilaian = None
            if item.tahap_seminar=="Seminar Proposal":
                try:
                    # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
                    check_role= list(ambil_pembimbing.filter(
                        nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
                    # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                    #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                    if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                        jadwal_data[jumlah].status_nilai1 = "Sudah Ada Penilaian"
                    else:
                        jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"

                except:
                    jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"
            else :
                try:
                    # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
                    check_role= list(ambil_pembimbing.filter(
                        nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
                    # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                    #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                    if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                        jadwal_data[jumlah].status_nilai1 = "Sudah Ada Penilaian"
                    else:
                        jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"

                except:
                    jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"
        
        
        
            jumlah += 1
            
    # for item in jadwal_data: 
    #     # print(item.status, item.status == "ACC")
    #     if item.status_nilai != "Belum Di Nilai" :
    #         jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
            
            
    return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info,"role":role})

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_dosen_bimbingan_belum_dinilai(request):
    user_info = user_information(request)
    role="Dosen Pembimbing"
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_pembimbing_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_pembimbing_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(
                dosen_pembimbing_1__in=nim_list)|jadwal_data.filter(
                dosen_pembimbing_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
    # jumlah=0
    # for item in jadwal_data:
    #     if item.tahap_seminar=="Seminar Proposal":
    #         try:
    #             # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
    #             check_role= list(ambil_pembimbing.filter(
    #                 nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
    #             # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
    #             #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
    #             if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
    #                 jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
    #             else:
    #                 jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

    #         except:
    #             jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
    #     else :
    #         try:
    #             # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
    #             check_role= list(ambil_pembimbing.filter(
    #                 nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
    #             # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
    #             #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
    #             if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
    #                 jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
    #             else:
    #                 jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

    #         except:
    #             jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
    #     jumlah += 1

  
    # for item in jadwal_data: 
    #     # print(item.status, item.status == "ACC")
    #     if item.status_nilai != "Belum Di Nilai" :
    #         jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
            
    jumlah=0  
    for item in jadwal_data:
        # try:
            # cek_pembimbing
            tahap_list=[]
            status_dosen=False
            if item.dosen_pembimbing_2==None:
                status_dosen=True
            else:
                pass
                # detailpenilaian_data=list(detailpenilaian.objects.filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).values_list("id_role_dosen",flat=True))
                # hasil= len(detailpenilaian_data)
                # if hasil==4:
                #     status_dosen=True
            # print(item.dosen_pembimbing_2)       
            # print(status_dosen)
                   
            if item.tahap_seminar=="Seminar Proposal":
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>=2  and status_dosen==True :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                else :
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    jadwal_data[jumlah].tahap_penilaian = None
            else : 
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>=2  and status_dosen==True :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                else :
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    jadwal_data[jumlah].tahap_penilaian = None
                
            # if penilaian.objects.filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.mahasiswa).exists():
                
            #     jumlah_penilaian=list(penilaian.objects.filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.mahasiswa).order_by().values_list("id_detail_penilaian__nama_tahap",flat=True).distinct())
                
            #     # print(list(jumlah_penilaian))
            #     if len(jumlah_penilaian)==3  and status_dosen==True :
            #         jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
            #     elif len(jumlah_penilaian)==3 and status_dosen==False :
            #         jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian: Belum Ada Penilaian 2 Dosen Pembimbing"
            #     elif len(jumlah_penilaian)!=3:
            #         jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                
            #     jadwal_data[jumlah].tahap_penilaian = jumlah_penilaian
            # else:
            #     jadwal_data[jumlah].tahap_penilaian = None
            #     jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
            
        # except:
        #     jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        #     jadwal_data[jumlah].tahap_penilaian = None
        
            jumlah += 1
            
    # for item in jadwal_data: 
    #     # print(item.status, item.status == "ACC")
    #     if item.status_nilai != "Belum Di Nilai" :
    #         jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
            
    for item in jadwal_data: 
        # print(item.status, item.status == "ACC")
        if item.status_nilai != "Belum Di Nilai" :
            jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
    jumlah=0  
    for item in jadwal_data:
        try:
            # cek_pembimbing
            tahap_list=[]
            status_dosen=False
            if item.dosen_pembimbing_2==None:
                status_dosen=True
            else:
                pass
                # detailpenilaian_data=list(detailpenilaian.objects.filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).values_list("id_role_dosen",flat=True))
                # hasil= len(detailpenilaian_data)
                # if hasil==4:
                #     status_dosen=True
            # print(item.dosen_pembimbing_2)       
            # print(status_dosen)
                   
            if item.tahap_seminar=="Seminar Proposal":
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>=2  and status_dosen==True :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                else :
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    jadwal_data[jumlah].tahap_penilaian = None
            else : 
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>=2  and status_dosen==True :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                else :
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    jadwal_data[jumlah].tahap_penilaian = None
        except : 
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
            jadwal_data[jumlah].tahap_penilaian = None
        
        if item.tahap_seminar=="Seminar Proposal":
            try:
                # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
                check_role= list(ambil_pembimbing.filter(
                    nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                    jadwal_data[jumlah].status_nilai1 = "Sudah Ada Penilaian"
                else:
                    jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"

            except:
                jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"
        else :
            try:
                # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
                check_role= list(ambil_pembimbing.filter(
                    nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                    jadwal_data[jumlah].status_nilai1 = "Sudah Ada Penilaian"
                else:
                    jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"

            except:
                jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"
        

        jumlah += 1
            
    return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info,"role":role})

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_dosen_bimbingan_sudah_dinilai(request):
    user_info = user_information(request)
    role="Dosen Pembimbing"
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_pembimbing_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_pembimbing_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(
                dosen_pembimbing_1__in=nim_list)|jadwal_data.filter(
                dosen_pembimbing_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
        
    # jumlah=0
    # for item in jadwal_data:
    #     if item.tahap_seminar=="Seminar Proposal":
    #         try:
    #             # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
    #             check_role= list(ambil_pembimbing.filter(
    #                 nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
    #             # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
    #             #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
    #             if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
    #                 jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
    #             else:
    #                 jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

    #         except:
    #             jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
    #     else :
    #         try:
    #             # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
    #             check_role= list(ambil_pembimbing.filter(
    #                 nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
    #             # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
    #             #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
    #             if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
    #                 jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
    #             else:
    #                 jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

    #         except:
    #             jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
    #     jumlah += 1

  
    # for item in jadwal_data: 
    #     # print(item.status, item.status == "ACC")
    #     if item.status_nilai == "Belum Di Nilai" :
    #         jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)    
    jumlah=0  
    for item in jadwal_data:
        try:
            # cek_pembimbing
            tahap_list=[]
            status_dosen=False
            if item.dosen_pembimbing_2==None:
                status_dosen=True
            else:
                pass
                # detailpenilaian_data=list(detailpenilaian.objects.filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).values_list("id_role_dosen",flat=True))
                # hasil= len(detailpenilaian_data)
                # if hasil==4:
                #     status_dosen=True
            # print(item.dosen_pembimbing_2)       
            # print(status_dosen)
                   
            if item.tahap_seminar=="Seminar Proposal":
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>=2  and status_dosen==True :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                else :
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    jadwal_data[jumlah].tahap_penilaian = None
            else : 
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>=2  and status_dosen==True :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                else :
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    jadwal_data[jumlah].tahap_penilaian = None
        except : 
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
            jadwal_data[jumlah].tahap_penilaian = None
        

        jumlah += 1
            
    for item in jadwal_data: 
        # print(item.status, item.status == "ACC")
        if item.status_nilai != "Sudah Ada Seluruh Penilaian" :
            jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
    jumlah=0  
    for item in jadwal_data:
        try:
            # cek_pembimbing
            tahap_list=[]
            status_dosen=False
            if item.dosen_pembimbing_2==None:
                status_dosen=True
            else:
                pass
                # detailpenilaian_data=list(detailpenilaian.objects.filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).values_list("id_role_dosen",flat=True))
                # hasil= len(detailpenilaian_data)
                # if hasil==4:
                #     status_dosen=True
            # print(item.dosen_pembimbing_2)       
            # print(status_dosen)
                   
            if item.tahap_seminar=="Seminar Proposal":
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>=2  and status_dosen==True :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                else :
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    jadwal_data[jumlah].tahap_penilaian = None
            else : 
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>=2  and status_dosen==True :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                else :
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    jadwal_data[jumlah].tahap_penilaian = None
        except : 
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
            jadwal_data[jumlah].tahap_penilaian = None
        if item.tahap_seminar=="Seminar Proposal":
            try:
                # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
                check_role= list(ambil_pembimbing.filter(
                    nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                    jadwal_data[jumlah].status_nilai1 = "Sudah Ada Penilaian"
                else:
                    jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"

            except:
                jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"
        else :
            try:
                # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
                check_role= list(ambil_pembimbing.filter(
                    nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                    jadwal_data[jumlah].status_nilai1 = "Sudah Ada Penilaian"
                else:
                    jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"

            except:
                jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"
        
        

        jumlah += 1
    return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info,"role":role})
            
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_dosen_bimbingan_sebagian_dinilai(request):
    user_info = user_information(request)
    role="Dosen Pembimbing"
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_pembimbing_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_pembimbing_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(status="Active").filter(role="Pembimbing 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(
                dosen_pembimbing_1__in=nim_list)|jadwal_data.filter(
                dosen_pembimbing_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
        
    # jumlah=0
    # for item in jadwal_data:
    #     if item.tahap_seminar=="Seminar Proposal":
    #         try:
    #             # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
    #             check_role= list(ambil_pembimbing.filter(
    #                 nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
    #             # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
    #             #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
    #             if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
    #                 jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
    #             else:
    #                 jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

    #         except:
    #             jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
    #     else :
    #         try:
    #             # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
    #             check_role= list(ambil_pembimbing.filter(
    #                 nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
    #             # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
    #             #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
    #             if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
    #                 jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
    #             else:
    #                 jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

    #         except:
    #             jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
    #     jumlah += 1

  
    # for item in jadwal_data: 
    #     # print(item.status, item.status == "ACC")
    #     if item.status_nilai == "Belum Di Nilai" :
    #         jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
            
    jumlah=0  
    for item in jadwal_data:
        try:
            # cek_pembimbing
            tahap_list=[]
            status_dosen=False
            if item.dosen_pembimbing_2==None:
                status_dosen=True
            else:
                pass
                # detailpenilaian_data=list(detailpenilaian.objects.filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).values_list("id_role_dosen",flat=True))
                # hasil= len(detailpenilaian_data)
                # if hasil==4:
                #     status_dosen=True
            # print(item.dosen_pembimbing_2)       
            # print(status_dosen)
                   
            if item.tahap_seminar=="Seminar Proposal":
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>=2  and status_dosen==True :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                else :
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    jadwal_data[jumlah].tahap_penilaian = None
            else : 
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>=2  and status_dosen==True :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                else :
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    jadwal_data[jumlah].tahap_penilaian = None
        except : 
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
            jadwal_data[jumlah].tahap_penilaian = None
        

        jumlah += 1
    for item in jadwal_data: 
        # print(item.status, item.status == "ACC")
        if item.status_nilai == "Belum Di Nilai" or item.status_nilai == "Sudah Ada Seluruh Penilaian" :
            jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
            
    jumlah=0  
    for item in jadwal_data:
        try:
            # cek_pembimbing
            tahap_list=[]
            status_dosen=False
            if item.dosen_pembimbing_2==None:
                status_dosen=True
            else:
                pass
                # detailpenilaian_data=list(detailpenilaian.objects.filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).values_list("id_role_dosen",flat=True))
                # hasil= len(detailpenilaian_data)
                # if hasil==4:
                #     status_dosen=True
            # print(item.dosen_pembimbing_2)       
            # print(status_dosen)
                   
            if item.tahap_seminar=="Seminar Proposal":
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>=2  and status_dosen==True :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                else :
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    jadwal_data[jumlah].tahap_penilaian = None
            else : 
                if  status_dosen==True  :
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True))
                else:
                    cek_roledosen=list(roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_1.id_role_dosen).values_list("id_role_dosen",flat=True)|roledosen.objects.filter(nim=item.mahasiswa).filter(id_role_dosen=item.dosen_pembimbing_2.id_role_dosen).values_list("id_role_dosen",flat=True))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap=item.tahap_seminar).filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).filter(id_role_dosen__in=cek_roledosen)
                # print(cek_penilaian)
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                cek_penilaian=  detailpenilaian.objects.filter(nama_tahap="Bimbingan").filter(id_role_dosen__nim=item.mahasiswa).filter(id_role_dosen__in=cek_roledosen)
                # tahap_list=tahap_list+cek_penilaian
                tahap_list=tahap_list+list(cek_penilaian.values_list("nama_tahap","id_role_dosen__role"))
                # print("",item.mahasiswa,cek_penilaian.values_list("id_role_dosen__role"))
                # print(tahap_list)
                if len(tahap_list)>=4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>=2  and status_dosen==True :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Seluruh Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<4 and status_dosen==False :
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                elif len(tahap_list)>0 and len(tahap_list)<2 and status_dosen==True:
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Sebagian Penilaian"
                    jadwal_data[jumlah].tahap_penilaian = tahap_list
                else :
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
                    jadwal_data[jumlah].tahap_penilaian = None
        except : 
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
            jadwal_data[jumlah].tahap_penilaian = None
            
        if item.tahap_seminar=="Seminar Proposal":
            try:
                # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
                check_role= list(ambil_pembimbing.filter(
                    nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                    jadwal_data[jumlah].status_nilai1 = "Sudah Ada Penilaian"
                else:
                    jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"

            except:
                jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"
        else :
            try:
                # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
                check_role= list(ambil_pembimbing.filter(
                    nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                    jadwal_data[jumlah].status_nilai1 = "Sudah Ada Penilaian"
                else:
                    jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"

            except:
                jadwal_data[jumlah].status_nilai1 = "Belum Di Nilai"
        

        jumlah += 1
            
    return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info,"role":role})

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_dosen_sempro_tanpa_filter(request):
    role="Dosen Seminar Proposal"
    user_info = user_information(request)
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Proposal 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_penguji_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_penguji_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(role="Penguji Seminar Proposal 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(
                dosen_penguji_1__in=nim_list)|jadwal_data.filter(
                dosen_penguji_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
    
    jumlah=0
    for item in jadwal_data:
            try:
                # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
                check_role= list(ambil_pembimbing.filter(
                    nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

            except:
                jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
           
            jumlah += 1
    
  
    # for item in jadwal_data: 
    #         # print(item.status, item.status == "ACC")
    #         if item.status_nilai != "Belum Di Nilai" :
    #             jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
    # cek_nilai = detailpenilaian.objects.filter(id_role_dosen__nip=)
    return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info,"role":role})

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_dosen_sempro(request):
    role="Dosen Seminar Proposal"
    user_info = user_information(request)
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Proposal 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_penguji_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_penguji_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Proposal 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(
                dosen_penguji_1__in=nim_list)|jadwal_data.filter(
                dosen_penguji_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
    
    jumlah=0
    for item in jadwal_data:
            try:
                # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
                check_role= list(ambil_pembimbing.filter(
                    nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

            except:
                jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
           
            jumlah += 1
    
  
    # for item in jadwal_data: 
    #         # print(item.status, item.status == "ACC")
    #         if item.status_nilai != "Belum Di Nilai" :
    #             jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
    # cek_nilai = detailpenilaian.objects.filter(id_role_dosen__nip=)
    return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info,"role":role})

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_dosen_sempro_belum_dinilai_tanpa_filter(request):
    role="Dosen Seminar Proposal"
    user_info = user_information(request)
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Proposal 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_penguji_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_penguji_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(role="Penguji Seminar Proposal 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(
                dosen_penguji_1__in=nim_list)|jadwal_data.filter(
                dosen_penguji_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
    
    jumlah=0
    for item in jadwal_data:
        try:
            # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
            check_role= list(ambil_pembimbing.filter(
                nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
            # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
            if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
            else:
                jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

        except:
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
        jumlah += 1

  
    for item in jadwal_data: 
        # print(item.status, item.status == "ACC")
        if item.status_nilai != "Belum Di Nilai" :
            jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
            
    jumlah=0
    for item in jadwal_data:
        try:
            # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
            check_role= list(ambil_pembimbing.filter(
                nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
            # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
            if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
            else:
                jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

        except:
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
        jumlah += 1
            
    return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info,"role":role})

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_dosen_sempro_belum_dinilai(request):
    role="Dosen Seminar Proposal"
    user_info = user_information(request)
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Proposal 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_penguji_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_penguji_2__nip=user_info[0])
        
    else:
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Proposal 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(
                dosen_penguji_1__in=nim_list)|jadwal_data.filter(
                dosen_penguji_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
    
    jumlah=0
    for item in jadwal_data:
        try:
            # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
            check_role= list(ambil_pembimbing.filter(
                nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
            # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
            if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
            else:
                jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

        except:
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
        jumlah += 1

  
    for item in jadwal_data: 
        # print(item.status, item.status == "ACC")
        if item.status_nilai != "Belum Di Nilai" :
            jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
            
    jumlah=0
    for item in jadwal_data:
        try:
            # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
            check_role= list(ambil_pembimbing.filter(
                nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
            # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
            if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
            else:
                jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

        except:
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
        jumlah += 1
            
    return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info,"role":role})

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_dosen_sempro_sudah_dinilai_tanpa_filter(request):
    role="Dosen Seminar Proposal"
    user_info = user_information(request)
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Proposal 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_penguji_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_penguji_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(role="Penguji Seminar Proposal 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(
                dosen_penguji_1__in=nim_list)|jadwal_data.filter(
                dosen_penguji_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
    
    jumlah=0
    for item in jadwal_data:
        try:
            # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
            check_role= list(ambil_pembimbing.filter(
                nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
            # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
            if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
            else:
                jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

        except:
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
        jumlah += 1

  
    for item in jadwal_data: 
        # print(item.status, item.status == "ACC")
        if item.status_nilai == "Belum Di Nilai" :
            jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
            
    jumlah=0
    for item in jadwal_data:
        try:
            # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
            check_role= list(ambil_pembimbing.filter(
                nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
            # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
            if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
            else:
                jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

        except:
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
        jumlah += 1
            
    return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info,"role":role})


@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_dosen_sempro_sudah_dinilai(request):
    role="Dosen Seminar Proposal"
    user_info = user_information(request)
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Proposal 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_penguji_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_penguji_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Proposal 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(
                dosen_penguji_1__in=nim_list)|jadwal_data.filter(
                dosen_penguji_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
    
    jumlah=0
    for item in jadwal_data:
        try:
            # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
            check_role= list(ambil_pembimbing.filter(
                nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
            # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
            if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
            else:
                jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

        except:
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
        jumlah += 1

  
    for item in jadwal_data: 
        # print(item.status, item.status == "ACC")
        if item.status_nilai == "Belum Di Nilai" :
            jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
            
    jumlah=0
    for item in jadwal_data:
        try:
            # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
            check_role= list(ambil_pembimbing.filter(
                nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
            # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
            if detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
            else:
                jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

        except:
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
        jumlah += 1
            
    return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info,"role":role})


@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_dosen_semhas_tanpa_filter(request):
    role="Dosen Seminar Hasil"
    user_info = user_information(request)
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Hasil 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_penguji_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_penguji_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(role="Penguji Seminar Hasil 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(
                dosen_penguji_1__in=nim_list)|jadwal_data.filter(
                dosen_penguji_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
        
    jumlah=0
    for item in jadwal_data:
            try:
                # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
                check_role= list(ambil_pembimbing.filter(
                    nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

            except:
                jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
           
            jumlah += 1
    # for item in jadwal_data: 
    #         # print(item.status, item.status == "ACC")
    #         if item.status_nilai != "Belum Di Nilai" :
    #             jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
    # cek_nilai = detailpenilaian.objects.filter(id_role_dosen__nip=)
    return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info,"role":role})

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_dosen_semhas(request):
    role="Dosen Seminar Hasil"
    user_info = user_information(request)
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Hasil 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_penguji_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_penguji_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Hasil 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(
                dosen_penguji_1__in=nim_list)|jadwal_data.filter(
                dosen_penguji_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
        
    jumlah=0
    for item in jadwal_data:
            try:
                # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
                check_role= list(ambil_pembimbing.filter(
                    nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
                # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
                #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
                if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                    jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
                else:
                    jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

            except:
                jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
           
            jumlah += 1
    # for item in jadwal_data: 
    #         # print(item.status, item.status == "ACC")
    #         if item.status_nilai != "Belum Di Nilai" :
    #             jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
    # cek_nilai = detailpenilaian.objects.filter(id_role_dosen__nip=)
    return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info,"role":role})

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_dosen_semhas_belum_dinilai_tanpa_filter(request):
    role="Dosen Seminar Hasil"
    user_info = user_information(request)
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Hasil 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_penguji_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_penguji_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(role="Penguji Seminar Hasil 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(
                dosen_penguji_1__in=nim_list)|jadwal_data.filter(
                dosen_penguji_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
        
    jumlah=0
    for item in jadwal_data:
        try:
            # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
            check_role= list(ambil_pembimbing.filter(
                nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
            # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
            if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
            else:
                jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

        except:
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
        jumlah += 1
    for item in jadwal_data: 
        # print(item.status, item.status == "ACC")
        if item.status_nilai != "Belum Di Nilai" :
            jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
                
    jumlah=0
    for item in jadwal_data:
        try:
            # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
            check_role= list(ambil_pembimbing.filter(
                nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
            # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
            if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
            else:
                jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

        except:
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
        jumlah += 1
    # cek_nilai = detailpenilaian.objects.filter(id_role_dosen__nip=)
    return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info,"role":role})


@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_dosen_semhas_belum_dinilai(request):
    role="Dosen Seminar Hasil"
    user_info = user_information(request)
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Hasil 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_penguji_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_penguji_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Hasil 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(
                dosen_penguji_1__in=nim_list)|jadwal_data.filter(
                dosen_penguji_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
        
    jumlah=0
    for item in jadwal_data:
        try:
            # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
            check_role= list(ambil_pembimbing.filter(
                nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
            # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
            if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
            else:
                jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

        except:
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
        jumlah += 1
    for item in jadwal_data: 
        # print(item.status, item.status == "ACC")
        if item.status_nilai != "Belum Di Nilai" :
            jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
                
    jumlah=0
    for item in jadwal_data:
        try:
            # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
            check_role= list(ambil_pembimbing.filter(
                nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
            # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
            if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
            else:
                jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

        except:
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
        jumlah += 1
    # cek_nilai = detailpenilaian.objects.filter(id_role_dosen__nip=)
    return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info,"role":role})

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_dosen_semhas_sudah_dinilai_tanpa_filter(request):
    role="Dosen Seminar Hasil"
    user_info = user_information(request)
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Hasil 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_penguji_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_penguji_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(role="Penguji Seminar Hasil 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(
                dosen_penguji_1__in=nim_list)|jadwal_data.filter(
                dosen_penguji_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
        
    jumlah=0
    for item in jadwal_data:
        try:
            # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
            check_role= list(ambil_pembimbing.filter(
                nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
            # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
            if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
            else:
                jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

        except:
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
        jumlah += 1
    for item in jadwal_data: 
        # print(item.status, item.status == "ACC")
        if item.status_nilai == "Belum Di Nilai" :
            jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
                
    jumlah=0
    for item in jadwal_data:
        try:
            # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
            check_role= list(ambil_pembimbing.filter(
                nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
            # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
            if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
            else:
                jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

        except:
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
        jumlah += 1
    # cek_nilai = detailpenilaian.objects.filter(id_role_dosen__nip=)
    return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info,"role":role})


@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def jadwal_dosen_semhas_sudah_dinilai(request):
    role="Dosen Seminar Hasil"
    user_info = user_information(request)
    nim_list=[]
    if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Penguji Seminar Hasil 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
        jadwal_data=jadwal_seminar.objects.filter(dosen_penguji_1__nip=user_info[0])|jadwal_seminar.objects.filter(dosen_penguji_2__nip=user_info[0])
    else:
        ambil_pembimbing=roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(status="Active").filter(role="Penguji Seminar Hasil 2")
        for item in ambil_pembimbing:
            nim_list.append(item.id_role_dosen)
            
        jadwal_data=jadwal_seminar.objects.all()
     
    try:
        jadwal_data=jadwal_data.filter(
                dosen_penguji_1__in=nim_list)|jadwal_data.filter(
                dosen_penguji_2__in=nim_list)
        # proposals = proposal.objects.all()

    except:
        jadwal_data = []
        
    jumlah=0
    for item in jadwal_data:
        try:
            # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
            check_role= list(ambil_pembimbing.filter(
                nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
            # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
            if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
            else:
                jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

        except:
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
        jumlah += 1
    for item in jadwal_data: 
        # print(item.status, item.status == "ACC")
        if item.status_nilai == "Belum Di Nilai" :
            jadwal_data=jadwal_data.exclude(id_jadwal_seminar=item.id_jadwal_seminar)
                
    jumlah=0
    for item in jadwal_data:
        try:
            # detailpenilaian_data=detailpenilaian.objects.filter(nama_tahap="Seminar Proposal").filter(id_role_dosen__nim=item.mahasiswa).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists()
            check_role= list(ambil_pembimbing.filter(
                nim=item.mahasiswa).values_list("id_role_dosen",flat=True))
            # print(penilaian.objects.filter(id_detail_penilaian__nama_tahap="Seminar Proposal").filter(id_detail_penilaian__id_role_dosen__in=check_role).filter(
            #     id_detail_penilaian__id_role_dosen__nim=item.nim).exists())
            if detailpenilaian.objects.filter(nama_tahap="Seminar Hasil").filter(id_role_dosen__in=check_role).filter(id_jadwal_seminar=item.id_jadwal_seminar).exists():
                jadwal_data[jumlah].status_nilai = "Sudah Ada Penilaian"
            else:
                jadwal_data[jumlah].status_nilai = "Belum Di Nilai"

        except:
            jadwal_data[jumlah].status_nilai = "Belum Di Nilai"
        
        jumlah += 1
    # cek_nilai = detailpenilaian.objects.filter(id_role_dosen__nip=)
    return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info,"role":role})


# @login_required(login_url="/login")
# @role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
# def jadwal_mhs_dosen_get_sempro(request):
#     user_info = user_information(request)
#     if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
#         jadwal_data=jadwal_seminar.objects.filter(nama_tahap="Seminar Proposal").filter(dosen_penguji_1__nip=user_info[0])|jadwal_seminar.objects.filter(nama_tahap="Seminar Proposal").filter(dosen_penguji_2__nip=user_info[0])
#     else:
#         jadwal_data=jadwal_seminar.objects.filter(nama_tahap="Seminar Proposal")
#     return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info})

# @login_required(login_url="/login")
# @role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
# def jadwal_mhs_dosen_get_semhas(request):
#     user_info = user_information(request)
#     if user_info[2].name == "Dosen" or user_info[2].name == "Manajemen Departemen" or user_info[2].name == "Kompartemen":
#         jadwal_data=jadwal_seminar.objects.filter(nama_tahap="Seminar Hasil").filter(dosen_penguji_1__nip=user_info[0])|jadwal_seminar.objects.filter(nama_tahap="Seminar Hasil").filter(dosen_penguji_2__nip=user_info[0])
#     else:
#         jadwal_data=jadwal_seminar.objects.filter(nama_tahap="Seminar Hasil")
#     return render(request, 'dosen/jadwal_penilaian.html', {"jadwals": jadwal_data, "user_info": user_info})


# Progress Mahasiswa
# Menampilkan list mahasiswa dan angkatan  dan progress
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def mahasiswa_jumlah_get(request):
    user_info = user_information(request)
    list_nim=[]
#     # Lulus
#     lulus_list=list(bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim"))
#     for i in range(len(lulus_list)):
#         list_nim.append(lulus_list[i][0])
#     # print("lulus",lulus_list)

#     # Sudah Bimbingan
#     proposals=bimbingan.objects.exclude(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update')
#     proposals_list=list(bimbingan.objects.exclude(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim").distinct())
 
#     for i in range (len(proposals_list)):
#              list_nim.append(proposals_list[i][0])
#     # print("proposal",list_nim)
#     proposals=proposals.annotate(nim_count=Count('id_proposal__nim'))
#     # print(proposals)
#     proposals_akhir=None
#     # print(set(proposals.values_list("id_proposal__nim", flat=True)))
#     for id in set(proposals.values_list("id_proposal__nim", flat=True)):
#         # print(id)
#         proposals1=proposals.filter(id_proposal__nim=id).values("id_proposal__nama_tahap","id_proposal__nim","id_proposal__nim__id_user__first_name","status_bimbingan")[:1]
#         # proposals1=proposals1.distinct()
#         # print(proposals1)
#         if proposals_akhir==None:
#             # print("here")
#             proposals_akhir=proposals1
#         else:
#             proposals_akhir=proposals_akhir|proposals1
#         # print(proposals_akhir)
#     try :
#         proposals_akhir=proposals_akhir.annotate(NIM_4=Cast('id_proposal__nim', output_field=CharField()))
#         proposals_akhir=proposals_akhir.annotate(NIM_5=Substr('NIM_4', 1, 2))
#         proposals_akhir=proposals_akhir.values('NIM_5',"id_proposal__nama_tahap","status_bimbingan").annotate(dcount=Count('NIM_5'))
#     except : 
#         proposals_akhir=[]
        
#     # print(proposals_akhir)

#     # Upload Proposal
#     # nim_proposal = proposal.objects.exclude(nim__in=list_nim).values_list('nim').distinct()
#     # print(nim_proposal)
#     proposal_upload = proposal.objects.order_by('-tanggal_update').exclude(nim__in=list_nim)
# proposal_upload = proposal_upload.filter(id_proposal__in=proposal_upload.values('nim').annotate(max_id=Max('id_proposal')).values('max_id'))
#     proposals_list2=list(proposal_upload.values_list("nim").distinct())
#     for i in range (len(proposals_list2)):
#         #  print(proposals_list[i])
#             list_nim.append(proposals_list2[i][0])
#     # print("proposal belum",list_nim)
#     # print(list_nim)
#     # nim_proposal=proposal_upload.values_list('nim','nama_tahap').distinct()
#     # print(nim_proposal)
#     proposal_upload=proposal_upload.annotate(NIM_4=Cast('nim', output_field=CharField()))
#     proposal_upload=proposal_upload.annotate(NIM_5=Substr('NIM_4', 1, 2))
#     proposal_upload=proposal_upload.values('NIM_5',"nama_tahap").annotate(dcount=Count('NIM_5'))
#     # print("proposal belum",proposal_upload)
#     # print("proposal belum",list_nim)


#     # Sudah dapat eval Topik
#     evaluasitopiks=evaluasitopik.objects.exclude(id_usulan_topik__nim__in=list_nim)
# evaluasitopiks = evaluasitopiks.filter(id_evaluasi_topik__in=evaluasitopiks.values('id_usulan_topik__nim').annotate(max_id=Max('id_evaluasi_topik')).values('max_id'))
#     # print(evaluasitopiks)
#     evaluasitopiks_list=list(evaluasitopiks.values_list("id_usulan_topik__nim").distinct())
#     # print(evaluasitopiks_list)
#     for i in range (len(evaluasitopiks_list)):
#         #  print(proposals_list[i])
#             list_nim.append(evaluasitopiks_list[i][0])
#     # print("eval topik",list_nim)
#     evaluasitopiks=evaluasitopiks.annotate(NIM_4=Cast('id_usulan_topik__nim', output_field=CharField()))
#     evaluasitopiks=evaluasitopiks.annotate(NIM_5=Substr('NIM_4', 1, 2))
#     evaluasitopiks=evaluasitopiks.values('NIM_5',"status_topik").annotate(dcount=Count('NIM_5'))
#     # print(evaluasitopiks)

#    # Sudah Mengerjakan Topik
#     usulantopiks=usulantopik.objects.exclude(nim__in=list_nim)
#     # print(usulantopiks)
#     usulantopiks_list=list(usulantopiks.values_list("nim").distinct())
#     # print(usulantopiks_list)
#     for i in range (len(usulantopiks_list)):
#         #  print(proposals_list[i])
#             list_nim.append(usulantopiks_list[i][0])
#     # print("usul topik",list_nim)
#     usulantopiks=usulantopiks.annotate(NIM_4=Cast('nim', output_field=CharField()))
#     usulantopiks=usulantopiks.annotate(NIM_5=Substr('NIM_4', 1, 2))
#     usulantopiks=usulantopiks.values('NIM_5').annotate(dcount=Count('NIM_5'))

#     # Belum Buat Topik
#     nim_topik=evaluasitopik.objects.exclude(id_usulan_topik__nim__in=list_nim).values_list('id_usulan_topik__nim')
#     mahasiswa_topik=mahasiswa.objects.exclude(nim__in=list_nim)
#     # print(mahasiswa_topik)
#     mahasiswa_topik=mahasiswa_topik.annotate(NIM_4=Cast('nim', output_field=CharField()))
#     mahasiswa_topik=mahasiswa_topik.annotate(NIM_5=Substr('NIM_4', 1, 2))
#     mahasiswa_topik=mahasiswa_topik.values('NIM_5').annotate(dcount=Count('NIM_5'))
#     # print(mahasiswa_topik)
    
    # Lulus
    lulus_list=list(bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim"))
    for i in range(len(lulus_list)):
        list_nim.append(lulus_list[i][0])
    # print("lulus",lulus_list)

    # Sudah Bimbingan
    proposals=bimbingan.objects.exclude(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update')
    proposals_list=list(bimbingan.objects.exclude(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim").distinct())
 
    for i in range (len(proposals_list)):
             list_nim.append(proposals_list[i][0])
    # print("proposal",list_nim)
    proposals=proposals.annotate(nim_count=Count('id_proposal__nim'))
    # print(proposals)
    proposals_akhir=None
    # print(set(proposals.values_list("id_proposal__nim", flat=True)))
    for id in set(proposals.values_list("id_proposal__nim", flat=True)):
        # print(id)
        proposals1=proposals.filter(id_proposal__nim=id).values("id_proposal__nama_tahap","id_proposal__nim","id_proposal__nim__id_user__first_name","status_bimbingan")[:1]
        # proposals1=proposals1.distinct()
        # print(proposals1)
        if proposals_akhir==None:
            # print("here")
            proposals_akhir=proposals1
        else:
            proposals_akhir=proposals_akhir|proposals1
        # print(proposals_akhir)
    try : 
        proposals_akhir=proposals_akhir.annotate(NIM_4=Cast('id_proposal__nim__angkatan', output_field=CharField()))
        # proposals_akhir=proposals_akhir.annotate(NIM_5=Substr('NIM_4', 1, 2))
        proposals_akhir=proposals_akhir.values('NIM_4',"id_proposal__nama_tahap","status_bimbingan").annotate(dcount=Count('NIM_4'))
        # print(proposals_akhir)
    except : 
        pass
    # Upload Proposal
    # nim_proposal = proposal.objects.exclude(nim__in=list_nim).values_list('nim').distinct()
    # print(nim_proposal)
    proposal_upload = proposal.objects.order_by('-tanggal_update').exclude(nim__in=list_nim)
    proposal_upload = proposal_upload.filter(id_proposal__in=proposal_upload.values('nim').annotate(max_id=Max('id_proposal')).values('max_id'))
    proposals_list2=list(proposal_upload.values_list("nim").distinct())
    for i in range (len(proposals_list2)):
        #  print(proposals_list[i])
            list_nim.append(proposals_list2[i][0])
    # print("proposal belum",list_nim)
    # print(list_nim)
    # nim_proposal=proposal_upload.values_list('nim','nama_tahap').distinct()
    # print(nim_proposal)
    proposal_upload=proposal_upload.annotate(NIM_4=Cast('nim__angkatan', output_field=CharField()))
    # proposal_upload=proposal_upload.annotate(NIM_5=Substr('NIM_4', 1, 2))
    proposal_upload=proposal_upload.values('NIM_4',"nama_tahap").annotate(dcount=Count('NIM_4'))
    # print("proposal belum",proposal_upload)
    # print("proposal belum",list_nim)


    # Sudah dapat eval Topik
    evaluasitopiks=evaluasitopik.objects.exclude(id_usulan_topik__nim__in=list_nim)
    evaluasitopiks = evaluasitopiks.filter(id_evaluasi_topik__in=evaluasitopiks.values('id_usulan_topik__nim').annotate(max_id=Max('id_evaluasi_topik')).values('max_id'))
    # print(evaluasitopiks)
    evaluasitopiks_list=list(evaluasitopiks.values_list("id_usulan_topik__nim").distinct())
    # print(evaluasitopiks_list)
    for i in range (len(evaluasitopiks_list)):
        #  print(proposals_list[i])
            list_nim.append(evaluasitopiks_list[i][0])
    # print("eval topik",list_nim)
    evaluasitopiks=evaluasitopiks.annotate(NIM_4=Cast('id_usulan_topik__nim__angkatan', output_field=CharField()))
    # evaluasitopiks=evaluasitopiks.annotate(NIM_5=Substr('NIM_4', 1, 2))
    evaluasitopiks=evaluasitopiks.values('NIM_4',"status_topik").annotate(dcount=Count('NIM_4'))
    # print(evaluasitopiks)

   # Sudah Mengerjakan Topik
    usulantopiks=usulantopik.objects.exclude(nim__in=list_nim)
    usulantopiks = usulantopiks.filter(id_usulan_topik__in=usulantopiks.values('nim').annotate(max_id=Max('id_usulan_topik')).values('max_id'))
    # print(usulantopiks)
    usulantopiks_list=list(usulantopiks.values_list("nim").distinct())
    # print(usulantopiks_list)
    for i in range (len(usulantopiks_list)):
        #  print(proposals_list[i])
            list_nim.append(usulantopiks_list[i][0])
    # print("usul topik",list_nim)
    usulantopiks=usulantopiks.annotate(NIM_4=Cast('nim__angkatan', output_field=CharField()))
    # usulantopiks=usulantopiks.annotate(NIM_5=Substr('NIM_4', 1, 2))
    usulantopiks=usulantopiks.values('NIM_4').annotate(dcount=Count('NIM_4'))

    # Belum Buat Topik
    nim_topik=evaluasitopik.objects.exclude(id_usulan_topik__nim__in=list_nim).values_list('id_usulan_topik__nim')
    mahasiswa_topik=mahasiswa.objects.exclude(nim__in=list_nim)
    # print(mahasiswa_topik)
    mahasiswa_topik=mahasiswa_topik.annotate(NIM_4=Cast('angkatan', output_field=CharField()))
    # mahasiswa_topik=mahasiswa_topik.annotate(NIM_5=Substr('NIM_4', 1, 2))
    mahasiswa_topik=mahasiswa_topik.values('NIM_4').annotate(dcount=Count('NIM_4'))
    # print(mahasiswa_topik)


    return render(request, 'mahasiswa/mahasiswa_angkatan.html', {"proposals": proposals_akhir
                                                                 ,"mahasiswa_topik":mahasiswa_topik
                                                                 ,"evaluasitopiks":evaluasitopiks,
                                                                 "proposal_upload":proposal_upload,
                                                                 "usulantopiks":usulantopiks,
                                                                   "user_info": user_info})


# Progress Mahasiswa
# Menampilkan list mahasiswa dan angkatan  dan progress
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def mahasiswa_jumlah_get_progress(request):
    user_info = user_information(request)
    list_nim=[]
    list_progress=[]
    list_progress_jumlah=[]
    # Lulus
    lulus_list=list(bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim"))
    for i in range(len(lulus_list)):
        list_nim.append(lulus_list[i][0])
    # print("lulus",lulus_list)

    # Sudah Bimbingan
    proposals=bimbingan.objects.exclude(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update')
    proposals_list=list(bimbingan.objects.exclude(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim").distinct())
 
    for i in range (len(proposals_list)):
             list_nim.append(proposals_list[i][0])
    # print("proposal",list_nim)
    proposals=proposals.annotate(nim_count=Count('id_proposal__nim'))
    # print(proposals)
    proposals_akhir=None
    # print(set(proposals.values_list("id_proposal__nim", flat=True)))
    for id in set(proposals.values_list("id_proposal__nim", flat=True)):
        # print(id)
        proposals1=proposals.filter(id_proposal__nim=id).values("id_proposal__nama_tahap","id_proposal__nim","id_proposal__nim__id_user__first_name","status_bimbingan")[:1]
        # proposals1=proposals1.distinct()
        # print(proposals1)
        if proposals_akhir==None:
            # print("here")
            proposals_akhir=proposals1
        else:
            proposals_akhir=proposals_akhir|proposals1
        # print(proposals_akhir)
    
    proposals_akhir=proposals_akhir.values("id_proposal__nama_tahap","status_bimbingan").annotate(dcount=Count("*"))
    # print(proposals_akhir)

    for item in proposals_akhir:
        # print(item)
        list_progress_jumlah.append(item["dcount"])
        list_progress.append(item["id_proposal__nama_tahap"] +" : "+ item["status_bimbingan"])

    # Upload Proposal
    proposal_upload = proposal.objects.order_by('-tanggal_update').exclude(nim__in=list_nim)
    proposal_upload = proposal_upload.filter(id_proposal__in=proposal_upload.values('nim').annotate(max_id=Max('id_proposal')).values('max_id'))
    proposals_list2=list(proposal_upload.values_list("nim").distinct())
    for i in range (len(proposals_list2)):
            list_nim.append(proposals_list2[i][0])

    proposal_upload=proposal_upload.values("nama_tahap").annotate(dcount=Count('nama_tahap'))
    # print("apa",proposal_upload)
    for item in proposal_upload:
        list_progress_jumlah.append(item["dcount"])
        list_progress.append(item["nama_tahap"]  +" : "+ "Belum Diperiksa Dosen")

    # Sudah dapat eval Topik
    evaluasitopiks=evaluasitopik.objects.exclude(id_usulan_topik__nim__in=list_nim)
    evaluasitopiks = evaluasitopiks.filter(id_evaluasi_topik__in=evaluasitopiks.values('id_usulan_topik__nim').annotate(max_id=Max('id_evaluasi_topik')).values('max_id'))
    evaluasitopiks_list=list(evaluasitopiks.values_list("id_usulan_topik__nim").distinct())
    for i in range (len(evaluasitopiks_list)):

            list_nim.append(evaluasitopiks_list[i][0])
    evaluasitopiks=evaluasitopiks.values("status_topik").annotate(dcount=Count('*'))

    for item in evaluasitopiks:
        list_progress_jumlah.append(item["dcount"])
        list_progress.append( "Topik : "+ item["status_topik"])
    # list_progress_jumlah.append(evaluasitopiks.filter(status_topik="ACC").count())
    # list_progress.append("Topik : ACC")
    # list_progress_jumlah.append(evaluasitopiks.filter(status_topik="Revisi").count())
    # list_progress.append("Topik : Revisi")
    # list_progress_jumlah.append(evaluasitopiks.filter(status_topik="Submit").count())
    # list_progress.append("Topik : Submit")
    # list_progress_jumlah.append(evaluasitopiks.filter(status_topik="Dalam Evaluasi").count())
    # list_progress.append("Topik : Dalam Evaluasi")

   # Sudah Mengerjakan Topik
    usulantopiks=usulantopik.objects.exclude(nim__in=list_nim)
    usulantopiks = usulantopiks.filter(id_usulan_topik__in=usulantopiks.values('nim').annotate(max_id=Max('id_usulan_topik')).values('max_id'))
    # print(usulantopiks)
    usulantopiks_list=list(usulantopiks.values_list("nim").distinct())
    # print(usulantopiks_list)
    for i in range (len(usulantopiks_list)):
        #  print(proposals_list[i])
            list_nim.append(usulantopiks_list[i][0])
    list_progress_jumlah.append(usulantopiks.count())
    list_progress.append("Topik : Sudah Submit")
   

    # Belum Buat Topik
    mahasiswa_topik=mahasiswa.objects.exclude(nim__in=list_nim).count()
    list_progress_jumlah.append(mahasiswa_topik)
    list_progress.append("Belum Membuat Topik")


    # print(mahasiswa_topik)


    return render(request, 'mahasiswa/mahasiswa_angkatan_2.html', {"list_progress": list_progress
                                                                 ,"list_progress_jumlah":list_progress_jumlah,
                                                                   "user_info": user_info})

# tabulasi jumlah pesrta skripsi berdasarkan tahun angkatan 
def mahasiswa_jumlah_get_tahun(request):
    user_info = user_information(request)
    list_nim=[]
    # Lulus
    lulus_list=list(bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim"))
    for i in range(len(lulus_list)):
        list_nim.append(lulus_list[i][0])

    # Sudah Bimbingan
    proposals=bimbingan.objects.exclude(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update')
    proposals_list=list(bimbingan.objects.exclude(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim").distinct())
    for i in range (len(proposals_list)):
             list_nim.append(proposals_list[i][0])
    proposals=proposals.annotate(nim_count=Count('id_proposal__nim'))
    proposals_akhir=None
    for id in set(proposals.values_list("id_proposal__nim", flat=True)):
        proposals1=proposals.filter(id_proposal__nim=id).values("id_proposal__nama_tahap","id_proposal__nim","id_proposal__nim__id_user__first_name","status_bimbingan")[:1]
        if proposals_akhir==None:
            proposals_akhir=proposals1
        else:
            proposals_akhir=proposals_akhir|proposals1


    # Upload Proposal
    proposal_upload = proposal.objects.order_by('-tanggal_update').exclude(nim__in=list_nim)
    proposal_upload = proposal_upload.filter(id_proposal__in=proposal_upload.values('nim').annotate(max_id=Max('id_proposal')).values('max_id'))
    proposals_list2=list(proposal_upload.values_list("nim").distinct())
    for i in range (len(proposals_list2)):
            list_nim.append(proposals_list2[i][0])

    # Sudah dapat eval Topik
    evaluasitopiks=evaluasitopik.objects.exclude(id_usulan_topik__nim__in=list_nim)
    evaluasitopiks = evaluasitopiks.filter(id_evaluasi_topik__in=evaluasitopiks.values('id_usulan_topik__nim').annotate(max_id=Max('id_evaluasi_topik')).values('max_id'))
    evaluasitopiks_list=list(evaluasitopiks.values_list("id_usulan_topik__nim").distinct())
    for i in range (len(evaluasitopiks_list)):
            list_nim.append(evaluasitopiks_list[i][0])

   # Sudah Mengerjakan Topik
    usulantopiks=usulantopik.objects.exclude(nim__in=list_nim)
    usulantopiks = usulantopiks.filter(id_usulan_topik__in=usulantopiks.values('nim').annotate(max_id=Max('id_usulan_topik')).values('max_id'))
    usulantopiks_list=list(usulantopiks.values_list("nim").distinct())
    for i in range (len(usulantopiks_list)):
        #  print(proposals_list[i])
            list_nim.append(usulantopiks_list[i][0])


    # Belum Buat Topik
    mahasiswa_topik=mahasiswa.objects.exclude(nim__in=list_nim)
    mahasiswa_topiks_list=list(mahasiswa_topik.values_list("nim").distinct())
    for i in range (len(mahasiswa_topiks_list)):
        #  print(proposals_list[i])
            list_nim.append(mahasiswa_topiks_list[i][0])


    list_nim=list(set(list_nim))
    # list_angkatan=[]
    # for item in list_nim:
    #     # print(2000+(int(str(item)[0:2])))
    #     list_angkatan.append(2000+(int(str(item)[0:2])))
    # list_angkatan_unique=list(set(list_angkatan))
    # list_angkatan_unique.sort(reverse=True)
    list_angkatan=[]
    for item in list_nim:
        # print(2000+(int(str(item)[0:2])))
        list_angkatan.append(mahasiswa.objects.get(nim=item).angkatan)
    list_angkatan_unique=list(set(list_angkatan))
    list_angkatan_unique.sort(reverse=True)
    list_jumlah_angkatan=[]
    for i in list_angkatan_unique:
        list_jumlah_angkatan.append(list_angkatan.count(i))
    # print(list_angkatan_unique)
    # print(list_jumlah_angkatan)
    # print(list_nim)
    
    total_mahasiswa=sum(list_jumlah_angkatan)

    return render(request, 'mahasiswa/mahasiswa_angkatan_angka.html', {"list_angkatan_unique": list_angkatan_unique
                                                                 ,"list_jumlah_angkatan":list_jumlah_angkatan,
                                                                    "total_mahasiswa":total_mahasiswa,
                                                                   "user_info": user_info})

# Progress Mahasiswa
# Membuat data Progreess mahasiswa bersama progress dan marking mahasiswa berhenti mengerjakan skripsi selama 3-6 buln 
# todo add progress 3 bulan 6 bulan peringatan
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
def mahasiswa_progress_by_bulan(request):
    user_info = user_information(request)
    list_nim=[]

    # Lulus
    lulus_mhs=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim").annotate(Tanggal_Update_Terakhir=datetime.datetime.now()-Max("tanggal_update"))
    lulus_list=list(bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim"))
    for i in range(len(lulus_list)):
        list_nim.append(lulus_list[i][0])

    # Sudah Bimbingan
    proposals=bimbingan.objects.exclude(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update')
    proposals_list=list(bimbingan.objects.exclude(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim").distinct())
    for i in range(len(proposals_list)):

        list_nim.append(proposals_list[i][0])
    proposals=proposals.annotate(nim_count=Count('id_proposal__nim'))
    proposals_akhir=[]
    for id in set(proposals.values_list("id_proposal__nim", flat=True)):
        proposals_akhir.append(proposals.filter(id_proposal__nim=id).values(NamaTahap=F("id_proposal__nama_tahap"),nim=F("id_proposal__nim"),Nama=F("id_proposal__nim__id_user__first_name"),status=F("status_bimbingan")).annotate(Tanggal_Update_Terakhir=datetime.datetime.now()-Max("tanggal_update")).first())

    # Upload Proposal
    proposal_upload = proposal.objects.order_by('-tanggal_update').exclude(nim__in=list_nim).annotate(Tanggal_Update_Terakhir=datetime.datetime.now()-Max("tanggal_update"))
    proposal_upload = proposal_upload.filter(id_proposal__in=proposal_upload.values('nim').annotate(max_id=Max('id_proposal')).values('max_id'))
    proposals_list2=list(proposal_upload.values_list("nim").distinct())
    for i in range (len(proposals_list2)):
            list_nim.append(proposals_list2[i][0])
    
    # Sudah dapat eval Topik
    evaluasitopiks=evaluasitopik.objects.exclude(id_usulan_topik__nim__in=list_nim).annotate(Tanggal_Update_Terakhir=datetime.datetime.now()-Max("tanggal_update"))
    evaluasitopiks = evaluasitopiks.filter(id_evaluasi_topik__in=evaluasitopiks.values('id_usulan_topik__nim').annotate(max_id=Max('id_evaluasi_topik')).values('max_id'))
    evaluasitopiks_list=list(evaluasitopiks.values_list("id_usulan_topik__nim").distinct())
    # print(evaluasitopiks_list)
    for i in range (len(evaluasitopiks_list)):
            list_nim.append(evaluasitopiks_list[i][0])


    # Sudah Mengerjakan Topik
    # usulantopiks=usulantopik.objects.exclude(nim__in=list_nim).annotate(Tanggal_Update_Terakhir=datetime.datetime.now().date()-Max("tanggal_update")).distinct()
    
    usulantopiks = usulantopik.objects.exclude(nim__in=list_nim).annotate(Tanggal_Update_Terakhir=datetime.datetime.now().date() - Max("tanggal_update"))
    usulantopiks = usulantopiks.filter(id_usulan_topik__in=usulantopiks.values('nim').annotate(max_id=Max('id_usulan_topik')).values('max_id'))
    
    # print(usulantopiks)
    usulantopiks_list=list(usulantopiks.values_list("nim").distinct())
    # print(len(usulantopiks_list))
    for i in range (len(usulantopiks_list)):
            list_nim.append(usulantopiks_list[i][0])

    # Belum Buat Topik
    mahasiswa_topik=mahasiswa.objects.exclude(nim__in=list_nim).annotate(Tanggal_Update_Terakhir=datetime.datetime.now().date()-Max("id_user__date_joined"))

    update_terakhir=[]
    for i in proposals_akhir:
        update_terakhir.append(i["Tanggal_Update_Terakhir"].days)
    for i in mahasiswa_topik:
        update_terakhir.append(i.Tanggal_Update_Terakhir.days)
    for i in proposal_upload:
        update_terakhir.append(i.Tanggal_Update_Terakhir.days)
    for i in usulantopiks:
        update_terakhir.append(i.Tanggal_Update_Terakhir.days)
    for i in evaluasitopiks:
        update_terakhir.append(i.Tanggal_Update_Terakhir.days)
    jumlah_diatas_3_bulan=sum(i>90 for i in update_terakhir)
    # print(jumlah_diatas_3_bulan)
    # print(proposals_akhir,"1")
    # print(list(set(mahasiswa_topik)),"2")
    # print(proposal_upload,"3")
    # print(usulantopiks,"4")
    # print(lulus_mhs,"5")
    # print(evaluasitopiks,"6")

    return render(request, 'mahasiswa/mahasiswa_progress_with_marker.html', {"proposals": proposals_akhir,
                                                                             "mahasiswa_topik":mahasiswa_topik,
                                                                             "proposal_upload":proposal_upload,
                                                                             "usulantopiks":usulantopiks,                                                                     "usulantopiks":usulantopiks,
                                                                             "lulusmhs":lulus_mhs,
                                                                             "evaluasitopiks":evaluasitopiks, 
                                                                             "user_info": user_info})

@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])
# progresss mahasiswa : penampilan hari terakhir bimbingan
def mahasiswa_progress_by_bulan_dosen(request):
    user_info = user_information(request)
    
    # nim_list=[]
    if user_info[2].name != "Mahasiswa":
        ambil_pembimbing=roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(status="Active").filter(role="Pembimbing 2")
        # print("peniliannya",list_nim_penilaian)

    # for item in ambil_pembimbing:
    #     nim_list.append(item.nim.nim)
    nim_list=list(ambil_pembimbing.values_list("nim__nim",flat=True))
    # print("my",nim_list)
    
    list_nim=[]

    # Lulus
    lulus_mhs=bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim").annotate(Tanggal_Update_Terakhir=datetime.datetime.now()-Max("tanggal_update"))
    lulus_list=list(bimbingan.objects.filter(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim"))
    for i in range(len(lulus_list)):
        list_nim.append(lulus_list[i][0])

    # Sudah Bimbingan
    proposals=bimbingan.objects.exclude(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update')
    proposals=proposals.filter(id_proposal__nim__nim__in=nim_list)
    proposals_list=list(bimbingan.objects.exclude(id_proposal__nama_tahap="Laporan Akhir (Revisi Seminar Hasil)",status_bimbingan="ACC").order_by('-tanggal_update').values_list("id_proposal__nim").distinct())
    for i in range(len(proposals_list)):

        list_nim.append(proposals_list[i][0])
    proposals=proposals.annotate(nim_count=Count('id_proposal__nim'))
    proposals_akhir=[]
    for id in set(proposals.values_list("id_proposal__nim", flat=True)):
        proposals_akhir.append(proposals.filter(id_proposal__nim=id).values(NamaTahap=F("id_proposal__nama_tahap"),nim=F("id_proposal__nim"),Nama=F("id_proposal__nim__id_user__first_name"),status=F("status_bimbingan")).annotate(Tanggal_Update_Terakhir=datetime.datetime.now()-Max("tanggal_update")).first())

    # Upload Proposal
    proposal_upload = proposal.objects.order_by('-tanggal_update').exclude(nim__in=list_nim).annotate(Tanggal_Update_Terakhir=datetime.datetime.now()-Max("tanggal_update"))
    proposal_upload = proposal_upload.filter(id_proposal__in=proposal_upload.values('nim').annotate(max_id=Max('id_proposal')).values('max_id'))
    proposal_upload = proposal_upload.filter(nim__nim__in=nim_list)
    proposals_list2=list(proposal_upload.values_list("nim").distinct())
    for i in range (len(proposals_list2)):
            list_nim.append(proposals_list2[i][0])
    
    # Sudah dapat eval Topik
    evaluasitopiks=evaluasitopik.objects.exclude(id_usulan_topik__nim__in=list_nim).annotate(Tanggal_Update_Terakhir=datetime.datetime.now()-Max("tanggal_update"))
    evaluasitopiks = evaluasitopiks.filter(id_evaluasi_topik__in=evaluasitopiks.values('id_usulan_topik__nim').annotate(max_id=Max('id_evaluasi_topik')).values('max_id'))
    evaluasitopiks=evaluasitopiks.filter(id_usulan_topik__nim__nim__in=nim_list)
    evaluasitopiks_list=list(evaluasitopiks.values_list("id_usulan_topik__nim").distinct())
    # print(evaluasitopiks_list)
    for i in range (len(evaluasitopiks_list)):
            list_nim.append(evaluasitopiks_list[i][0])


    # Sudah Mengerjakan Topik
    usulantopiks=usulantopik.objects.exclude(nim__in=list_nim).annotate(Tanggal_Update_Terakhir=datetime.datetime.now().date()-Max("tanggal_update"))
    usulantopiks = usulantopiks.filter(id_usulan_topik__in=usulantopiks.values('nim').annotate(max_id=Max('id_usulan_topik')).values('max_id'))
    usulantopiks=usulantopiks.filter(nim__nim__in=nim_list)
    # print(usulantopiks)
    usulantopiks_list=list(usulantopiks.values_list("nim").distinct())
    # print(usulantopiks_list)
    for i in range (len(usulantopiks_list)):
            list_nim.append(usulantopiks_list[i][0])

    # Belum Buat Topik
    mahasiswa_topik=mahasiswa.objects.exclude(nim__in=list_nim).annotate(Tanggal_Update_Terakhir=datetime.datetime.now().date()-Max("id_user__date_joined"))
    mahasiswa_topik=mahasiswa_topik.filter(nim__in=nim_list)

    
    update_terakhir=[]
    update_terakhir_filter_dosen=[]
    for i in proposals_akhir:
        # print("ini i ", i)
        update_terakhir.append(i["Tanggal_Update_Terakhir"].days)
        if i["nim"] in nim_list:
            # print("checknim")
            update_terakhir_filter_dosen.append(i["Tanggal_Update_Terakhir"].days)
        
    for i in mahasiswa_topik:
        # print("ini i 2 ", i.nim)
        update_terakhir.append(i.Tanggal_Update_Terakhir.days)
        if i.nim in nim_list:
            # print("checknim")
            update_terakhir_filter_dosen.append(i.Tanggal_Update_Terakhir.days)
    for i in proposal_upload:
        update_terakhir.append(i.Tanggal_Update_Terakhir.days)
        if i.nim.nim in nim_list:
            # print("usulan check true")
            # print("checknim")
            update_terakhir_filter_dosen.append(i.Tanggal_Update_Terakhir.days)
    for i in usulantopiks:
        update_terakhir.append(i.Tanggal_Update_Terakhir.days)
        if i.nim.nim in nim_list:
            # print("usulan check true")
            # print("checknim")
            update_terakhir_filter_dosen.append(i.Tanggal_Update_Terakhir.days)
    for i in evaluasitopiks:
        # print("ini i 2 ", i.id_usulan_topik.nim.nim)
        update_terakhir.append(i.Tanggal_Update_Terakhir.days)
        if i.id_usulan_topik.nim.nim in nim_list:
            # print("eval check true")
            update_terakhir_filter_dosen.append(i.Tanggal_Update_Terakhir.days)
    # print("cek",update_terakhir)
    jumlah_diatas_3_bulan=sum(i>90 for i in update_terakhir)
    jumlah_diatas_3_bulan_dosen=sum(i>90 for i in update_terakhir_filter_dosen)
    # print(jumlah_diatas_3_bulan)
    # print("dosen",jumlah_diatas_3_bulan_dosen)

    return render(request, 'mahasiswa/mahasiswa_progress_with_marker.html', {"proposals": proposals_akhir,
                                                                             "mahasiswa_topik":mahasiswa_topik,
                                                                             "proposal_upload":proposal_upload,
                                                                             "usulantopiks":usulantopiks,                                                                     "usulantopiks":usulantopiks,
                                                                             "lulusmhs":lulus_mhs,
                                                                             "evaluasitopiks":evaluasitopiks, 
                                                                             "user_info": user_info})
    
# Jadwal Semester: create
# Membuat data Jadwal Semester 
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Properta'])
# @permission_required("skripsi_app.add_dosen", raise_exception=True)
def jadwal_semester_create(request):
    user_info = user_information(request)
    if request.method == "POST":
        form = JadwalSemesterForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect("../jadwalsemesterget")
    else:
        form = JadwalSemesterForm()
    return render(request, 'jadwal/jadwal_semester_create.html', {"form": form, "user_info": user_info})


# Jadwal Semester: update
# memperbaharui data jadwal semester berdasarkan id jadwal semester
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Properta'])
# @permission_required("skripsi_app.add_dosen", raise_exception=True)
def jadwal_semester_update(request,id):
    user_info = user_information(request)
    jadwal_semester_data = jadwal_semester.objects.get(pk=id)
    if request.method == "POST":
        form = JadwalSemesterForm(request.POST,instance=jadwal_semester_data)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.warning(request,"Data Jadwal Semester Telah Berhasil Diperbarui! ")
            return redirect("../jadwalsemesterget")
    else:
        form = JadwalSemesterForm(instance=jadwal_semester_data)
    return render(request, 'jadwal/jadwal_semester_update.html', {"form": form, "user_info": user_info})

# Jadwal Semester: read
# melihat list data jadwal semester berdasarkan id jadwal semester
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Properta'])
# @permission_required("auth.add_user", raise_exception=True)
def jadwal_semester_get(request):
    user_info = user_information(request)
    jadwal_semesters = jadwal_semester.objects.all()
    return render(request, 'jadwal/jadwal_semester_get.html', {"jadwal_semesters": jadwal_semesters, "user_info": user_info})


# Jadwal Semester: delete
# menghapus data jadwal semester berdasarkan id jadwal semester
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Properta'])
# @permission_required("skripsi_app.delete_dosen", raise_exception=True)
def jadwal_semester_delete(request, id):
    delete_data = jadwal_semester.objects.get(pk=id)
    messages.error(request,"Data Jadwal Semester Telah Berhasil Dihapus! ")
    delete_data.delete()
    return redirect('../jadwalsemesterget')

# todo: ngitung last bab 4 acc - daftar skripsi no bug testing
# rentang llulus untuk dapat waktu kelulusan rata rata
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])  
def get_data_rentang_lulus(request, id):
    user_info = user_information(request)
    data_proposal=bimbingan.objects.filter(status_bimbingan="ACC").filter(id_proposal__nama_tahap="Laporan Akhir").order_by('-tanggal_update').values("id_proposal__nim","id_proposal__nim__id_user__first_name","id_proposal__nim__semester_daftar_skripsi__tanggal_awal_semester").annotate(tanggal_max=Max('tanggal_update'))
    # data_proposal = proposal.objects.all()
    # data_proposal = proposal.objects.filter()
    data_proposal.masa_studi=data_proposal.id_proposal__nim__semester_daftar_skripsi__tanggal_awal_semester-data_proposal.tanggal_max
    # data_semester = jadwal_semester.objects.get(pk=id)
    # delete_data.delete()
    return render(request, 'jadwal/data_masa_studi.html', {"data_proposals": data_proposal, "user_info": user_info})

# Penampilan list penilaian mahasiswa
# @permission_required("skripsi_app.add_dosen", raise_exception=True)
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen''Properta'])  
def penilaian_full(request):
    user_info = user_information(request)
    penilaians=penilaian.objects.all()
    return render(request, 'penilaian/penilaian_full.html', {"penilaians": penilaians, "user_info": user_info})

# Penampilan list mahasiswa berdasarkan nim untuk menampilkan nilai nantinya
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])  
# @permission_required("skripsi_app.add_dosen", raise_exception=True)
def penilaian_list(request):
    user_info = user_information(request)
    penilaians=penilaian.objects.all().values_list("id_detail_penilaian__id_role_dosen__nim__nim").distinct()
    nim_list=[]
    for item in penilaians :
        # print(item)
        for item2 in item :
            nim_list.append(item2)
    penilaian_mhs=mahasiswa.objects.filter(nim__in=nim_list )
    # if a==a:
    #     pass
    return render(request, 'penilaian/penilaian_list.html', {"penilaians": penilaian_mhs, "user_info": user_info})
# Penampilan list mahasiswa berdasarkan nim untuk menampilkan nilai nantinya tapi di filter dosen pembimbing
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])  
# @permission_required("skripsi_app.add_dosen", raise_exception=True)
def penilaian_list_dosen(request):
    user_info = user_information(request)
    penilaians=penilaian.objects.all().values_list("id_detail_penilaian__id_role_dosen__nim__nim").distinct()
    nim_list=[]
    for item in penilaians :
        # print(item)
        for item2 in item :
            nim_list.append(item2)
    penilaian_mhs=mahasiswa.objects.filter(nim__in=nim_list )
    roledosen_cek=roledosen.objects.filter(nip=user_info[0]).filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(role="Pembimbing 2")
    list_roledosen=list(roledosen_cek.values_list("nim__nim",flat=True).distinct())
    # print(list_roledosen)
    penilaian_mhs=penilaian_mhs.filter(nim__in=list_roledosen)
    # if user_info[2].name == "Dosen" or user_info[2].name == "Kmpartemen":
        # pass
    return render(request, 'penilaian/penilaian_list.html', {"penilaians": penilaian_mhs, "user_info": user_info})


# Penampilan list mahasiswa berdasarkan nim untuk menampilkan nilai nantinya tapi di filter dosen penguji sempro
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])  
# @permission_required("skripsi_app.add_dosen", raise_exception=True)
def penilaian_list_dosen_sempro(request):
    user_info = user_information(request)
    role="Seminar Proposal"
    penilaians=penilaian.objects.all().values_list("id_detail_penilaian__id_role_dosen__nim__nim").distinct()
    nim_list=[]
    for item in penilaians :
        # print(item)
        for item2 in item :
            nim_list.append(item2)
    penilaian_mhs=mahasiswa.objects.filter(nim__in=nim_list )
    roledosen_cek=roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Proposal 2")
    list_roledosen=list(roledosen_cek.values_list("nim__nim",flat=True).distinct())
    # print(list_roledosen)
    penilaian_mhs=penilaian_mhs.filter(nim__in=list_roledosen)
    # if user_info[2].name == "Dosen" or user_info[2].name == "Kmpartemen":
        # pass
    return render(request, 'penilaian/penilaian_list.html', {"penilaians": penilaian_mhs, "user_info": user_info,"role":role})

# Penampilan list mahasiswa berdasarkan nim untuk menampilkan nilai nantinya tapi di filter dosen penguji semhas
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])  
# @permission_required("skripsi_app.add_dosen", raise_exception=True)
def penilaian_list_dosen_semhas(request):
    role="Seminar Hasil"
    user_info = user_information(request)
    penilaians=penilaian.objects.all().values_list("id_detail_penilaian__id_role_dosen__nim__nim").distinct()
    nim_list=[]
    for item in penilaians :
        # print(item)
        for item2 in item :
            nim_list.append(item2)
    penilaian_mhs=mahasiswa.objects.filter(nim__in=nim_list )
    roledosen_cek=roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Hasil 2")
    list_roledosen=list(roledosen_cek.values_list("nim__nim",flat=True).distinct())
    # print(list_roledosen)
    penilaian_mhs=penilaian_mhs.filter(nim__in=list_roledosen)
    # if user_info[2].name == "Dosen" or user_info[2].name == "Kmpartemen":
        # pass
    return render(request, 'penilaian/penilaian_list.html', {"penilaians": penilaian_mhs, "user_info": user_info,"role":role})

# Penampilan list penilaian sempro
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])  
# @permission_required("skripsi_app.add_dosen", raise_exception=True)
def penilaian_sempro(request):
    user_info = user_information(request)
    penilaians=penilaian.objects.all().exclude(id_detail_penilaian__nama_tahap="Seminar Hasil").exclude(id_detail_penilaian__nama_tahap="Bimbingan")
    return render(request, 'penilaian/penilaian_full.html', {"penilaians": penilaians, "user_info": user_info})

# Penampilan list penilaian semhas
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])  
# @permission_required("skripsi_app.add_dosen", raise_exception=True)
def penilaian_semhas(request):
    user_info = user_information(request)
    penilaians=penilaian.objects.all().exclude(id_detail_penilaian__nama_tahap="Seminar Proposal").exclude(id_detail_penilaian__nama_tahap="Bimbingan")
    return render(request, 'penilaian/penilaian_full.html', {"penilaians": penilaians, "user_info": user_info})

# Penampilan list penilaian bimbingan
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])  
# @permission_required("skripsi_app.add_dosen", raise_exception=True)
def penilaian_bimbingan(request):
    user_info = user_information(request)
    penilaians=penilaian.objects.all().exclude(id_detail_penilaian__nama_tahap="Bimbingan").exclude(id_detail_penilaian__nama_tahap="Seminar Proposal")
    return render(request, 'penilaian/penilaian_full.html', {"penilaians": penilaians, "user_info": user_info})

# Penampilan list penilaian sempro berdasar nim
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])  
# @permission_required("skripsi_app.add_dosen", raise_exception=True)
def penilaian_sempro_nim(request,nim):
    user_info = user_information(request)
    penilaians=penilaian.objects.filter(id_detail_penilaian__id_role_dosen__nim__nim=nim).exclude(id_detail_penilaian__nama_tahap="Seminar Hasil").exclude(id_detail_penilaian__nama_tahap="Bimbingan")
    return render(request, 'penilaian/penilaian_full.html', {"penilaians": penilaians, "user_info": user_info})
# Penampilan list penilaian sempro berdasar nim untuk penguji sempro
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])  
# @permission_required("skripsi_app.add_dosen", raise_exception=True)
def penilaian_sempro_nim_filter(request,nim):
    user_info = user_information(request)
    roledosen_cek=roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Proposal 2")
    list_roledosen=list(roledosen_cek.values_list("nip__nip",flat=True).distinct())
    
    penilaians=penilaian.objects.filter(id_detail_penilaian__id_role_dosen__nim__nim=nim).exclude(id_detail_penilaian__nama_tahap="Seminar Hasil").exclude(id_detail_penilaian__nama_tahap="Bimbingan")
    penilaians=penilaians.filter(id_detail_penilaian__id_role_dosen__nip__nip__in=list_roledosen)
    return render(request, 'penilaian/penilaian_full.html', {"penilaians": penilaians, "user_info": user_info})

# Penampilan list penilaian sempro berdasar nim
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])  
# @permission_required("skripsi_app.add_dosen", raise_exception=True)
def penilaian_sempro_jadwal_seminar(request,id_jadwal_seminar):
    user_info = user_information(request)
    penilaians=penilaian.objects.filter(id_detail_penilaian__id_jadwal_seminar__id_jadwal_seminar=id_jadwal_seminar).exclude(id_detail_penilaian__nama_tahap="Seminar Hasil").exclude(id_detail_penilaian__nama_tahap="Bimbingan")
    return render(request, 'penilaian/penilaian_full.html', {"penilaians": penilaians, "user_info": user_info})
# Penampilan list penilaian sempro berdasar nim untuk penguji sempro
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])  
# @permission_required("skripsi_app.add_dosen", raise_exception=True)
def penilaian_sempro_jadwal_seminar_filter(request,id_jadwal_seminar):
    user_info = user_information(request)
    roledosen_cek=roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Proposal 1")|roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Proposal 2")|roledosen.objects.filter(nip=user_info[0]).filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(role="Pembimbing 2")
    list_roledosen=list(roledosen_cek.values_list("nip__nip",flat=True).distinct())
    print(list_roledosen)
    penilaians=penilaian.objects.filter(id_detail_penilaian__id_jadwal_seminar__id_jadwal_seminar=id_jadwal_seminar).exclude(id_detail_penilaian__nama_tahap="Seminar Hasil").exclude(id_detail_penilaian__nama_tahap="Bimbingan")
    penilaians=penilaians.filter(id_detail_penilaian__id_role_dosen__nip__nip__in=list_roledosen)
    return render(request, 'penilaian/penilaian_full.html', {"penilaians": penilaians, "user_info": user_info})

# Penampilan list penilaian semhas berdasar nim
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])  
# @permission_required("skripsi_app.add_dosen", raise_exception=True)
def penilaian_semhas_nim(request,nim):
    user_info = user_information(request)
    penilaians=penilaian.objects.filter(id_detail_penilaian__id_role_dosen__nim__nim=nim).exclude(id_detail_penilaian__nama_tahap="Seminar Proposal").exclude(id_detail_penilaian__nama_tahap="Bimbingan")
    return render(request, 'penilaian/penilaian_full.html', {"penilaians": penilaians, "user_info": user_info})

# Penampilan list penilaian semhas berdasar nim untuk penguji semhas
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])  
# @permission_required("skripsi_app.add_dosen", raise_exception=True)
def penilaian_semhas_nim_filter(request,nim):
    user_info = user_information(request)
    # user_info = user_information(request)
    roledosen_cek=roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Hasil 2")
    # list_roledosen=list(roledosen_cek.values_list("nim__nim",flat=True).distinct())
    list_roledosen=list(roledosen_cek.values_list("nip__nip",flat=True).distinct())
    # print()
    penilaians=penilaian.objects.filter(id_detail_penilaian__id_role_dosen__nim__nim=nim).exclude(id_detail_penilaian__nama_tahap="Seminar Proposal").exclude(id_detail_penilaian__nama_tahap="Bimbingan")
    penilaians=penilaians.filter(id_detail_penilaian__id_role_dosen__nip__nip__in=list_roledosen)
    return render(request, 'penilaian/penilaian_full.html', {"penilaians": penilaians, "user_info": user_info})


# Penampilan list penilaian semhas berdasar jadwal seminar
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])  
# @permission_required("skripsi_app.add_dosen", raise_exception=True)
def penilaian_semhas_jadwal_seminar(request,id_jadwal_seminar):
    user_info = user_information(request)
    penilaians=penilaian.objects.filter(id_detail_penilaian__id_jadwal_seminar__id_jadwal_seminar=id_jadwal_seminar).exclude(id_detail_penilaian__nama_tahap="Seminar Proposal").exclude(id_detail_penilaian__nama_tahap="Bimbingan")
    return render(request, 'penilaian/penilaian_full.html', {"penilaians": penilaians, "user_info": user_info})

# Penampilan list penilaian semhas berdasar id jadwal seminar untuk penguji semhas
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])  
# @permission_required("skripsi_app.add_dosen", raise_exception=True)
def penilaian_semhas_jadwal_seminar_filter(request,id_jadwal_seminar):
    user_info = user_information(request)
    # user_info = user_information(request)
    roledosen_cek=roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Hasil 1")|roledosen.objects.filter(nip=user_info[0]).filter(role="Penguji Seminar Hasil 2")|roledosen.objects.filter(nip=user_info[0]).filter(role="Pembimbing 1")|roledosen.objects.filter(nip=user_info[0]).filter(role="Pembimbing 2")
    # list_roledosen=list(roledosen_cek.values_list("nim__nim",flat=True).distinct())
    list_roledosen=list(roledosen_cek.values_list("nip__nip",flat=True).distinct())
    # print()
    penilaians=penilaian.objects.filter(id_detail_penilaian__id_jadwal_seminar__id_jadwal_seminar=id_jadwal_seminar).exclude(id_detail_penilaian__nama_tahap="Seminar Proposal").exclude(id_detail_penilaian__nama_tahap="Bimbingan")
    penilaians=penilaians.filter(id_detail_penilaian__id_role_dosen__nip__nip__in=list_roledosen)
    return render(request, 'penilaian/penilaian_full.html', {"penilaians": penilaians, "user_info": user_info})


# Penampilan list penilaian bimbingan berdasar nim untuk dosen pembimbing
@login_required(login_url="/login")
@role_required(allowed_roles=['Admin','Manajemen Departemen','Kompartemen','Dosen','Properta'])  
def penilaian_bimbingan_nim(request,nim):
    user_info = user_information(request)
    penilaians=penilaian.objects.filter(id_detail_penilaian__id_role_dosen__nim__nim=nim).exclude(id_detail_penilaian__nama_tahap="Seminar Hasil").exclude(id_detail_penilaian__nama_tahap="Seminar Proposal")
    return render(request, 'penilaian/penilaian_full.html', {"penilaians": penilaians, "user_info": user_info})

# def login(request):
#     return render(request, 'login.html')


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


# def detail(request, id_mahasiswa):
#     return HttpResponse("You're looking at mahasiswa %s." % id_mahasiswa)


# def results(request, id_mahasiswa):
#     response = "You're looking at the results of mahasiswa %s."
#     return HttpResponse(response % id_mahasiswa)


# def vote(request, id_mahasiswa):
#     return HttpResponse("You're voting on mahasiswa %s." % id_mahasiswa)
