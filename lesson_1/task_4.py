"""
Преобразовать слова «разработка», «администрирование»,
«protocol», «standard» из строкового представления в байтовое и выполнить обратное преобразование
(используя методы encode и decode).
"""

words = ['разработка', 'администрирование', 'protocol', 'standard']

for i, word in enumerate(words):
    b_word = word.encode('utf-8')
    print(f'Слово №{i + 1} в байтов представлении: {b_word}')
    new_word = b_word.decode('utf-8')
    print(f'Слово №{i + 1} в строковом представлении: {new_word}\n')
