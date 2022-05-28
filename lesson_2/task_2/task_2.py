"""
Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров —
товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date).
Функция должна предусматривать запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""

import json


def write_order_to_json(item, quantity, price, buyer, date):
    dict_to_json = {
        'Товар': item,
        'Количество': quantity,
        'Цена': price,
        'Покупатель': buyer,
        'Дата': date,
    }
    with open('orders.json', encoding='utf-8') as f:
        data = json.load(f)

    with open('orders.json', 'w', encoding='utf-8') as f_n:
        data['orders'].append(dict_to_json)
        json.dump(data, f_n, indent=4, ensure_ascii=False)


write_order_to_json('Телевизор', '2', '5500', 'Иванов Иван', '21.04.2022')
write_order_to_json('PlayStation', '1', '55300', 'Max', '11.04.2022')
write_order_to_json('Стол', '1', '1000', 'Петров В.А.', '01.04.2022')
write_order_to_json('Диван', '2', '25500', 'Смирнов', '30.04.2022')
