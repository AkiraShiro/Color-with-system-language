# Импортируем модуль для работы с win32api
import win32api

# Импортируем модуль для работы с pyqt5
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtCore import Qt, QThread

# Создаем класс для виджета с цветом
class ColorWidget(QWidget):
    # Конструктор класса
    def __init__(self):
        # Вызываем конструктор родительского класса
        super().__init__()
        # Устанавливаем прозрачный фон
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Устанавливаем флаги окна
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        # Устанавливаем размер и положение окна
        self.setGeometry(0, 0, 100, 100)
        # Создаем атрибут для хранения текущей раскладки
        self.layout = "unknown"

    # Метод для рисования цвета в углу экрана
    def paintEvent(self, event):
        # Создаем объект рисования
        painter = QPainter(self)
        # Если раскладка русская, то рисуем красный круг
        if self.layout == "ru":
            painter.setBrush(QBrush(Qt.red))
        # Если раскладка английская, то рисуем зеленый круг
        elif self.layout == "en":
            painter.setBrush(QBrush(Qt.green))
        # Если раскладка неизвестная, то рисуем серый круг
        else:
            painter.setBrush(QBrush(Qt.gray))
        # Рисуем круг в углу экрана
        painter.drawEllipse(0, 0, 100, 100)

# Создаем класс для потока с обновлением цвета и раскладки
class ColorThread(QThread):
    # Конструктор класса
    def __init__(self, widget):
        # Вызываем конструктор родительского класса
        super().__init__()
        # Сохраняем ссылку на виджет
        self.widget = widget

    # Метод для запуска потока
    def run(self):
        # Входим в бесконечный цикл
        while True:
            # Обновляем виджет
            self.widget.update()
            # Обновляем раскладку виджета
            self.widget.layout = get_layout()
            # Ждем 100 миллисекунд
            #self.sleep(1)

# Функция для определения текущей раскладки
def get_layout():
    # Получаем идентификатор текущей раскладки
    id = win32api.GetKeyboardLayout()
    print(id)
    # Если идентификатор равен 1049, то это русская раскладка
    if id == 68748313:
        return "ru"
        # Если идентификатор равен 1033, то это английская раскладка
    elif id == 67699721:
        return "en"
    # Иначе возвращаем неизвестную раскладку
    else:
        return "unknown"

# Создаем приложение
app = QApplication([])

# Создаем виджет с цветом
widget = ColorWidget()

# Создаем поток с обновлением цвета и раскладки
thread = ColorThread(widget)

# Запускаем поток
thread.start()

# Показываем виджет
widget.show()

# Запускаем главный цикл приложения
app.exec_()