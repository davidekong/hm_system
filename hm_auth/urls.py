from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.logIn, name='login'),
    path('home/', views.home, name='home'),
    path('pick-an-account/', views.choose_add_account, name='choose_add_account'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('join-hospital/', views.join_hospital, name='join_hospital'),
    path('add-hospital/', views.add_hospital, name='add_hospital'),
    path('logout/', views.logout_user, name='logout'),
    path('table/', views.table, name='table'),
]