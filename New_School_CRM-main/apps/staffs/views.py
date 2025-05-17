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
        # form = StuReportCardForm(initial={'term': request.GET.get('term', 'Term I')})  # prefill term if passed

    return render(request, 'staffs/reportcard_form.html', {'form': form})

# @login_required
# def reportcard_create(request):
#     if request.method == 'POST':
#         form = StuReportCardForm(request.POST)
#         if form.is_valid():
#             new_card = form.save(commit=False)
#             # Auto-assign Term
#             existing_cards = StuReportCard.objects.filter(student=new_card.student).order_by('created_at')

#             existing_terms = existing_cards.values_list('term', flat=True)

#             if "Term I" not in existing_terms:
#                 new_card.term = "Term I"
#             elif "Term II" not in existing_terms:
#                 new_card.term = "Term II"
#             else:
#                 # fallback if more terms needed
#                 new_card.term = f"Term {len(existing_terms) + 1}"

#             new_card.save()
#             return redirect('staff-reportcard-list')
#     else:
#         form = StuReportCardForm()
#     return render(request, 'staffs/reportcard_form.html', {'form': form})


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


##### notification function for staff
# from django.contrib.admin.views.decorators import staff_member_required
# from ..students.models import StaffNotification

# @staff_member_required
# def staff_notifications(request):
#     notifications = StaffNotification.objects.all().order_by('-created_at')
#     return render(request, 'staffs/staff_notification.html', {'notifications': notifications})


# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseForbidden
# from ..students.models import StaffNotification

# @login_required
# def staff_notifications(request):
#     if not request.user.groups.filter(name="Staff").exists() and not request.user.is_staff:
#         return HttpResponseForbidden("You do not have permission to view this page.")

#     notifications = StaffNotification.objects.all().order_by('-created_at')
#     return render(request, 'staffs/staff_notification.html', {'notifications': notifications})


############### staff notification function working good and also delete function working good

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from ..students.models import StaffNotification

# @login_required
# def staff_notifications(request):
#     print("Current user:", request.user.username)
#     notifications = StaffNotification.objects.all().order_by('-created_at')
#     notifications.update(is_read=True)
#     return render(request, 'staffs/staff_notification.html', {'notifications': notifications})


# from django.shortcuts import redirect, get_object_or_404
# from django.views.decorators.csrf import csrf_protect
# from django.contrib import messages

# @csrf_protect
# @login_required
# def delete_notification(request, notification_id):
#     if request.method == 'POST':
#         notification = get_object_or_404(StaffNotification, id=notification_id)
#         notification.delete()
#         messages.success(request, "Notification deleted successfully.")
#     return redirect('staff_notifications')



######### now, staff notification once delete panna adminpanle la delet agama, staff template la matum hide agum
######### but now, admin panel la delete panna staff panel la delete agum

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from ..students.models import StaffNotification, HiddenNotification
from django.http import HttpResponseForbidden

@login_required
def staff_notifications(request):
    # Get list of notification IDs hidden by current staff
    hidden_ids = HiddenNotification.objects.filter(
        staff=request.user
    ).values_list('notification_id', flat=True)

    # Exclude hidden notifications
    notifications = StaffNotification.objects.exclude(id__in=hidden_ids).order_by('-created_at')
    # unread_count = StaffNotification.objects.all().filter(is_read=False).count()
    unread_count = notifications.filter(is_read=False).count()
    # Mark visible notifications as read
    # notifications.update(is_read=True)

    return render(request, 'staffs/staff_notification.html', 
                  {'notifications': notifications, 
                   'unread_count':unread_count
                   })
@csrf_protect
@login_required
def mark_notification_as_read_for_staff(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(StaffNotification, id=notification_id)
        notification.is_read = True
        notification.save()
        messages.success(request, "Notification marked as read.")
    return redirect('staff_notifications')


@csrf_protect
@login_required
def hide_notification(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(StaffNotification, id=notification_id)

        # Only staff (non-superusers) can hide
        if request.user.is_superuser:
            return HttpResponseForbidden("Principal should delete in admin panel, not hide.")

        HiddenNotification.objects.get_or_create(staff=request.user, notification=notification)
        messages.success(request, "Notification hidden.")
    return redirect('staff_notifications')

@csrf_protect
@login_required
def hide_selected_notifications(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_notifications')
        notifications = StaffNotification.objects.filter(id__in=selected_ids)

        if request.user.is_superuser:
            return HttpResponseForbidden("Principal should delete in admin panel, not hide.")

        for notification in notifications:
            HiddenNotification.objects.get_or_create(staff=request.user, notification=notification)

        messages.success(request, f"{len(selected_ids)} notification(s) hidden.")
    return redirect('staff_notifications')



# Optional: Principal only can delete in admin panel.
# @csrf_protect
# @login_required
# def delete_notification(request, notification_id):
#     if not request.user.is_superuser:
#         return HttpResponseForbidden("Only Principal can delete notifications.")
    
#     if request.method == 'POST':
#         notification = get_object_or_404(StaffNotification, id=notification_id)
#         notification.delete()
#         messages.success(request, "Notification deleted successfully.")
    
#     return redirect('staff_notifications')

############ student fees management function

# from django.shortcuts import render
# from .models import StudentFeesRecord

# def student_fees_management(request):
#     fees = StudentFeesRecord.objects.select_related('student').all()
#     return render(request, 'staffs/student_fees_management.html', {'fees': fees})



########## students fees management function 2nd type

from django.shortcuts import render, redirect, get_object_or_404
from .models import StudentFeesRecord
from .forms import StudentFeesRecordForm

def student_fees_management(request):
    fees = StudentFeesRecord.objects.select_related('student').all()
    return render(request, 'staffs/student_fees_management.html', {'fees': fees})

def add_student_fee(request):
    if request.method == 'POST':
        form = StudentFeesRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student-fees')
    else:
        form = StudentFeesRecordForm()
    return render(request, 'staffs/student_fees_form.html', {'form': form})

def edit_student_fee(request, fee_id):
    fee = get_object_or_404(StudentFeesRecord, id=fee_id)
    if request.method == 'POST':
        form = StudentFeesRecordForm(request.POST, instance=fee)
        if form.is_valid():
            form.save()
            return redirect('student-fees')
    else:
        form = StudentFeesRecordForm(instance=fee)
    return render(request, 'staffs/student_fees_form.html', {'form': form})

def delete_student_fee(request, fee_id):
    fee = get_object_or_404(StudentFeesRecord, id=fee_id)
    fee.delete()
    return redirect('student-fees')
