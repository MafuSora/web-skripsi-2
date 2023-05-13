from django.contrib import admin
from .models import dosen, mahasiswa, kompartemen
# Register your models here.
admin.site.register(dosen)
admin.site.register(mahasiswa)
admin.site.register(kompartemen)
