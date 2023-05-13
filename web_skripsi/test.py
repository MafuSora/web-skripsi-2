import os

# Mendapatkan direktori dari file saat ini (misalnya manage.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigasi ke atas (menuju folder root proyek)
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))

# Mencetak jalur absolut menuju folder root proyek
print(project_root)