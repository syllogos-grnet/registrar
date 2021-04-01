from django.core.management.base import BaseCommand, CommandError

from syndromes.models import Registar
from syndromes.notify import notify_by_email


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--registar-id', type=str, help='Member registar id')
        parser.add_argument('--email', type=str, help='Member email address')
        parser.add_argument(
            '--all', action='store_true', help='Notify all members')

    def _get_opts(self, opts):
        return opts.get('registar_id'), opts.get('email'), opts.get('all')

    def _notify_by_email(self, member):
        try:
            notify_by_email(member.registar_id)
        except Exception as e:
            print(f'Failed with {member} ', e)
        else:
            print(f'Notified {member}')

    def handle(self, *args, **opts):
        registar_id, email, all_ = self._get_opts(opts)
        if not (bool(registar_id) ^ bool(email) ^ bool(all_)):
            raise CommandError(
                'Use exactly one of --email, --registar-id, --all')
        elif all_:
            for member in Registar.objects.all():
                self._notify_by_email(member)
        else:
            if email:
                member = Registar.get_by_email(email)
            else:
                member = Registar.get_by_registar_id(registar_id)
            if member:
                self._notify_by_email(member)
            else:
                raise CommandError('Not in registar')
