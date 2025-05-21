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
from ..students.models import StuReportCard , Student
from ..students.forms import StuReportCardForm
from django.contrib.auth.decorators import login_required

@login_required
def reportcard_list(request):
    cards = StuReportCard.objects.all()
    return render(request, 'staffs/reportcard_list.html', {'cards': cards})

# @login_required
# def reportcard_create(request):
#     if request.method == 'POST':
#         form = StuReportCardForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('staff-reportcard-list')
#     else:
#         form = StuReportCardForm()

#     return render(request, 'staffs/reportcard_form.html', {'form': form})




######### new function for student report card

# @login_required
# def reportcard_create(request):
#     student_id = request.GET.get('student_id')
#     term = request.GET.get('term')

#     initial_data = {}

#     # Check if we are creating a new report card for an existing student
#     if student_id and term:
#         # Get latest report card of student (excluding same term)
#         previous_cards = StuReportCard.objects.filter(student_id=student_id).exclude(term=term).order_by('-id')
#         if previous_cards.exists():
#             previous = previous_cards.first()
#             # Pre-fill data except marks, totals, status, parent signature
#             initial_data = {
#                 'student': previous.student,
#                 'standard': previous.standard,
#                 'section': previous.section,
#                 'academic_session': previous.academic_session,
#                 'father_name': previous.father_name,
#                 'mother_name': previous.mother_name,
#                 'address': previous.address,
#                 'admission_number': previous.admission_number,
#                 'roll_number': previous.roll_number,
#                 'date_of_birth': previous.date_of_birth,

                
#                 'all_subject_mark': previous.all_subject_mark,
#                 'total_marks': previous.total_marks,

#                 'signature_class_teacher': previous.signature_class_teacher,
#                 'signature_principal': previous.signature_principal,
#                 # leave marks blank
#             }

#     if request.method == 'POST':
#         form = StuReportCardForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('staff-reportcard-list')
#     else:
#         form = StuReportCardForm(initial=initial_data)

#     return render(request, 'staffs/reportcard_form.html', {'form': form})





##### 2nd type for student report card

# @login_required
# def reportcard_create(request):
#     student_id = request.GET.get('student_id')
#     term = request.GET.get('term')

#     initial_data = {}

#     if student_id:
#         # Fetch previous report card for this student
#         previous_cards = StuReportCard.objects.filter(student_id=student_id).order_by('-id')

#         if previous_cards.exists():
#             previous = previous_cards.first()
#             initial_data = {
#                 'student': previous.student,
#                 'standard': previous.standard,
#                 'section': previous.section,
#                 'academic_session': previous.academic_session,
#                 'father_name': previous.father_name,
#                 'mother_name': previous.mother_name,
#                 'address': previous.address,
#                 'admission_number': previous.admission_number,
#                 'roll_number': previous.roll_number,
#                 'date_of_birth': previous.date_of_birth,
#                 'all_subject_mark': previous.all_subject_mark,
#                 'total_marks': previous.total_marks,
#                 'signature_class_teacher': previous.signature_class_teacher,
#                 'signature_principal': previous.signature_principal,
#                 # Term will be selected separately
#                 'term': term if term else None
#             }

#     if request.method == 'POST':
#         form = StuReportCardForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('staff-reportcard-list')
#     else:
#         form = StuReportCardForm(initial=initial_data)

#     return render(request, 'staffs/reportcard_form.html', {'form': form})


##### 3rd type for student report card

# from django.contrib import messages

# @login_required
# def reportcard_create(request):
#     student_id = request.GET.get('student_id')
#     term = request.GET.get('term')

#     initial_data = {}
#     if student_id:
#         previous_cards = StuReportCard.objects.filter(student_id=student_id).order_by('-id')
#         if previous_cards.exists():
#             previous = previous_cards.first()
#             initial_data = {
#                 'student': previous.student,
#                 'standard': previous.standard,
#                 'section': previous.section,
#                 'academic_session': previous.academic_session,
#                 'father_name': previous.father_name,
#                 'mother_name': previous.mother_name,
#                 'address': previous.address,
#                 'admission_number': previous.admission_number,
#                 'roll_number': previous.roll_number,
#                 'date_of_birth': previous.date_of_birth,
#                 'all_subject_mark': previous.all_subject_mark,
#                 'signature_class_teacher': previous.signature_class_teacher,
#                 'signature_principal': previous.signature_principal,
#                 'term': term if term else None
#             }

