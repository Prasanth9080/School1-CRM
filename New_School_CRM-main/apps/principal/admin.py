from django.contrib import admin

####### student fees record admin

from .models import Principal_StudentFeesRecord

@admin.register(Principal_StudentFeesRecord)
class Principal_StudentFeesRecordAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'student_class','term', 'session', 'this_term_fees', 'previous_term_balance',
        'total_amount','paid_amount','balance_payable_amount', 'status', 'created_by', 'created_at', 'gender', 'starting_date', 'ending_date'
    )
    search_fields = ('student__username', 'term', 'session')
    readonly_fields = ('status', 'total_amount','paid_amount','balance_payable_amount',)
    search_fields = ('student__username', 'session__name')
    list_filter = ('status', 'term', 'session')
