from django.test import TestCase
from skripsi_app.models import jadwal_seminar,cpmk, jadwal_semester, kompartemen, mahasiswa, dosen,kompartemendosen,usulantopik,evaluasitopik,roledosen,detailpenilaian,sub_cpmk,notifikasi,bimbingan,proposal,penilaian
from django.core.files import File
from django.contrib.auth.models import User,Group
from datetime import datetime
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile


class UserTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )

    def test_create_user(self):
        user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='newpass'
        )
        self.assertEqual(User.objects.count(), 2)

    def test_read_user(self):
        user = User.objects.get(id=self.test_user.id)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')

    def test_update_user(self):
        user = User.objects.get(id=self.test_user.id)
        user.email = 'newemail@example.com'
        user.save()
        updated_user = User.objects.get(id=self.test_user.id)
        self.assertEqual(updated_user.email, 'newemail@example.com')
        
    def test_change_user_password(self):
        user = User.objects.get(id=self.test_user.id)
        user.set_password('newpass')
        user.save()
        self.assertTrue(user.check_password('newpass'))

    def test_delete_user(self):
        user = User.objects.get(id=self.test_user.id)
        user.delete()
        self.assertEqual(User.objects.count(), 0)
        
class JadwalSemesterModelTestCase(TestCase):
    def setUp(self):
        self.jadwal = jadwal_semester.objects.create(
            nama_semester='Semester Ganjil',
            tahun_semester=2024,
            tanggal_awal_semester='2023-08-01',
            tanggal_akhir_semester='2023-12-31',
        )

    def test_create_jadwal_semester(self):
        jadwal_baru = jadwal_semester.objects.create(
            nama_semester='Semester Genap',
            tahun_semester=2024,
            tanggal_awal_semester='2024-01-01',
            tanggal_akhir_semester='2024-05-31',
        )
        self.assertEqual(jadwal_semester.objects.count(), 2)

    def test_read_jadwal_semester(self):
        jadwal = jadwal_semester.objects.get(nama_semester='Semester Ganjil')
        self.assertEqual(jadwal.nama_semester, 'Semester Ganjil')

    def test_update_jadwal_semester(self):
        self.jadwal.tanggal_awal_semester = datetime.strptime('2023-09-01', '%Y-%m-%d').date()
        self.jadwal.save()
        jadwal = jadwal_semester.objects.get(nama_semester='Semester Ganjil')
        self.assertEqual(jadwal.tanggal_awal_semester, datetime.strptime('2023-09-01', '%Y-%m-%d').date())

    def test_delete_jadwal_semester(self):
        self.jadwal.delete()
        self.assertEqual(jadwal_semester.objects.count(), 0)


     
class cpmk_utamaTestCase(TestCase):
    def setUp(self):
        self.jadwal = jadwal_semester.objects.create(nama_semester='Semester 1',tahun_semester=2024, tanggal_awal_semester='2023-01-01', tanggal_akhir_semester='2023-06-30')
        self.cpmk_utama_obj = cpmk.objects.create(
            id_cpmk="CPMK-001",
            keterangan_cpmk="Deskripsi cpmk_utama pertama",
            tahun_angkatan=2019,
            id_nama_semester=self.jadwal
            
        )

    def test_cpmk_utama_creation(self):
        cpmk.objects.create(
            id_cpmk="new_id",
            id_nama_semester=self.jadwal,
            tahun_angkatan=2024,
            keterangan_cpmk="new_keterangan"
        )
        new_cpmk = cpmk.objects.get(id_cpmk="new_id")
        self.assertEqual(new_cpmk.__str__(), "new_id-2024-Semester 1 2024-new_keterangan")

    def test_cpmk_utama_update(self):
        self.cpmk_utama_obj.id_cpmk = "CPMK-002"
        self.cpmk_utama_obj.keterangan_cpmk = "Deskripsi cpmk_utama kedua"
        self.cpmk_utama_obj.save()

        self.assertEqual(self.cpmk_utama_obj.__str__(), "CPMK-002-2019-Semester 1 2024-Deskripsi cpmk_utama kedua")
        
    def test_read_cpmk(self):
        cpmk1 = cpmk.objects.get(id_cpmk='CPMK-001')
        self.assertEqual(cpmk1.keterangan_cpmk, 'Deskripsi cpmk_utama pertama')
        
        cpmk.objects.create(id_cpmk='CPMK002',id_nama_semester=self.jadwal,
            tahun_angkatan=2024, keterangan_cpmk='Deskripsi cpmk_utama kedua')
        cpmks = cpmk.objects.all()
        self.assertEqual(len(cpmks), 2)

    def test_cpmk_utama_deletion(self):
        self.cpmk_utama_obj.delete()
        self.assertFalse(cpmk.objects.filter(id_cpmk="CPMK-001").exists())
        
class KompartemenTest(TestCase):
    def setUp(self):
        # membuat instance model kompartemen
        self.kompartemen = kompartemen.objects.create(nama_kompartemen='Kompartemen A')

    def test_str(self):
        expected = 'Kompartemen A'
        actual = str(self.kompartemen)
        self.assertEqual(expected, actual)

    def test_create_kompartemen(self):
        # membuat instance model kompartemen baru
        kompartemen_baru = kompartemen.objects.create(nama_kompartemen='Kompartemen B')

        # memastikan bahwa instance model baru telah dibuat
        self.assertTrue(kompartemen.objects.filter(nama_kompartemen='Kompartemen B').exists())

    def test_update_kompartemen(self):
        # mengubah nilai pada instance model kompartemen yang sudah ada
        self.kompartemen.nama_kompartemen = 'Kompartemen C'
        self.kompartemen.save()

        # memastikan bahwa nilai telah diubah
        expected = 'Kompartemen C'
        actual = kompartemen.objects.get(pk=self.kompartemen.pk).nama_kompartemen
        self.assertEqual(expected, actual)
        
    def test_delete_kompartemen(self):
        self.kompartemen.delete()
        self.assertEqual(kompartemen.objects.count(), 0)




class MahasiswaCRUDTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username='testuser', first_name='Test', last_name='User')
        self.jadwal = jadwal_semester.objects.create(nama_semester='Semester 1',tahun_semester=2024, tanggal_awal_semester='2023-01-01', tanggal_akhir_semester='2023-06-30')
        self.mahasiswa = mahasiswa.objects.create(nim=123456789,angkatan=2019, semester_daftar_skripsi=self.jadwal, id_user=self.user)
    
    def test_create_mahasiswa(self):
        new_user = User.objects.create(username='newuser', first_name='New', last_name='User')
        new_jadwal = jadwal_semester.objects.create(nama_semester='Semester 2',tahun_semester=2024, tanggal_awal_semester='2023-07-01', tanggal_akhir_semester='2023-12-31')
        new_mahasiswa = mahasiswa.objects.create(nim=987654321,angkatan=2019, semester_daftar_skripsi=new_jadwal, id_user=new_user)
        self.assertEqual(new_mahasiswa.nim, 987654321)
        self.assertEqual(new_mahasiswa.semester_daftar_skripsi, new_jadwal)
        self.assertEqual(new_mahasiswa.id_user, new_user)
    
    def test_read_mahasiswa(self):
        mahasiswa_db = mahasiswa.objects.get(nim=123456789)
        self.assertEqual(mahasiswa_db.nim, str(123456789))
        self.assertEqual(mahasiswa_db.semester_daftar_skripsi, self.jadwal)
        self.assertEqual(mahasiswa_db.id_user, self.user)
    
    def test_update_mahasiswa(self):
        new_jadwal = jadwal_semester.objects.create(nama_semester='Semester 3',tahun_semester=2024, tanggal_awal_semester='2024-01-01', tanggal_akhir_semester='2024-06-30')
        self.mahasiswa.semester_daftar_skripsi = new_jadwal
        self.mahasiswa.save()
        mahasiswa_db = mahasiswa.objects.get(nim=123456789)
        self.assertEqual(mahasiswa_db.semester_daftar_skripsi, new_jadwal)
    
    def test_delete_mahasiswa(self):
        self.mahasiswa.delete()
        with self.assertRaises(mahasiswa.DoesNotExist):
            mahasiswa.objects.get(nim=123456789)
            

class DosenTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='dosen_test', 
            first_name='Dosen', 
            last_name='Test'
        )
        self.dosen=dosen.objects.create(
            nip=1234567890, 
            id_user=self.user
        )

    def test_create_dosen(self):
        new_user = User.objects.create(username='newuser', first_name='New', last_name='User')
        new_dosen = dosen.objects.create(nip=2345678901,  id_user=new_user)
        self.assertEqual(new_dosen.nip, 2345678901)
        # self.assertEqual(new_dosen.semester_daftar_skripsi, new_jadwal)
        self.assertEqual(new_dosen.id_user, new_user)

    def test_read_mahasiswa(self):
        dosen_db = dosen.objects.get(nip=1234567890)
        self.assertEqual(dosen_db.nip, str(1234567890))
        self.assertEqual(dosen_db.id_user, self.user)
    
        
    def test_update_dosen(self):
        # print(dosen.objects.all())
        dosen_obj = dosen.objects.get(nip=1234567890)
        user = User.objects.create_user(
            username='dosen_test3', 
            password='password123', 
            first_name='Dosen', 
            last_name='Test3'
        )
        dosen_obj.id_user = user
        dosen_obj.nip = 1234554321
        dosen_obj.save()
        self.assertEqual(dosen_obj.nip, 1234554321)
        self.assertEqual(dosen_obj.id_user, user)

    def test_delete_dosen(self):
        dosen_obj = dosen.objects.get(nip=1234567890)
        dosen_obj.delete()
        dosen_exists = dosen.objects.filter(nip=1234567890).exists()
        self.assertFalse(dosen_exists)


class KompartemenDosenCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', first_name='Test', last_name='User')
        # self.user2 = User.objects.create(username='testuser2', first_name='Test2', last_name='User2')
        self.kompartemen = kompartemen.objects.create(nama_kompartemen="Kompartemen Test")
        self.dosen = dosen.objects.create(nip=123456789, id_user=self.user)
        self.kompartemendosen = kompartemendosen.objects.create(id_kompartemen=self.kompartemen, nip=self.dosen)
        
    def test_create_kompartemendosen(self):
        kompartemen_baru = kompartemen.objects.create(nama_kompartemen="Kompartemen Baru")
        user_baru = User.objects.create(username='testuser2', first_name='Test2', last_name='User2')
        dosen_baru = dosen.objects.create(nip=987654321, id_user=user_baru)
        kompartemendosen.objects.create(id_kompartemen=kompartemen_baru, nip=dosen_baru)
        self.assertEqual(kompartemendosen.objects.count(), 2)

    def test_read_kompartemendosen(self):
        kompartemendosen_db = kompartemendosen.objects.get(id_dosen_kompartemen=self.kompartemendosen.id_dosen_kompartemen)
        self.assertEqual(kompartemendosen_db.id_kompartemen, self.kompartemen)
        self.assertEqual(str(kompartemendosen_db.nip), str(self.dosen))

    def test_update_kompartemendosen(self):
        kompartemen_baru = kompartemen.objects.create(nama_kompartemen="Kompartemen Baru")
        self.kompartemendosen.id_kompartemen = kompartemen_baru
        self.kompartemendosen.save()
        kompartemendosen_db = kompartemendosen.objects.get(id_dosen_kompartemen=self.kompartemendosen.id_dosen_kompartemen)
        self.assertEqual(kompartemendosen_db.id_kompartemen, kompartemen_baru)

    def test_delete_kompartemendosen(self):
        kompartemendosen.objects.filter(id_dosen_kompartemen=self.kompartemendosen.id_dosen_kompartemen).delete()
        self.assertEqual(kompartemendosen.objects.count(), 0)  


class UsulanTopikTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', first_name='Test', last_name='User')
        self.user2 = User.objects.create(username='testuser2', first_name='Test2', last_name='User2')
        self.user3 = User.objects.create(username='testuser3', first_name='Test3', last_name='User3')
        self.jadwal = jadwal_semester.objects.create(nama_semester='Semester 1',tahun_semester=2024, tanggal_awal_semester='2023-01-01', tanggal_akhir_semester='2023-06-30')
        self.mahasiswa = mahasiswa.objects.create(nim=123456789,angkatan=2019, semester_daftar_skripsi=self.jadwal, id_user=self.user)
        self.dosen1 = dosen.objects.create(nip=321, id_user=self.user2)
        self.dosen2 = dosen.objects.create(nip=543, id_user=self.user3)
        self.usulan_topik = usulantopik.objects.create(
            nim=self.mahasiswa, 
            permintaan_dosen_1=self.dosen1, 
            permintaan_dosen_2="Dosen 2", 
            judul_topik="Judul topik", 
            keterangan="Keterangan"
        )

    def test_create_usulan_topik(self):
        usulan_topik_baru = usulantopik.objects.create(
            nim=self.mahasiswa, 
            permintaan_dosen_1=self.dosen1, 
            permintaan_dosen_2="Dosen 2", 
            judul_topik="Judul topik baru", 
            keterangan="Keterangan"
        )

        self.assertEqual(usulantopik.objects.count(), 2)
        self.assertEqual(usulan_topik_baru.judul_topik, "Judul topik baru")

    def test_read_usulan_topik(self):
        self.assertEqual(usulantopik.objects.count(), 1)
        self.assertEqual(self.usulan_topik.judul_topik, "Judul topik")

    def test_update_usulan_topik(self):
        self.usulan_topik.judul_topik = "Judul topik terbaru"
        self.usulan_topik.save()

        usulan_topik = usulantopik.objects.get(pk=self.usulan_topik.pk)
        self.assertEqual(usulan_topik.judul_topik, "Judul topik terbaru")

    def test_delete_usulan_topik(self):
        self.usulan_topik.delete()
        self.assertEqual(usulantopik.objects.count(), 0)


class EvaluasiTopikTest(TestCase):

    def setUp(self):
        # create dummy data for testing
        self.kompartemen = kompartemen.objects.create(nama_kompartemen='Kompartemen A')
        self.dosen = dosen.objects.create(nip='1234567890', id_user=User.objects.create(username='dosen1'))
        self.jadwal = jadwal_semester.objects.create(nama_semester='Semester 1',tahun_semester=2024, tanggal_awal_semester='2023-01-01', tanggal_akhir_semester='2023-06-30')
        self.mahasiswa = mahasiswa.objects.create(nim=123456789,angkatan=2019, semester_daftar_skripsi=self.jadwal, id_user=User.objects.create(username='mahasiswa1'))
        # self.mahasiswa = mahasiswa.objects.create(nim='123456789', id_user=User.objects.create(username='mahasiswa1'))
        self.kompartemen_dosen = kompartemendosen.objects.create(id_kompartemen=self.kompartemen, nip=self.dosen)
        self.usulan_topik = usulantopik.objects.create(nim=self.mahasiswa, permintaan_dosen_1=self.dosen, judul_topik='judul topik', file_topik=File(open('./skripsi_app/test_folder/test.txt', 'rb')))
        self.evaluasi_topik = evaluasitopik.objects.create(id_dosen_kompartemen=self.kompartemen_dosen, id_usulan_topik=self.usulan_topik, status_topik=evaluasitopik.SUBMIT, catatan='')

    def test_create_evaluasi_topik(self):
        # create new evaluasi topik
        evaluasi_topik = evaluasitopik.objects.create(
            id_dosen_kompartemen=self.kompartemen_dosen,
            id_usulan_topik=self.usulan_topik,
            status_topik=evaluasitopik.DALAM_EVALUASI,
            catatan='Evaluasi sedang dalam proses',
            tanggal_buat=datetime.now(),
            tanggal_update=datetime.now()
        )
        self.assertEqual(evaluasitopik.objects.count(), 2)

    def test_read_evaluasi_topik(self):
        # retrieve existing evaluasi topik
        evaluasi_topik = evaluasitopik.objects.get(id_evaluasi_topik=self.evaluasi_topik.id_evaluasi_topik)
        self.assertEqual(evaluasi_topik.id_dosen_kompartemen.id_kompartemen, self.kompartemen)
        self.assertEqual(evaluasi_topik.id_usulan_topik, self.usulan_topik)
        self.assertEqual(evaluasi_topik.status_topik, evaluasitopik.SUBMIT)

    def test_update_evaluasi_topik(self):
        # update existing evaluasi topik
        self.evaluasi_topik.status_topik = evaluasitopik.REVISI
        self.evaluasi_topik.catatan = 'Harap perbaiki topik'
        self.evaluasi_topik.save()

        # retrieve updated evaluasi topik
        evaluasi_topik = evaluasitopik.objects.get(id_evaluasi_topik=self.evaluasi_topik.id_evaluasi_topik)
        self.assertEqual(evaluasi_topik.status_topik, evaluasitopik.REVISI)
        self.assertEqual(evaluasi_topik.catatan, 'Harap perbaiki topik')

    def test_delete_evaluasi_topik(self):
        # delete existing evaluasi topik
        self.evaluasi_topik.delete()
        self.assertEqual(evaluasitopik.objects.count(), 0)
        
        
