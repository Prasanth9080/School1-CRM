# students/forms.py

from django import forms
from .models import LeaveRequeststudent

class LeaveRequeststudentForm(forms.ModelForm):
    class Meta:
        model = LeaveRequeststudent
        fields = ['standard', 'reason']

######## new forms for studetn report card

# from django import forms
# from .models import StuReportCard

# class StuReportCardForm(forms.ModelForm):
#     class Meta:
#         model = StuReportCard
#         fields = [
#             'student', 'standard', 'tamil', 'english', 'maths',
#             'science', 'social', 'status', 'comments', 'parent_signature'
#         ]


from django import forms
from .models import StuReportCard
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

class StuReportCardForm(forms.ModelForm):
    class Meta:
        model = StuReportCard
        fields = '__all__'
        widgets = {
            'address': CKEditorWidget(),
            'comments': CKEditorWidget(),
        }

    # def __init__(self, *args, **kwargs):
    #     super(StuReportCardForm, self).__init__(*args, **kwargs)
    #     self.fields['student'].queryset = User.objects.filter(groups__name='STUDENT')
    #     self.fields['student'].label_from_instance = lambda obj: f"{obj.username}"  # 👈 Only username



##### attendence form for student

from django import forms
from .models import AttendanceRecord
from django.contrib.auth.models import User

class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super(AttendanceRecordForm, self).__init__(*args, **kwargs)
    #     self.fields['student'].queryset = User.objects.filter(groups__name='STUDENT')

