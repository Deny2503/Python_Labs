from itertools import combinations

# (обозначение, название, размер, очки выживания)
ITEMS = [
    ("r", "Винтовка", 3, 25),
    ("p", "Пистолет", 2, 15),
    ("a", "Боекомплект", 2, 15),
    ("m", "Аптечка", 2, 20),
    ("i", "Ингалятор", 1, 5),
    ("k", "Нож", 1, 15),
    ("x", "Топор", 3, 20),
    ("t", "Оберег", 1, 25),
    ("f", "Фляжка", 1, 15),
    ("d", "Антидот", 1, 10),
    ("s", "Еда", 2, 20),
    ("c", "Арбалет", 2, 20),
]

ROWS, COLS = 3, 3
REQUIRED = "d"
START_POINTS = 15

TOTAL_VALUE = sum(v for _, _, _, v in ITEMS)


def score(taken):
    # Итоговые очки: старт + взятые предметы - не взятые предметы
    taken_value = sum(v for _, _, _, v in taken)
    return START_POINTS + taken_value - (TOTAL_VALUE - taken_value)


def knapsack(items, capacity, required=None):
    chosen = []
    if required:
        req = next(it for it in items if it[0] == required)
        if req[2] > capacity:
            return None
        chosen.append(req)
        capacity -= req[2]
        items = [it for it in items if it[0] != required]

    n = len(items)
    # dp[i][w] — максимальная ценность из первых i предметов при вместимости w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        _, _, size, value = items[i - 1]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if size <= w and dp[i - 1][w - size] + value > dp[i][w]:
                dp[i][w] = dp[i - 1][w - size] + value

    # Восстановление набора предметов
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            chosen.append(items[i - 1])
            w -= items[i - 1][2]
    return chosen


def build_inventory(taken, rows, cols):
    # Раскладываем предметы по сетке построчно: одна ячейка — одно обозначение
    # Крупные предметы первыми, чтобы раскладка была аккуратнее
    cells = []
    for code, _, size, _ in sorted(taken, key=lambda it: -it[2]):
        cells.extend([code] * size)
    cells += ["-"] * (rows * cols - len(cells))  # пустые ячейки, если остались
    return [cells[r * cols:(r + 1) * cols] for r in range(rows)]


def print_inventory(grid):
    for row in grid:
        print(",".join(f"[{c}]" for c in row))


def all_positive_combinations(capacity, required=None):
    # Перебор всех подмножеств: подходят по месту, содержат обязательный предмет и дают счёт > 0
    result = []
    for k in range(1, len(ITEMS) + 1):
        for combo in combinations(ITEMS, k):
            if sum(it[2] for it in combo) > capacity:
                continue
            if required and required not in (it[0] for it in combo):
                continue
            s = score(combo)
            if s > 0:
                result.append((combo, s))
    result.sort(key=lambda x: -x[1])
    return result


def main():
    capacity = ROWS * COLS
    print(f"Вариант 6: инвентарь {ROWS}x{COLS}, паранойя (нужен антидот), стартовые очки {START_POINTS}\n")

    # Основное задание
    taken = knapsack(ITEMS, capacity, REQUIRED)
    print("Оптимальный набор:")
    print_inventory(build_inventory(taken, ROWS, COLS))
    final = score(taken)
    print(f"\nИтоговые очки выживания: {final}")
    print("Счёт положительный — Том дойдёт!" if final > 0 else "Счёт не положительный — решения нет.")

    # Доп. задание 1: инвентарь на 7 ячеек
    print("\n" + "=" * 50)
    print("Допзадание 1: инвентарь на 7 ячеек")
    taken7 = knapsack(ITEMS, 7, REQUIRED)
    best7 = score(taken7)
    names7 = ", ".join(f"{it[1]} ({it[0]})" for it in taken7)
    print(f"Лучший возможный набор: {names7}")
    print(f"Максимально достижимый счёт: {best7}")
    if best7 > 0:
        print("Решение существует:")
        print_inventory(build_inventory(taken7, 1, 7))
    else:
        print("Решения нет: даже оптимальный (по ДП) набор даёт счёт <= 0,")
        print("значит любой другой набор на 7 ячеек даст не больше, т.е. тоже <= 0.")

    # Доп. задание 2: все комбинации с положительным счётом
    print("\n" + "=" * 50)
    print(f"Допзадание 2: все комбинации для {ROWS}x{COLS} с положительным счётом")
    combos = all_positive_combinations(capacity, REQUIRED)
    for combo, s in combos:
        codes = " ".join(it[0] for it in combo)
        used = sum(it[2] for it in combo)
        print(f"  {codes:<20} ячеек: {used}  очки: {s}")
    print(f"Всего комбинаций: {len(combos)}")


if __name__ == "__main__":
    main()