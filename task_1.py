# Код взят из домашнего задания из 9-го семинара "Декораторы"
# Функции generate_csv_file и save_to_json для генерации csv файла и сохранения результата в json файла убрал для
# лаконичности решения конкретной задачи. Задание и решение закомментировано и свернуто ниже (Ctr -/+).

"""
Задание:
Создайте функцию generate_csv_file(file_name, rows), которая будет генерировать по три случайны числа в каждой строке,
от 100-1000 строк, и записывать их в CSV-файл. Функция принимает два аргумента:

file_name (строка) - имя файла, в который будут записаны данные.
rows(целое число) - количество строк (записей) данных, которые нужно сгенерировать.

Создайте функцию find_roots(a, b, c), которая будет находить корни квадратного уравнения вида ax^2 + bx + c = 0.
Функция принимает три аргумента: a, b, c (целые числа) - коэффициенты квадратного уравнения.

Функция возвращает:
None, если уравнение не имеет корней (дискриминант отрицателен).
Одно число, если уравнение имеет один корень (дискриминант равен нулю).
Два числа (корни), если уравнение имеет два корня (дискриминант положителен).

Создайте декоратор save_to_json(func), который будет оборачивать функцию find_roots. Декоратор выполняет следующие
действия:
Читает данные из CSV-файла, переданного в аргументе функции, исходя из аргумента args[0].
Для каждой строки данных вычисляет корни квадратного уравнения с помощью функции find_roots.
Сохраняет результаты в формате JSON в файл results.json. Каждая запись JSON содержит параметры a, b, c и результаты
вычислений.
Таким образом, после выполнения функций generate_csv_file и find_roots в файле results.json будет сохранена информация
 о параметрах и результатах вычислений для каждой строки данных из CSV-файла.

Решение:

import csv
import json
from random import randint


def save_to_json(func):

    def wrapper(*args):
        res_json = []
        with open(args[0], 'r', encoding='utf-8') as f:
            read = csv.reader(f)
            for nums in read:
                a, b, c = map(int, nums)
                res = func(a, b, c)
                data = {'parameters': [a, b, c], 'result': res}
                res_json.append(data)
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(res_json, f)

    return wrapper


@save_to_json
def find_roots(a, b, c):
    d = b ** 2 - 4 * a * c
    if d < 0:
        return None
    elif d == 0:
        return -b / (2 * a)
    else:
        x_1 = (-b + d ** 0.5) / (2 * a)
        x_2 = (-b - d ** 0.5) / (2 * a)
        return x_1, x_2


def generate_csv_file(file_name, rows):
    with open(file_name, 'w', newline='', encoding='utf-8') as f:
        csv_write = csv.writer(f)
        for _ in range(rows):
            data = [randint(1, 1000) for _ in range(3)]
            csv_write.writerow(data)


generate_csv_file("input_data.csv", 101)
find_roots("input_data.csv")
"""

# РЕШЕНИЕ АТТЕСТАЦИОННОЙ ЗАДАЧИ

import logging
import argparse
from typing import Callable

logging.basicConfig(filename="log_py.log", filemode="a", level=logging.INFO)


def save_to_json(func: Callable) -> Callable:
    def wrapper(*args):
        res = func(*args)
        return res

    return wrapper


@save_to_json
def find_roots(a: int, b: int, c: int) -> str:
    try:
        a, b, c = int(a), int(b), int(c)
    except ValueError as e:
        logging.error(f'Значения a, b, c должны быть числом. Ошибка {e}')  # Логируем ошибку если она есть
        return f'Значения a, b, c должны быть числом. Ошибка {e}'

    d = b ** 2 - 4 * a * c
    if d < 0:
        res = f'Действительных корней нет при: {a = }, {b = }, {c = }'
    elif d == 0:
        res = f'Уравнение имеет один корень: {-b / (2 * a)}'
    else:
        x_1 = (-b + d ** 0.5) / (2 * a)
        x_2 = (-b - d ** 0.5) / (2 * a)
        res = f'Уравнение имеет два корня: {x_1}, {x_2}'
    logging.info(res)  # Логируем результат работы функции
    return res


def parse():
    parser = argparse.ArgumentParser(
        description='Находим корни квадратного уравнения',
        epilog='При вводе значения в виде строки получаем ошибку',
        prog='find_roots()')
    parser.add_argument('-a', '--a', default=1, help='Введите число a: ')
    parser.add_argument('-b', '--b', default=2, help='Введите число b: ')
    parser.add_argument('-c', '--c', default=1, help='Введите число c: ')
    args = parser.parse_args()
    return find_roots(args.a, args.b, args.c)


if __name__ == '__main__':
    print(find_roots(4, 10, 5))
    print(parse())
