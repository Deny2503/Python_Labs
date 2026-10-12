import os
import time

def flag():
    print("\033[41m" + " " * 40 + "\033[0m")  # красный
    print("\033[47m" + " " * 40 + "\033[0m")  # белый

    print("\033[44m" + " " * 40 + "\033[0m")  # синий
    print("\033[44m" + " " * 40 + "\033[0m")  # синий

    print("\033[47m" + " " * 40 + "\033[0m")  # белый
    print("\033[41m" + " " * 40 + "\033[0m")  # красный




def animation():
    # Кадр 1
    os.system("cls")
    print("*")
    time.sleep(0.5)
    # Кадр 2
    os.system("cls")
    print("   *")
    time.sleep(0.5)
    # Кадр 3
    os.system("cls")
    print("      *")
    time.sleep(0.5)
    # Кадр 4
    os.system("cls")
    print("         *")
    time.sleep(0.5)



def diagram():
    file = open("sequence.txt", "r")
    text = file.read()
    file.close()
    text_numbers = text.split()
    numbers = []
    for number in text_numbers:
        numbers.append(float(number))
    more = 0
    less = 0
    for number in numbers:
        if number < 0:
            continue
        if number > 5:
            more = more + 1
        elif number < 5:
            less = less + 1
    total = more + less

    if total == 0:
        print("Подходящих чисел нет")
        return

    # Считаем проценты
    more_percent = more / total * 100
    less_percent = less / total * 100

    print("Чисел больше 5:", more)
    print("Чисел меньше 5:", less)

    print("Больше 5:", round(more_percent, 1), "%")
    print("Меньше 5:", round(less_percent, 1), "%")

    print()
    print("Диаграмма:")

    more_bar = int(more_percent / 5)
    less_bar = int(less_percent / 5)

    print("> 5:", "#" * more_bar)
    print("< 5:", "#" * less_bar)

print("Флаг Таиланда:")
flag()

print()

print("Узор:")


input("\nНажми Enter для запуска анимации")

animation()

os.system("cls")

print("Обработка sequence.txt:")
diagram()