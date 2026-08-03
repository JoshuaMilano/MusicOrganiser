from PySide6.QtWidgets import QApplication
from QtComponents import MainWindow

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()