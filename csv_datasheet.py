import pandas as pd
import os
import json
from pathlib import Path
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# Путь к директории с исходными CSV файлами
input_directory = 'exclandcsv/mosfets'
save_path = str(Path(__file__).parent.resolve())

def process_csv_file(input_csv_path):
    # Чтение CSV файла
    df = pd.read_csv(input_csv_path, delimiter=';')

    # Проверка наличия первого столбца
    first_column = df.columns[0]  # Получаем имя первого столбца

    # Словарь для хранения информации о каждой серии в текущем CSV файле
    file_info_local = {}

    # Создание файлов CSV в соответствующих директориях
    for series in df[first_column].unique():
        # Фильтрация данных для текущей серии
        series_data = df[df[first_column] == series]

        # Получение пути к директории из столбца "Datasheet part"
        datasheet_path = series_data['Datasheet part'].iloc[0]
        directory_path = os.path.join(save_path, "Datasheet", input_directory.split("/")[1], series)

        # Путь для сохранения файла CSV
        output_csv_path = os.path.join(directory_path, f'{series}.csv')

        # Проверка, существует ли директория
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Created directory for series {series}")

        # Сохранение данных в CSV файл
        series_data.to_csv(output_csv_path, index=False, sep=';')

        # Формирование путей для PDF и изображения
        pdf_path = f"/Datasheet/{input_directory.split('/')[1]}/{series}.pdf"
        img_path = series_data['Image path'].iloc[0]
        if type(img_path) is np.int64:
            img_path = None

        # Добавление информации в локальную JSON структуру для текущего CSV файла
        file_info_local = {
            series+".csv":{
                "pdf": pdf_path,
                "img": img_path
            }
        }
        print(img_path)

        # Путь для сохранения локального JSON файла рядом с текущим CSV файлом
        json_local_output_path = os.path.splitext(output_csv_path)[0] + '.json'

        # Запись локального JSON файла
        with open(json_local_output_path, 'w') as json_file:
            json.dump(file_info_local, json_file, indent=4)

# Использование многопоточности для обработки CSV файлов
with ThreadPoolExecutor() as executor:
    futures = []
    for input_csv_path in Path(input_directory).glob('*.csv'):
        futures.append(executor.submit(process_csv_file, input_csv_path))

    # Ожидание завершения всех задач
    for future in futures:
        future.result()

print("Файлы CSV и JSON созданы для каждой серии.")