#     if request.method == 'POST':
#         form = StuReportCardForm(request.POST)
#         if form.is_valid():
#             student = form.cleaned_data.get('student')
#             term = form.cleaned_data.get('term')

#             # Check for duplicate
#             if StuReportCard.objects.filter(student=student, term=term).exists():
#                 messages.error(request, f"Report card for {student.get_full_name()} in {term} already exists.")
#             else:
#                 form.save()
#                 messages.success(request, "Report card created successfully.")
#                 return redirect('staff-reportcard-list')
#     else:
#         form = StuReportCardForm(initial=initial_data)

#     return render(request, 'staffs/reportcard_form.html', {'form': form})



######### 4th type for student report card

# @login_required
# def reportcard_create(request):
#     student_id = request.GET.get('student_id')
#     term = request.GET.get('term')

#     initial_data = {}

#     if student_id:
#         previous_cards = StuReportCard.objects.filter(student_id=student_id).exclude(term=term).order_by('-id')
#         if previous_cards.exists():
#             previous = previous_cards.first()
#             initial_data = {
#                 'student': previous.student,
#                 'standard': previous.standard,
#                 'section': previous.section,
#                 'academic_session': previous.academic_session,
#                 'father_name': previous.father_name,
#                 'mother_name': previous.mother_name,
#                 'address': previous.address,
#                 'admission_number': previous.admission_number,
#                 'roll_number': previous.roll_number,
#                 'date_of_birth': previous.date_of_birth,
#                 'all_subject_mark': previous.all_subject_mark,
#                 'signature_class_teacher': previous.signature_class_teacher,
#                 'signature_principal': previous.signature_principal,
#                 'term': term if term else None
#             }
#         else:
#             # Student has no report card yet, just prefill student and term
#             initial_data = {
#                 'student': student_id,
#                 'term': term if term else None
#             }

#     if request.method == 'POST':
#         form = StuReportCardForm(request.POST)
#         if form.is_valid():
#             student = form.cleaned_data['student']
#             term = form.cleaned_data['term']
#             # Check if already exists
#             if StuReportCard.objects.filter(student=student, term=term).exists():
#                 messages.error(request, f"Report card for {student.get_full_name()} in {term} already exists.")
#             else:
#                 form.save()
#                 messages.success(request, "Report card created successfully.")
#                 return redirect('staff-reportcard-list')
#     else:
#         form = StuReportCardForm(initial=initial_data)

#     return render(request, 'staffs/reportcard_form.html', {'form': form})




###### 5th type for student report card

# @login_required
# def reportcard_create(request):
#     student_id = request.GET.get('student_id')
#     term = request.GET.get('term')

#     initial_data = {}
#     existing_card = None

#     if student_id and term:
#         # Check if this exact student-term already has a report card
#         existing_card = StuReportCard.objects.filter(student_id=student_id, term=term).first()

#         if existing_card:
#             # Already created — display existing data
#             initial_data = {
#                 'student': existing_card.student,
#                 'term': existing_card.term,
#                 'standard': existing_card.standard,
#                 'section': existing_card.section,
#                 'academic_session': existing_card.academic_session,
#                 'father_name': existing_card.father_name,
#                 'mother_name': existing_card.mother_name,
#                 'address': existing_card.address,
#                 'admission_number': existing_card.admission_number,
#                 'roll_number': existing_card.roll_number,
#                 'date_of_birth': existing_card.date_of_birth,
#                 'tamil': existing_card.tamil,
#                 'english': existing_card.english,
#                 'maths': existing_card.maths,
#                 'science': existing_card.science,
#                 'social': existing_card.social,
#                 'overall_total': existing_card.overall_total,
#                 'total_marks': existing_card.total_marks,
#                 'status': existing_card.status,
#                 'parent_signature': existing_card.parent_signature,
#                 'signature_class_teacher': existing_card.signature_class_teacher,
#                 'signature_principal': existing_card.signature_principal,
#             }