class RoleDosenTestCase(TestCase):

    def setUp(self):
        # create dummy data for testing
        self.dosen = dosen.objects.create(nip='1234567890', id_user=User.objects.create(username='dosen1'))
        self.jadwal = jadwal_semester.objects.create(nama_semester='Semester 1',tahun_semester=2024, tanggal_awal_semester='2023-01-01', tanggal_akhir_semester='2023-06-30')
        self.mahasiswa = mahasiswa.objects.create(nim=123456789,angkatan=2019, semester_daftar_skripsi=self.jadwal, id_user=User.objects.create(username='mahasiswa1'))
        
        # self.mahasiswa = mahasiswa.objects.create(nim='123456789', id_user=User.objects.create(username='mahasiswa1'))
        self.role_dosen = roledosen.objects.create(nip=self.dosen, nim=self.mahasiswa, role=roledosen.P1)

    def test_create_role_dosen(self):
        # create new role dosen
        role_dosen = roledosen.objects.create(
            nip=self.dosen,
            nim=self.mahasiswa,
            role=roledosen.P2,
            status='Active',
            tanggal_buat=datetime.now(),
            tanggal_update=datetime.now()
        )
        self.assertEqual(roledosen.objects.count(), 2)

    def test_read_role_dosen(self):
        # retrieve existing role dosen
        role_dosen = roledosen.objects.get(id_role_dosen=self.role_dosen.id_role_dosen)
        self.assertEqual(str(role_dosen.nip), str(self.dosen))
        self.assertEqual(str(role_dosen.nim), str(self.mahasiswa))
        self.assertEqual(role_dosen.role, roledosen.P1)

    def test_update_role_dosen(self):
        # update existing role dosen
        self.role_dosen.role = roledosen.US1
        self.role_dosen.status = 'Finished'
        self.role_dosen.save()

        # retrieve updated role dosen
        role_dosen = roledosen.objects.get(id_role_dosen=self.role_dosen.id_role_dosen)
        self.assertEqual(role_dosen.role, roledosen.US1)
        self.assertEqual(role_dosen.status, 'Finished')

    def test_delete_role_dosen(self):
        # delete existing role dosen
        self.role_dosen.delete()
        self.assertEqual(roledosen.objects.count(), 0)
        
class DetailPenilaianTest(TestCase):
    def setUp(self):
        self.dosen = dosen.objects.create(nip='1234567890', id_user=User.objects.create(username='dosen1'))
        self.jadwal = jadwal_semester.objects.create(nama_semester='Semester 1',tahun_semester=2024, tanggal_awal_semester='2023-01-01', tanggal_akhir_semester='2023-06-30')
        self.mahasiswa = mahasiswa.objects.create(nim=123456789,angkatan=2019, semester_daftar_skripsi=self.jadwal, id_user=User.objects.create(username='mahasiswa1'))
        # self.mahasiswa = mahasiswa.objects.create(nim='123456789', id_user=User.objects.create(username='mahasiswa1'))
        self.role_dosen = roledosen.objects.create(nip=self.dosen, nim=self.mahasiswa, role='Pembimbing 1')
        self.detail_penilaian = detailpenilaian.objects.create(id_role_dosen=self.role_dosen, nama_tahap='Bimbingan', hasil_review='Hasil review test', status_kelulusan='Lulus')

    def test_create_detail_penilaian(self):
        detail_penilaian = detailpenilaian.objects.create(id_role_dosen=self.role_dosen, nama_tahap='Seminar Proposal', hasil_review='Hasil review test', status_kelulusan='Lulus')
        self.assertEqual(detail_penilaian.id_role_dosen, self.role_dosen)
        self.assertEqual(detail_penilaian.nama_tahap, 'Seminar Proposal')
        self.assertEqual(detail_penilaian.hasil_review, 'Hasil review test')
        self.assertEqual(detail_penilaian.status_kelulusan, 'Lulus')
        self.assertTrue(timezone.now() - detail_penilaian.tanggal_buat < timezone.timedelta(seconds=1))
        self.assertTrue(timezone.now() - detail_penilaian.tanggal_update < timezone.timedelta(seconds=1))

    def test_read_detail_penilaian(self):
        detail_penilaian = detailpenilaian.objects.get(id_detail_penilaian=self.detail_penilaian.id_detail_penilaian)
        self.assertEqual(detail_penilaian.id_role_dosen, self.role_dosen)
        self.assertEqual(detail_penilaian.nama_tahap, 'Bimbingan')
        self.assertEqual(detail_penilaian.hasil_review, 'Hasil review test')
        self.assertEqual(detail_penilaian.status_kelulusan, 'Lulus')
        self.assertTrue(timezone.now() - detail_penilaian.tanggal_buat < timezone.timedelta(seconds=1))
        self.assertTrue(timezone.now() - detail_penilaian.tanggal_update < timezone.timedelta(seconds=1))

    def test_update_detail_penilaian(self):
        detail_penilaian = detailpenilaian.objects.get(id_detail_penilaian=self.detail_penilaian.id_detail_penilaian)
        detail_penilaian.nama_tahap = 'Seminar Hasil'
        detail_penilaian.hasil_review = 'Hasil review test setelah update'
        detail_penilaian.status_kelulusan = 'Tidak Lulus'
        detail_penilaian.save()

        updated_detail_penilaian = detailpenilaian.objects.get(id_detail_penilaian=self.detail_penilaian.id_detail_penilaian)
        self.assertEqual(updated_detail_penilaian.id_role_dosen, self.role_dosen)
        self.assertEqual(updated_detail_penilaian.nama_tahap, 'Seminar Hasil')
        self.assertEqual(updated_detail_penilaian.hasil_review, 'Hasil review test setelah update')
        self.assertEqual(updated_detail_penilaian.status_kelulusan, 'Tidak Lulus')
        self.assertTrue(updated_detail_penilaian.tanggal_buat < updated_detail_penilaian.tanggal_update)

    def test_delete_detail_penilaian(self):
        # detail_penilaian = detailpenilaian.objects.get(id_detail_penilaian=self.detail_penilaian.id_detail_penilaian)
        # detail_penilaian.delete()
        self.detail_penilaian.delete()
        self.assertEqual(detailpenilaian.objects.count(), 0)

        
