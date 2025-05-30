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

@csrf_protect
@login_required
def delete_selected_notifications(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_notifications')
        StaffNotification.objects.filter(id__in=selected_ids).delete()
        messages.success(request, f"{len(selected_ids)} notification(s) deleted successfully.")
    return redirect('principal_notifications')




######### student fees record management functionalities only hide for principal role 
# not fully deleted staff and also database ##########


from django.shortcuts import render, redirect, get_object_or_404
from ..staffs.models import StudentFeesRecord

def principal_student_fees(request):
    fees = StudentFeesRecord.objects.select_related('student').filter(hidden_by_principal=False)
    return render(request, 'principal/principal_student_fees.html', {'fees': fees})

def principal_hide_student_fee(request, fee_id):
    fee = get_object_or_404(StudentFeesRecord, id=fee_id)
    fee.hidden_by_principal = True
    fee.save()
    return redirect('principal-student-fees')



########################### principal ciculation sent function

from django.shortcuts import render, get_object_or_404, redirect
from .models import Circulation
from .forms import CirculationForm
from django.contrib.auth.decorators import login_required

@login_required
def circulation_list(request):
    circulations = Circulation.objects.all().order_by('-created_at')
    return render(request, 'principal/principal_circulation.html', {'circulations': circulations})

@login_required
def circulation_create(request):
    if request.method == 'POST':
        form = CirculationForm(request.POST)
        if form.is_valid():
            circulation = form.save(commit=False)
            circulation.created_by = request.user
            circulation.save()
            return redirect('circulation_list')
    else:
        form = CirculationForm()
    return render(request, 'principal/principal_circulation_form.html', {'form': form})

@login_required
def circulation_edit(request, pk):
    circulation = get_object_or_404(Circulation, pk=pk)
    form = CirculationForm(request.POST or None, instance=circulation)
    if form.is_valid():
        form.save()
        return redirect('circulation_list')
    return render(request, 'principal/principal_circulation_form.html', {'form': form})

@login_required
def circulation_delete(request, pk):
    circulation = get_object_or_404(Circulation, pk=pk)
    if request.method == 'POST':
        circulation.delete()
        messages.success(request,"Circulation message deleted successfully")
        return redirect('circulation_list')
    return render(request, 'principal/principal_circulation_confirm_delete.html', {'circulation': circulation})


######## student circulation views

from .models import Circulation, CirculationReadHide

@login_required
def student_circulation_view(request):
    # Filter: audience=all or students, and not hidden by this student
    hidden_ids = CirculationReadHide.objects.filter(user=request.user, role='student').values_list('circulation_id', flat=True)
    circulations = Circulation.objects.filter(audience__in=['all', 'students']).exclude(id__in=hidden_ids).order_by('-created_at')
    return render(request, 'students/student_circulation.html', {'circulations': circulations})


####### staff circulation views

@login_required
def staff_circulation_view(request):
    hidden_ids = CirculationReadHide.objects.filter(user=request.user, role='staff').values_list('circulation_id', flat=True)
    circulations = Circulation.objects.filter(audience__in=['all', 'staff']).exclude(id__in=hidden_ids).order_by('-created_at')
    return render(request, 'staffs/staff_circulation.html', {'circulations': circulations})


####### hide circulation view

@login_required
def hide_circulation(request, pk, role):
    circulation = get_object_or_404(Circulation, pk=pk)
    CirculationReadHide.objects.get_or_create(user=request.user, circulation=circulation, role=role)
    if role == 'student':
        messages.success(request,"Deleted successfully")
        return redirect('student-circulation')
    else:
        messages.success(request, "Deleted successfully")
        return redirect('staff-circulation')