#         else:
#             # Get from previous term for same student
#             previous_cards = StuReportCard.objects.filter(student_id=student_id).exclude(term=term).order_by('-id')
#             if previous_cards.exists():
#                 prev = previous_cards.first()
#                 initial_data = {
#                     'student': prev.student,
#                     'term': term,
#                     'standard': prev.standard,
#                     'section': prev.section,
#                     'academic_session': prev.academic_session,
#                     'father_name': prev.father_name,
#                     'mother_name': prev.mother_name,
#                     'address': prev.address,
#                     'admission_number': prev.admission_number,
#                     'roll_number': prev.roll_number,
#                     'date_of_birth': prev.date_of_birth,
#                     'signature_class_teacher': prev.signature_class_teacher,
#                     'signature_principal': prev.signature_principal,
#                 }

#     if request.method == 'POST':
#         form = StuReportCardForm(request.POST)
#         if form.is_valid():
#             # Prevent duplicate creation
#             existing = StuReportCard.objects.filter(student=form.cleaned_data['student'], term=form.cleaned_data['term'])
#             if existing.exists():
#                 messages.error(request, 'Report card already exists for this student and term.')
#             else:
#                 form.save()
#                 messages.success(request, 'Report card created successfully.')
#                 return redirect('staff-reportcard-list')
#     else:
#         form = StuReportCardForm(initial=initial_data)

#     return render(request, 'staffs/reportcard_form.html', {'form': form, 'existing_card': existing_card})


###### 6th type for student report card

# @login_required
# def reportcard_create(request):
#     student_id = request.GET.get('student_id')
#     term = request.GET.get('term')

#     initial_data = {}
#     existing_card = None
#     readonly = False  # <- flag

#     if student_id and term:
#         existing_card = StuReportCard.objects.filter(student_id=student_id, term=term).first()

#         if existing_card:
#             readonly = True  # Make form non-editable
#             initial_data = {
#                 'student': existing_card.student,
#                 'term': existing_card.term,
#                 'standard': existing_card.standard,
#                 'section': existing_card.section,
#                 'academic_session': existing_card.academic_session,
#                 'father_name': existing_card.father_name,
#                 'mother_name': existing_card.mother_name,
#                 'address': existing_card.address,
#                 'admission_number': existing_card.admission_number,
#                 'roll_number': existing_card.roll_number,
#                 'date_of_birth': existing_card.date_of_birth,
#                 'tamil': existing_card.tamil,
#                 'english': existing_card.english,
#                 'maths': existing_card.maths,
#                 'science': existing_card.science,
#                 'social': existing_card.social,
#                 'overall_total': existing_card.overall_total,
#                 'total_marks': existing_card.total_marks,
#                 'status': existing_card.status,
#                 'parent_signature': existing_card.parent_signature,
#                 'signature_class_teacher': existing_card.signature_class_teacher,
#                 'signature_principal': existing_card.signature_principal,
#             }

#     form = StuReportCardForm(initial=initial_data)

#     if readonly:
#         for field in form.fields.values():
#             field.widget.attrs['readonly'] = True
#             field.widget.attrs['disabled'] = True  # prevents POSTing values too

#     if request.method == 'POST' and not readonly:
#         form = StuReportCardForm(request.POST)
#         if form.is_valid():
#             existing = StuReportCard.objects.filter(student=form.cleaned_data['student'], term=form.cleaned_data['term'])
#             if existing.exists():
#                 messages.error(request, 'Report card already exists for this student and term.')
#             else:
#                 form.save()
#                 messages.success(request, 'Report card created successfully.')
#                 return redirect('staff-reportcard-list')

#     return render(request, 'staffs/reportcard_form.html', {
#         'form': form,
#         'readonly': readonly,
#         'existing_card': existing_card,
#     })

##### 7th type for student report card

