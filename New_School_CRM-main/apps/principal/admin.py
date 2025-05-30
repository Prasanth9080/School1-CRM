from django.contrib import admin

####### student fees record admin

from .models import Principal_StudentFeesRecord,Circulation

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

    
from django.contrib import admin
from .models import Circulation,CirculationReadHide

@admin.register(Circulation)
class CirculationAdmin(admin.ModelAdmin):
    list_display = ['title', 'audience', 'created_by', 'created_at']

@admin.register(CirculationReadHide)
class CirculationReadHideAdmin(admin.ModelAdmin):
    list_display = ['user', 'circulation', 'role']
