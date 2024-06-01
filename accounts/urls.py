from django.urls import path
from . import views

urlpatterns = [
    path('accounts/login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('accounts/logout/',views.exit,name='exit'),
]