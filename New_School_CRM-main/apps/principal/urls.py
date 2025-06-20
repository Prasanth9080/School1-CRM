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


    ######## principal circulation:
    # path('add/', views.add_circulation, name='add_circulation'),
    # path('edit/<int:pk>/', views.edit_circulation, name='edit_circulation'),
    # path('delete/<int:pk>/', views.delete_circulation, name='delete_circulation'),
    # path('list/', views.view_circulations, name='view_circulations'),

    path('circulation/', views.circulation_list, name='circulation_list'),
    path('circulation/create/', views.circulation_create, name='circulation_create'),
    path('circulation/edit/<int:pk>/', views.circulation_edit, name='circulation_edit'),
    path('circulation/delete/<int:pk>/', views.circulation_delete, name='circulation_delete'),
    
   ######## student circulation url

    path('student/circulations/', views.student_circulation_view, name='student-circulation'),
    path('circulation/hide/<int:pk>/<str:role>/', views.hide_circulation, name='hide-circulation'),

    ####### staff circulation url

    path('staff/circulations/', views.staff_circulation_view, name='staff-circulation'),
    path('circulation/hide/<int:pk>/<str:role>/', views.hide_circulation, name='hide-circulation'),


    ##### for staffclass schedule 

    
    path('class-schedule/', views.class_schedule_list, name='principal-class-schedule-list'),
    path('class-schedule/create/', views.class_schedule_create, name='principal-cls-schedule-create'),
    path('class-schedule/edit/<int:pk>/', views.class_schedule_edit, name='principal-cls-schedule-edit'),
    path('class-schedule/delete/<int:pk>/', views.class_schedule_delete, name='principal-cls-schedule-delete'),



    # Staff URL to view their own schedule
    path('staff/class-schedule/', views.staff_class_schedule_view, name='staff-class-schedule'),


]   
 