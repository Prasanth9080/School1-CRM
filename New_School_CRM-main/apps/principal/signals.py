# principal/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from staffs.models import StudentFeesRecord
from principal.models import Principal_StudentFeesRecord

@receiver(post_save, sender=StudentFeesRecord)
def copy_fee_to_principal(sender, instance, created, **kwargs):
    if created:
        Principal_StudentFeesRecord.objects.create(
            student=instance.student,
            student_class=instance.student_class,
            term=instance.term,
            session=instance.session,
            this_term_fees=instance.this_term_fees,
            previous_term_balance=instance.previous_term_balance,
            paid_amount=instance.paid_amount,
            gender=instance.gender,
            starting_date=instance.starting_date,
            ending_date=instance.ending_date,
            created_by='staff'
        )
