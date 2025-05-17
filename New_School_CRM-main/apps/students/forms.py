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


# from django import forms
# from .models import StuReportCard
# from ckeditor.widgets import CKEditorWidget
# from django.contrib.auth.models import User
# from django.contrib.auth.models import Group

# class StuReportCardForm(forms.ModelForm):
#     class Meta:
#         model = StuReportCard
#         fields = '__all__'
#         widgets = {
#             'address': CKEditorWidget(),
#             'comments': CKEditorWidget(),
#         }

    # def __init__(self, *args, **kwargs):
    #     super(StuReportCardForm, self).__init__(*args, **kwargs)
    #     self.fields['student'].queryset = User.objects.filter(groups__name='STUDENT')
    #     self.fields['student'].label_from_instance = lambda obj: f"{obj.username}"  # 👈 Only username





######## new.....

# from django import forms
# from .models import StuReportCard

# class StuReportCardForm(forms.ModelForm):
#     class Meta:
#         model = StuReportCard
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super(StuReportCardForm, self).__init__(*args, **kwargs)

#         instance = kwargs.get('instance', None)
#         term = self.initial.get('term') or (instance.term if instance else None)

#         # Check if it's a Term I record
#         is_term1 = term == "Term I" or not term

#         common_fields = [
#             'standard', 'section', 'academic_session', 'father_name',
#             'mother_name', 'address', 'admission_number', 'roll_number',
#             'date_of_birth', 'comments', 'signature_class_teacher',
#             'signature_principal',
#         ]

#         if not is_term1:
#             # Make common fields hidden or disabled for Term II and III
#             for field in common_fields:
#                 if field in self.fields:
#                     self.fields[field].widget = forms.HiddenInput()
#                     self.fields[field].required = False

#         # Optional: prevent changing term once saved
#         if instance:
#             self.fields['term'].disabled = True



############ new ......

# students/forms.py

from django import forms
from .models import StuReportCard

class StuReportCardForm(forms.ModelForm):
    class Meta:
        model = StuReportCard
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(StuReportCardForm, self).__init__(*args, **kwargs)

        if 'student' in self.data:
            student_id = self.data.get('student')
        elif self.instance and self.instance.pk:
            student_id = self.instance.student.id
        else:
            student_id = None

        # If Term I already exists for this student, hide certain fields
        if student_id:
            from .models import StuReportCard
            try:
                term1_card = StuReportCard.objects.get(student__id=student_id, term="Term I")
                if not self.instance.pk or self.instance.term != "Term I":
                    # Hide all the common fields
                    for field_name in [
                        'standard', 'section', 'academic_session',
                        'father_name', 'mother_name', 'address',
                        'admission_number', 'roll_number', 'date_of_birth',
                        'comments', 'signature_class_teacher', 'signature_principal'
                    ]:
                        self.fields[field_name].widget = forms.HiddenInput()
                        self.fields[field_name].required = False
            except StuReportCard.DoesNotExist:
                pass






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

