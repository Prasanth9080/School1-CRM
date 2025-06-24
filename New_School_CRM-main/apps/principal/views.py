from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.staffs.models import LeaveRequeststaff


def principal_dashboard(request):
    return render (request, "principal/principal_data.html")

# @login_required
# def principalstaffleavereport(request):
#     leaves = LeaveRequeststaff.objects.all()

#     if request.method == "POST":
#         leave_id = request.POST.get("leave_id")
#         action = request.POST.get("action")
#         leave = LeaveRequeststaff.objects.get(id=leave_id)
#         if action == "approve":
#             leave.status = "approved"
#         elif action == "reject":
#             leave.status = "rejected"
#         leave.save()
#         return redirect('principal-staff-leave-report')

#     return render(request, "principal/principal_staffleavereport.html", {"leaves": leaves})

#### new ....
# @login_required
# def principalstaffleavereport(request):
#     leaves = LeaveRequeststaff.objects.all().order_by('-leave_date')

#     if request.method == "POST":
#         leave_id = request.POST.get("leave_id")
#         action = request.POST.get("action")
#         leave = LeaveRequeststaff.objects.get(id=leave_id)
#         if action == "approve":
#             leave.status = "approved"
#         elif action == "reject":
#             leave.status = "rejected"
#         leave.save()
#         return redirect('principal-staff-leave-report')

#     return render(request, "principal/principal_staffleavereport.html", {"leaves": leaves})

###### new 3 ...

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from apps.staffs.models import LeaveRequeststaff

# @login_required
# def principalstaffleavereport(request):
#     leaves = LeaveRequeststaff.objects.all().order_by('-start_date')

#     if request.method == "POST":
#         leave_id = request.POST.get("leave_id")
#         action = request.POST.get("action")
#         try:
#             leave = LeaveRequeststaff.objects.get(id=leave_id)
#             if action == "approve":
#                 leave.status = "approved"
#             elif action == "reject":
#                 leave.status = "rejected"
#             leave.save()
#         except LeaveRequeststaff.DoesNotExist:
#             pass  # Handle if needed

#         return redirect('principal-staff-leave-report')

#     return render(request, "principal/principal_staffleavereport.html", {"leaves": leaves})

############### updated func for leave request avoid duplicate method 1


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.staffs.models import LeaveRequeststaff

@login_required
def principalstaffleavereport(request):
    leaves = LeaveRequeststaff.objects.all().order_by('-start_date')

    if request.method == "POST":
        leave_id = request.POST.get("leave_id")
        action = request.POST.get("action")
        try:
            leave = LeaveRequeststaff.objects.get(id=leave_id)
            if action == "approve":
                leave.status = "approved"
            elif action == "reject":
                leave.status = "rejected"
            leave.save()
        except LeaveRequeststaff.DoesNotExist:
            pass  # Optional: Add error logging

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

# @login_required
# def circulation_create(request):
#     if request.method == 'POST':
#         form = CirculationForm(request.POST)
#         if form.is_valid():
#             circulation = form.save(commit=False)
#             circulation.created_by = request.user
#             circulation.save()
#             return redirect('circulation_list')
#     else:
#         form = CirculationForm()
#     return render(request, 'principal/principal_circulation_form.html', {'form': form})

##### updated for create circulation sent staff and student

# from django.contrib.auth.models import User, Group
# from django.core.mail import send_mass_mail
# from django.contrib import messages

# @login_required
# def circulation_create(request):
#     if request.method == 'POST':
#         form = CirculationForm(request.POST)
#         if form.is_valid():
#             circulation = form.save(commit=False)
#             circulation.created_by = request.user
#             circulation.save()

#             # ✅ Send email if audience is 'all'
#             if circulation.audience == 'all':
#                 subject = f"New Circulation: {circulation.title}"
#                 message = circulation.content
#                 from_email = 'noreply@schoolcrm.com'

#                 # Get all staff and student users
#                 staff_users = User.objects.filter(groups__name='staff').exclude(email='').distinct()
#                 student_users = User.objects.filter(groups__name='student').exclude(email='').distinct()

