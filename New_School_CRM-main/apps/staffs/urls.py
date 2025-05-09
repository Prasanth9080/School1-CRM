from django.urls import path
from . views import *

from . import views

from .views import (
    StaffCreateView,
    StaffDeleteView,
    StaffDetailView,
    StaffListView,
    StaffUpdateView,
)

urlpatterns = [
    path("list/", StaffListView.as_view(), name="staff-list"),
    path("<int:pk>/", StaffDetailView.as_view(), name="staff-detail"),
    path("create/", StaffCreateView.as_view(), name="staff-create"),
    path("<int:pk>/update/", StaffUpdateView.as_view(), name="staff-update"),
    path("<int:pk>/delete/", StaffDeleteView.as_view(), name="staff-delete"),

    path("staff-leave/", staffattendance, name="staff-attendance"),
    path("data/", staffdata, name="staff-data"),
    path("students/leavereport/", staffstuleavereport, name="staff-student-leave-report"),
    path("staff-class/", staffclasssechedule, name="staff-class-sechedule"),

    path('leaverequest/', views.staff_leave_request, name='staff-leave-request'),

##### new url for student reportcard
    path("students/reportcards/", reportcard_list, name="staff-reportcard-list"),
    path("students/reportcards/create/", reportcard_create, name="staff-reportcard-create"),
    path("students/reportcards/<int:pk>/update/", reportcard_update, name="staff-reportcard-update"),
    path("students/reportcards/<int:pk>/delete/", reportcard_delete, name="staff-reportcard-delete"),


##### attendance url

# staff urls
path('students/attendance/', views.attendance_list, name='staff-attendance-list'),
path('students/attendance/create/', views.attendance_create, name='staff-attendance-create'),
path('students/attendance/<int:pk>/edit/', views.attendance_update, name='staff-attendance-update'),
path('students/attendance/<int:pk>/delete/', views.attendance_delete, name='staff-attendance-delete'),


###### new url for staff
    path('staff-attendance/', views.staff_attendance_view, name='staff-attendance-view'),
##### notfication url:
    path('notifications/', views.staff_notifications, name='staff_notifications'),
    path('notifications/hide/<int:notification_id>/', views.hide_notification, name='hide_notification'),
    # path('notifications/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('notifications/mark-read-staff/<int:notification_id>/', views.mark_notification_as_read_for_staff, name='mark_notification_as_read_for_staff'),


###### standard student fees url

# path('student-fees/', views.student_fees_management, name='student-fees'),

    path('students/fees/', views.student_fees_management, name='student-fees'),
    path('students/fees/add/', views.add_student_fee, name='add-student-fee'),
    path('students/fees/<int:fee_id>/edit/', views.edit_student_fee, name='edit-student-fee'),
    path('students/fees/<int:fee_id>/delete/', views.delete_student_fee, name='delete-student-fee'),

]
  