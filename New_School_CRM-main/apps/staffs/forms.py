# students/forms.py

from django import forms
from .models import LeaveRequeststaff

class LeaveRequeststaffForm(forms.ModelForm):
    class Meta:
        model = LeaveRequeststaff
        fields = [ 'reason']


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

from django import forms
from .models import StudentFeesRecord

class StudentFeesRecordForm(forms.ModelForm):
    class Meta:
        model = StudentFeesRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Disable the status field (staff can’t change it)
        self.fields['status'].disabled = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Force status to 'pending' if creating new record
        if not instance.pk:
            instance.status = 'pending'
        if commit:
            instance.save()
        return instance