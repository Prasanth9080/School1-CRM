from django.urls import path
from . import views 
from .views import *


urlpatterns = [

    path('attendance/', views.principal_dashboard, name='principal-data'),
    path("staff/leavereport/", principalstaffleavereport, name="principal-staff-leave-report"),
    # path('leave-request/', views.student_leave_request, name='student-leave-request'),

    ##### new url for staff attendance
    path('staff/attendance/', views.staff_attendance_list, name='principal-attendance-list'),
    path('staff/attendance/create/', views.staff_attendance_create, name='principal-attendance-create'),
    path('staff/attendance/<int:pk>/edit/', views.staff_attendance_update, name='principal-attendance-update'),
    path('staff/attendance/<int:pk>/delete/', views.staff_attendance_delete, name='principal-attendance-delete'),


    path('notifications/', views.principal_notifications, name='principal_notifications'),
    path('notifications/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('notifications/mark-read-principal/<int:notification_id>/', views.mark_notification_as_read_for_principal, name='mark_notification_as_read_for_principal'),
    path('notifications/delete-selected/', views.delete_selected_notifications, name='delete_selected_notifications'),

    ##### student fees record urls

    # path('student-fees/', views.principal_student_fees_management, name='principal-student-fees'),
    # path('student-fees/add/', views.principal_add_student_fee, name='principal-add-student-fee'),
    # path('student-fees/<int:fee_id>/edit/', views.principal_edit_student_fee, name='principal-edit-student-fee'),
    # path('student-fees/<int:fee_id>/delete/', views.principal_delete_student_fee, name='principal-delete-student-fee'),


    # path('student-fees', views.principal_student_fees, name="principal-student-fees"),
    # path('student-fees/<int:fee_id>/delete', views.principal_delete_student_fee, name="principal-delete-student-fee")

##### student fee record only hide on principal role #####
    path('student-fees/', views.principal_student_fees, name='principal-student-fees'),
    path('student-fees/<int:fee_id>/hide/', views.principal_hide_student_fee, name='principal-hide-student-fee'),

]
 