from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
# from .models import Mahasiswa, Dosen
# handler403 = 'skripsi_app.views.permission_denied'
urlpatterns = [
     
    path('', views.start, name='start'),
    path('homepage/', views.start, name='start'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('home/', views.dashboard, name='home'),
    path('testerror/', views.test_error, name='test_error'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name="password_change_form.html")),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name="password_change_done.html"),
         name='password_change_done'),
    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_after_email.html"), 
     name="password_reset_confirm"),
    #     path('index', views.index, name='index'),
    # ex: /polls/5/
    # path('<int:id_mahasiswa>/', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # path('<int:id_mahasiswa>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    #     path('<int:id_mahasiswa>/vote/', views.vote, name='vote'),
    #     path('login/', views.login, name='login'),
    path('changeuser/<str:id>', views.change_user,
         name='change_user'),

     # notifikasi delete
     path('notifikasi_delete/<int:id>', views.notifikasi_delete, name='notifikasi_delete'),

     # Update tanggal
    path('update/usulantopik/', views.update_tanggal_usulantopik, name='update_tanggal_usulantopik'),
    path('update/evaluasitopik/', views.update_tanggal_evaluasitopik, name='update_tanggal_evaluasitopik'),
    path('update/proposal/', views.update_tanggal_proposal, name='update_tanggal_proposal'),
    path('update/bimbingan/', views.update_tanggal_bimbingan, name='update_tanggal_bimbingan'),

    # register mahasiswa
    path('register/', views.register, name='register'),
    # register dosen
    path('usercreate/', views.user_create, name='user_create'),
    # user
    path('userget/', views.user_get, name='user_get'),
    path('user_read/<int:id>', views.user_read, name='user_read'),
    path('user_update/<int:id>', views.user_update, name='user_update'),
    path('user_delete/<int:id>', views.user_delete, name='user_delete'),
    # todo : group

    # usergroup
    path('usergroupget/', views.usergroup_get, name='usergroupget'),
    path('usergroup_update/<int:id>',
         views.usergroup_update, name='usergroup_update'),

    # kompartemen
    path('kompartemencreate/', views.kompartemen_create, name='kompartemen_create'),
    path('kompartemenget/', views.kompartemen_get, name='kompartemen_get'),
    path('kompartemen_update/<int:id>',
         views.kompartemen_update, name='kompartemen_update'),
    path('kompartemen_delete/<int:id>',
         views.kompartemen_delete, name='kompartemen_delete'),

    # Dosen

    path('dosencreate/', views.dosen_create, name='dosen_create'),
    #     path('createdosen2/', views.create_dosen2, name='create_dosen2'),
    path('dosenget/', views.dosen_get, name='dosen_get'),
    path('dosen_read/<str:id>', views.dosen_read, name='dosen_read'),
    path('dosen_update/<str:id>', views.dosen_update, name='dosen_update'),
    path('dosen_delete/<str:id>',
         views.dosen_delete, name='dosen_delete'),

    # mahasiswa
    path('mahasiswacreate/', views.mahasiswa_create, name='mahasiswa_create'),
    path('usermahasiswacreate/', views.user_create_mhs, name='user_create_mhs'),
    path('mahasiswaget/', views.mahasiswa_get, name='mahasiswa_get'),
     # progress mahasiswa
    path('mahasiswaprogress/', views.mahasiswa_progress_get, name='mahasiswa_progress_get'),
    path('mahasiswaprogressbulan/', views.mahasiswa_progress_by_bulan, name='mahasiswa_progress_by_bulan'),
    path('mahasiswaprogressbulan/dosen', views.mahasiswa_progress_by_bulan_dosen, name='mahasiswa_progress_by_bulan_dosen'),
    path('mahasiswawaktu/', views.mahasiswa_waktu_get, name='mahasiswa_waktu_get'),
    path('mahasiswawaktu/usulan/acc-revisi-semhas', views.mahasiswa_waktu_get_usulan, name='mahasiswa_waktu_get_usulan'),
    path('mahasiswawaktu/evaluasi/acc-sempro', views.mahasiswa_waktu_get_evaluasi, name='mahasiswa_waktu_get_evaluasi'),
    path('mahasiswawaktu/acc-revisi-sempro/acc-revisi-semhas', views.mahasiswa_waktu_get_berkas, name='mahasiswa_waktu_get_berkas'),
    path('mahasiswawaktu/durasi-evaluasi', views.mahasiswa_waktu_get_kompartemen, name='mahasiswa_waktu_get_kompartemen'),
    
    path('mahasiswa_read/<str:id>', views.mahasiswa_read, name='mahasiswa_read'),
    path('mahasiswa_update/<str:id>',
         views.mahasiswa_update, name='mahasiswa_update'),
    path('mahasiswa_delete/<str:id>',
         views.mahasiswa_delete, name='mahasiswa_delete'),

    # komartemen dosen
    path('kompartemendosencreate/', views.kompartemendosen_create,
         name='kompartemendosen_create'),
    path('kompartemendosenget/', views.kompartemendosen_get,
         name='kompartemendosen_get'),
    path('kompartemendosen_update/<int:id>',
         views.kompartemendosen_update, name='kompartemendosen_update'),
    path('kompartemendosen_delete/<int:id>',
         views.kompartemendosen_delete, name='kompartemendosen_delete'),

    # Usulan Topik
    path('usulantopikcreate/', views.usulantopik_create,
         name='usulantopik_create'),
    path('usulantopikcreatefull/', views.usulantopik_create_full,
         name='usulantopik_create_full'),
    path('usulantopikget/', views.usulantopik_get,
         name='usulantopik_get'),
    path('usulantopikget/acc/', views.usulantopik_get_acc,
         name='usulantopik_get_acc'),
    path('usulantopikget1/', views.usulantopik_get_1_year,
         name='usulantopik_get_1_year'),
    path('usulantopik_get_filter_dosen/', views.usulantopik_get_filter_dosen,
         name='usulantopik_get_filter_dosen'),
    
    path('usulantopik_get_filter_dosen_pembimbing/', views.usulantopik_get_filter_dosen_pembimbing,
         name='usulantopik_get_filter_dosen_pembimbing'),
    path('usulantopik_get_filter_ACC/', views.usulantopik_get_filter_ACC,
         name='usulantopik_get_filter_ACC'),
    path('usulantopik_get_filter/kompartemen', views.usulantopik_get_filter_kompartemen,
         name='usulantopik_get_filter_kompartemen'),
    path('usulantopik_get_filter/dosen', views.usulantopik_getfilter_dosen,
         name='usulantopik_getfilter_dosen'),
    path('usulantopik_get_filter_ACC/kompartemen', views.usulantopik_get_filter_ACC_kompartemen,
         name='usulantopik_get_filter_ACC_kompartemen'),
    path('usulantopik_get_filter_belum_ACC/kompartemen', views.usulantopik_get_filter_revisi_kompartemen,
         name='usulantopik_get_filter_revisi_kompartemen'),
    path('usulantopik_get_filter_ACC/dosen', views.usulantopik_get_filter_ACC_dosen,
         name='usulantopik_get_filter_ACC_dosen'),
    path('usulantopik_read/<int:id>',
         views.usulantopik_read, name='usulantopik_read'),
    path('usulantopik_update/<int:id>',
         views.usulantopik_update, name='usulantopik_update'),
    path('usulantopik_delete/<int:id>',
         views.usulantopik_delete, name='usulantopik_delete'),

    # Evaluasi Topik
    path('evaluasitopikcreate/', views.evaluasitopik_create,
         name='evaluasitopik_create'),
    path('evaluasitopik_create/<int:id>', views.evaluasitopik_create_id_usulan,
         name='evaluasitopik_create_id_usulan'),
    path('evaluasitopikcreate/<int:id>', views.evaluasitopik_create_sekdept,
         name='evaluasitopik_create_sekdept'),
    path('evaluasitopikget/', views.evaluasitopik_get,
         name='evaluasitopik_get'),
    path('evaluasitopikgetrevise/', views.evaluasitopik_get_ACC,
         name='evaluasitopik_get_ACC'),
    
    path('evaluasitopikget/acc', views.evaluasitopik_get_sudah_ACC,
         name='evaluasitopik_get_sudah_ACC'),
    path('evaluasitopikget/revisi', views.evaluasitopik_get_sudah_revisi,
         name='evaluasitopik_get_sudah_revisi'),
    path('evaluasitopikget/evaluasi', views.evaluasitopik_get_sudah_evaluasi,
         name='evaluasitopik_get_sudah_evaluasi'),
    
    
    path('evaluasitopikget/<int:id>', views.evaluasitopik_get_id_usulan,
         name='evaluasitopik_get_id_usulan'),
    path('kompartemenmax/',
         views.dosenevalkompartemen_max, name='dosenevalkompartemen_max'),
    #     path('evaluasitopik_read/<int:id>',
    #          views.evaluasitopik_read, name='evaluasitopik_read'),
    path('evaluasitopik_read/<int:id>',
         views.evaluasitopik_read, name='evaluasitopik_read'),
    path('evaluasitopik_update/<int:id>',
         views.evaluasitopik_update, name='evaluasitopik_update'),
    path('evaluasitopik_delete/<int:id>',
         views.evaluasitopik_delete, name='evaluasitopik_delete'),
    # roledosen
    path('roledosencreate/',
         views.dosenpembimbing_create, name='dosenpembimbing_create'),
    path('roledosencreate/<int:id>',
         views.dosenpembimbing_create_sekdept, name='dosenpembimbing_create_sekdept'),
    
     path('roledosenget/pembimbing/active',
         views.dosenpembimbing_get_active, name='dosenpembimbing_get_active'),
     path('roledosenget/pembimbing/finished',
         views.dosenpembimbing_get_finished, name='dosenpembimbing_get_finished'),
     path('roledosenget/pembimbing/active/filter',
         views.dosenpembimbing_get_active_filter, name='dosenpembimbing_get_active_filter'),
     path('roledosenget/pembimbing/finished/filter',
         views.dosenpembimbing_get_finished_filter, name='dosenpembimbing_get_finished_filter'),
    
    
    path('roledosenget/pembimbing',
         views.dosenpembimbing_get_pembimbing, name='dosenpembimbing_get_pembimbing'),
    path('roledosenget/sempro',
         views.dosenpembimbing_get_sempro, name='dosenpembimbing_get_sempro'),
    path('roledosenget/semhas',
         views.dosenpembimbing_get_semhas, name='dosenpembimbing_get_semhas'),
    path('roledosenmax/<str:my_variable>',
         views.dosenpembimbing_max, name='dosenpembimbing_max'),
    path('roledosenget/sekdept',
         views.dosenpembimbing_get_sekdept, name='dosenpembimbing_get_sekdept'),
    path('roledosenget/',
         views.dosenpembimbing_get, name='dosenpembimbing_get'),
    path('roledosen_update/<int:id>',
         views.dosenpembimbing_update, name='dosenpembimbing_update'),
    path('roledosen_delete/<int:id>',
         views.dosenpembimbing_delete, name='dosenpembimbing_delete'),

    # bimbingan
    path('bimbingancreate/',
         views.bimbingan_create, name='bimbingan_create'),
    path('bimbingan_create/<int:id>',
         views.bimbingan_create_dosen, name='bimbingan_create_dosen'),
    path('bimbinganget/',
         views.bimbingan_get, name='bimbingan_get'),
    
    path('bimbinganget_acc/',
         views.bimbingan_get_acc, name='bimbingan_get_acc'),
    path('bimbinganget_lain/',
         views.bimbingan_get_lain_lain, name='bimbingan_get_lain_lain'),
    path('bimbinganget_diperiksa/',
         views.bimbingan_get_sudah_diperiksa, name='bimbingan_get_sudah_diperiksa'),
    path('bimbinganget_revisi/',
         views.bimbingan_get_revisi, name='bimbingan_get_revisi'),
    
    
    path('bimbingangetproposal/<int:id>',
         views.bimbingan_get_proposal, name='bimbingan_get_proposal'),
    path('bimbingan_read/<int:id>',
         views.bimbingan_read, name='bimbingan_read'),
    path('bimbingan_update/<int:id>',
         views.bimbingan_update, name='bimbingan_update'),
    path('bimbingan_update_proposal/<int:id>',
         views.bimbingan_update_proposal, name='bimbingan_update_proposal'),
    path('bimbingan_delete/<int:id>',
         views.bimbingan_delete, name='bimbingan_delete'),
    # Proposal
    path('proposalcreatefull/',
         views.proposal_create_full, name='proposal_create_full'),
    path('proposalcreate/',
         views.proposal_create, name='proposal_create'),
    path('proposalget/',
         views.proposal_get, name='proposal_get'),
    path('proposalget_nilai/',
         views.proposal_get_filter_dinilai, name='proposal_get_filter_dinilai'),
    path('proposalget_belum_nilai/',
         views.proposal_get_filter_belum_dinilai, name='proposal_get_filter_belum_dinilai'),
    path('proposalget5/',
         views.proposal_get_5_years, name='proposal_get_5_years'),
    path('proposalget5/sempro',
         views.proposal_get_5_years_proposal, name='proposal_get_5_years_proposal'),
    path('proposalget5/semhas',
         views.proposal_get_5_years_hasil, name='proposal_get_5_years_hasil'),
    path('proposalget_acc/',
         views.proposal_get_filter_ACC, name='proposal_get_filter_ACC'),
    path('proposalget_revisi/',
         views.proposal_get_filter_revisi, name='proposal_get_filter_revisi'),
    path('proposalget_diperiksa/',
         views.proposal_get_filter_belum_diperiksa, name='proposal_get_filter_belum_diperiksa'),
    path('proposalget_sempro/dosen',
         views.proposal_get_filter_sempro, name='proposal_get_filter_sempro'),
    path('proposalget_sempro/jadwal',
         views.proposal_get_filter_sempro_jadwal, name='proposal_get_filter_sempro_jadwal'),
    path('proposalget_semhas/dosen',
         views.proposal_get_filter_semhas, name='proposal_get_filter_semhas'),
    path('proposalget_semhas/jadwal',
         views.proposal_get_filter_semhas_jadwal, name='proposal_get_filter_semhas_jadwal'),
    path('proposalget/<int:id>',
         views.bimbingan_get_id_proposal, name='bimbingan_get_id_proposal'),
    path('proposalget/pembimbing',
         views.proposal_get_dosen, name='proposal_get_dosen'),
    
    path('proposalget/pembimbing/acc',
         views.proposal_get_dosen_filter_acc, name='proposal_get_dosen_filter_acc'),
    path('proposalget/pembimbing/sudah_diperiksa',
         views.proposal_get_dosen_filter_sudah_periksa, name='proposal_get_dosen_filter_sudah_periksa'),
    path('proposalget/pembimbing/revisi',
         views.proposal_get_dosen_filter_revisi, name='proposal_get_dosen_filter_revisi'),
    path('proposalget/pembimbing/sudah_acc',
         views.proposal_get_dosen_filter_sudah_acc, name='proposal_get_dosen_filter_sudah_acc'),
    
    
    path('proposalget/pembimbing/lengkap_nilai',
         views.proposal_get_dosen_lengkap_penilaian, name='proposal_get_dosen_lengkap_penilaian'),
    path('proposalget/pembimbing/nilai',
         views.proposal_get_dosen_sudah_dinilai, name='proposal_get_dosen_sudah_dinilai'),
    
    path('proposalget/pembimbing/nilai/belum',
         views.proposal_get_dosen_belum_dinilai, name='proposal_get_dosen_belum_dinilai'),
    path('proposalget/pembimbing/nilai/sebagian',
         views.proposal_get_dosen_sudah_dinilai_sebagian, name='proposal_get_dosen_sudah_dinilai_sebagian'),
    
    path('proposalget/sempro',
         views.proposal_get_sempro, name='proposal_get_sempro'),
    path('proposalget/sempro/nilai',
         views.proposal_get_sempro_sudah_nilai, name='proposal_get_sempro_sudah_nilai'),
    path('proposalget/semhas',
         views.proposal_get_semhas, name='proposal_get_semhas'),
    path('proposalget/semhas/nilai',
         views.proposal_get_semhas_sudah_dinilai, name='proposal_get_semhas_sudah_dinilai'),
    path('proposal_update/<int:id>',
         views.proposal_update, name='proposal_update'),
    path('proposal_read/<int:id>',
         views.proposal_read, name='proposal_read'),
    path('proposal_delete/<int:id>',
         views.proposal_delete, name='proposal_delete'),

     # Penilaian 
     path('penilaian_sempro_dosen_1/<int:id_jadwal_seminar>',
         views.penilaian_sempro_dosen_1, name='penilaian_sempro_dosen_1'),
     path('penilaian_sempro_dosen_2/<int:id_jadwal_seminar>',
         views.penilaian_sempro_dosen_2, name='penilaian_sempro_dosen_2'),
     
     
     path('penilaian_sempro_dosen_pembimbing_1/<int:id_jadwal_seminar>',
         views.penilaian_sempro_dosen_pembimbing_1, name='penilaian_sempro_dosen_pembimbing_1'),
     path('penilaian_sempro_dosen_pembimbing_2/<int:id_jadwal_seminar>',
         views.penilaian_sempro_dosen_pembimbing_2, name='penilaian_sempro_dosen_pembimbing_2'),
     path('penilaian_bimbingan_dosen_1/<int:id_jadwal_seminar>',
         views.penilaian_bimbingan_dosen_1, name='penilaian_bimbingan_dosen_1'),
     path('penilaian_bimbingan_dosen_2/<int:id_jadwal_seminar>',
         views.penilaian_bimbingan_dosen_2, name='penilaian_bimbingan_dosen_2'),
     path('penilaian_bimbingan_dosen_1_by_nim/<str:nim>',
         views.penilaian_bimbingan_dosen_1_by_nim, name='penilaian_bimbingan_dosen_1_by_nim'),
     path('penilaian_bimbingan_dosen_2_by_nim/<str:nim>',
         views.penilaian_bimbingan_dosen_2_by_nim, name='penilaian_bimbingan_dosen_2_by_nim'),
     path('penilaian_semhas_dosen_pembimbing_1/<int:id_jadwal_seminar>',
         views.penilaian_semhas_dosen_pembimbing_1, name='penilaian_semhas_dosen_pembimbing_1'),
     path('penilaian_semhas_dosen_pembimbing_2/<int:id_jadwal_seminar>',
         views.penilaian_semhas_dosen_pembimbing_2, name='penilaian_semhas_dosen_pembimbing_2'),
     
     
     path('penilaian_semhas_dosen_1/<int:id_jadwal_seminar>',
         views.penilaian_semhas_dosen_1, name='penilaian_semhas_dosen_1'),
     path('penilaian_semhas_dosen_2/<int:id_jadwal_seminar>',
         views.penilaian_semhas_dosen_2, name='penilaian_semhas_dosen_2'),
     
     path('penilaian_no_list_mahasiswa/<str:nim>',
         views.jadwal_dosen_bimbingan_no_filter_nim, name='jadwal_dosen_bimbingan_no_filter_nim'),
     path('penilaian_list_mahasiswa/<str:nim>',
         views.jadwal_dosen_bimbingan_filter_nim, name='jadwal_dosen_bimbingan_filter_nim'),
     path('penilaian_list/',
         views.penilaian_list, name='penilaian_list'),
     path('penilaian_list_dosen/',
         views.penilaian_list_dosen, name='penilaian_list_dosen'),
     path('penilaian_list_dosen_semhas/',
         views.penilaian_list_dosen_semhas, name='penilaian_list_dosen_semhas'),
     path('penilaian_list_dosen_sempro/',
         views.penilaian_list_dosen_sempro, name='penilaian_list_dosen_sempro'),
     
     
     
     
     path('penilaian_get_full/',
         views.penilaian_full, name='penilaian_full'),
     
     path('penilaian_get_sempro/',
         views.penilaian_sempro, name='penilaian_sempro'),
     path('penilaian_get_semhas/',
         views.penilaian_semhas, name='penilaian_semhas'),
     

     
     path('penilaian_get_bimbingan/',
         views.penilaian_bimbingan, name='penilaian_bimbingan'),
     
     path('penilaian_get_sempro/<str:nim>',
         views.penilaian_sempro_nim, name='penilaian_sempro_nim'),
     path('penilaian_get_semhas/<str:nim>',
         views.penilaian_semhas_nim, name='penilaian_semhas_nim'),
     
     path('penilaian_get_sempro_filter/<str:nim>',
         views.penilaian_sempro_nim_filter, name='penilaian_sempro_nim_filter'),
     path('penilaian_get_semhas_filter/<str:nim>',
         views.penilaian_semhas_nim_filter, name='penilaian_semhas_nim_filter'),
     
     path('jadwal_seminar_utama/',
         views.jadwal_seminar_utama, name='jadwal_seminar_utama'),
     
     
     path('penilaian_get_sempro/seminar/<int:id_jadwal_seminar>',
         views.penilaian_sempro_jadwal_seminar, name='penilaian_sempro_jadwal_seminar'),
     path('penilaian_get_sempro_filter/seminar/<int:id_jadwal_seminar>',
         views.penilaian_sempro_jadwal_seminar_filter, name='penilaian_sempro_jadwal_seminar_filter'),
     
     path('penilaian_get_semhas/seminar/<int:id_jadwal_seminar>',
         views.penilaian_semhas_jadwal_seminar, name='penilaian_semhas_jadwal_seminar'),
     path('penilaian_get_semhas_filter/seminar/<int:id_jadwal_seminar>',
         views.penilaian_semhas_jadwal_seminar_filter, name='penilaian_semhas_jadwal_seminar_filter'),
     
     path('penilaian_get_bimbingan/<str:nim>',
         views.penilaian_bimbingan_nim, name='penilaian_bimbingan_nim'),

     # nilai
     path('nilai_sempro/<str:nim>',
         views.nilai_sempro_get, name='nilai_sempro_get'),
     path('nilai_semhas/<str:nim>',
         views.nilai_semhas_get, name='nilai_semhas_get'),
     path('nilai_bimbingan/<str:nim>',
         views.nilai_bimbingan_get, name='nilai_bimbingan_get'),
     
     # nilai seminar
     path('nilai_sempro/seminar/<int:id_jadwal_seminar>',
         views.nilai_sempro_get_seminar, name='nilai_sempro_get_seminar'),
     path('nilai_semhas/seminar/<int:id_jadwal_seminar>',
         views.nilai_semhas_get_seminar, name='nilai_semhas_get_seminar'),
     path('nilai_bimbingan/seminar/<int:id_jadwal_seminar>',
         views.nilai_bimbingan_get_seminar, name='nilai_bimbingan_get_seminar'),
     
     # list review seminar
     path('review_all/',
         views.list_detail_penilaian, name='list_detail_penilaian'),
     path('review_bimbingan/',
         views.list_detail_penilaian_bimbingan, name='list_detail_penilaian_bimbingan'),
     path('review_sempro/',
         views.list_detail_penilaian_sempro, name='list_detail_penilaian_sempro'),
     path('review_semhas/',
         views.list_detail_penilaian_semhas, name='list_detail_penilaian_semhas'),
     
     # jadwal seminar
     path('jadwalcreate/',
         views.jadwal_create, name='jadwal_create'),
     path('jadwalcreate/filter',
         views.jadwal_create_tanpa_filter, name='jadwal_create_tanpa_filter'),
     path('jadwalget/',
         views.jadwal_get, name='jadwal_get'),
     path('jadwalgettoday/',
         views.jadwal_get_today, name='jadwal_get_today'),
     path('jadwalget/nomorinduk',
         views.jadwal_mhs_dosen_get, name='jadwal_mhs_dosen_get'),
     path('jadwalupdate/<int:id>',
         views.jadwal_update, name='jadwal_update'),
     path('jadwalupdate/filter/<int:id>',
         views.jadwal_update_tanpa_filter, name='jadwal_update_tanpa_filter'),
     path('jadwaldelete/<int:id>',
         views.jadwal_delete, name='jadwal_delete'),
     

     
     path('tabulasi_penilaian/',
         views.tabulasi_penilaian, name='tabulasi_penilaian'),
     
     path('tabulasi_penilaian/bimbingan/belum',
         views.tabulasi_penilaian_belum_lengkap_bimbingan, name='tabulasi_penilaian_belum_lengkap_bimbingan'),
     path('tabulasi_penilaian/bimbingan/sudah',
         views.tabulasi_penilaian_sudah_lengkap_bimbingan, name='tabulasi_penilaian_sudah_lengkap_bimbingan'),
     path('tabulasi_penilaian/sempro/belum',
         views.tabulasi_penilaian_belum_lengkap_sempro, name='tabulasi_penilaian_belum_lengkap_sempro'),
     path('tabulasi_penilaian/sempro/sudah',
         views.tabulasi_penilaian_sudah_lengkap_sempro, name='tabulasi_penilaian_sudah_lengkap_sempro'),
     path('tabulasi_penilaian/semhas/belum',
         views.tabulasi_penilaian_belum_lengkap_semhas, name='tabulasi_penilaian_belum_lengkap_semhas'),
     path('tabulasi_penilaian/semhas/sudah',
         views.tabulasi_penilaian_sudah_lengkap_semhas, name='tabulasi_penilaian_sudah_lengkap_semhas'),
     
     path('tabulasi_penilaian_no_filter/',
         views.tabulasi_penilaian_no_filter, name='tabulasi_penilaian_no_filter'),
     
     path('jadwal_bimbingan/',
         views.jadwal_dosen_bimbingan_tanpa_filter, name='jadwal_dosen_bimbingan_tanpa_filter'),
     path('jadwal_bimbingan_2/',
         views.jadwal_dosen_bimbingan_tanpa_filter_2, name='jadwal_dosen_bimbingan_tanpa_filter_2'),
     # jadwal_dosen_bimbingan_tanpa_filter_2
     path('jadwal_bimbingan/all',
         views.jadwal_dosen_bimbingan, name='jadwal_dosen_bimbingan'),
     path('jadwal_bimbingan_2/all',
         views.jadwal_dosen_bimbingan_2, name='jadwal_dosen_bimbingan_2'),
     # jadwal_dosen_bimbingan_2
     path('jadwal_bimbingan/nilai',
         views.jadwal_dosen_bimbingan_sudah_dinilai, name='jadwal_dosen_bimbingan_sudah_dinilai'),
     path('jadwal_bimbingan_2/nilai',
         views.jadwal_dosen_bimbingan_sudah_dinilai_2, name='jadwal_dosen_bimbingan_sudah_dinilai_2'),
     # jadwal_dosen_bimbingan_sudah_dinilai_2
     path('jadwal_bimbingan/sebagian',
         views.jadwal_dosen_bimbingan_sebagian_dinilai, name='jadwal_dosen_bimbingan_sebagian_dinilai'),
     path('jadwal_bimbingan/belum',
         views.jadwal_dosen_bimbingan_belum_dinilai, name='jadwal_dosen_bimbingan_belum_dinilai'),
     path('jadwal_bimbingan_2/belum',
         views.jadwal_dosen_bimbingan_belum_dinilai_2, name='jadwal_dosen_bimbingan_belum_dinilai_2'),
     
     # jadwal_dosen_bimbingan_belum_dinilai_2

     path('jadwal_sempro/',
         views.jadwal_dosen_sempro_tanpa_filter, name='jadwal_dosen_sempro_tanpa_filter'),
     path('jadwal_sempro/all',
         views.jadwal_dosen_sempro, name='jadwal_dosen_sempro'),
     path('jadwal_sempro/nilai',
         views.jadwal_dosen_sempro_sudah_dinilai, name='jadwal_dosen_sempro_sudah_dinilai'),
     # path('jadwal_sempro/sebagian',
     #     views.jadwal_dosen_bimbingan_sebagian_dinilai, name='jadwal_dosen_bimbingan_sebagian_dinilai'),
     path('jadwal_sempro/belum',
         views.jadwal_dosen_sempro_belum_dinilai, name='jadwal_dosen_sempro_belum_dinilai'),
     
     path('jadwal_semhas/',
         views.jadwal_dosen_semhas_tanpa_filter, name='jadwal_dosen_semhas_tanpa_filter'),
     path('jadwal_semhas/all',
         views.jadwal_dosen_semhas, name='jadwal_dosen_semhas'),
     path('jadwal_semhas/nilai',
         views.jadwal_dosen_semhas_sudah_dinilai, name='jadwal_dosen_semhas_sudah_dinilai'),
     # path('jadwal_sempro/sebagian',
     #     views.jadwal_dosen_bimbingan_sebagian_dinilai, name='jadwal_dosen_bimbingan_sebagian_dinilai'),
     path('jadwal_semhas/belum',
         views.jadwal_dosen_semhas_belum_dinilai, name='jadwal_dosen_semhas_belum_dinilai'),

     path('listangkatan/',
         views.mahasiswa_jumlah_get, name='mahasiswa_jumlah_get'),
     path('listangkatanget/',
         views.mahasiswa_jumlah_get_progress, name='mahasiswa_jumlah_get_progress'),
     path('listangkatan_onlytahun/',
         views.mahasiswa_jumlah_get_tahun, name='mahasiswa_jumlah_get_tahun'),

     # Jadwal Semester
     path('jadwalsemestercreate/',
         views.jadwal_semester_create, name='jadwal_semester_create'),
     path('jadwalsemesterget/',
         views.jadwal_semester_get, name='jadwal_semester_get'),
     path('jadwal_semester_update/<int:id>',
         views.jadwal_semester_update, name='jadwal_semester_update'),
     path('jadwal_semester_delete/<int:id>',
         views.jadwal_semester_delete, name='jadwal_semester_delete'),

     # cpmk
     path('sub_cpmk_create/',
         views.Sub_CPMK_create, name='Sub_CPMK_create'),
     path('sub_cpmk_get/',
         views.Sub_CPMK_get, name='Sub_CPMK_get'),
     path('sub_cpmk_update/<str:id>',
         views.Sub_CPMK_update, name='Sub_CPMK_update'),
     path('sub_cpmk_delete/<str:id>',
         views.Sub_CPMK_delete, name='Sub_CPMK_delete'),
     # cpmk
     path('cpmk_create/',
         views.CPMK_create, name='CPMK_create'),
     path('cpmk_get/',
         views.CPMK_get, name='CPMK_get'),
     path('cpmk_update/<int:id>',
         views.CPMK_update, name='CPMK_update'),
     path('cpmk_delete/<int:id>',
         views.CPMK_delete, name='CPMK_delete'),
     
     path('dosen_info/',
         views.dosen_information, name='dosen_information'),
     path('mhs_info/',
         views.mhs_information, name='mhs_information'),
     path('mhs_info/1/',
         views.mhs_information_one_year, name='mhs_information_one_year'),
     path('mhs_info/5/',
         views.mhs_information_five_year, name='mhs_information_five_year'),
     
     path('mhs_info/topik/1/',
         views.mhs_information_topik_one_year, name='mhs_information_topik_one_year'),
    
]
