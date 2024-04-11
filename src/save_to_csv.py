import pandas


def save_new_file(data: dict):
    df = pandas.DataFrame(data)
    df.to_csv('test.csv', index=False, encoding='utf-8')


def add_data_to_file(data: dict):
    df = pandas.read_csv('test.csv')
    for column_name, value in data.items():
        df[column_name] = value
    df.to_csv('test.csv', index=False, encoding='utf-8')