class SubCpmkModelTestCase(TestCase):

    def setUp(self):
        self.jadwal = jadwal_semester.objects.create(nama_semester='Semester 1',tahun_semester=2024, tanggal_awal_semester='2023-01-01', tanggal_akhir_semester='2023-06-30')
#       self.mahasiswa = mahasiswa.objects.create(nim=123456789,angkatan=2019, semester_daftar_skripsi=self.jadwal, id_user=User.objects.create(username='mahasiswa1'))
        self.cpmk_obj = cpmk.objects.create(id_cpmk='CPMK001',id_nama_semester=self.jadwal,tahun_angkatan=2024, keterangan_cpmk='Deskripsi CPMK 1')
        # cpmk.objects.create(id_cpmk='CPMK002',id_nama_semester=self.jadwal,
#             tahun_angkatan=2024, keterangan_cpmk='Deskripsi cpmk_utama kedua')
        sub_cpmk.objects.create(
            id_sub_cpmk='SubCPMK001',
            tahun_angkatan=2019,
            id_nama_semester=self.jadwal,
            keterangan_sub_cpmk='Deskripsi Sub CPMK 1',
            id_cpmk=self.cpmk_obj,
            bobot_persen_sempro='50%',
            bobot_sempro=0.5,
            bobot_persen_semhas='50%',
            bobot_semhas=0.5,
            bobot_persen_pembimbing='30%',
            bobot_pembimbing=0.3
        )

    def test_create_sub_cpmk(self):
        sub_cpmk_obj = sub_cpmk.objects.create(
            id_sub_cpmk='SubCPMK002',
            keterangan_sub_cpmk='Deskripsi Sub CPMK 2',
            tahun_angkatan=2019,
            id_cpmk=self.cpmk_obj,
            id_nama_semester=self.jadwal,
            bobot_persen_sempro='30%',
            bobot_sempro=0.3,
            bobot_persen_semhas='70%',
            bobot_semhas=0.7,
            bobot_persen_pembimbing='20%',
            bobot_pembimbing=0.2
        )
        self.assertEqual(sub_cpmk_obj.keterangan_sub_cpmk, 'Deskripsi Sub CPMK 2')

    def test_read_sub_cpmk(self):
        sub_cpmk_obj = sub_cpmk.objects.get(id_sub_cpmk='SubCPMK001')
        self.assertEqual(sub_cpmk_obj.keterangan_sub_cpmk, 'Deskripsi Sub CPMK 1')

    def test_update_sub_cpmk(self):
        sub_cpmk_obj = sub_cpmk.objects.get(id_sub_cpmk='SubCPMK001')
        sub_cpmk_obj.keterangan_sub_cpmk = 'Deskripsi Sub CPMK 1 (Updated)'
        sub_cpmk_obj.save()
        self.assertEqual(sub_cpmk_obj.keterangan_sub_cpmk, 'Deskripsi Sub CPMK 1 (Updated)')

    def test_delete_sub_cpmk(self):
        sub_cpmk_obj = sub_cpmk.objects.get(id_sub_cpmk='SubCPMK001')
        sub_cpmk_obj.delete()
        self.assertRaises(sub_cpmk.DoesNotExist, sub_cpmk.objects.get, id_sub_cpmk='SubCPMK001')


class NotifikasiModelTestCase(TestCase):

    def setUp(self):
        notifikasi.objects.create(
            nip='NIP001',
            nim=None,
            messages='Pesan notifikasi 1',
            status=False
        )

    def test_create_notifikasi(self):
        notifikasi_obj = notifikasi.objects.create(
            nip=None,
            nim='NIM002',
            messages='Pesan notifikasi 2',
            status=True
        )
        self.assertEqual(notifikasi_obj.messages, 'Pesan notifikasi 2')

    def test_read_notifikasi(self):
        notifikasi_obj = notifikasi.objects.get(nip='NIP001')
        self.assertEqual(notifikasi_obj.messages, 'Pesan notifikasi 1')

    def test_update_notifikasi(self):
        notifikasi_obj = notifikasi.objects.get(nip='NIP001')
        notifikasi_obj.messages = 'Pesan notifikasi 1 (Updated)'
        notifikasi_obj.save()
        self.assertEqual(notifikasi_obj.messages, 'Pesan notifikasi 1 (Updated)')

    def test_delete_notifikasi(self):
        notifikasi_obj = notifikasi.objects.get(nip='NIP001')
        notifikasi_obj.delete()
        self.assertRaises(notifikasi.DoesNotExist, notifikasi.objects.get, nip='NIP001')




