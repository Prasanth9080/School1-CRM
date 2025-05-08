from apps.students.models import StaffNotification

def unread_notifications_count(request):
    if request.user.is_authenticated:
        count = StaffNotification.objects.filter(is_read=False).count()
        return {'unread_count': count}
    return {}
