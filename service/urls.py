from django.urls import path

from . import views


app_name = 'service' 

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file')
]
