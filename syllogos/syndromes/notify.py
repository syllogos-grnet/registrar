from django.core import mail

from syndromes.models import Registar

from_email = 'ds-syllogos@grnet.gr'
notify_message = """
Αγαπητό μέλος του συλλόγου,

έχετε εγγραφεί στο σύλλογο ως «{name}».
Σύμφωνα με τα αρχεία μας, οφείλετε {dept:.2f} ευρώ.

Μπορείτε να εξοφλήσετε το χρέος σας με κατάθεση στον τραπεζικό λογαριασμό του
συλλόγου και να ενημερώσετε άμεσα με email το ΔΣ του Συλλόγου
( {from_email} )

Ο λογαριασμός του Συλλόγου
---
Εθνική Τράπεζα της Ελλάδας
IBAN: GR4401107210000072110088977
ΣΥΛΛΟΓΟΣ ΕΡΓΑΖΟΜΕΝΩΝ ΚΑΙ ΣΥΝΕΡΓΑΤΩΝ ΕΔΥΤΕ

Σε περίπτωση κατάθεσης με κόστος συναλλαγής (π.χ. από διαφορετική τράπεζα), θα
πρέπει να επωμισθείτε τις σχετικές τραπεζικές χρεώσεις, διαφορετικά το κόστος
αυτό θα προστεθεί ως χρέος σας προς το σύλλογο.

Αν πιστεύετε ότι έχει γίνει κάποιο λάθος, επικοινωνήστε με το ΔΣ του Συλλόγου
ώστε να βρεθεί το πρόβλημα.

Αυτό το email αποστέλεται αυτόματα με script,
υπ' ευθύνη του ΔΣ του Συλλόγου Εργαζομένων και Συνεργατών ΕΔΥΤΕ
"""


def notify_by_email(registar_id):
    person = Registar.objects.get(registar_id=registar_id)
    kw = {
        'subject': '[Σύλλογος Ε&Σ ΕΔΥΤΕ] Ενημέρωση συνδρομών',
        'message': notify_message.format(
            name=person.name, dept=person.dept, from_email=from_email),
        'from_email': from_email,
        'recipient_list': [person.email, ]
    }
    with mail.get_connection() as connection:
        kw['connection'] = connection
        email_msg = mail.EmailMessage(**kw)
        email_msg.send(fail_silently=False)
