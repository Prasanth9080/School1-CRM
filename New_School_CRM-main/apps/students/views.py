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



######  /////// ######### razorpay payment function

# import razorpay
# from django.conf import settings
# from django.shortcuts import render, redirect
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required
# from .models import Payment
# from django.http import HttpResponseBadRequest

# client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# @login_required
# def initiate_payment(request):
#     if request.method == "POST":
#         amount = int(request.POST['amount']) * 100  # amount in paisa
#         user = request.user

#         data = {
#             "amount": amount,
#             "currency": "INR",
#             "receipt": f"receipt_{user.id}"
#         }
#         order = client.order.create(data=data)

#         # Save payment in DB
#         payment = Payment.objects.create(
#             user=user,
#             order_id=order.get('id'),
#             amount=amount / 100,
#             status='Pending'
#         )

#         return render(request, 'students/razorpay_payment.html', {
#             'order_id': order['id'],
#             'amount': amount,
#             'key': settings.RAZORPAY_KEY_ID,
#             'user': user,
#             'payment': payment
#         })
#     return render(request, 'students/initiate_payment.html')

# @csrf_exempt
# def payment_success(request):
#     if request.method == "POST":
#         data = request.POST
#         try:
#             client.utility.verify_payment_signature({
#                 'razorpay_order_id': data['razorpay_order_id'],
#                 'razorpay_payment_id': data['razorpay_payment_id'],
#                 'razorpay_signature': data['razorpay_signature']
#             })
#         except razorpay.errors.SignatureVerificationError:
#             return HttpResponseBadRequest()

#         # Update payment record
#         payment = Payment.objects.get(order_id=data['razorpay_order_id'])
#         payment.payment_id = data['razorpay_payment_id']
#         payment.signature = data['razorpay_signature']
#         payment.status = 'Complete'
#         payment.save()

#         return render(request, 'students/payment_success.html', {'payment': payment})
#     return HttpResponseBadRequest()




### new

# from django.shortcuts import render
# from django.conf import settings
# import razorpay
# from .models import Payment
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponseBadRequest

# client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# @login_required
# def initiate_payment(request):
#     if request.method == "POST":
#         try:
#             amount = int(request.POST.get('amount', 0)) * 100  # amount in paisa
#             if amount <= 0:
#                 return render(request, 'students/initiate_payment.html', {
#                     'error': "Invalid amount entered."
#                 })

#             data = {
#                 "amount": amount,
#                 "currency": "INR",
#                 "receipt": f"receipt_{request.user.id}"
#             }

#             order = client.order.create(data=data)

#             payment = Payment.objects.create(
#                 user=request.user,
#                 order_id=order.get('id'),
#                 amount=amount / 100,
#                 status='Pending'
#             )

#             return render(request, 'students/razorpay_payment.html', {
#                 'order_id': order['id'],
#                 'amount': amount,
#                 'key': settings.RAZORPAY_KEY_ID,
#                 'user': request.user,
#                 'payment': payment
#             })
#         except Exception as e:
#             return render(request, 'students/initiate_payment.html', {
#                 'error': f"Server error: {str(e)}"
#             })

#     return render(request, 'students/initiate_payment.html')

# @csrf_exempt
# def payment_success(request):
#     if request.method == "POST":
#         data = request.POST
#         try:
#             client.utility.verify_payment_signature({
#                 'razorpay_order_id': data['razorpay_order_id'],
#                 'razorpay_payment_id': data['razorpay_payment_id'],
#                 'razorpay_signature': data['razorpay_signature']
#             })
#         except razorpay.errors.SignatureVerificationError:
#             return HttpResponseBadRequest()

#         # Update payment record
#         payment = Payment.objects.get(order_id=data['razorpay_order_id'])
#         payment.payment_id = data['razorpay_payment_id']
#         payment.signature = data['razorpay_signature']
#         payment.status = 'Complete'
#         payment.save()

#         return render(request, 'students/payment_success.html', {'payment': payment})
#     return HttpResponseBadRequest()



###### another new 2nd working good condition

# from django.shortcuts import render, redirect
# from django.conf import settings
# from .models import Payment
# import razorpay
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required

# client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# @login_required
# def initiate_payment(request):
#     if request.method == "POST":
#         amount = int(request.POST.get("amount")) * 100  # in paisa
#         user = request.user

#         # Razorpay order create
#         order = client.order.create({
#             "amount": amount,
#             "currency": "INR",
#             "payment_capture": "1"
#         })

#         # Save payment record
#         payment = Payment.objects.create(
#             user=user,
#             order_id=order['id'],
#             amount=amount / 100,
#             status='Pending'
#         )

#         context = {
#             "order_id": order['id'],
#             "amount": amount,
#             "key": settings.RAZORPAY_KEY_ID,
#             "user": user,
#         }
#         return render(request, "students/razorpay_payment.html", context)

