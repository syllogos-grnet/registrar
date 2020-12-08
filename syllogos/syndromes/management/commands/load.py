import logging
import sys

from django.core.management.base import BaseCommand, CommandError

from syndromes.load import reload_registar

# Set logger from load to print to stdout
load_logger = logging.getLogger('syndromes.load')
load_logger.setLevel(logging.INFO)
stdout_handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(message)s')
stdout_handler.setFormatter(formatter)
load_logger.addHandler(stdout_handler)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'xlsm-path', type=str, help='Path of the registar file (.xlsm)')
        parser.add_argument(
            '--yes',
            action='store_true',
            help='Just do the think, do not bug me with questions',
        )

    def handle(self, *args, **opts):
        xlsm_path = opts.get('xlsm-path')
        if not (opts.get('yes')) and input(
                'Empty and reload the registar? (Y|n)') not in ('Y', ''):
            print('Maybe another time')
            return
        for entry, inserted in reload_registar(xlsm_path):
            if not inserted:
                print('\tERROR:', entry)
