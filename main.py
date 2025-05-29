import random
import enchant

from tkinter import messagebox
from tkinter import *
from collections import Counter


d_ua = enchant.Dict("uk_UA")  # укр
dic_path = r'words.txt'

GUESSED_WORD = ''
UPPER_LETTERS = ['Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', 'Х', 'Ї']
MIDDLE_LETTERS = ['Ф', 'І', 'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж', 'Є']
LOWER_LETTERS = ["'", 'Я', 'Ч', 'С', 'М', 'И', 'Т', 'Ь', 'Б', 'Ю', 'Ґ']

max_letters = 5
letter_click = 0
current_word = ''
word_click = 0

buttons_upper = {}
buttons_middle = {}
buttons_lower = {}

used_words = {}

COUNTS = {}


def reset_game():
    global current_word, letter_click, word_click, used_words, COUNTS, root

    # Сначала закрыть текущее окно, если оно существует
    if root:
        root.destroy()

    current_word = ""
    letter_click = 0
    word_click = 0
    used_words = {}
    COUNTS = {}

    choose_word()
    createGUI()


def handle_win():
    messagebox.showinfo(
        "Вітаємо!",
        f"Ви вгадали слово: {GUESSED_WORD}!\nКількість спроб: {len(used_words)}"
    )


def delete_word():
    global current_word, letter_click
    for i in range(len(labels[word_click])):
        labels[word_click][i].config(text='-')
    letter_click = 0
    current_word = ''


def update_colors():
    darkKhaki = '#d1c400'  # DarkKhaki — тёмно-жёлтый оттенок
    # Сначала зелёные — правильные буквы на правильных местах
    for index in range(len(GUESSED_WORD)):
        if current_word[index] == GUESSED_WORD[index]:
            labels[word_click - 1][index].config(foreground='green')
            COUNTS[current_word[index]] -= 1
            btn = (buttons_upper.get(current_word[index])
                   or buttons_middle.get(current_word[index])
                   or buttons_lower.get(current_word[index]))
            if btn:
                btn.config(fg='green')

    # Потом жёлтые — буквы есть, но на другой позиции
    for index in range(len(GUESSED_WORD)):
        if current_word[index] != GUESSED_WORD[index]:
            if current_word[index] in GUESSED_WORD and COUNTS[current_word[index]] > 0:
                labels[word_click - 1][index].config(foreground=darkKhaki)
                COUNTS[current_word[index]] -= 1
                btn = (buttons_upper.get(current_word[index])
                       or buttons_middle.get(current_word[index])
                       or buttons_lower.get(current_word[index]))
                if btn:
                    current_btn_color = btn.cget('fg')
                    if current_btn_color != 'green':
                        btn.config(fg=darkKhaki)

            else:
                labels[word_click - 1][index].config(foreground='gray')
                btn = (buttons_upper.get(current_word[index])
                       or buttons_middle.get(current_word[index])
                       or buttons_lower.get(current_word[index]))
                if btn:
                    # Меняем цвет кнопки только если она ещё не зелёная или жёлтая
                    current_btn_color = btn.cget('fg')
                    if current_btn_color not in ('green', darkKhaki):
                        btn.config(fg='gray')


def confirm_word():
    global word_click, current_word, letter_click, root, COUNTS

    if not current_word:
        return

    is_valid = d_ua.check(current_word)

    if not is_valid:
        messagebox.showwarning("Помилка", f"Слово '{current_word}' недійсне.")
        delete_word()
        return

    if current_word in used_words:
        messagebox.showwarning("Увага", "Це слово вже було використано. Спробуйте інше.")
        delete_word()
        return

    used_words[current_word] = used_words.get(current_word, 0) + 1

    if len(current_word.replace(" ", '')) == max_letters:
        word_click += 1
        letter_click = 0

        COUNTS = Counter(GUESSED_WORD)
        update_colors()

        if current_word == GUESSED_WORD:
            handle_win()
            return

        current_word = ''

        if word_click >= 6:

            restart = messagebox.askyesno(
                "Гру завершено",
                f"Ви не вгадали слово.\nПравильне слово: {GUESSED_WORD}\n\nБажаєте зіграти ще раз?"
            )

            if restart:
                reset_game()


def delete_letter():
    global letter_click, current_word
    if letter_click <= 0:
        return
    letter_click -= 1
    current_word = current_word[:letter_click]

    labels[word_click][letter_click].config(text='-')


def click_on_btn(letter):
    global word_click, letter_click, current_word
    if (0 <= letter_click < max_letters) and (0 <= word_click < 6):
        labels[word_click][letter_click].config(text=letter)
        letter_click += 1
        current_word += letter


def choose_word():
    global GUESSED_WORD, COUNTS

    with open(dic_path, mode='r', encoding='UTF-8') as file:
        words = [word.split('/')[0].strip() for word in file if len(word.split('/')[0].strip()) == max_letters]

    GUESSED_WORD = random.choice(words).upper()

def createGUI():
    global frames, labels, root, confirm_button, delete_button
    root = Tk()
    root.title("Wordle")
    root.geometry("800x800+600+200")

    frames = []
    labels = []

    for i in range(6):
        f = Frame(root)
        row_labels = []
        for j in range(5):
            lbl = Label(f, text='-', width=2, height=1,
                        font=('Courier', 20, 'bold'),
                        bg='lightgrey', relief='solid', borderwidth=1)
            lbl.pack(side=LEFT, padx=5)
            row_labels.append(lbl)
        f.pack(pady=(60, 20) if i == 0 else 20)
        frames.append(f)
        labels.append(row_labels)

    upper_keyboard = Frame(root)
    middle_keyboard = Frame(root)
    lower_keyboard = Frame(root)

    for letter in UPPER_LETTERS:
        btn = Button(upper_keyboard, text=f'{letter}', font=('Courier', 16, 'bold'),
                     command=lambda l=letter: click_on_btn(l))
        btn.pack(side=LEFT, padx=5)
        buttons_upper[letter] = btn

    upper_keyboard.pack(side=TOP, pady=10)

    for letter in MIDDLE_LETTERS:
        btn = Button(middle_keyboard, text=f'{letter}', font=('Courier', 16, 'bold'),
                     command=lambda l=letter: click_on_btn(l))
        btn.pack(side=LEFT, padx=5)
        buttons_middle[letter] = btn

    delete_button = Button(middle_keyboard, text='🗑', font=('Courier', 16, 'bold'), command=delete_letter)
    delete_button.pack(side=LEFT, padx=5)
    middle_keyboard.pack(side=TOP, pady=10)

    for letter in LOWER_LETTERS:
        btn = Button(lower_keyboard, text=f'{letter}', font=('Courier', 16, 'bold'),
                     command=lambda l=letter: click_on_btn(l))
        btn.pack(side=LEFT, padx=5)
        buttons_lower[letter] = btn

    confirm_button = Button(lower_keyboard, text='✅', font=('Courier', 16, 'bold'), command=confirm_word)
    confirm_button.pack(side=LEFT, padx=5)
    lower_keyboard.pack(side=TOP, pady=10)

    root.mainloop()


choose_word()
createGUI()
