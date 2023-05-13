import os

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_skripsi.settings')

from django.test import Client
from locust import HttpUser, task, between,TaskSet

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.login()
        
    def login(self):    
        # Login ke aplikasi menggunakan built-in Django login
        # self.client = Client()
        # self.client.login(username="admin1", password="adminadmin123321")
        response = self.client.get('login/',name="login")
        csrftoken = response.cookies['csrftoken']
        self.client.post('login/?=next/',{'username':'admin1','password':'adminadmin123321'},headers={'X-CSRFtoken':csrftoken}, name="login")

    @task
    def view_homepage(self):
        self.client.get("",name='start')
        
    @task
    def view_dashboard(self):
        self.client.get("dashboard",name='dashboard')
