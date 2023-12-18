
from django.contrib import admin
from django.urls import path
from main.views import AdmissionViewSet

urlpatterns = [
    path("enroll_student", AdmissionViewSet.as_view({"post":"enroll_student"})),
    path("update_student", AdmissionViewSet.as_view({"post":"update_student"})),
]
