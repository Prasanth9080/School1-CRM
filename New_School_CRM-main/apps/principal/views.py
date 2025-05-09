from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.staffs.models import LeaveRequeststaff


def principal_dashboard(request):
    return render (request, "principal/principal_data.html")

@login_required
def principalstaffleavereport(request):
    leaves = LeaveRequeststaff.objects.all()

    if request.method == "POST":
        leave_id = request.POST.get("leave_id")
        action = request.POST.get("action")
        leave = LeaveRequeststaff.objects.get(id=leave_id)
        if action == "approve":
            leave.status = "approved"
        elif action == "reject":
            leave.status = "rejected"
        leave.save()
        return redirect('principal-staff-leave-report')

    return render(request, "principal/principal_staffleavereport.html", {"leaves": leaves})




##### attendance function for staff ######


from django.shortcuts import render, redirect, get_object_or_404
from ..staffs.models import StaffAttendanceRecord
from ..staffs.forms import StaffAttendanceForm
from django.contrib.auth.decorators import login_required

# Principal - manage all staff attendance
@login_required
def staff_attendance_list(request):
    records = StaffAttendanceRecord.objects.all()
    return render(request, 'principal/principal_attendance_list.html', {'records': records})

@login_required
def staff_attendance_create(request):
    form = StaffAttendanceForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('principal-attendance-list')
    return render(request, 'principal/principal_attendance_form.html', {'form': form})

@login_required
def staff_attendance_update(request, pk):
    record = get_object_or_404(StaffAttendanceRecord, pk=pk)
    form = StaffAttendanceForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('principal-attendance-list')
    return render(request, 'principal/principal_attendance_form.html', {'form': form})

@login_required
def staff_attendance_delete(request, pk):
    record = get_object_or_404(StaffAttendanceRecord, pk=pk)
    record.delete()
    return redirect('principal-attendance-list')




##########

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..students.models import StaffNotification

@login_required
def principal_notifications(request):
    print("Current user:", request.user.username)
    notifications = StaffNotification.objects.all().order_by('-created_at')
    unread_count = StaffNotification.objects.all().filter(is_read=False).count()
    # notifications.update(is_read=True)
    return render(request, 'principal/principal_notification.html', 
                  {'notifications': notifications, 'unread_count':unread_count})


from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

@csrf_protect
@login_required
def delete_notification(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(StaffNotification, id=notification_id)
        notification.delete()
        messages.success(request, "Notification deleted successfully.")
    return redirect('principal_notifications') 


@login_required
def mark_notification_as_read_for_principal(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(StaffNotification, id=notification_id)
        notification.is_read = True
        notification.save()
        messages.success(request, "Notification marked as read.")
    return redirect('principal_notifications')  # or 'staff_notifications' based on role


######### student fees record management functionalities ##########


from django.shortcuts import render
from ..staffs.models import StudentFeesRecord
from .models import Principal_StudentFeesRecord

def principal_student_fees(request):
    fees = StudentFeesRecord.objects.select_related('student').all()
    return render(request, 'principal/principal_student_fees.html', {'fees': fees})

def principal_delete_student_fee(request, fee_id):
    fee = get_object_or_404(Principal_StudentFeesRecord, id=fee_id)
    fee.delete()
    return redirect('principal-student-fees')