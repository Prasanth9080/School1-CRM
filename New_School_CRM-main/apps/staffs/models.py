from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Staff(models.Model):
    STATUS = [("active", "Active"), ("inactive", "Inactive")]

    GENDER = [("male", "Male"), ("female", "Female")]

    current_status = models.CharField(max_length=10, choices=STATUS, default="active")
    surname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    other_name = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, default="male")
    date_of_birth = models.DateField(default=timezone.now)
    date_of_admission = models.DateField(default=timezone.now)

    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
    mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )

    address = models.TextField(blank=True)
    others = models.TextField(blank=True)

    def __str__(self):
        return f"{self.surname} {self.firstname} {self.other_name}"

    def get_absolute_url(self):
        return reverse("staff-detail", kwargs={"pk": self.pk})


######## leave request model for staff ########

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 

class LeaveRequeststaff(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    date_applied = models.DateTimeField(auto_now_add=True)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.staff.username} - {self.status}" 
    

######### attendance model for staff ########

from django.db import models
from django.contrib.auth.models import User

STAFF_ATTENDANCE_STATUS = (
    ('present', 'Present'),
    ('absent', 'Absent'),
    ('permission', 'Permission'),
)

WEEK_DAYS = (
    ('mon', 'Monday'),
    ('tue', 'Tuesday'),
    ('wed', 'Wednesday'),
    ('thu', 'Thursday'),
    ('fri', 'Friday'),
)

class StaffAttendanceRecord(models.Model):
    staff = models.ForeignKey(User,limit_choices_to={'userprofile__role': 'teacher'}, on_delete=models.CASCADE)
    date = models.DateField()
    month = models.CharField(max_length=20)
    day = models.CharField(max_length=10, choices=WEEK_DAYS)
    status = models.CharField(max_length=15, choices=STAFF_ATTENDANCE_STATUS)
    message = models.TextField(blank=True)
    signature = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.staff.username} - {self.date} - {self.status}"