# @login_required
# def reportcard_create(request):
#     student_id = request.GET.get('student_id')
#     term = request.GET.get('term')

#     existing_card = None
#     initial_data = {}
#     disable_fields = []  # list of fields to disable

#     if student_id and term:
#         existing_card = StuReportCard.objects.filter(student_id=student_id, term=term).first()

#         if existing_card:
#             # Report card already exists — show all in read-only
#             initial_data = {field.name: getattr(existing_card, field.name) for field in StuReportCard._meta.fields}
#             disable_fields = [field.name for field in StuReportCard._meta.fields if field.name != 'student']
#         else:
#             # New term for same student → fetch previous data to prefill
#             previous_cards = StuReportCard.objects.filter(student_id=student_id).exclude(term=term).order_by('-id')
#             if previous_cards.exists():
#                 prev = previous_cards.first()
#                 initial_data = {
#                     'student': prev.student,
#                     'standard': prev.standard,
#                     'section': prev.section,
#                     'academic_session': prev.academic_session,
#                     'father_name': prev.father_name,
#                     'mother_name': prev.mother_name,
#                     'address': prev.address,
#                     'admission_number': prev.admission_number,
#                     'roll_number': prev.roll_number,
#                     'date_of_birth': prev.date_of_birth,
#                     'signature_class_teacher': prev.signature_class_teacher,
#                     'signature_principal': prev.signature_principal,
#                 }

#                 # Disable prefilled fields except marks and student
#                 disable_fields = list(initial_data.keys())

#     if request.method == 'POST':
#         form = StuReportCardForm(request.POST)
#         if form.is_valid():
#             student = form.cleaned_data['student']
#             term = form.cleaned_data['term']
#             # Prevent duplicates
#             if StuReportCard.objects.filter(student=student, term=term).exists():
#                 messages.error(request, 'This student already has a report card for the selected term.')
#             else:
#                 form.save()
#                 messages.success(request, 'Report card created successfully.')
#                 return redirect('staff-reportcard-list')
#     else:
#         form = StuReportCardForm(initial=initial_data)

#         # Disable specified fields
#         for field_name in disable_fields:
#             if field_name in form.fields:
#                 form.fields[field_name].widget.attrs['readonly'] = True
#                 form.fields[field_name].widget.attrs['disabled'] = True

#     return render(request, 'staffs/reportcard_form.html', {
#         'form': form,
#         'student_selected': student_id is not None,
#     })


###### 8th type for student report card'

# @login_required
# def reportcard_create(request):
#     from django.contrib import messages

#     student_id = request.GET.get('student_id')
#     term = request.GET.get('term')

#     initial_data = {}
#     existing_card = None
#     readonly = False

#     if student_id and term:
#         existing_card = StuReportCard.objects.filter(student_id=student_id, term=term).first()

#         if existing_card:
#             readonly = True
#             initial_data = {
#                 'student': existing_card.student,
#                 'term': existing_card.term,
#                 'standard': existing_card.standard,
#                 'section': existing_card.section,
#                 'academic_session': existing_card.academic_session,
#                 'father_name': existing_card.father_name,
#                 'mother_name': existing_card.mother_name,
#                 'address': existing_card.address,
#                 'admission_number': existing_card.admission_number,
#                 'roll_number': existing_card.roll_number,
#                 'date_of_birth': existing_card.date_of_birth,
#                 'tamil': existing_card.tamil,
#                 'english': existing_card.english,
#                 'maths': existing_card.maths,
#                 'science': existing_card.science,
#                 'social': existing_card.social,
#                 'overall_total': existing_card.overall_total,
#                 'total_marks': existing_card.total_marks,
#                 'status': existing_card.status,
#                 'parent_signature': existing_card.parent_signature,
#                 'signature_class_teacher': existing_card.signature_class_teacher,
#                 'signature_principal': existing_card.signature_principal,

#                 'comments': existing_card.comments,
#                 'overall_grade': existing_card.overall_grade,
#                 'date': existing_card.date,
#                 'total_marks': existing_card.total_marks,
#                 'all_subject_mark': existing_card.all_subject_mark,
#                 'overall_percentage': existing_card.overall_percentage,
#             }

