from django.urls import path

from . import views


app_name = 'service' 

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_file, name='upload'),
    path('download/', views.download_file, name='download'),
]
