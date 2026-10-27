import csv
import random
import xml.etree.ElementTree as ET

# Чтение файла
books = []
with open('books.csv', encoding='cp1251') as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        books.append(row)

# Проверка на длину
count = 0
for book in books:
    if len(book['Название']) > 30:
        count += 1
print('Записей с названием длиннее 30 символов:', count)

# Поиск книги по автору и от 150 р
author = input('\nВведите автора: ').strip().lower()
found = False
for book in books:
    price = float(book['Цена поступления'].replace(',', '.'))
    if author in book['Автор'].lower() and price >= 150:
        print(book['Название'], '-', book['Автор'], '-', price, 'руб.')
        found = True
if not found:
    print('Книги не найдены')

# Генератор библиографических ссылок
random_books = random.sample(books, 20)
with open('bibliography.txt', 'w', encoding='utf-8') as f:
    for i, book in enumerate(random_books, 1):
        year = book['Дата поступления'].split()[0].split('.')[2]
        f.write(f"{i}. {book['Автор']}. {book['Название']} - {year}\n")
print('\nСписок ссылок сохранён в bibliography.txt')

with open('currency.xml', 'rb') as f:
    data = f.read()
try:
    text = data.decode('utf-8')
except UnicodeDecodeError:
    text = data.decode('cp1251')
text = text[text.find('?>') + 2:]
root = ET.fromstring(text)
values = []
for valute in root.findall('Valute'):
    value = float(valute.find('Value').text.replace(',', '.'))
    values.append(value)
print('\nСредний показатель Value:', round(sum(values) / len(values), 4))

# Перечень тегов без повторений
tags = set()
for book in books:
    for tag in book['Жанр книги'].split('#'):
        tag = tag.strip()
        if tag:
            tags.add(tag)
print('\nВсе теги:')
for tag in sorted(tags):
    print(tag)

# Самые популярные 20 книг
# Одна книга может быть в нескольких экземплярах, поэтому суммируем выдачи
popularity = {}
for book in books:
    key = (book['Название'], book['Автор'])
    popularity[key] = popularity.get(key, 0) + int(book['Кол-во выдач'])

top = sorted(popularity.items(), key=lambda item: item[1], reverse=True)[:20]
print('\nСамые популярные 20 книг:')
for i, ((title, author), count) in enumerate(top, 1):
    print(f"{i}. {title} - {author} ({count} выдач)")
