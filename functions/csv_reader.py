import csv



def get_column_values(file_path, column_name):
    values = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            value = row.get(column_name)
            if value not in (None, '', 'null', 'NULL'):
                values.append(value)

    return values
