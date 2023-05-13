DJANGO 101

--WHEN CANNOT ENTER  virtual environment --
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
    or
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted -Force
    or 
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass -Force

--create venv--
virtualenv --python C:\Users\ADMIN\AppData\Local\Programs\Python\Python310\python.exe env

--start venv--
& d:/Hafizh/web-skripsi/env/Scripts/Activate.ps1

---REQUIREMENT.TXT how to make it ---
install all pip then ,
pip freeze > requirements.txt

-- install requirements.txt--
pip install -r requirements.txt

-- start poroject django--
django-admin startproject web-si-skripsi

--start app django--
django-admin startapp app-skripsi
