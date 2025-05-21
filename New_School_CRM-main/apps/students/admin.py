from django.contrib import admin
from .models import Student, StudentBulkUpload, LeaveRequeststudent, StuReportCard,AttendanceRecord, Payment,StaffNotification,HiddenNotification

class StudentAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'surname', 'firstname', 'other_name', 'gender', 'date_of_birth', 'current_class', 'date_of_admission', 'parent_mobile_number')
    search_fields = ('registration_number', 'surname', 'firstname', 'other_name')
    list_filter = ('gender', 'current_class', 'current_status')
    ordering = ('surname', 'firstname', 'other_name')
    readonly_fields = ('date_of_admission',)

class StudentBulkUploadAdmin(admin.ModelAdmin):
    list_display = ('date_uploaded', 'csv_file')
    readonly_fields = ('date_uploaded',)


class LeaveRequeststudentAdmin(admin.ModelAdmin):
    list_display =('student', 'standard', 'reason','date_applied','status')


class StuReportCardAdmin(admin.ModelAdmin):
    list_display = ('student', 'standard', 'tamil','english','maths','science','social','all_subject_mark','total_marks','overall_total','overall_percentage','overall_grade',
    'father_name','mother_name','address','date_of_birth','admission_number','roll_number',
 'status','term','comments', 'signature_class_teacher','signature_principal','parent_signature',   'created_at')
#     list_display =('student','standard','section','academic_session', 'father_name', 'mother_name','address','admission_number','roll_number','date_of_birth','subjects','total_term1','total_term2','total_final',
# 'percent_term1','percent_term2','percent_final','grade_term1','grade_term2','grade_final','comments','term','status','date','signature_class_teacher','signature_principal','parent_signature','created_at')


class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'month','date', 'day','status','message','signature')
 


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_id', 'order_id', 'amount', 'status', 'created_at', 'fees_record')
@admin.register(StaffNotification)
class StaffNotificationAdmin(admin.ModelAdmin):
    list_display = ('id','student', 'message', 'is_read',  'created_at')
@admin.register(HiddenNotification)
class HiddenNotificationAdmin(admin.ModelAdmin):
    list_display = ('id','staff', 'notification', 'hidden_at',)

# admin.site.register(Payment, PaymentAdmin)

admin.site.register(AttendanceRecord, AttendanceRecordAdmin)

admin.site.register(StuReportCard, StuReportCardAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(LeaveRequeststudent, LeaveRequeststudentAdmin)
admin.site.register(StudentBulkUpload, StudentBulkUploadAdmin)
