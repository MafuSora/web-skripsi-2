# import os

# # Mendapatkan direktori dari file saat ini (misalnya manage.py)
# current_dir = os.path.dirname(os.path.abspath(__file__))

# # Navigasi ke atas (menuju folder root proyek)
# project_root = os.path.abspath(os.path.join(current_dir, os.pardir))

# # Mencetak jalur absolut menuju folder root proyek
# print(project_root)


my_list = [1, 2, 3, None, '', 4, 0]

cleaned_list = list(filter(lambda x: x is not None and x != '', my_list))

print(cleaned_list)  # Output: [1, 2, 3, 4]



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
                    nama_tahap="Proposal Akhir").count()
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
                    id_proposal__nama_tahap="Proposal Akhir").count()
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
                    nama_tahap="Proposal Akhir").count()
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
                    id_proposal__nama_tahap="Proposal Akhir").count()
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
                    nama_tahap="Proposal Akhir").count()
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
                    id_proposal__nama_tahap="Proposal Akhir").count()
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
                    nama_tahap="Proposal Akhir").count()
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
                    id_proposal__nama_tahap="Proposal Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1

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
                    id_proposal__nama_tahap="Proposal Akhir").count()
                # print(get_object)
                proposals[jumlah].jumlah_semhas = get_object
            except:
                proposals[jumlah].jumlah_semhas = 0
            jumlah += 1

    # print(proposals.ID_Proposal)
    return render(request, 'bimbingan/proposal_get.html', {"proposals": proposals,"role":role, "user_info": user_info})
# Proposal :Read 