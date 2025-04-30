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


