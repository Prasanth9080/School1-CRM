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

    path("attendance/", staffattendance, name="staff-attendance"),
    path("data/", staffdata, name="staff-data"),
    path("leavereport/", staffstuleavereport, name="staff-student-leave-report"),
    path("class/", staffclasssechedule, name="staff-class-sechedule"),

    path('leaverequest/', views.staff_leave_request, name='staff-leave-request'),

##### new url for student reportcard
    path("reportcards/", reportcard_list, name="staff-reportcard-list"),
    path("reportcards/create/", reportcard_create, name="staff-reportcard-create"),
    path("reportcards/<int:pk>/update/", reportcard_update, name="staff-reportcard-update"),
    path("reportcards/<int:pk>/delete/", reportcard_delete, name="staff-reportcard-delete"),


##### attendance url

# staff urls
path('staff/attendance/', views.attendance_list, name='staff-attendance-list'),
path('staff/attendance/create/', views.attendance_create, name='staff-attendance-create'),
path('staff/attendance/<int:pk>/edit/', views.attendance_update, name='staff-attendance-update'),
path('staff/attendance/<int:pk>/delete/', views.attendance_delete, name='staff-attendance-delete'),


###### new url for staff
    path('staff-attendance/', views.staff_attendance_view, name='staff-attendance-view'),

]
