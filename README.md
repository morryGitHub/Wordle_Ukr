# 🇺🇦 Wordle_Ukr — Ukrainian Wordle Game

**Wordle_Ukr** — це локалізована українська версія відомої гри Wordle.  
**Wordle_Ukr** is a localized Ukrainian version of the famous Wordle game.

---

## 🎮 Можливості | Features

- 🇺🇦 Повна підтримка української мови  
  Full Ukrainian language support  
- 🔠 Слово з 5 літер, 6 спроб  
  5-letter word, 6 attempts  
- ✅ Візуальні підказки (зелений/жовтий)  
  Visual hints (green/yellow)  
- 🖥 Гра запускається локально, без інтернету  
  Runs locally, no internet needed  

---

## 🚀 Запуск гри | Running the Game

### 🖱  Запуск `.exe` |  Run `.exe`

1. Перейдіть у папку `dist/`  
   Go to the `dist/` folder  
2. Запустіть файл `Wordle_Ukr.exe`  
   Run `Wordle_Ukr.exe`  

> ⚠️ Windows може показати попередження. Натисніть “Додатково” → “Все одно виконати”.  
> ⚠️ Windows might show a warning. Click “More info” → “Run anyway”.

---

## 🌐 Як адаптувати гру під англійську | How to adapt the game for English

Гру легко змінити під англомовну версію.  
You can easily modify the game to support English.

### 🔄 Що потрібно зробити | What you need to do:

📄 Додайте англійський словник (текстовий файл)        
Add an English word list (plain `.txt` file) with 5-letter words.


🧠 У коді замініть наступні змінні:  
   In `main.py`, replace the following lines:

```python
# Було / Original (Ukrainian):
d_ua = enchant.Dict("uk_UA")  # укр
dic_path = r"C:\Wordle_Ukr\words.txt"
```

```python
# Стало / New (English):
d_en = enchant.Dict("en_US")  # англ
dic_path = r"C:\Wordle_Ukr\words_en.txt"
```

🔁 Запустіть гру з новими налаштуваннями  
   Run the game with the new configuration.

> 💡 Файл `words_en.txt` повинен містити **одне слово з 5 літер на рядок**.
> 💡 The file `words_en.txt` must contain **one 5-letter word per line**.

---

## 🛠 Збірка .exe файлу самостійно | Build .exe Yourself

Щоб зібрати `.exe` для запуску без Python, виконайте такі кроки:  
To build the `.exe` file to run without Python, follow these steps:

1. 🐍 Встановіть Python 3.10+  
   Install Python 3.10+

2. 📦 Встановіть PyInstaller:  
   Install PyInstaller:

```bash
pip install pyinstaller
```

3. 📂 Перейдіть у папку з `main.py` (термінал/командний рядок).   
   Navigate to the folder with `main.py` (terminal/command prompt).

4. ⚙️ Виконайте команду збірки:  
   Run the build command:

```bash
pyinstaller --onefile --noconsole Wordle_Ukr.py
```

5. 📁 Після успішної збірки `.exe` файл з’явиться у папці `dist/`.   
   After successful build, the `.exe` file will be in the `dist/` folder.

6. ✏️ За бажанням, перейменуйте файл (наприклад, у `Wordle_Ukr.exe`).   
   Optionally rename the file (e.g. `Wordle_Ukr.exe`).

---
