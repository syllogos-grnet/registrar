from django.core import mail
from django.utils import timezone

from syllogos.settings import (EMAIL_FROM, EMAILS_LIMIT, NOTIFY_MESSAGE,
                               NOTIFY_SUBJECT, RESET_EMAILS_LIMIT_AFTER)
from syndromes.models import NotificationLog, Registar


def notify_by_email(registar_id):
    person = Registar.objects.get(registar_id=registar_id)
    kw = {
        'subject': NOTIFY_SUBJECT,
        'body': NOTIFY_MESSAGE.format(
            name=person.name, dept=person.dept, from_email=EMAIL_FROM),
        'from_email': EMAIL_FROM,
        'to': [person.email, ]
    }
    with mail.get_connection() as connection:
        kw['connection'] = connection
        email_msg = mail.EmailMessage(**kw)
        email_msg.send(fail_silently=False)

    try:
        return NotificationLog.objects.create(
            registar=person, email=person.email, description='email')
    except Exception:
        pass


def too_many_notifications(email):
    start_date = timezone.now() - timezone.timedelta(
        seconds=RESET_EMAILS_LIMIT_AFTER)
    old_notifications = NotificationLog.objects.filter(
        email=email, description='email', timestamp__gte=start_date)
    return len(old_notifications) >= EMAILS_LIMIT