#                 recipients = list(staff_users.values_list('email', flat=True)) + \
#                              list(student_users.values_list('email', flat=True))

#                 # Batch send using send_mass_mail
#                 messages_to_send = [(subject, message, from_email, [email]) for email in recipients]

#                 if messages_to_send:
#                     send_mass_mail(messages_to_send, fail_silently=False)

#             messages.success(request, "Circulation created and emails sent.")
#             return redirect('circulation_list')
#     else:
#         form = CirculationForm()
#     return render(request, 'principal/principal_circulation_form.html', {'form': form})

######### circulation send in 2nd type

# from django.contrib.auth.models import User
# from django.core.mail import send_mass_mail
# from django.contrib import messages
# from django.shortcuts import render, redirect
# from .models import Circulation
# from .forms import CirculationForm
# from django.contrib.auth.decorators import login_required

# @login_required
# def circulation_create(request):
#     if request.method == 'POST':
#         form = CirculationForm(request.POST)
#         if form.is_valid():
#             circulation = form.save(commit=False)
#             circulation.created_by = request.user
#             circulation.save()

#             # DEBUG: Check audience value
#             print("Audience selected:", circulation.audience)

#             if circulation.audience == 'all':
#                 subject = f"New Circulation: {circulation.title}"
#                 message = circulation.content
#                 from_email = 'noreply@schoolcrm.com'  # Replace as needed

#                 # Get users in 'staff' and 'student' groups
#                 staff_users = User.objects.filter(groups__name='staff').exclude(email='').distinct()
#                 student_users = User.objects.filter(groups__name='student').exclude(email='').distinct()

#                 recipients = list(staff_users.values_list('email', flat=True)) + \
#                              list(student_users.values_list('email', flat=True))

#                 # DEBUG: Show all recipient emails
#                 print("Recipients:", recipients)

#                 messages_to_send = [(subject, message, from_email, [email]) for email in recipients]

#                 try:
#                     if messages_to_send:
#                         send_mass_mail(messages_to_send, fail_silently=False)
#                         print("Emails sent successfully.")
#                     else:
#                         print("No recipients found to send email.")
#                 except Exception as e:
#                     print("Error sending email:", e)

#             messages.success(request, "Circulation created successfully.")
#             return redirect('circulation_list')
#     else:
#         form = CirculationForm()

#     return render(request, 'principal/principal_circulation_form.html', {'form': form})

##### 3rd

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.contrib.auth.models import User, Group
# from django.core.mail import send_mass_mail
# from .forms import CirculationForm
# from .models import Circulation

# @login_required
# def circulation_create(request):
#     if request.method == 'POST':
#         form = CirculationForm(request.POST)
#         if form.is_valid():
#             circulation = form.save(commit=False)
#             circulation.created_by = request.user
#             circulation.save()

#             # ✅ Check if audience is 'all' to send emails
#             if circulation.audience == 'all':
#                 subject = f"New Circulation: {circulation.title}"
#                 message = circulation.content
#                 from_email = 'noreply@schoolcrm.com'

#                 # 🔍 Get users in 'staff' and 'student' groups
#                 staff_group = Group.objects.filter(name='staff').first()
#                 student_group = Group.objects.filter(name='student').first()

#                 # If group is not found, use an empty queryset
#                 staff_users = staff_group.user_set.exclude(email='') if staff_group else User.objects.none()
#                 student_users = student_group.user_set.exclude(email='') if student_group else User.objects.none()

#                 recipients = list(staff_users.values_list('email', flat=True)) + \
#                              list(student_users.values_list('email', flat=True))

#                 print("Audience selected:", circulation.audience)
#                 print("Recipients found:", recipients)

