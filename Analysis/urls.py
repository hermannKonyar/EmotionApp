from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.image_upload_and_analyze, name='image_upload_and_analyze'),
]
