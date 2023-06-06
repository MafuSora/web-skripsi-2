# DJANGO 101

## Creating Virtual Environment

1. Install VirtualEnvironment Library

> ``pip install virtualenv ``
> ``virtualenv <virtual_environment_name>``

2. Use This Command

> ``virtualenv --python C:\Users\<computer_name>\AppData\Local\Programs\Python\Python310\python.exe env``

3. still stuck, use this command

> ``python3 -m venv <virtual_environment_name>``

## Start Virtual ENV

* Use this command

> ``venv\Scripts\Activate.ps1``

## Stop Virtual Environment

* Use this command

> ``deactivate``

## HOW TO MAKE : REQUIREMENT.TXT

1. install all pip

```
pip install django
pip install django-mathfilters
pip install crispy-bootstrap5
pip install django-crispy-forms
pip install django-cleanup
pip install psycopg2
pip install pillow
pip install gunicorn
pip install django-cors-headers
pip install django-googledrive-storage
```

## HOW TO INSTALL : FREEZING REQUIREMENTS MODULE

* Use this command to make the requirements.txt

> ``pip freeze > requirements.txt``

## HOW TO INSTALL : REQUIREMENT.TXT

* Use this command

> ``pip install -r requirements.txt``

## CHANGE TO FREE POSTGRE DB

*1.* Neon.tech

```
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'neondb',
    'USER': '******',
    'PASSWORD': '********',
    'HOST': ******.ap-southeast-1.aws.neon.tech',
    'PORT': '5432',
  }
}
```

*2.* supabase

```
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'postgres',
    'USER': 'postgres',
    'PASSWORD': '******',
    'HOST': 'db.******.supabase.co',
    'PORT': '5432',
  }
}
```

*3.* SQLite

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## FREE HOSTING

* Free For Python :

> * Python Anywhere
> * Vercell

## Free DB

* DB POSTGRE :

> * supabase (500MB)
> * neon.tech (3000MB)

## some reference:

* White Noise heroku isssue :

> https://whitenoise.evans.io/en/stable/django.html

* Azure BLOB :

> https://stackoverflow.com/questions/69605603/what-should-go-in-my-procfile-for-a-django-application

* Azure BLOB :

> https://medium.com/@DawlysD/django-using-azure-blob-storage-to-handle-static-media-assets-from-scratch-90cbbc7d56be

* Amazon Bucket S3 :

> https://simpleisbetterthancomplex.com/tutorial/2017/08/01/how-to-setup-amazon-s3-in-a-django-project.html

* Drive Can save file thread :

> https://stackoverflow.com/questions/59254707/how-to-use-google-drive-to-save-media-files-for-a-django-app-that-is-deployed-in

* Free 15 GB :

> https://django-googledrive-storage.readthedocs.io/en/latest/#installation

* search file GDrive :

> https://developers.google.com/drive/api/guides/search-files#python

* drive api docs :

> https://developers.google.com/drive/api

* SMTP :

> https://kb.synology.com/en-my/SRM/tutorial/How_to_use_Gmail_SMTP_server_to_send_emails_for_SRM

* datatable (export table to document) :
* chartJS  (Make a chart) :
* Bootstrap 5 :
* Select 2 :
* Fontawesome :

## WHEN CANNOT ENTER  VIRTUAL ENVIRONMENT environment

1. Use This Command

> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted

2. Still Stuck, Use This Command

> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted -Force

3. Still Stuck, Use this command

> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass -Force

## Create django Project

* Use this command
  > ``django-admin startproject <project_name>``
  >

## Create django App

* Use this command

> ``django-admin startapp <app_name>``

## Dump Data :JSON

> ``python manage.py dumpdata > name_file.json``

## Load Data :JSON

> ``python manage.py loaddata name_file.json``

## INSTALL LOAD TEST

> ``pip install locust``

## LOCUST LOAD TEST

> ``locust -f load_test.py``

## RUN UNIT TESTING : Different Folder

> ``python manage.py test name_folder.name_file``

## RUN UNIT TESTING : Same Folder

> ``python manage.py test name_file``

# COVERAGE TEST

> ```
> pip install coverage
> coverage run --source "module_will_be_tested" manage.py test -v 2
>
> coverage report
> ```

# REPORT COVERAGE : HTML

`coverage html`

# For Debugging

1. Make Sure See The Cronologist Email Report On Web Skripsi Gmail Account or ask the chronologist to person who got error
2. On Django Don't Forget To turn off `DEBUG=False` To `DEBUG=True`
