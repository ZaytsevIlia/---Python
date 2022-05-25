"""
Каждое из слов «class», «function», «method» записать в байтовом типе. Сделать это необходимо в автоматическом,
а не ручном режиме, с помощью добавления литеры b к текстовому значению,
(т.е. ни в коем случае не используя методы encode, decode или функцию bytes) и определить тип,
содержимое и длину соответствующих переменных.
"""

words = ['class', 'function', 'method']
b_words = []

for word in words:
    b_words.append(eval(f"b'{word}'"))

for word in b_words:
    print(f'{word}, тип переменной: {type(word)}, длина переменной: {len(word)}')