class PenilaianModelTestCase(TestCase):
    def setUp(self):
        # Membuat objek detailpenilaian
        self.dosen = dosen.objects.create(nip='1234567890', id_user=User.objects.create(username='dosen1'))
        self.jadwal = jadwal_semester.objects.create(nama_semester='Semester 1',tahun_semester=2024, tanggal_awal_semester='2023-01-01', tanggal_akhir_semester='2023-06-30')
        self.mahasiswa = mahasiswa.objects.create(nim=123456789,angkatan=2019, semester_daftar_skripsi=self.jadwal, id_user=User.objects.create(username='mahasiswa1'))
        # self.mahasiswa = mahasiswa.objects.create(nim='123456789', id_user=User.objects.create(username='mahasiswa1'))
        self.cpmk_obj = cpmk.objects.create(id_cpmk='CPMK001',id_nama_semester=self.jadwal,tahun_angkatan=2024, keterangan_cpmk='Deskripsi CPMK 1')
        self.role_dosen = roledosen.objects.create(nip=self.dosen, nim=self.mahasiswa, role='Pembimbing 1')
        self.detail_penilaian = detailpenilaian.objects.create(id_role_dosen=self.role_dosen, nama_tahap='Bimbingan', hasil_review='Hasil review test', status_kelulusan='Lulus')
        
        # Membuat objek sub_cpmk
        self.sub_cpmk = sub_cpmk.objects.create(
            id_sub_cpmk='001', 
            keterangan_sub_cpmk='Sub-CPMK 1',
            tahun_angkatan=2019,
            id_cpmk=self.cpmk_obj,
            id_nama_semester=self.jadwal,
            bobot_persen_sempro='30%',
            bobot_sempro=0.3,
            bobot_persen_semhas='50%',
            bobot_semhas=0.5,
            bobot_persen_pembimbing='20%',
            bobot_pembimbing=0.2
        )

        # Membuat objek penilaian
        self.penilaian = penilaian.objects.create(
            id_detail_penilaian=self.detail_penilaian,
            id_sub_cpmk=self.sub_cpmk,
            nilai=85
        )

    def test_create_penilaian(self):
        # Mengecek jumlah objek sebelum dan sesudah pembuatan objek baru
        jumlah_objek_sebelum = penilaian.objects.count()
        penilaian.objects.create(
            id_detail_penilaian=self.detail_penilaian,
            id_sub_cpmk=self.sub_cpmk,
            nilai=90
        )
        jumlah_objek_sesudah = penilaian.objects.count()
        
        # Memastikan objek berhasil dibuat
        self.assertNotEqual(jumlah_objek_sebelum, jumlah_objek_sesudah)

    def test_read_penilaian(self):
        # Membuat query set untuk mencari objek penilaian berdasarkan nilai
        hasil_query = penilaian.objects.filter(nilai=85)

        # Memastikan hanya satu objek yang ditemukan
        self.assertEqual(hasil_query.count(), 1)

        # Memastikan nilai objek ditemukan sama dengan nilai yang diharapkan
        self.assertEqual(hasil_query.first().nilai, 85)

    def test_update_penilaian(self):
        # Mengambil objek penilaian yang sudah dibuat pada setUp
        objek_penilaian = penilaian.objects.get(nilai=85)

        # Mengupdate nilai objek penilaian
        objek_penilaian.nilai = 90
        objek_penilaian.save()

        # Memastikan nilai objek berhasil diupdate
        self.assertEqual(objek_penilaian.nilai, 90)

    def test_delete_penilaian(self):
        # Membuat query set untuk mencari objek penilaian berdasarkan nilai
        objek_penilaian = penilaian.objects.filter(nilai=85).first()

        # Menghapus objek penilaian
        objek_penilaian.delete()

        # Memastikan objek berhasil dihapus
        self.assertEqual(penilaian.objects.filter(nilai=85).count(), 0)
        



class ProposalModelTestCase(TestCase):
    def setUp(self):
        self.jadwal = jadwal_semester.objects.create(nama_semester='Semester 1',tahun_semester=2024, tanggal_awal_semester='2023-01-01', tanggal_akhir_semester='2023-06-30')
        self.mahasiswa = mahasiswa.objects.create(nim=123456789,angkatan=2019, semester_daftar_skripsi=self.jadwal, id_user=User.objects.create(username='mahasiswa1'))
        # self.mahasiswa = mahasiswa.objects.create(nim='123456789', id_user=User.objects.create(username='mahasiswa1'))
        self.proposal = proposal.objects.create(
            nim=self.mahasiswa,
            nama_tahap=proposal.proposal_awal,
            judul_proposal="Test Proposal",
            file_proposal=SimpleUploadedFile("test.pdf", b"content"),
            keterangan="Test Keterangan"
        )
        self.proposal_id = self.proposal.id_proposal

    def test_create_proposal(self):
        mhs = mahasiswa.objects.create(nim="67890",angkatan=2019, semester_daftar_skripsi=self.jadwal,id_user=User.objects.create(username='mahasiswa2'))
        file_proposal = SimpleUploadedFile("test2.pdf", b"content")
        proposal.objects.create(
            nim=mhs,
            nama_tahap=proposal.laporan_akhir,
            judul_proposal="Test Proposal 2",
            file_proposal=file_proposal,
            keterangan="Test Keterangan 2"
        )
        count = proposal.objects.all().count()
        self.assertEqual(count, 2)

    def test_read_proposal(self):
        proposal_baru = proposal.objects.get(id_proposal=self.proposal_id)
        self.assertEqual(str(proposal_baru.nim), str(self.mahasiswa))
        self.assertEqual(proposal_baru.nama_tahap, proposal.proposal_awal)
        self.assertEqual(proposal_baru.judul_proposal, "Test Proposal")
        self.assertEqual(proposal_baru.keterangan, "Test Keterangan")

    def test_update_proposal(self):
        proposal_baru = proposal.objects.get(id_proposal=self.proposal_id)
        proposal_baru.judul_proposal = "Updated Test Proposal"
        proposal_baru.save()
        proposal_baru_2 = proposal.objects.get(id_proposal=self.proposal_id)
        self.assertEqual(proposal_baru_2.judul_proposal, "Updated Test Proposal")

    def test_delete_proposal(self):
        proposal.objects.get(id_proposal=self.proposal_id).delete()
        count = proposal.objects.all().count()
        self.assertEqual(count, 0)



