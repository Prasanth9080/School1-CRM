from django.urls import path
from . import views 
from .views import *


urlpatterns = [

    path('attendance/', views.principal_dashboard, name='principal-data'),
    path("leavereport/", principalstaffleavereport, name="principal-staff-leave-report"),
    # path('leave-request/', views.student_leave_request, name='student-leave-request'),

    ##### new url for staff attendance
    path('principal/attendanceeee/', views.staff_attendance_list, name='principal-attendance-list'),
    path('principal/attendance/create/', views.staff_attendance_create, name='principal-attendance-create'),
    path('principal/attendance/<int:pk>/edit/', views.staff_attendance_update, name='principal-attendance-update'),
    path('principal/attendance/<int:pk>/delete/', views.staff_attendance_delete, name='principal-attendance-delete'),

]
 