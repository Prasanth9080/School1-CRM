
from django import forms
from .models import Principal_StudentFeesRecord

class Principal_StudentFeesRecordForm(forms.ModelForm):
    class Meta:
        model = Principal_StudentFeesRecord
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





##### new ....

# from django import forms
# from .models import Principal_StudentFeesRecord

# class Principal_StudentFeesRecordForm(forms.ModelForm):
#     class Meta:
#         model = Principal_StudentFeesRecord
#         fields = '__all__'
#         exclude = ['created_by', 'created_at', 'total_amount', 'balance_payable_amount', 'status']

#     def clean(self):
#         cleaned_data = super().clean()
#         student = cleaned_data.get('student')
#         term = cleaned_data.get('term')
#         session = cleaned_data.get('session')

#         if self.instance.pk is None:  # Only on create
#             if Principal_StudentFeesRecord.objects.filter(student=student, term=term, session=session).exists():
#                 raise forms.ValidationError("A fee record for this student, term, and session already exists.")
        
#         return cleaned_data




##################### ciculation form details

# forms.py
from django import forms
from .models import Circulation

class CirculationForm(forms.ModelForm):
    class Meta:
        model = Circulation
        fields = ['title', 'content', 'audience']

