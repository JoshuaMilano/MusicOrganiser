from PySide6.QtWidgets import QApplication
from QtComponents import MainWindow
from QtStyles import GLOBAL_STYLES

if __name__ == '__main__':
    app = QApplication([])
    app.setStyleSheet(GLOBAL_STYLES)
    window = MainWindow()
    window.show()
    app.exec()