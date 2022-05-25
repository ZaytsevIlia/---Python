"""
Определить, какие из слов «attribute», «класс», «функция»,
«type» невозможно записать в байтовом типе. Важно: решение должно быть универсальным,
т.е. не зависеть от того, какие конкретно слова мы исследуем.
"""

words = ['attribute', 'класс', 'функция', 'type']

for word in words:
    try:
        new_word = word.encode('ascii')
        print(new_word)
    except UnicodeEncodeError:
        print(f'Слово: \'{word}\' невозможно записать в байтовом типе')
