from django.urls import path

from . import views


app_name = 'service' 

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_file, name='upload'),
    path('user_files/', views.user_files, name='user_files'),
    path('download/<int:file_id>/', views.download_file, name='download'),
]
