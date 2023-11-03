import sys
import os
import csv
import argparse
from collections import Generator
import logging

import django
# sys.path.append("/path/to/store") #here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "syllogos.settings")
django.setup()

from syndromes.load import (
    xlsx_to_records, only_active, get_date, calculate_dept
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stdout_handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(message)s')
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)


def export_can_vote(xlsx_file_path: str) -> Generator:
    writer = csv.writer(sys.stdout, delimiter=",")
    for record in xlsx_to_records(xlsx_file_path, only_active):
        try:
            registar_id = int(record['Α/Α'])
            subscription_date = get_date(record['Εγγραφή'])
            first_name = record.get('Όνομα', '-')
            last_name = record.get('Επίθετο', '-')
            email = (record['PR'] or "").strip()
            dept = calculate_dept(record, subscription_date, accept_partial_payment_for_last_installment=True)
            if dept > 0.0:
                logger.info(f'{registar_id}. {last_name} not allowed to vote')
                continue
            else:
                logger.info(f'{registar_id}. {last_name} can vote')
            row = (registar_id, email, first_name, last_name)
            writer.writerow(row)
        except Exception as e:
            logger.info(f"ERROR: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export members who can vote")
    parser.add_argument('xlsx_file', type=str)
    args = parser.parse_args()
    xlsx_file = args.xlsx_file
    export_can_vote(xlsx_file)
