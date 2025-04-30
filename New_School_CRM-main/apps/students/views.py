import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from apps.finance.models import Invoice

from .models import Student, StudentBulkUpload


# class StudentListView(LoginRequiredMixin, ListView):
#     model = Student
#     template_name = "students/student_list.html"

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = 'students'

    def get_queryset(self):
        queryset = super().get_queryset()
        # print("Students in queryset:", queryset)  # Debugging line
        return queryset


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_detail.html"

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        context["payments"] = Invoice.objects.filter(student=self.object)
        return context


class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student
    fields = "__all__"
    success_message = "New student successfully added."

    def get_form(self): 
        """add date picker in forms"""
        form = super(StudentCreateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
        return form


class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    fields = "__all__"
    success_message = "Record successfully updated."

    def get_form(self):
        """add date picker in forms"""
        form = super(StudentUpdateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
        # form.fields['passport'].widget = widgets.FileInput()
        return form


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy("student-list")


class StudentBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentBulkUpload
    template_name = "students/students_upload.html"
    fields = ["csv_file"]
    success_url = "/student/list"
    success_message = "Successfully uploaded students"


class DownloadCSVViewdownloadcsv(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="student_template.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "registration_number",
                "surname",
                "firstname1",
                "other_names1",
                "gender1",
                "parent_number1",
                "address1",
                "current_class",
            ]
        )

        return response


#######/////////// checking for redirecting stude_index.html page

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from .decorators import role_required


# @login_required
# @role_required('student')
# def student_dashboard(request):
#     return render(request, 'templates/students/student_dashboard.html')

############### working good, ela pageku correct ah naviagate agum


from django.shortcuts import  render

def studentreport(request):
    # return render(request, 'corecode/student_dashboard.html')s
    return render(request, 'students/student_report.html')


# def studentattendance(request):
#     # return render(request, 'corecode/student_dashboard.html')s
#     return render(request, 'students/student_attendance.html')


######### old student_attendance function

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from .models import LeaveRequeststudent

# @login_required
# def studentattendance(request):
#     student = request.user
#     leaves = LeaveRequeststudent.objects.filter(student=student)
#     return render(request, 'students/student_attendance.html', {'leaves': leaves})

from .models import LeaveRequeststudent
from .forms import LeaveRequeststudentForm

@login_required
def studentattendance(request):
    student = request.user
    leaves = LeaveRequeststudent.objects.filter(student=student)

    if request.method == "POST":
        form = LeaveRequeststudentForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.student = student
            leave.save()
            return redirect('student-attendance')
    else:
        form = LeaveRequeststudentForm()

    return render(request, 'students/student_attendance.html', {
        'leaves': leaves,
        'form': form
    })



# def studentdashboard(request):
#     return render (request, 'students/student_dashboard.html')


def studentdata(request):
    # return render (request, 'students/student_data.html')
    return render (request, 'students/student_leave_request.html')


# students/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LeaveRequeststudentForm
from .models import LeaveRequeststudent


@login_required
def student_leave_request(request):
    if request.method == 'POST':
        form = LeaveRequeststudentForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.student = request.user
            leave.save()
            return redirect('student-attendance')  # or show confirmation
    else:
        form = LeaveRequeststudentForm()
    
    return render(request, 'students/student_leave_request.html', {'form': form})



####### new models for student report card

# from .models import StuReportCard
# from django.contrib.auth.decorators import login_required

# @login_required
# def student_report_card_view(request):
#     cards = StuReportCard.objects.filter(student=request.user)
#     return render(request, 'students/student_report_card.html', {'cards': cards})



# students/views.py



# from xhtml2pdf import pisa
# from django.template.loader import get_template
# from django.http import HttpResponse
# from .models import StuReportCard
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render

# @login_required
# def student_report_card_view(request):
#     cards = StuReportCard.objects.filter(student=request.user)
 
#     if 'download' in request.GET:
#         template_path = 'students/student_report_card_pdf.html'
#         context = {'cards': cards, 'user': request.user}
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="report_card_{request.user.username}.pdf"'
        
#         template = get_template(template_path)
#         html = template.render(context)

#         pisa_status = pisa.CreatePDF(html, dest=response)
#         if pisa_status.err:
#             return HttpResponse('We had some errors <pre>' + html + '</pre>')
#         return response

#     return render(request, 'students/student_report_card.html', {'cards': cards})


###### all fields data download in pdf format


# from django.template.loader import get_template
# from django.http import HttpResponse
# from xhtml2pdf import pisa
# from .models import StuReportCard
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render

# @login_required
# def student_report_card_view(request):
#     cards = StuReportCard.objects.filter(student=request.user)

#     if 'download' in request.GET:
#         template_path = 'students/student_report_card_pdf.html'
#         context = {'cards': cards, 'user': request.user}
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="report_card_{request.user.username}.pdf"'

#         template = get_template(template_path)
#         html = template.render(context)

#         pisa_status = pisa.CreatePDF(html, dest=response)
#         if pisa_status.err:
#             return HttpResponse('We had some errors <pre>' + html + '</pre>')
#         return response

#     return render(request, 'students/student_report_card.html', {'cards': cards})



####### new download functions:
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from .models import StuReportCard
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import uuid
from datetime import datetime
import random

def generate_unique_invoice_number():
    return f"{random.randint(100000, 999999)}"

@login_required
def student_report_card_view(request):
    # Fetching the report cards for the logged-in user
    cards = StuReportCard.objects.filter(student=request.user)

    # Generate a unique invoice number
    # invoice_number = uuid.uuid4().int  # UUID will create a unique value, convert to integer
    
    invoice_number =  generate_unique_invoice_number()

    invoice_date = datetime.now().strftime('%B %d, %Y')  # Current date
    invoice_time = datetime.now().strftime('%H:%M:%S')  # Current time

    logo_url = request.build_absolute_uri('/media/profile_pictures/school4.png')

    if 'download' in request.GET:
        # Define the template and context to be passed
        template_path = 'students/student_report_card_pdf.html'
        context = {
            'cards': cards,
            'user': request.user,
            'invoice_number': invoice_number,
            'invoice_date': invoice_date,
            'invoice_time': invoice_time,
            'logo_url': logo_url
        }

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_card_{request.user.username}.pdf"'

        template = get_template(template_path)
        html = template.render(context)

        # Generate the PDF
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

    # Render the regular HTML page
    return render(request, 'students/student_report_card.html', {'cards': cards})



############################## new views.py function for another pdf download




# from django.template.loader import get_template
# from django.http import HttpResponse
# from xhtml2pdf import pisa
# from .models import StuReportCard
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# import random
# from datetime import datetime

# def generate_unique_invoice_number():
#     return f"{random.randint(100000, 999999)}"

# @login_required
# def student_report_card_view(request):
#     cards = StuReportCard.objects.filter(student=request.user).first()
    
#     invoice_number = generate_unique_invoice_number()
#     invoice_date = datetime.now().strftime('%B %d, %Y')
#     invoice_time = datetime.now().strftime('%H:%M:%S')

#     context = {
#         'card': cards,
#         'user': request.user,
#         'invoice_number': invoice_number,
#         'invoice_date': invoice_date,
#         'invoice_time': invoice_time,
#     }

#     if 'download' in request.GET:
#         template_path = 'students/student_report_card_pdf.html'
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="report_card_{request.user.username}.pdf"'
#         template = get_template(template_path)
#         html = template.render(context)
#         pisa_status = pisa.CreatePDF(html, dest=response)
#         if pisa_status.err:
#             return HttpResponse('We had some errors <pre>' + html + '</pre>')
#         return response

#     return render(request, 'students/student_report_card.html', context)





####### attendance record functions for student

# students/views.py

from .models import AttendanceRecord
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def student_attendance_view(request):
    records = AttendanceRecord.objects.filter(student=request.user)
    return render(request, 'students/student_attendance_report.html', {'records': records})