class BimbinganTest(TestCase):
    def setUp(self):
        self.jadwal = jadwal_semester.objects.create(nama_semester='Semester 1',tahun_semester=2024, tanggal_awal_semester='2023-01-01', tanggal_akhir_semester='2023-06-30')
        self.mahasiswa = mahasiswa.objects.create(nim=123456789,angkatan=2019, semester_daftar_skripsi=self.jadwal, id_user=User.objects.create(username='mahasiswa1'))
        # self.mahasiswa = mahasiswa.objects.create(nim='123456789', id_user=User.objects.create(username='mahasiswa1'))
        self.proposal = proposal.objects.create(
            nim=self.mahasiswa,
            nama_tahap=proposal.proposal_awal,
            judul_proposal="Test Proposal",
            file_proposal=SimpleUploadedFile("test.pdf", b"content"),
            keterangan="Test Keterangan"
        )
        self.proposal_id = self.proposal.id_proposal
        # self.proposal = proposal.objects.create(judul='Judul Proposal')
        self.dosen = dosen.objects.create(nip='1234567890', id_user=User.objects.create(username='dosen1'))
        # self.mahasiswa = mahasiswa.objects.create(nim='123456789', id_user=User.objects.create(username='mahasiswa1'))
        self.role_dosen = roledosen.objects.create(nip=self.dosen, nim=self.mahasiswa, role=roledosen.P1)
        self.bimbingan = bimbingan.objects.create(id_proposal=self.proposal, id_role_dosen=self.role_dosen, status_bimbingan='Submit')

    def test_create_bimbingan(self):
        bimbingan_baru = bimbingan.objects.create(id_proposal=self.proposal, id_role_dosen=self.role_dosen, status_bimbingan='ACC')
        self.assertEqual(bimbingan_baru.id_proposal, self.proposal)
        self.assertEqual(bimbingan_baru.id_role_dosen, self.role_dosen)
        self.assertEqual(bimbingan_baru.status_bimbingan, 'ACC')
        self.assertTrue(timezone.now() - bimbingan_baru.tanggal_buat < timezone.timedelta(seconds=1))
        self.assertTrue(timezone.now() - bimbingan_baru.tanggal_update < timezone.timedelta(seconds=1))

    def test_read_bimbingan(self):
        bimbingan_read = bimbingan.objects.get(id_bimbingan=self.bimbingan.id_bimbingan)
        self.assertEqual(bimbingan_read.id_proposal, self.proposal)
        self.assertEqual(bimbingan_read.id_role_dosen, self.role_dosen)
        self.assertEqual(bimbingan_read.status_bimbingan, 'Submit')
        self.assertTrue(timezone.now() - bimbingan_read.tanggal_buat < timezone.timedelta(seconds=1))
        self.assertTrue(timezone.now() - bimbingan_read.tanggal_update < timezone.timedelta(seconds=1))

    def test_update_bimbingan(self):
        bimbingan_update = bimbingan.objects.get(id_bimbingan=self.bimbingan.id_bimbingan)
        bimbingan_update.status_bimbingan = 'Revisi'
        bimbingan_update.save()

        updated_bimbingan = bimbingan.objects.get(id_bimbingan=self.bimbingan.id_bimbingan)
        self.assertEqual(updated_bimbingan.id_proposal, self.proposal)
        self.assertEqual(updated_bimbingan.id_role_dosen, self.role_dosen)
        self.assertEqual(updated_bimbingan.status_bimbingan, 'Revisi')
        self.assertTrue(updated_bimbingan.tanggal_buat < updated_bimbingan.tanggal_update)

    def test_delete_bimbingan(self):
        bimbingan_delete = bimbingan.objects.get(id_bimbingan=self.bimbingan.id_bimbingan)
        bimbingan_delete.delete()
        count = bimbingan.objects.all().count()
        self.assertEqual(count, 0)


