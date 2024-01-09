from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('add-an-account/', views.add_account, name='add_account'),
    path('add-a-patient/', views.add_patient, name='add_patient'),
    path('add-a-personnel/', views.add_personnel, name='add_personnel'),
]