#     return render(request, "students/initiate_payment.html")


# from .models import StaffNotification  # Add this at the top

# # @csrf_exempt
# # def payment_success(request):
# #     if request.method == "POST":
# #         data = request.POST
# #         try:
# #             order_id = data.get("razorpay_order_id")
# #             payment_id = data.get("razorpay_payment_id")
# #             signature = data.get("razorpay_signature")

# #             payment = Payment.objects.get(order_id=order_id)
# #             payment.payment_id = payment_id
# #             payment.signature = signature
# #             payment.status = "Complete"
# #             payment.save()

# #                 # After payment.save()
# #             StaffNotification.objects.create(
# #                 student=payment.user,
# #                 message=f"{payment.user.username} has paid the school fees successfully. Please verify and generate the invoice."
# #             )
# #             return render(request, "students/payment_success.html", {"payment": payment})
# #         except Payment.DoesNotExist:
# #             return HttpResponse("Payment not found", status=404)
# #     return HttpResponse("Invalid request", status=400)

# from django.http import HttpResponse, HttpResponseRedirect
# from django.urls import reverse

# @csrf_exempt
# def payment_success(request):
#     if request.method == "POST":
#         data = request.POST
#         try:
#             order_id = data.get("razorpay_order_id")
#             payment_id = data.get("razorpay_payment_id")
#             signature = data.get("razorpay_signature")

#             payment = Payment.objects.get(order_id=order_id)
#             if payment.status != "Complete":  # prevent re-saving
#                 payment.payment_id = payment_id
#                 payment.signature = signature
#                 payment.status = "Complete"
#                 payment.save()

#                 # Create notification once
#                 StaffNotification.objects.create(
#                     student=payment.user,
#                     message=f"{payment.user.username} has paid the school fees successfully. Please verify and generate the invoice."
#                 )

#             # Store payment ID in session to access in GET
#             request.session['payment_id'] = payment.id
#             return HttpResponseRedirect(reverse('show_payment_success'))

#         except Payment.DoesNotExist:
#             return HttpResponse("Payment not found", status=404)
#     return HttpResponse("Invalid request", status=400)



# @login_required
# def show_payment_success(request):
#     payment_id = request.session.pop('payment_id', None)
#     if not payment_id:
#         return redirect('initiate_payment')

#     try:
#         payment = Payment.objects.get(id=payment_id)
#         return render(request, "students/payment_success.html", {"payment": payment})
#     except Payment.DoesNotExist:
#         return redirect('initiate_payment')

#### *************************************** old code

# ######################### this is staff notification model inside added payment model fields data related function
# from django.shortcuts import render, redirect
# from django.conf import settings
# from .models import Payment ,StaffNotification
# import razorpay
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse, HttpResponseRedirect
# from django.urls import reverse
# from ..staffs.models import StudentFeesRecord
# from ..principal.models import Principal_StudentFeesRecord #### principal student fees report create panna intha model use pannanum
# from decimal import Decimal

# client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# # @login_required
# # def initiate_payment(request):
# #     if request.method == "POST":
# #         amount = int(request.POST.get("amount")) * 100  # in paisa
# #         user = request.user

# #         # Razorpay order create
# #         order = client.order.create({
# #             "amount": amount,
# #             "currency": "INR",
# #             "payment_capture": "1"
# #         })

# #         # Save payment record
# #         payment = Payment.objects.create(
# #             user=user,
# #             order_id=order['id'],
# #             amount=amount / 100,
# #             status='Pending'
# #         )

# #         context = {
# #             "order_id": order['id'],
# #             "amount": amount,
# #             "key": settings.RAZORPAY_KEY_ID,
# #             "user": user,
# #         }
# #         return render(request, "students/razorpay_payment.html", context)

# #     return render(request, "students/initiate_payment.html")

# ####### working good, but staff student oda fees-record create pannalum principal create pannalum show aguthu

# @login_required
# def initiate_payment(request):
#     user = request.user
#     try:
#         # Get the most recent fee record for the student
#         fee_record = StudentFeesRecord.objects.filter(student=user).latest('created_at')
#     except StudentFeesRecord.DoesNotExist:
#         return render(request, "students/initiate_payment.html", {"error": "No fees assigned by staff yet."})

#     if request.method == "POST":
#         amount = int(request.POST.get("amount")) * 100  # Razorpay expects amount in paisa

#         order = client.order.create({
#             "amount": amount,
#             "currency": "INR",
#             "payment_capture": "1"
#         })

#         payment = Payment.objects.create(
#             user=user,
#             order_id=order['id'],
#             amount=amount / 100,
#             status='Pending',
#             fees_record=fee_record
#         )

