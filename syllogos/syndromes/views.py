from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from syndromes.forms import EmailForm
from syndromes.models import Registar
from syndromes.notify import notify_by_email


@csrf_exempt
def request_dept_by_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            email = form.cleaned_data.get('email')
            return dept_by_email(request, email)
    else:
        form = EmailForm()

    return render(request, 'mydept.html', {'form': form})


def dept_by_email(request, email):
    try:
        member = Registar.get_by_email(email)
    except Registar.DoesNotExist:
        return render(request, 'noemail.html', {'email': email})
    else:
        notify_by_email(member.registar_id)
        return render(request, 'emailsent.html', {'email': email})
