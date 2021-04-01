from django.core import mail

from syndromes.models import Registar

from syllogos.settings import NOTIFY_SUBJECT, NOTIFY_MESSAGE, EMAIL_FROM


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

