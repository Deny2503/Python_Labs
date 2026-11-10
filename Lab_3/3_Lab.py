import tkinter as tk
import random
import wave
import winsound
import io
import threading

symbols = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


# вес одного символа
def get_weight(s):
    if s.isdigit():
        return int(s)
    else:
        return ord(s) - 64  # ord("A") = 65, значит A будет 1


# среднее значение блока
def get_average(block):
    summa = 0
    for s in block:
        summa = summa + get_weight(s)
    return summa / len(block)


# просто случайные символы
def random_block(length):
    block = ""
    for i in range(length):
        block = block + random.choice(symbols)
    return block


# генерируем блоки пока среднее не попадет от 10 до 15
def good_block(length):
    block = random_block(length)
    while get_average(block) < 10 or get_average(block) > 15:
        block = random_block(length)
    return block


def make_key():
    return good_block(5) + "-" + good_block(4) + "-" + good_block(4)


# ---------------- музыка ----------------

def make_music():
    rate = 22050
    note_time = int(rate * 0.5)  # одна нота 0.5 сек, медленно и спокойно

    # частоты нот (0 - пауза)
    notes = [262, 392, 330, 392, 523, 0, 494, 392,
             220, 330, 262, 330, 440, 0, 392, 330,
             175, 262, 220, 262, 349, 0, 330, 262,
             196, 294, 247, 294, 392, 0, 0, 0]

    sound = bytearray()
    for freq in notes:
        for i in range(note_time):
            if freq == 0:
                sound.append(128)
            else:
                # громкость плавно уменьшается к концу ноты
                volume = int(25 * (1 - i / note_time))
                period = rate / freq
                if i % period < period / 2:
                    sound.append(128 + volume)
                else:
                    sound.append(128 - volume)

    memory = io.BytesIO()
    f = wave.open(memory, "wb")
    f.setnchannels(1)
    f.setsampwidth(1)
    f.setframerate(rate)
    f.writeframes(sound)
    f.close()
    return memory.getvalue()


music = make_music()


# играем мелодию по кругу
def play_forever():
    while True:
        winsound.PlaySound(music, winsound.SND_MEMORY)

threading.Thread(target=play_forever, daemon=True).start()


# ---------------- окно ----------------

window = tk.Tk()
window.title("Keygen")
window.resizable(False, False)

canvas = tk.Canvas(window, width=440, height=827)
canvas.pack()

# картинка на фон
picture = tk.PhotoImage(file="image.png")
canvas.create_image(0, 0, image=picture, anchor="nw")

# надпись
canvas.create_text(222, 47, text="MINECRAFT", font=("Courier New", 26, "bold"), fill="black")
title = canvas.create_text(220, 45, text="MINECRAFT", font=("Courier New", 26, "bold"), fill="lime")

# темный прямоугольник под кнопками
canvas.create_rectangle(20, 300, 420, 560, fill="black", stipple="gray75", outline="lime", width=3)

key_label = canvas.create_text(220, 340, text="?????-????-????", font=("Courier New", 24, "bold"), fill="orange")
info_label = canvas.create_text(220, 375, text="Нажми GENERATE", font=("Courier New", 11, "bold"), fill="white")

# поле для ключа
entry = tk.Entry(window, font=("Courier New", 15, "bold"), width=18, justify="center")
canvas.create_window(220, 420, window=entry)


# ---------------- кнопка ----------------

# сначала крутим случайные символы, потом показываем ключ
def spin(count, key):
    if count > 0:
        fake = random_block(5) + "-" + random_block(4) + "-" + random_block(4)
        canvas.itemconfig(key_label, text=fake, fill="orange")
        window.after(50, spin, count - 1, key)
    else:
        canvas.itemconfig(key_label, text=key, fill="lime")

        parts = key.split("-")
        text = "Средние: " + str(get_average(parts[0])) + " - " + str(get_average(parts[1])) + " - " + str(get_average(parts[2]))
        canvas.itemconfig(info_label, text=text)

        entry.delete(0, tk.END)
        entry.insert(0, key)
        button.config(state="normal")


def click():
    button.config(state="disabled")
    key = make_key()
    spin(20, key)


button = tk.Button(window, text="GENERATE", font=("Courier New", 13, "bold"),
                   bg="saddlebrown", fg="lime", width=14, command=click)
canvas.create_window(220, 490, window=button)


# ---------------- анимация ----------------

# искры из лавы
sparks = []
for i in range(40):
    x = random.randint(0, 440)
    y = random.randint(600, 827)
    color = random.choice(["yellow", "orange", "red"])
    sparks.append(canvas.create_rectangle(x, y, x + 3, y + 3, fill=color, width=0))

colors = ["lime", "yellow", "orange", "red", "magenta", "cyan"]
frame = 0


def animate():
    global frame
    frame = frame + 1

    # искры летят вверх, если улетели высоко - обратно вниз
    for spark in sparks:
        canvas.move(spark, random.randint(-1, 1), -2)
        if canvas.coords(spark)[1] < 580:
            canvas.move(spark, 0, 240)

    # надпись меняет цвет
    canvas.itemconfig(title, fill=colors[(frame // 10) % len(colors)])

    window.after(30, animate)


animate()
window.mainloop()