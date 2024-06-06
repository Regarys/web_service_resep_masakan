from django.urls import path, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    DetailResepMasakanApiView, MenuUtamaApiView, RegisterUserAPIView, LoginView, DetailresepMasakanView, LogoutAPIView,
)

app_name = 'api'
urlpatterns = [
    path('api/detail_resep_masakan', views.DetailResepMasakanListApiView.as_view()),
    path('api/menu_utama', views.MenuUtamaListApiView.as_view()),
    path('api/detail_resep_masakan/<int:id>', views.DetailResepMasakanApiView.as_view()),
    path('api/menu_utama/<int:id>', views.MenuUtamaApiView.as_view()),
    path('api/register', RegisterUserAPIView.as_view()),
    path('api/login', LoginView.as_view()),
    path('api/logout', views.LogoutAPIView.as_view()),
    path('api/detail_resep', views.DetailresepMasakanView.as_view()),
    path('api/detail_menu_filter/', views.DetailResepMasakanFilterApi.as_view()),
]