#                 if recipients:
#                     # Prepare messages
#                     messages_to_send = [(subject, message, from_email, [email]) for email in recipients]
#                     try:
#                         send_mass_mail(messages_to_send, fail_silently=False)
#                         print("Emails sent successfully.")
#                     except Exception as e:
#                         print("Email sending failed:", str(e))
#                         messages.error(request, "Circulation created but failed to send email.")
#                 else:
#                     print("No valid recipients found.")
#                     messages.warning(request, "Circulation created, but no recipients found to send email.")
#             else:
#                 print("Audience is not 'all'; skipping email.")

#             messages.success(request, "Circulation created successfully.")
#             return redirect('circulation_list')
#     else:
#         form = CirculationForm()

#     return render(request, 'principal/principal_circulation_form.html', {'form': form})


### 4th

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User, Group
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib import messages

# from .models import Circulation
# from .forms import CirculationForm


# @login_required
# def circulation_create(request):
#     if request.method == 'POST':
#         form = CirculationForm(request.POST)
#         if form.is_valid():
#             circulation = form.save(commit=False)
#             circulation.created_by = request.user
#             circulation.save()

#             # ✅ Prepare email subject/message
#             subject = f"New Circulation: {circulation.title}"
#             message = (
#                 f"Dear User,\n\n"
#                 f"A new circulation has been posted:\n\n"
#                 f"Title: {circulation.title}\n"
#                 f"Content: {circulation.content}\n\n"
#                 f"Please check your circulation dashboard for more details.\n\n"
#                 f"Regards,\nSchool CRM"
#             )

#             # ✅ Decide recipients based on audience
#             recipient_list = []
#             try:
#                 if circulation.audience == 'all':
#                     staff_emails = Group.objects.get(name='staff').user_set.values_list('email', flat=True)
#                     student_emails = Group.objects.get(name='student').user_set.values_list('email', flat=True)
#                     recipient_list = list(set(staff_emails) | set(student_emails))

#                 elif circulation.audience == 'staff':
#                     staff_emails = Group.objects.get(name='staff').user_set.values_list('email', flat=True)
#                     recipient_list = list(staff_emails)

#                 elif circulation.audience == 'students':
#                     student_emails = Group.objects.get(name='student').user_set.values_list('email', flat=True)
#                     recipient_list = list(student_emails)

#                 # Filter out empty emails
#                 recipient_list = [email for email in recipient_list if email]

#                 if recipient_list:
#                     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False)
#                     messages.success(request, "Circulation created and email notifications sent.")
#                 else:
#                     messages.warning(request, "Circulation created, but no recipients found for selected audience.")

#             except Exception as e:
#                 print("Email send error:", str(e))  # Or use logging
#                 messages.warning(request, "Circulation created, but email notification failed.")

#             return redirect('circulation_list')

#     else:
#         form = CirculationForm()

#     return render(request, 'principal/principal_circulation_form.html', {'form': form})


##### 5th... principal created an circulation after send in own pricnipal email id:::::

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib import messages

# from .models import Circulation
# from .forms import CirculationForm

# @login_required
# def circulation_create(request):
#     if request.method == 'POST':
#         form = CirculationForm(request.POST)
#         if form.is_valid():
#             # Save the new circulation
#             circulation = form.save(commit=False)
#             circulation.created_by = request.user
#             circulation.save()

#             # ── EMAIL NOTIFICATION TO PRINCIPAL ──
#             principal_email = request.user.email
#             if principal_email:
#                 subject = f"[Your School CRM] Circulation Created: {circulation.title}"
#                 message = (
#                     f"Hello {request.user.get_full_name() or request.user.username},\n\n"
#                     f"You have successfully created a new circulation:\n\n"
#                     f"Title: {circulation.title}\n"
#                     f"Audience: {circulation.get_audience_display()}\n"
#                     f"Created At: {circulation.created_at:%Y-%m-%d %H:%M}\n\n"
#                     f"Content:\n{circulation.content}\n\n"
#                     f"You are receiving this email because you created the circulation in the School CRM.\n\n"
#                     f"Regards,\n"
#                     f"School CRM Notification System"
#                 )
#                 try:
#                     send_mail(
#                         subject,
#                         message,
#                         settings.DEFAULT_FROM_EMAIL,
#                         [principal_email],
#                         fail_silently=False
#                     )
#                     messages.success(request, "Circulation created and emailed to you successfully.")
#                 except Exception as e:
#                     # If emailing fails, still keep the circulation, but warn the user
#                     print("Email to principal failed:", e)
#                     messages.warning(request, "Circulation created, but we couldn’t send the email notification to your address.")
#             else:
#                 # No email address on file for the principal
#                 messages.warning(request, "Circulation created, but you have no email on file to receive a notification.")