#         return render(request, "students/razorpay_payment.html", {
#             "order_id": order['id'],
#             "amount": amount,
#             "key": settings.RAZORPAY_KEY_ID,
#             "user": user,
#             "csrf_token": request.META['CSRF_COOKIE'],  # ensure Razorpay success POST works
#         })

#     return render(request, "students/initiate_payment.html", {"fee_record": fee_record})

# @csrf_exempt
# def payment_success(request):
#     if request.method == "POST":
#         data = request.POST
#         try:
#             order_id = data.get("razorpay_order_id")
#             payment_id = data.get("razorpay_payment_id")
#             signature = data.get("razorpay_signature")

#             payment = Payment.objects.get(order_id=order_id)
#             if payment.status != "Complete":
#                 payment.payment_id = payment_id
#                 payment.signature = signature
#                 payment.status = "Complete"
#                 payment.save()

#                 # if payment.fees_record:
#                 #     payment.fees_record.status = 'paid'
#                 #     payment.fees_record.save()


#                 # Find matching StudentFeesRecord for this student and term/session
#                 fees_record = StudentFeesRecord.objects.filter(
#                     student=payment.user,
#                     status__in=["pending", "partial"]
#                 ).order_by('-created_at').first()

#                 if fees_record:
#                     fees_record.paid_amount += Decimal(str(payment.amount)) 
#                     fees_record.save()  # triggers save logic to update status and balance
               
               
               
#                 if payment.amount >= payment.fees_record.total_amount:
#                     payment.fees_record.status = 'paid'
#                 else:
#                     payment.fees_record.status = 'partial'


#                 # Create notification and link to payment
#                 StaffNotification.objects.create(
#                     student=payment.user,
#                     amount=payment,
#                     message=(
#                         f"{payment.user.username} paid ₹{payment.amount} successfully. "
#                         f"Order ID: {payment.order_id}, Payment ID: {payment.payment_id}, Status: {payment.status}"
#                     )
#                 )

#             request.session['payment_id'] = payment.id
#             return HttpResponseRedirect(reverse('show_payment_success'))

#         except Payment.DoesNotExist:
#             return HttpResponse("Payment not found", status=404)
#     return HttpResponse("Invalid request", status=400)

# @login_required
# def show_payment_success(request):
#     payment_id = request.session.pop('payment_id', None)
#     if not payment_id:
#         return redirect('initiate_payment')

#     try:
#         payment = Payment.objects.get(id=payment_id)
#         return render(request, "students/payment_success.html", {"payment": payment})
#     except Payment.DoesNotExist:
#         return redirect('initiate_payment')
    


# #######...........

# from django.contrib.auth.decorators import login_required
# from ..staffs.models import StudentFeesRecord

# @login_required
# def student_fee_detail_view(request):
#     fees = StudentFeesRecord.objects.filter(student=request.user)
#     return render(request, 'students/student_fee_detail.html', {'fees': fees})





######################## new new new new 


from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from decimal import Decimal
import razorpay
from django.contrib import messages
from .models import Payment, StaffNotification
from ..staffs.models import StudentFeesRecord

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@login_required
def initiate_payment(request):
    user = request.user
    try:
        fee_record = StudentFeesRecord.objects.filter(student=user).latest('created_at')
    except StudentFeesRecord.DoesNotExist:
        return render(request, "students/initiate_payment.html", {"error": "No fees assigned by staff yet."})
    
    latest_payment = Payment.objects.filter(user=user).order_by('-created_at').first()

    if request.method == "POST":
        try:
            entered_amount = Decimal(request.POST.get("amount"))
        except (ValueError, TypeError):
            return render(request, "students/initiate_payment.html", {
                "fee_record": fee_record,
                "error": "Invalid amount entered.",
                "latest_payment" : latest_payment
            })

        if entered_amount <= 0:
            return render(request, "students/initiate_payment.html", {
                "fee_record": fee_record,
                "error": "Amount must be greater than zero.",
                "latest_payment":latest_payment
            })

        # if entered_amount > fee_record.balance_payable_amount:
        #     return render(request, "students/initiate_payment.html", {
        #         "fee_record": fee_record,
        #         "error": f"⚠️ You cannot pay more than the remaining balance (₹{fee_record.balance_payable_amount})."
        #     })
        
        if entered_amount > fee_record.balance_payable_amount:
            messages.error(
                request,
                f"⚠️ You cannot pay more than the remaining balance(₹{fee_record.balance_payable_amount})."
            )
            return redirect('initiate_payment')  # Redirect to reload and show message

        amount_paise = int(entered_amount * 100)

        # Create Razorpay Order
        order = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": "1"
        })

        # Save Payment object
        payment = Payment.objects.create(
            user=user,
            order_id=order['id'],
            amount=entered_amount,
            status='Pending',
            fees_record=fee_record
        )

        return render(request, "students/razorpay_payment.html", {
            "order_id": order['id'],
            "amount": amount_paise,
            "key": settings.RAZORPAY_KEY_ID,
            "user": user,
            "csrf_token": request.META['CSRF_COOKIE'],
        }) 

    return render(request, "students/initiate_payment.html", {"fee_record": fee_record, "latest_payment":latest_payment})


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST
        order_id = data.get("razorpay_order_id")
        payment_id = data.get("razorpay_payment_id")
        signature = data.get("razorpay_signature")

        try:
            payment = Payment.objects.get(order_id=order_id)
        except Payment.DoesNotExist:
            return HttpResponse("Payment not found", status=404)

        if payment.status != "Complete":
            payment.payment_id = payment_id
            payment.signature = signature
            payment.status = "Complete"
            payment.save()

            # Update the fees record
            fee_record = payment.fees_record
            fee_record.paid_amount += Decimal(str(payment.amount))
            fee_record.save()  # triggers status + balance update

            # Optional: Explicitly set status again
            if fee_record.paid_amount >= fee_record.total_amount:
                fee_record.status = 'paid'
            elif fee_record.paid_amount > 0:
                fee_record.status = 'partial'
            else:
                fee_record.status = 'pending'
            fee_record.save()

            # Notify staff
            StaffNotification.objects.create(
                student=payment.user,
                amount=payment,
                message=(
                    f"{payment.user.username} paid ₹{payment.amount} successfully. "
                    f"Order ID: {payment.order_id}, Payment ID: {payment.payment_id}, Status: {payment.status}"
                )
            )

        request.session['payment_id'] = payment.id
        return HttpResponseRedirect(reverse('show_payment_success'))

    return HttpResponse("Invalid request", status=400)


