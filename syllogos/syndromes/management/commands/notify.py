from django.core.management.base import BaseCommand, CommandError

from syndromes.models import Registar


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--registar-id', type=str, help='Member registar id')
        parser.add_argument('--email', type=str, help='Member email address')
        parser.add_argument('--all', type=str, help='Notify all members')

    def _get_opts(self, opts):
        return opts.get('registar_id'), opts.get('email'), opts.get('all')

    def handle(self, *args, **opts):
        registar_id, email, all_ = self._get_opts(opts)
        print(registar_id, email, all_)
