import os
from datetime import datetime

import pandas


def save_to_csv(data: dict, file_path: str = "test.csv") -> None:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Переименовываем столбец 'station_status' во временную метку
    data[timestamp] = data['station_status']
    del data['station_status']

    if os.path.exists(file_path):
        _add_data_to_file(data, file_path, timestamp)
    else:
        _create_new_file(data, file_path)


def _add_data_to_file(data: dict, file_path: str, timestamp: str):
    new_data_df = pandas.DataFrame(data)
    old_data_df = pandas.read_csv(file_path)

    for index, new_row in new_data_df.iterrows():
        # Поиск строки в существующем DataFrame, где значения 'old_data_df' совпадают
        # с соответствующими значениями из текущей новой строки.
        existing_row = old_data_df[(old_data_df['station_number'] == new_row['station_number'])
                                   & (old_data_df['station_address'] == new_row['station_address'])
                                   & (old_data_df['station_name'] == new_row['station_name'])
                                   & (old_data_df['station_type'] == new_row['station_type'])]

        if not existing_row.empty:
            old_data_df.at[existing_row.index[0], timestamp] = new_row[timestamp]
        else:
            # Если объекта нет в существующих данных, добавляем новую строку
            new_row_df = pandas.DataFrame([new_row], columns=new_data_df.columns)
            old_data_df = pandas.concat([old_data_df, new_row_df], ignore_index=True)

    old_data_df.to_csv(file_path, index=False, encoding='utf-8')


def _create_new_file(data: dict, file_path: str):
    df = pandas.DataFrame(data)
    df.to_csv(file_path, index=False, encoding='utf-8')