@login_required
def show_payment_success(request):
    payment_id = request.session.pop('payment_id', None)
    if not payment_id:
        return redirect('initiate_payment')

    try:
        payment = Payment.objects.get(id=payment_id)
    except Payment.DoesNotExist:
        return redirect('initiate_payment')

    return render(request, "students/payment_success.html", {"payment": payment})


@login_required
def student_fee_detail_view(request):
    fees = StudentFeesRecord.objects.filter(student=request.user)
    return render(request, 'students/student_fee_detail.html', {'fees': fees})


######## student fees download in pdf

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
import random

from .models import Payment


def generate_unique_invoice_number():
    return f"INV-{random.randint(100000, 999999)}"


# @login_required
# def download_payment_pdf(request):
#     user = request.user
#     latest_payment = Payment.objects.filter(user=user).order_by('-created_at').first()

#     if not latest_payment:
#         return HttpResponse("No payment record found.")

#     invoice_number = generate_unique_invoice_number()
#     invoice_date = datetime.now().strftime('%B %d, %Y')  # e.g., May 09, 2025
#     invoice_time = datetime.now().strftime('%I:%M %p')    # e.g., 03:45 PM

#     # Get logo full URL (adjust path to your actual media root config)
#     logo_url = request.build_absolute_uri('/media/profile_pictures/school4.png')

#     is_payment_complete=(
#         latest_payment.status == "Complete" and latest_payment.payment_id
#     )

#     template_path = 'students/student_payment_pdf.html'

#     context = {
#         'latest_payment': latest_payment,
#         'fee_record': latest_payment.fees_record,
#         'invoice_number': invoice_number,
#         'invoice_date': invoice_date,
#         'invoice_time': invoice_time,
#         'logo_url': logo_url,
#         'is_payment_complete' : is_payment_complete
#     }

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="payment_summary.pdf"'

#     template = get_template(template_path)
#     html = template.render(context)

#     pisa_status = pisa.CreatePDF(html, dest=response)

#     if pisa_status.err:
#         return HttpResponse('Error generating PDF')
#     return response


@login_required
def download_payment_pdf(request):
    user = request.user
    latest_payment = Payment.objects.filter(user=user).order_by('-created_at').first()

    if not latest_payment:
        return HttpResponse("No payment record found.")

    invoice_number = generate_unique_invoice_number()
    invoice_date = datetime.now().strftime('%B %d, %Y')
    invoice_time = datetime.now().strftime('%I:%M %p')
    logo_url = request.build_absolute_uri('/media/profile_pictures/school4.png')

    # ✅ Add the simplified flag here
    is_payment_complete = (
        latest_payment.status == "Complete" and latest_payment.payment_id
    )

    context = {
        'latest_payment': latest_payment,
        'fee_record': latest_payment.fees_record,
        'invoice_number': invoice_number,
        'invoice_date': invoice_date,
        'invoice_time': invoice_time,
        'logo_url': logo_url,
        'is_payment_complete': is_payment_complete,  # ✅ Pass to template
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="payment_summary.pdf"'

    template = get_template('students/student_payment_pdf.html')
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF')
    return response
