import json

import pandas


def xlsx_to_records(input_file_path: str, filter_func=None) -> list:
    data_frame = pandas.read_excel(input_file_path)
    data_str = data_frame.to_json(orient='records')
    for record in json.loads(data_str):
        if filter_func and not filter_func(record):
            continue
        yield record


def only_active(record: list) -> bool:
    return record.get('Κατάσταση') in ['ΕΝΕΡΓΟ', 'ΕΝΕΡΓΟ-ΑΠΟΧΩΡΗΣΗ']


if __name__ == '__main__':
    input_file_path = input('Input file path: ')
    output = list(xlsx_to_records(input_file_path, only_active))
    print(json.dumps(output, indent=2, ensure_ascii=False))
