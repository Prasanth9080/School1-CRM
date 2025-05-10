
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