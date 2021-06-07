from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from syndromes.forms import EmailForm
from syndromes.models import Registar
from syndromes.notify import notify_by_email, too_many_notifications


@csrf_exempt
def request_dept_by_email(request):
    valid = True
    if request.method == 'POST':
        form = EmailForm(request.POST)
        valid = form.is_valid()
        if valid:
            email = form.cleaned_data.get('email')
            return dept_by_email(request, email)
    else:
        form = EmailForm()

    return render(request, 'mydept.html', {'form': form, 'valid': valid})


def dept_by_email(request, email):
    try:
        member = Registar.get_by_email(email)
    except Registar.DoesNotExist:
        return HttpResponse(
            content=render(request, 'noemail.html', {'email': email}),
            content_type='text/html; charset=utf-8',
            status=404)
    else:
        if too_many_notifications(email):
            return render(request, 'toomanyemails.html', {'email': email})
        try:
            notify_by_email(member.registar_id)
        except Exception as e:
            print(e)
            return HttpResponse(
                content=render(request, '500.html'),
                content_type='text/html; charset=utf-8',
                status=500)
        return render(request, 'emailsent.html', {'email': email})