#         else:
#         # If no card for this term, try fetching latest other term card for prefill
#             previous_card = StuReportCard.objects.filter(student_id=student_id).exclude(term=term).order_by('-id').first()
#             if previous_card:
#                 initial_data = {
#                     'student': previous_card.student,
#                     'standard': previous_card.standard,
#                     'section': previous_card.section,
#                     'academic_session': previous_card.academic_session,
#                     'father_name': previous_card.father_name,
#                     'mother_name': previous_card.mother_name,
#                     'address': previous_card.address,
#                     'admission_number': previous_card.admission_number,
#                     'roll_number': previous_card.roll_number,
#                     'date_of_birth': previous_card.date_of_birth,
#                     'signature_class_teacher': previous_card.signature_class_teacher,
#                     'signature_principal': previous_card.signature_principal,
#                 }

#     form = StuReportCardForm(initial=initial_data)

#     if readonly:
#         for name, field in form.fields.items():
#             if name not in ['student', 'term']:
#                 field.widget.attrs['readonly'] = True
#                 field.widget.attrs['disabled'] = True  # prevents POST value

#     if request.method == 'POST' and not readonly:
#         form = StuReportCardForm(request.POST)
#         if form.is_valid():
#             exists = StuReportCard.objects.filter(
#                 student=form.cleaned_data['student'],
#                 term=form.cleaned_data['term']
#             ).exists()
#             if exists:
#                 messages.error(request, "A report card already exists for this student and term.")
#             else:
#                 form.save()
#                 messages.success(request, "Report card created successfully.")
#                 return redirect('staff-reportcard-list')

#     return render(request, 'staffs/reportcard_form.html', {
#         'form': form,
#         'readonly': readonly,
#         'existing_card': existing_card,
#     })



####### 9th type for student report card

# @login_required
# def reportcard_create(request):
#     from django.contrib import messages

#     student_id = request.GET.get('student_id')
#     term = request.GET.get('term')

#     initial_data = {}
#     existing_card = None
#     readonly = False

#     if student_id and term:
#         # Try to get existing report card for this student and term
#         existing_card = StuReportCard.objects.filter(student_id=student_id, term=term).first()

#         if existing_card:
#             readonly = True
#             initial_data = {
#                 field.name: getattr(existing_card, field.name)
#                 for field in StuReportCard._meta.fields
#             }
#         else:
#             # Try to prefill from latest other term if available
#             previous_card = StuReportCard.objects.filter(student_id=student_id).exclude(term=term).order_by('-id').first()
#             if previous_card:
#                 fields_to_copy = [
#                     'student', 'standard', 'section', 'academic_session',
#                     'father_name', 'mother_name', 'address',
#                     'admission_number', 'roll_number', 'date_of_birth',
#                     'signature_class_teacher', 'signature_principal',
#                 ]
#                 for field in fields_to_copy:
#                     initial_data[field] = getattr(previous_card, field)

#     # If POST, process the form
#     if request.method == 'POST':
#         form = StuReportCardForm(request.POST)
#         if form.is_valid():
#             student = form.cleaned_data['student']
#             term = form.cleaned_data['term']
#             # Prevent duplicate
#             if StuReportCard.objects.filter(student=student, term=term).exists():
#                 messages.error(request, "Report card already exists for this student and term.")
#             else:
#                 form.save()
#                 messages.success(request, "Report card created successfully.")
#                 return redirect('staff-reportcard-list')
#     else:
#         form = StuReportCardForm(initial=initial_data)

#         if readonly:
#             for name, field in form.fields.items():
#                 if name not in ['student', 'term']:
#                     field.widget.attrs['readonly'] = True
#                     field.widget.attrs['disabled'] = True

#     return render(request, 'staffs/reportcard_form.html', {
#         'form': form,
#         'readonly': readonly,
#         'existing_card': existing_card,
#     })



######### 10th type for student report card

# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from ..students.models import StuReportCard
# from ..students.forms import StuReportCardForm

