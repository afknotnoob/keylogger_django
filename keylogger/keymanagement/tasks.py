from django.core.mail import send_mail
from django.utils.timezone import now
from celery import shared_task
from django.conf import settings
from .models import KeyLog

@shared_task
def send_key_return_reminders():
    overdue_logs = KeyLog.objects.filter(return_status=False, checkout_time__date=now().date())

    for log in overdue_logs:
        staff = log.staff
        subject = "Reminder: Key Not Returned"
        message = f"Dear {staff.name},\n\nYou have not returned the key '{log.key.key_name}'. Please return it as soon as possible.\n\nThank you."
        send_mail(subject, message, settings.EMAIL_HOST_USER, [staff.email])

    return f"Sent {len(overdue_logs)} email reminders"