#             return redirect('circulation_list')
#     else:
#         form = CirculationForm()

#     return render(request, 'principal/principal_circulation_form.html', {'form': form})


######## upadted for circulation email send for all role users:

# from django.contrib.auth.models import User, Group
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib import messages
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import Circulation
# from .forms import CirculationForm

# @login_required
# def circulation_create(request):
#     if request.method == 'POST':
#         form = CirculationForm(request.POST)
#         if form.is_valid():
#             circulation = form.save(commit=False)
#             circulation.created_by = request.user
#             circulation.save()

#             subject = f"[Your School CRM] Circulation Created: {circulation.title}"
#             message = (
#                 f"Hello {request.user.get_full_name() or request.user.username},\n\n"
#                 f"You have successfully created a new circulation:\n\n"
#                 f"Title: {circulation.title}\n"
#                 f"Audience: {circulation.get_audience_display()}\n"
#                 f"Created At: {circulation.created_at:%Y-%m-%d %H:%M}\n\n"
#                 f"Content:\n{circulation.content}\n\n"
#                 f"You are receiving this email because you created the circulation in the School CRM.\n\n"
#                 f"Regards,\n"
#                 f"School CRM Notification System"
#             )

#             recipient_list = []

#             if circulation.audience in ['all', 'staff']:
#                 staff_group, _ = Group.objects.get_or_create(name='staff')
#                 staff_users = User.objects.filter(groups=staff_group, email__isnull=False).exclude(email='')
#                 recipient_list += [user.email for user in staff_users]

#             if circulation.audience in ['all', 'students']:
#                 student_group, _ = Group.objects.get_or_create(name='student')
#                 student_users = User.objects.filter(groups=student_group, email__isnull=False).exclude(email='')
#                 recipient_list += [user.email for user in student_users]

#             # Add principal (creator) email
#             if request.user.email:
#                 recipient_list.append(request.user.email)

#             # Remove duplicates
#             recipient_list = list(set(recipient_list))

#             try:
#                 send_mail(
#                     subject,
#                     message,
#                     settings.DEFAULT_FROM_EMAIL,
#                     recipient_list,
#                     fail_silently=False,
#                 )
#                 messages.success(request, "Circulation created and sent via email.")
#             except Exception as e:
#                 print("Email sending failed:", e)
#                 messages.warning(request, "Circulation created, but failed to send emails.")

#             return redirect('circulation_list')
#     else:
#         form = CirculationForm()

#     return render(request, 'principal/principal_circulation_form.html', {'form': form})


######### updated for cicrulation email send for all user 2nd method:


from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Circulation
from .forms import CirculationForm

User = get_user_model()

