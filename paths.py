import sys
import os


def resource_path(relative_path):
    """ Получить путь к ресурсу (работает и в .exe, и при запуске из .py) """
    try:
        base_path = sys._MEIPASS  # когда внутри .exe
    except AttributeError:
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, relative_path)