class JadwalSeminarModelTestCase(TestCase):
    def setUp(self):
        self.jadwal_semester = jadwal_semester.objects.create(nama_semester='Semester 1',tahun_semester=2024, tanggal_awal_semester='2023-01-01', tanggal_akhir_semester='2023-06-30')
        self.mahasiswa = mahasiswa.objects.create(nim=123456789,angkatan=2019, semester_daftar_skripsi=self.jadwal_semester, id_user=User.objects.create(username='mahasiswa1'))
        self.mahasiswa2 = mahasiswa.objects.create(nim=123456,angkatan=2019, semester_daftar_skripsi=self.jadwal_semester, id_user=User.objects.create(username='mahasiswa2'))
        self.mahasiswa3 = mahasiswa.objects.create(nim=1234566,angkatan=2019, semester_daftar_skripsi=self.jadwal_semester, id_user=User.objects.create(username='mahasiswa3'))
        self.dosen = dosen.objects.create(nip='1234567890', id_user=User.objects.create(username='dosen1'))
        self.dosen2 = dosen.objects.create(nip='123456', id_user=User.objects.create(username='dosen2'))
        self.jadwal = jadwal_seminar.objects.create(
            mahasiswa=self.mahasiswa,
            # dosen_pembimbing_1="Dosen Pembimbing 1",
            # dosen_pembimbing_2="Dosen Pembimbing 2",
            # dosen_penguji_1="Dosen Penguji 1",
            # dosen_penguji_2="Dosen Penguji 2",
            dosen_pembimbing_1=roledosen.objects.create(nip=self.dosen, nim=self.mahasiswa, role=roledosen.P1),
            dosen_pembimbing_2=roledosen.objects.create(nip=self.dosen, nim=self.mahasiswa, role=roledosen.P2),
            dosen_penguji_1=roledosen.objects.create(nip=self.dosen, nim=self.mahasiswa, role=roledosen.US1),
            dosen_penguji_2=roledosen.objects.create(nip=self.dosen, nim=self.mahasiswa, role=roledosen.US2),
            tahap_seminar=jadwal_seminar.tahapan_choices[0][0],
            ruang_seminar=jadwal_seminar.ruangan_seminar_choices[0][0],
            tanggal_seminar=datetime.today(),
            waktu_seminar=datetime.now().time(),
        )
        self.jadwal_id = self.jadwal.id_jadwal_seminar

    def test_create_jadwal_seminar(self):
        jadwal_seminar.objects.create(
            mahasiswa = self.mahasiswa2,
            dosen_pembimbing_1=roledosen.objects.create(nip=self.dosen2, nim=self.mahasiswa2, role=roledosen.P1),
            dosen_pembimbing_2=roledosen.objects.create(nip=self.dosen2, nim=self.mahasiswa2, role=roledosen.P2),
            dosen_penguji_1=roledosen.objects.create(nip=self.dosen2, nim=self.mahasiswa2, role=roledosen.UH1),
            dosen_penguji_2=roledosen.objects.create(nip=self.dosen2, nim=self.mahasiswa2, role=roledosen.UH2),
            tahap_seminar=jadwal_seminar.tahapan_choices[1][0],
            ruang_seminar=jadwal_seminar.ruangan_seminar_choices[1][0],
            tanggal_seminar=datetime.today(),
            waktu_seminar=datetime.now().time(),
        )
        count = jadwal_seminar.objects.all().count()
        self.assertEqual(count, 2)

    def test_read_jadwal_seminar(self):
        jadwal = jadwal_seminar.objects.get(id_jadwal_seminar=self.jadwal_id)
        # self.assertEqual(jadwal.mahasiswa, self.mahasiswa)
        self.assertEqual(str(jadwal.mahasiswa), str(self.mahasiswa))
        self.assertEqual(jadwal.dosen_pembimbing_1, self.jadwal.dosen_pembimbing_1)
        self.assertEqual(jadwal.dosen_pembimbing_2, self.jadwal.dosen_pembimbing_2)
        self.assertEqual(jadwal.dosen_penguji_1, self.jadwal.dosen_penguji_1)
        self.assertEqual(jadwal.dosen_penguji_2, self.jadwal.dosen_penguji_2)

    def test_update_jadwal_seminar(self):
        jadwal = jadwal_seminar.objects.get(id_jadwal_seminar=self.jadwal_id)
        jadwal.mahasiswa = self.mahasiswa3
        jadwal.save()
        jadwal = jadwal_seminar.objects.get(id_jadwal_seminar=self.jadwal_id)
        self.assertEqual(str(jadwal.mahasiswa), str(self.mahasiswa3))

    def test_delete_jadwal_seminar(self):
        jadwal_seminar.objects.get(id_jadwal_seminar=self.jadwal_id).delete()
        count = jadwal_seminar.objects.all().count()
        self.assertEqual(count, 0)
        


class GroupTest(TestCase):
    # @classmethod
    # def setUpTestData(cls):
    #     # Set up non-modified objects used by all test methods
    #     Group.objects.create(name='testgroup')
    def setUp(self):
        self.group=Group.objects.create(name='testgroup')
        self.group2=Group.objects.create(name='testgroup2')
        
    def test_read_group(self):
        group_test = Group.objects.get(name='testgroup')
        self.assertEqual(group_test.name, 'testgroup')
        
    def test_create_group(self):
        Group.objects.create(name='testgroup3')
        group_create = Group.objects.get(name='testgroup3')
        self.assertEqual(group_create.name, 'testgroup3')
        
    def test_update_group(self):
        group_update = Group.objects.get(name='testgroup2')
        group_update.name = 'newtestgroup'
        group_update.save()
        updated_group = Group.objects.get(name='newtestgroup')
        self.assertEqual(updated_group.name, 'newtestgroup')
        
    def test_delete_group(self):
        Group.objects.filter(id=1).delete()
        with self.assertRaises(Group.DoesNotExist):
            Group.objects.get(id=1)          
# class GroupTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Set up non-modified objects used by all test methods
#         Group.objects.create(name='testgroup')
        
#     def test_read_group(self):
#         group_test = Group.objects.get(id=1)
#         self.assertEqual(group_test.name, 'testgroup')
        
#     def test_create_group(self):
#         Group.objects.create(name='testgroup2')
#         group_create = Group.objects.get(id=2)
#         self.assertEqual(group_create.name, 'testgroup2')
        
#     def test_update_group(self):
#         group_update = Group.objects.get(id=1)
#         group_update.name = 'newtestgroup'
#         group_update.save()
#         updated_group = Group.objects.get(id=1)
#         self.assertEqual(updated_group.name, 'newtestgroup')
        
#     def test_delete_group(self):
#         Group.objects.filter(id=1).delete()
#         with self.assertRaises(Group.DoesNotExist):
#             Group.objects.get(id=1)
            

class UserGroupTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpass')
        cls.group = Group.objects.create(name='testgroup')
        cls.user.groups.add(cls.group)

    def test_add_user_to_group(self):
        group2 = Group.objects.create(name='testgroup2')
        self.user.groups.add(group2)
        self.assertEqual(self.user.groups.count(), 2)

    def test_remove_user_from_group(self):
        self.user.groups.remove(self.group)
        self.assertEqual(self.user.groups.count(), 0)

    def test_check_user_group_membership(self):
        self.assertTrue(self.user.groups.filter(name='testgroup').exists())
        self.assertFalse(self.user.groups.filter(name='testgroup2').exists())
        self.assertTrue(self.group.user_set.filter(username='testuser').exists())
        self.assertFalse(self.group.user_set.filter(username='testuser2').exists())

    def test_update_user_group(self):
        group2 = Group.objects.create(name='testgroup2')
        self.user.groups.add(group2)
        self.assertEqual(self.user.groups.count(), 2)
        self.user.groups.remove(self.group)
        self.assertEqual(self.user.groups.count(), 1)
        self.assertTrue(self.user.groups.filter(name='testgroup2').exists())
        self.assertFalse(self.user.groups.filter(name='testgroup').exists())
        self.assertFalse(self.group.user_set.filter(username='testuser').exists())
        self.assertTrue(group2.user_set.filter(username='testuser').exists())
