from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Staff


class StaffListView(ListView):
    model = Staff


class StaffDetailView(DetailView):
    model = Staff
    template_name = "staffs/staff_detail.html"


class StaffCreateView(SuccessMessageMixin, CreateView):
    model = Staff
    fields = "__all__"
    success_message = "New staff successfully added"

    def get_form(self):
        """add date picker in forms"""
        form = super(StaffCreateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 1})
        return form


class StaffUpdateView(SuccessMessageMixin, UpdateView):
    model = Staff
    fields = "__all__"
    success_message = "Record successfully updated."

    def get_form(self):
        """add date picker in forms"""
        form = super(StaffUpdateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 1})
        return form


class StaffDeleteView(DeleteView):
    model = Staff
    success_url = reverse_lazy("staff-list")


from django.shortcuts import  render

# def staffattendance(request):
#     return render (request, "staffs/staff_attendance.html")

from apps.staffs.models import LeaveRequeststaff
from .forms import LeaveRequeststaffForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def staffattendance(request):
    staff = request.user
    leaves = LeaveRequeststaff.objects.filter(staff=staff)

    if request.method == "POST":
        form = LeaveRequeststaffForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.staff = staff
            leave.save()
            return redirect('staff-attendance')
    else:
        form = LeaveRequeststaffForm()

    return render(request, 'staffs/staff_attendance.html', {
        'leaves': leaves,
        'form': form
    })

# def staffstuleavereport(request):
#     return render (request, "staffs/staff_stuleavereport.html")

# staffs/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.students.models import LeaveRequeststudent

@login_required
def staffstuleavereport(request):
    leaves = LeaveRequeststudent.objects.all()

    if request.method == "POST":
        leave_id = request.POST.get("leave_id")
        action = request.POST.get("action")
        leave = LeaveRequeststudent.objects.get(id=leave_id)
        if action == "approve":
            leave.status = "approved"
        elif action == "reject":
            leave.status = "rejected"
        leave.save()
        return redirect('staff-student-leave-report')

    return render(request, "staffs/staff_stuleavereport.html", {"leaves": leaves})


def staffdata(request):
    return render (request, "staffs/staff_data.html")

def staffclasssechedule(request):
    return render (request, "staffs/staff_classsechedule.html")



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LeaveRequeststaffForm
from .models import LeaveRequeststaff


@login_required
def staff_leave_request(request):
    if request.method == 'POST':
        form = LeaveRequeststaffForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.staff = request.user
            leave.save()
            return redirect('staff-attendance')  # or show confirmation
    else:
        form = LeaveRequeststaffForm()
    
    return render(request, 'staffs/staff_leave_request.html', {'form': form})


###### new function for student report card


from django.shortcuts import render, redirect, get_object_or_404
from ..students.models import StuReportCard
from ..students.forms import StuReportCardForm
from django.contrib.auth.decorators import login_required

@login_required
def reportcard_list(request):
    cards = StuReportCard.objects.all()
    return render(request, 'staffs/reportcard_list.html', {'cards': cards})

@login_required
def reportcard_create(request):
    if request.method == 'POST':
        form = StuReportCardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff-reportcard-list')
    else:
        form = StuReportCardForm()
    return render(request, 'staffs/reportcard_form.html', {'form': form})

@login_required
def reportcard_update(request, pk):
    card = get_object_or_404(StuReportCard, pk=pk)
    form = StuReportCardForm(request.POST or None, instance=card)
    if form.is_valid():
        form.save()
        return redirect('staff-reportcard-list')
    return render(request, 'staffs/reportcard_form.html', {'form': form})

@login_required
def reportcard_delete(request, pk):
    card = get_object_or_404(StuReportCard, pk=pk)
    card.delete()
    return redirect('staff-reportcard-list')


######## attendance record function for staff

# staffs/views.py

from ..students.models import AttendanceRecord
from ..students.forms import AttendanceRecordForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

@login_required
def attendance_list(request):
    records = AttendanceRecord.objects.all()
    return render(request, 'staffs/staff_attendance_list.html', {'records': records})

@login_required
def attendance_create(request):
    form = AttendanceRecordForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('staff-attendance-list')
    return render(request, 'staffs/staff_attendance_form.html', {'form': form})

@login_required
def attendance_update(request, pk):
    record = get_object_or_404(AttendanceRecord, pk=pk)
    form = AttendanceRecordForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('staff-attendance-list')
    return render(request, 'staffs/staff_attendance_form.html', {'form': form})

@login_required
def attendance_delete(request, pk):
    record = get_object_or_404(AttendanceRecord, pk=pk)
    record.delete()
    return redirect('staff-attendance-list')


###### attendance record function for staff

from django.shortcuts import render, redirect, get_object_or_404
from .models import StaffAttendanceRecord
from django.contrib.auth.decorators import login_required

# Staff - read-only view of their attendance
@login_required
def staff_attendance_view(request):
    records = StaffAttendanceRecord.objects.filter(staff=request.user)
    return render(request, 'staffs/staff_attendance_report.html', {'records': records})
