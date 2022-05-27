"""
Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов
info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными,
их открытие и считывание данных. В этой функции из считанных данных необходимо с помощью регулярных выражений
извлечь значения параметров «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно получиться четыре списка —
например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него названия столбцов отчета в виде списка:
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих столбцов также оформить
в виде списка и поместить в файл main_data (также для каждого файла);
Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение
данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().
"""

import csv
from chardet import detect
import os
import re


def get_data():
    os_prod_list = []  # Изготовитель системы
    os_name_list = []  # Название ОС
    os_code_list = []  # Код продукта
    os_type_list = []  # Тип системы

    file_list = os.listdir()
    for file in file_list:
        if file[-3:] == 'txt':
            with open(file, 'rb') as f:
                content = f.read()
            encoding = detect(content)['encoding']

            with open(file, encoding=encoding) as f:
                data = f.read()
                os_prod_reg = re.compile(r'Изготовитель системы:\s*\S*')
                os_prod_list.append(os_prod_reg.findall(data)[0].split()[2])

                os_name_reg = re.compile(r'Название ОС:.*')  # Microsoft Windows 7 Профессиональная
                result_name = os_name_reg.findall(data)[0].split(':')[1]
                os_name_reg_2 = re.compile(r'\S+\s\S+\s\d*\.?\d?\s\S*')
                os_name_list.append(os_name_reg_2.findall(result_name)[0])

                os_code_reg = re.compile(r'Код продукта:\s*\S*')
                os_code_list.append(os_code_reg.findall(data)[0].split()[2])

                os_type_reg = re.compile(r'Тип системы:.*')  # x64-based PC
                result_type = os_type_reg.findall(data)[0].split(':')[1]
                os_type_reg_2 = re.compile(r'\S+\d+\S+\s\S+')
                os_type_list.append(os_type_reg_2.findall(result_type)[0])

    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']

    data_for_csv = [
        os_prod_list,
        os_name_list,
        os_code_list,
        os_type_list,
    ]

    correct_data_for_csv = []
    correct_data_for_csv.append(headers)

    for i in range(len(data_for_csv[0])):
        line = [var[i] for var in data_for_csv]
        correct_data_for_csv.append(line)

    return correct_data_for_csv


def write_to_csv(file):
    with open(f'{file}.csv', 'w', encoding='utf-8') as f:
        F_WRITER = csv.writer(f)
        for row in get_data():
            F_WRITER.writerow(row)


write_to_csv('result')
