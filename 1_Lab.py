import os
import sys
import time

# Включаем поддержку ANSI-кодов в консоли
os.system("")

# Коды для изменения цвета фона в консоли
ESC = "\033["
RESET = ESC + "0m"
RED = ESC + "41m"
WHITE = ESC + "47m"
BLUE = ESC + "44m"
BLACK = ESC + "40m"

CLEAR = "cls"

os.system(CLEAR)
print("1. Флаг Таиланда\n")
# Список цветов полос флага
flag = [RED, WHITE, BLUE, BLUE, WHITE, RED]
# Выводим каждую полосу нужным цветом
for color in flag:
    print(color + " " * 36 + RESET)
input("\nEnter - дальше")

motif = [
    "      ##      ",
    "     #  #     ",
    "   ##    ##   ",
    "###        ###",
    "              ",
]
# Повторяем узор 3 раза по вертикали
for i in range(3):
    for line in motif:
        result = ""
        # Повторяем строку 3 раза по горизонтали
        for ch in line * 3:
            if ch == "#":
                result += BLACK + "  "
            else:
                result += WHITE + "  "
        print(result + RESET)
input("Enter - дальше")

# Создаём 4 кадра анимации
for frame in range(4):
    os.system("cls")
    # Выводим полосы флага со смещением вправо
    for color in flag:
        print("\033[" + str(frame * 10 + 1) + "C" + color + " " * 20 + RESET)
    time.sleep(0.5)
input("Enter - дальше")

os.system("cls")
numbers = open("sequence.txt").read().split()

more = 0
less = 0
for n in numbers:
    n = float(n)
    if n > 5:
        more += 1
    elif 0 <= n < 5:
        less += 1

p_more = round(more / (more + less) * 100)
p_less = 100 - p_more

print("Больше 5:", RED + " " * (p_more // 2) + RESET, p_more, "%")
print("Меньше 5:", BLUE + " " * (p_less // 2) + RESET, p_less, "%")
input("Enter - дальше")