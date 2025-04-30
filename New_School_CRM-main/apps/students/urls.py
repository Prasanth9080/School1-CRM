from django.urls import path
from . import views 
from .views import *


from .views import (
    DownloadCSVViewdownloadcsv,
    StudentBulkUploadView,
    StudentCreateView,
    StudentDeleteView,
    StudentDetailView,
    StudentListView,
    StudentUpdateView,
   
)

urlpatterns = [
    path("list", StudentListView.as_view(), name="student-list"),
    path("<int:pk>/", StudentDetailView.as_view(), name="student-detail"),
    path("create/", StudentCreateView.as_view(), name="student-create"),
    path("<int:pk>/update/", StudentUpdateView.as_view(), name="student-update"),
    path("delete/<int:pk>/", StudentDeleteView.as_view(), name="student-delete"),
    path("upload/", StudentBulkUploadView.as_view(), name="student-upload"),
    path("download-csv/", DownloadCSVViewdownloadcsv.as_view(), name="download-csv"),

    path('data/', views.studentdata, name='student-data'),
    path('report/', views.studentreport, name='student-report'),
    path('attendance/', views.studentattendance, name='student-attendance'),

    path('leaverequest/', views.student_leave_request, name='student-leave-request'),


    ##### new url for student reportcard

    # path("reportcard/", views.student_report_card_view, name="student-report-card"),
    path("reportcard/", views.student_report_card_view, name="student-report-card"),

    ##### attendance url
    path('student/attendance/', views.student_attendance_view, name='student-attendance-report'),


    ####### /////// ######### razor pay urls :

    path('payments/', views.initiate_payment, name='initiate_payment'),
    path('payments/success/', views.payment_success, name='payment_success'),

]