@login_required
def circulation_create(request):
    if request.method == 'POST':
        form = CirculationForm(request.POST)
        if form.is_valid():
            circulation = form.save(commit=False)
            circulation.created_by = request.user
            circulation.save()

            subject = f"[Your School CRM] Circulation Created: {circulation.title}"
            message = (
                f"Hello {request.user.get_full_name() or request.user.username},\n\n"
                f"You have successfully created a new circulation:\n\n"
                f"Title: {circulation.title}\n"
                f"Audience: {circulation.get_audience_display()}\n"
                f"Created At: {circulation.created_at:%Y-%m-%d %H:%M}\n\n"
                f"Content:\n{circulation.content}\n\n"
                f"You are receiving this email because you created the circulation in the School CRM.\n\n"
                f"Regards,\n"
                f"School CRM Notification System"
            )

            recipient_list = []

            # Add teachers (staff) if needed
            if circulation.audience in ['all', 'staff']:
                teacher_users = User.objects.filter(
                    userprofile__role='teacher',
                    email__isnull=False
                ).exclude(email='')
                recipient_list += [u.email for u in teacher_users]

            # Add students if needed
            if circulation.audience in ['all', 'students']:
                student_users = User.objects.filter(
                    userprofile__role='student',
                    email__isnull=False
                ).exclude(email='')
                recipient_list += [u.email for u in student_users]

            # Add principal (creator)
            if request.user.email:
                recipient_list.append(request.user.email)

            # Remove duplicates
            recipient_list = list(set(recipient_list))

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    recipient_list,
                    fail_silently=False,
                )
                messages.success(request, "Circulation created and emails sent successfully.")
            except Exception as e:
                print("Email sending failed:", e)
                messages.warning(request, "Circulation created, but email sending failed.")

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


##### for class schedule view for principal


from django.shortcuts import render, redirect, get_object_or_404
from .models import StaffClassSchedule
from .forms import StaffClassScheduleForm

def class_schedule_list(request):
    schedules = StaffClassSchedule.objects.all()
    return render(request, 'principal/class_schedule_list.html', {'schedules': schedules})

# def class_schedule_create(request):
#     if request.method == 'POST':
#         form = StaffClassScheduleForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('principal-class-schedule-list')
#     else:
#         form = StaffClassScheduleForm()
#     return render(request, 'principal/class_schedule_create.html', {'form': form})


###### new for class schedule create fucntions

from django.utils.timezone import now
from django.contrib.auth.models import User
from ..staffs.models import LeaveRequeststaff
from .forms import StaffClassScheduleForm
from .models import StaffClassSchedule
from django.shortcuts import render, redirect

def class_schedule_create(request):
    today = now().date()

    # Get all staff IDs who are on leave for *today*
    leave_staff_ids = LeaveRequeststaff.objects.filter(
        status='approved',
        start_date__lte=today,
        end_date__gte=today
    ).values_list('staff_id', flat=True)

    # All staff with role 'teacher' not on leave
    available_staff = User.objects.filter(userprofile__role='teacher').exclude(id__in=leave_staff_ids)

    if request.method == 'POST':
        form = StaffClassScheduleForm(request.POST, available_staff=available_staff)
        if form.is_valid():
            form.save()
            return redirect('principal-class-schedule-list')
    else:
        form = StaffClassScheduleForm(available_staff=available_staff)

    return render(request, 'principal/class_schedule_create.html', {'form': form})



def class_schedule_edit(request, pk):
    schedule = get_object_or_404(StaffClassSchedule, pk=pk)
    if request.method == 'POST':
        form = StaffClassScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('principal-class-schedule-list')
    else:
        form = StaffClassScheduleForm(instance=schedule)
    return render(request, 'principal/class_schedule_create.html', {'form': form, 'edit': True})

def class_schedule_delete(request, pk):
    schedule = get_object_or_404(StaffClassSchedule, pk=pk)
    schedule.delete()
    return redirect('principal-class-schedule-list')



########### class schedule only view for staff

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.models import User
# from .models import StaffClassSchedule
# from .forms import StaffClassScheduleForm

# @login_required
# def class_schedule_list(request):
#     # If principal (superuser or custom role), show all
#     if request.user.is_superuser or hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'principal':
#         schedules = StaffClassSchedule.objects.all()
#     else:
#         # Show only schedules for the logged-in staff member
#         schedules = StaffClassSchedule.objects.filter(staff_name=request.user)
#     return render(request, 'principal/class_schedule_list.html', {'schedules': schedules})


@login_required
def staff_class_schedule_view(request):
    schedules = StaffClassSchedule.objects.filter(staff_name=request.user)
    return render(request, 'staffs/staff_schedule_view.html', {'schedules': schedules})