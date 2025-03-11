from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from celery import shared_task

@shared_task
def send_reminder():
    from .models import KeyLog
    overdue_logs = KeyLog.objects.filter(return_status=False, checkout_time__date=now().date())

    for log in overdue_logs:
        staff_email = log.staff.email
        staff_name = log.staff.name
        key_name = log.key.key_name

        subject = "🔑 Key Return Reminder"
        message = f"Hello {staff_name},\n\nYou have not returned the key '{key_name}' that you took today.\nPlease return it as soon as possible.\n\nThank you!"
        from_email = "your_email@gmail.com"
        
        send_mail(subject, message, from_email, [staff_email])
