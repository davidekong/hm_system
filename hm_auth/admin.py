from django.contrib import admin
from .models import Patient, HospitalPersonnel, Hospital, MedicalRecord
# Register your models here.
admin.site.register(Patient)
admin.site.register(HospitalPersonnel)
admin.site.register(Hospital)
admin.site.register(MedicalRecord)