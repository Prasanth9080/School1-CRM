from django.db import models
from django.contrib.auth.models import User
from apps.corecode.models import AcademicTerm, AcademicSession, StudentClass, UserProfile  # replace 'your_app' with actual app name

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

    def save(self, *args, **kwargs):
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