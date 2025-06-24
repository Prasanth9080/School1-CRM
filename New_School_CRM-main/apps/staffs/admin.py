from django.contrib import admin
from .models import Staff, LeaveRequeststaff,StaffAttendanceRecord

class StaffAdmin(admin.ModelAdmin):
    list_display = ('surname', 'firstname', 'other_name', 'gender', 'date_of_birth', 'date_of_admission', 'mobile_number', 'current_status')
    search_fields = ('surname', 'firstname', 'other_name', 'mobile_number')
    list_filter = ('gender', 'current_status')
    ordering = ('surname', 'firstname', 'other_name')
    readonly_fields = ('date_of_admission',)




# class LeaveRequeststaffAdmin(admin.ModelAdmin):
#     list_display =('staff', 'reason','date_applied','status')


##### new 2 ....

from django.contrib import admin
from .models import LeaveRequeststaff

@admin.register(LeaveRequeststaff)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('staff', 'start_date', 'end_date', 'reason', 'is_emergency', 'status', 'date_applied')
    list_filter = ('status', 'is_emergency')
    search_fields = ('staff__username', 'reason')

class StaffAttendanceRecordAdmin(admin.ModelAdmin):
    list_display =('staff', 'date','month','day','status','message','signature')
    
####### student fees admin

from .models import StudentFeesRecord

@admin.register(StudentFeesRecord)
class StudentFeesRecordAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'term', 'session', 'this_term_fees', 'previous_term_balance',
        'total_amount','paid_amount','balance_payable_amount', 'status', 'created_at', 'gender', 'starting_date', 'ending_date'
    )
    search_fields = ('student__username', 'term', 'session')
    readonly_fields = ('status', 'total_amount','paid_amount','balance_payable_amount',)
    search_fields = ('student__username', 'session__name')
    list_filter = ('status', 'term', 'session')


admin.site.register(Staff, StaffAdmin)
# admin.site.register(LeaveRequeststaff)
# admin.site.register(LeaveRequeststaffAdmin)
admin.site.register(StaffAttendanceRecord, StaffAttendanceRecordAdmin)