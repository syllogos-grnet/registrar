import json
from collections import Generator
from logging import getLogger

import pandas
from dateutil.parser import isoparse
from django.utils.timezone import datetime
from pytz import utc

from syndromes.models import BIG_BANG, Registar

logger = getLogger(__name__)


def xlsx_to_records(input_file_path: str, filter_func=None) -> list:
    data_frame = pandas.read_excel(input_file_path)
    data_str = data_frame.to_json(orient='records', date_format='iso')
    for record in json.loads(data_str):
        if filter_func and not filter_func(record):
            continue
        yield record


def only_active(record: list) -> bool:
    return record.get('Κατάσταση') in ['ΕΝΕΡΓΟ', 'ΕΝΕΡΓΟ-ΑΠΟΧΩΡΗΣΗ']


def calculate_dept(record, subscription_date, accept_partial_payment_for_last_installment=False):
    dept = 10.0 - float(record.get('Εγγραφή.1', 0))
    installments = [k for k in record if 'Δόση' in k]
    installment_date, installment_dept = dict(), dict()
    for i in installments:
        year = i[-4:]
        month = '01' if i[0] == '1' else '07'
        date_str = f'01/{month}/{year}EET'
        installment_date[i] = datetime.strptime(date_str, '%d/%m/%Y%Z')
        installment_dept[i] = 10.0 if int(year) < 2018 else 5.0
    calc_min_partial_payment = lambda installment, year: installment - (4.0 if year < 2018 else 3.0) # assume 3-4 EUR max charge
    for i in installments:
        tzinfo = installment_date[i].tzinfo
        now = datetime.now(tzinfo)
        if utc.localize(installment_date[i]) > subscription_date and installment_date[i] < now:
            payed = float(record.get(i, 0) or 0)
            if calc_min_partial_payment(installment_dept[i], installment_date[i].year) <= payed < installment_dept[i] and accept_partial_payment_for_last_installment and (
                installment_date[i] == datetime(now.year, 1 if now.month < 7 else 7, 1)):
                payed = installment_dept[i]
            dept += installment_dept[i] - payed
    return dept


def get_date(date_record):
    if date_record:
        return isoparse(date_record)
    return utc.localize(BIG_BANG)


def load_registar(xlsx_file_path: str) -> Generator:
    for record in xlsx_to_records(xlsx_file_path, only_active):
        try:
            registar_id = int(record['Α/Α'])
            subscription_date = get_date(record['Εγγραφή'])
            name = ' '.join(
                [record.get('Όνομα', '-'), record.get('Επίθετο', '-')])
            email = (record['PR'] or "").strip()
            dept = calculate_dept(record, subscription_date)
            logger.info(f'{registar_id}. {name}')
            yield Registar.objects.get_or_create(
                registar_id=registar_id,
                subscription_date=subscription_date,
                name=name,
                email=email,
                dept=dept
            )

        except Exception as e:
            yield e, False


def reload_registar(xlsx_file_path: str) -> Generator:
    Registar.objects.all().delete()
    return load_registar(xlsx_file_path)
