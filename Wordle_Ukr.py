# todo доробити словник
# todo maybe create a db for saving user's results
# todo select language before game
# that's all -> new project
import os
import random
import enchant

from tkinter import messagebox
from tkinter import *
from collections import Counter
from paths import resource_path
from keybords import UPPER_LETTERS_UA, MIDDLE_LETTERS_UA, LOWER_LETTERS_UA
from keybords import UPPER_LETTERS_EN, MIDDLE_LETTERS_EN, LOWER_LETTERS_EN

d_ua = enchant.Dict("uk_UA")  # укр
d_en = enchant.Dict("en_US")  # eng

LANGUAGE = None
dic_path = None
languages = {
    "English": r"words_en.txt",
    "Ukrainian": r"words_ua.txt"
}

GUESSED_WORD = ''
max_letters = 5
letter_click = 0
current_word = ''
word_click = 0

buttons_upper = {}
buttons_middle = {}
buttons_lower = {}

used_words = {}

COUNTS = {}


def select_language():
    def confirm_selection(language):
        global LANGUAGE, dic_path
        if language:
            LANGUAGE = language
            dic_path = resource_path(os.path.join("dicts", languages[language]))

            question.destroy()
            choose_word()
            createGUI()

    question = Tk()
    question.title("Select Language")
    question.geometry("300x150+880+300")

    Label(question, text="Choose a language:", font=('Ariel', 16, 'bold')).pack(pady=10)
    frame = Frame(question)

    for lang in languages:
        (Button(frame, text=lang, font=('Ariel', 14), relief='solid', command=lambda l=lang: confirm_selection(l)).pack(
            side=LEFT, pady=5,
            padx=10))
    frame.pack(side=TOP)

    question.mainloop()


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
    restart = messagebox.askyesno(
        "Congratulations!",
        f"You guessed the word: {GUESSED_WORD}!\nNumber of attempts: {len(used_words)}\n\nWould you like to play again?"
    )

    if restart:
        reset_game()


def delete_word():
    global current_word, letter_click
    for i in range(len(labels[word_click])):
        labels[word_click][i].config(text='-')
    letter_click = 0
    current_word = ''


def update_colors():
    darkKhaki = '#d1c400'  # DarkKhaki — dark-yellow
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
        messagebox.showwarning("Error", f"The word '{current_word}' is invalid.")
        delete_word()
        return

    if current_word in used_words:
        messagebox.showwarning("Warning", "This word has already been used. Try another one.")
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
            root.destroy()
            return

        current_word = ''

        if word_click >= 6:

            restart = messagebox.askyesno(
                "Game Over",
                f"You did not guess the word.\nThe correct word was: {GUESSED_WORD}\n\nWould you like to play again?"
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
    if dic_path is None:
        return
    else:
        with open(dic_path, mode='r', encoding='utf-8') as file:  # type: ignore
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

    if LANGUAGE == next(iter(languages)):  # eng_keyboard
        first_line, second_line, third_line = UPPER_LETTERS_EN, MIDDLE_LETTERS_EN, LOWER_LETTERS_EN
    else:
        first_line, second_line, third_line = UPPER_LETTERS_UA, MIDDLE_LETTERS_UA, LOWER_LETTERS_UA

    for letter in first_line:
        btn = Button(upper_keyboard, text=f'{letter}', font=('Courier', 16, 'bold'),
                     command=lambda l=letter: click_on_btn(l))
        btn.pack(side=LEFT, padx=5)
        buttons_upper[letter] = btn

    upper_keyboard.pack(side=TOP, pady=10)

    for letter in second_line:
        btn = Button(middle_keyboard, text=f'{letter}', font=('Courier', 16, 'bold'),
                     command=lambda l=letter: click_on_btn(l))
        btn.pack(side=LEFT, padx=5)
        buttons_middle[letter] = btn

    delete_button = Button(middle_keyboard, text='🗑', font=('Courier', 16, 'bold'), command=delete_letter)
    delete_button.pack(side=LEFT, padx=5)
    middle_keyboard.pack(side=TOP, pady=10)

    for letter in third_line:
        btn = Button(lower_keyboard, text=f'{letter}', font=('Courier', 16, 'bold'),
                     command=lambda l=letter: click_on_btn(l))
        btn.pack(side=LEFT, padx=5)
        buttons_lower[letter] = btn

    confirm_button = Button(lower_keyboard, text='✅', font=('Courier', 16, 'bold'), command=confirm_word)
    confirm_button.pack(side=LEFT, padx=5)
    lower_keyboard.pack(side=TOP, pady=10)

    root.mainloop()


select_language()
