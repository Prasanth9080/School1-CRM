# students/forms.py

# from django import forms
# from .models import LeaveRequeststaff

# class LeaveRequeststaffForm(forms.ModelForm):
#     class Meta:
#         model = LeaveRequeststaff
#         fields = [ 'reason']

### new....
from django import forms
from .models import LeaveRequeststaff

class LeaveRequeststaffForm(forms.ModelForm):
    send_to_principal = forms.BooleanField(required=False, initial=True, label="Send leave request to principal")

    class Meta:
        model = LeaveRequeststaff
        fields = ['leave_date', 'reason', 'is_emergency']
        widgets = {
            'leave_date': forms.DateInput(attrs={'type': 'date'}),
        }



###### attendance form for staff

from django import forms
from .models import StaffAttendanceRecord
from django.contrib.auth.models import User

class StaffAttendanceForm(forms.ModelForm):
    class Meta:
        model = StaffAttendanceRecord
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }



######## student fees management form status  (visible) ah show agum ########
# from django import forms
# from .models import StudentFeesRecord

# class StudentFeesRecordForm(forms.ModelForm):
#     class Meta:
#         model = StudentFeesRecord
#         fields = '__all__'

######## student fees management form status ( disable ) ah show agum ########

# from django import forms
# from .models import StudentFeesRecord

# class StudentFeesRecordForm(forms.ModelForm):
#     class Meta:
#         model = StudentFeesRecord
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Disable the status field (staff can’t change it)
#         self.fields['status'].disabled = True

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         # Force status to 'pending' if creating new record
#         if not instance.pk:
#             instance.status = 'pending'
#         if commit:
#             instance.save()
#         return instance




from django.core.mail import send_mail
from .models import StudentFeesRecord
class StudentFeesRecordForm(forms.ModelForm):
    class Meta:
        model = StudentFeesRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].disabled = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        is_new = instance.pk is None  # Check if it's a new record

        # Set default status only on new records
        if is_new:
            instance.status = 'pending'

        if commit:
            instance.save()

            # 🔔 Send notification to student (only on new record)
            if is_new:
                send_mail(
                    subject='New Fee Record Created',
                    message=f"Dear {instance.student.username},\n\nYour fee record for the term '{instance.term}' and session '{instance.session}' has been created.\n\nTotal Fees: ₹{instance.total_amount}\nAmount Due: ₹{instance.balance_payable_amount}\n\nPlease make the payment before {instance.ending_date}.",
                    from_email='noreply@yourdomain.com',
                    recipient_list=[instance.student.email],
                    fail_silently=True,  # Optional: Avoid crashing if email fails
                )

        return instance