# @login_required
# def reportcard_create(request):
#     student_id = request.GET.get('student_id')
#     term = request.GET.get('term')

#     existing_card = None
#     readonly = False
#     initial_data = {}

#     if student_id and term:
#         # Check if report card exists for this student and term
#         existing_card = StuReportCard.objects.filter(student_id=student_id, term=term).first()

#         if existing_card:
#             # Display existing report in readonly mode
#             readonly = True
#             for field in StuReportCard._meta.fields:
#                 initial_data[field.name] = getattr(existing_card, field.name)
#         else:
#             # Try to prefill from previous report (different term)
#             previous_card = StuReportCard.objects.filter(student_id=student_id).exclude(term=term).order_by('-id').first()
#             if previous_card:
#                 fields_to_copy = [
#                     'student', 'standard', 'section', 'academic_session',
#                     'father_name', 'mother_name', 'address',
#                     'admission_number', 'roll_number', 'date_of_birth',
#                     'signature_class_teacher', 'signature_principal'
#                 ]
#                 for field in fields_to_copy:
#                     initial_data[field] = getattr(previous_card, field)

#     # Handle form submission
#     if request.method == 'POST' and not readonly:
#         form = StuReportCardForm(request.POST)
#         if form.is_valid():
#             student = form.cleaned_data['student']
#             term = form.cleaned_data['term']
#             if StuReportCard.objects.filter(student=student, term=term).exists():
#                 messages.error(request, "A report card already exists for this student and term.")
#             else: 
#                 form.save()
#                 messages.success(request, "Report card created successfully.")
#                 return redirect('staff-reportcard-list')
#     else:
#         form = StuReportCardForm(initial=initial_data)
#         if readonly:
#             for name, field in form.fields.items():
#                 if name not in ['student', 'term']:
#                     field.widget.attrs['readonly'] = True
#                     field.widget.attrs['disabled'] = True

#     return render(request, 'staffs/reportcard_form.html', {
#         'form': form,
#         'readonly': readonly,
#         'existing_card': existing_card,
#     })

##################################### this is new for staff already created student report not craeted function

######### newly 1st type for student report card

@login_required
def reportcard_create(request):
    from django.contrib import messages

    student_id = request.GET.get('student_id')
    term = request.GET.get('term')

    initial_data = {}
    readonly = False
    existing_card = None

    if student_id and term:
        existing_card = StuReportCard.objects.filter(student_id=student_id, term=term).first()

        if existing_card:
            readonly = True
            initial_data = {
                field.name: getattr(existing_card, field.name)
                for field in StuReportCard._meta.fields
            }
        else:
            # Prefill from latest previous card (for the same student, different term)
            previous_card = StuReportCard.objects.filter(student_id=student_id).exclude(term=term).order_by('-id').first()
            if previous_card:
                prefill_fields = [
                    'student', 'standard', 'section', 'academic_session',
                    'father_name', 'mother_name', 'address',
                    'admission_number', 'roll_number', 'date_of_birth',
                    'signature_class_teacher', 'signature_principal',
                ]
                initial_data = {
                    field: getattr(previous_card, field) for field in prefill_fields
                }
            # Also include term and student in initial data to retain selection
            initial_data['term'] = term
            initial_data['student'] = student_id

    form = StuReportCardForm(initial=initial_data)

    if readonly:
        for name, field in form.fields.items():
            if name not in ['student', 'term']:
                field.widget.attrs['readonly'] = True
                field.widget.attrs['disabled'] = True

    if request.method == 'POST' and not readonly:
        form = StuReportCardForm(request.POST)
        if form.is_valid():
            exists = StuReportCard.objects.filter(
                student=form.cleaned_data['student'],
                term=form.cleaned_data['term']
            ).exists()
            if exists:
                messages.error(request, "A report card already exists for this student and term.")
            else:
                form.save()
                messages.success(request, "Report card created successfully.")
                return redirect('staff-reportcard-list')

    return render(request, 'staffs/reportcard_form.html', {
        'form': form,
        'readonly': readonly,
        'existing_card': existing_card,
    })



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
