# urls.py
from django.urls import path
from skin_analysis import views

app_name = 'skin_analysis'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_image, name='upload'),
    path('analysis/<int:analysis_id>/', views.view_analysis, name='analysis'),
    path('history/', views.analysis_history, name='history'),
]