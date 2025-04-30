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