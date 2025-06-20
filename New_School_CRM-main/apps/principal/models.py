from django.db import models
from django.contrib.auth.models import User
from apps.corecode.models import AcademicTerm, AcademicSession, StudentClass, UserProfile  # replace 'your_app' with actual app name
from decimal import Decimal

class Principal_StudentFeesRecord(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('partial', 'Partial'),
    ]

    student = models.ForeignKey(User, limit_choices_to={'userprofile__role': 'student'}, on_delete=models.CASCADE)
    student_class = models.ForeignKey(StudentClass, on_delete=models.SET_NULL, null=True, blank=True)
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)

    this_term_fees = models.DecimalField(max_digits=10, decimal_places=2)
    previous_term_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance_payable_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    gender = models.CharField(max_length=10, choices=[("male", "Male"), ("female", "Female")])
    starting_date = models.DateField()
    ending_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_by = models.CharField(
        max_length=20,
        choices=(('staff', 'Staff'), ('principal', 'Principal')),
        default='principal'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    # def save(self, *args, **kwargs):
    #     self.total_amount = self.this_term_fees + self.previous_term_balance
    #     self.balance_payable_amount = self.total_amount - self.paid_amount

    #     # Automatically set status
    #     if self.paid_amount == 0:
    #         self.status = 'pending'
    #     elif self.balance_payable_amount > 0:
    #         self.status = 'partial'
    #     else:
    #         self.status = 'paid'

    #     super().save(*args, **kwargs)


    from decimal import Decimal

    def save(self, *args, **kwargs):
        # Ensure Decimal conversion
        self.this_term_fees = Decimal(str(self.this_term_fees))
        self.previous_term_balance = Decimal(str(self.previous_term_balance))
        self.paid_amount = Decimal(str(self.paid_amount))

        self.total_amount = self.this_term_fees + self.previous_term_balance
        self.balance_payable_amount = self.total_amount - self.paid_amount

        # Automatically set status
        if self.paid_amount == 0:
            self.status = 'pending'
        elif self.balance_payable_amount > 0:
            self.status = 'partial'
        else:
            self.status = 'paid'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.username} - {self.term.name} - {self.session.name}"
    


###### ###### #######  
# models.py
from django.db import models
from django.contrib.auth.models import User

class Circulation(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    audience_choices = [
        ('all', 'All'),
        ('staff', 'Staff'),
        ('students', 'Students'),
    ]
    audience = models.CharField(max_length=10, choices=audience_choices, default='all')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

#### hidding cirulations 

class CirculationReadHide(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    circulation = models.ForeignKey(Circulation, on_delete=models.CASCADE)
    role = models.CharField(max_length=10)  # 'student' or 'staff'

    class Meta:
        unique_together = ('user', 'circulation', 'role')

    def __str__(self):
        return f"{self.user} - {self.role} - {self.circulation}"




#### for staff class schedule

from django.db import models

STATUS_CHOICES = (
    ('present', 'Present'),
    ('absent', 'Absent'),
)
DAYS = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
)

class StaffClassSchedule(models.Model):
    staff_name = models.ForeignKey(User, limit_choices_to={'userprofile__role': 'teacher'}, on_delete=models.CASCADE)
    class_name = models.ForeignKey(
        StudentClass, on_delete=models.SET_NULL, blank=True, null=True
    )
    section = models.CharField(max_length=10)
    subject = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    day_of_week = models.CharField(max_length=10, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date_time = models.DateTimeField()

    def __str__(self):
        return f"{self.staff_name} - {self.class_name} {self.section} ({self.date_time})"


