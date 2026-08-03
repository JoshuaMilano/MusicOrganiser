from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QLabel, QMainWindow, QApplication
from core import organise_directory

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('MusicOrganiser')
        self.setFixedSize(QSize(600, 400))

        layout = QVBoxLayout()

        self.source_picker = FolderPicker(label_text='Original Folder', placeholder='Select the original folder')
        self.destination_picker = FolderPicker(label_text='Original Folder', placeholder='Select the original folder')
        layout.addWidget(self.source_picker)
        layout.addWidget(self.destination_picker)

        self.status_label = QLabel('Ready...')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        self.sort_button = QPushButton('Sort')
        self.sort_button.clicked.connect(self.run_sort)
        layout.addWidget(self.sort_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def run_sort(self):
        source_path = self.source_picker.path_display.text()
        target_path = self.destination_picker.path_display.text()

        if not source_path or not target_path:
            self.status_label.setText('Error: Please choose a source path and a destination path')
            return

        self.status_label.setText('Sorting...')
        self.sort_button.setEnabled(False)
        QApplication.processEvents()

        try:
            total_songs, total_albums, total_artists = organise_directory(source_path, target_path)
            self.status_label.setText(f'Success!:\nSorted {total_artists} Artists\nSorted {total_albums} Albums\nSorted {total_songs} Songs')
        except Exception as e:
            self.status_label.setText(f'An Error occurred: {str(e)}')

        finally:
            self.sort_button.setEnabled(True)

class FolderPicker(QWidget):
    def __init__(self, *, label_text: str = 'Select a folder', placeholder: str = 'Select a folder...'):
        super().__init__()
        widget_layout = QVBoxLayout()

        self.label = QLabel(label_text)
        widget_layout.addWidget(self.label)

        folder_select_layout = QHBoxLayout()

        self.path_display = QLineEdit()
        self.path_display.setPlaceholderText(placeholder)

        self.browse_button = QPushButton('Browse...')
        self.browse_button.clicked.connect(self.open_folder_dialog)

        folder_select_layout.addWidget(self.path_display)
        folder_select_layout.addWidget(self.browse_button)

        widget_layout.addLayout(folder_select_layout)

        widget_layout.addStretch()
        self.setLayout(widget_layout)

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select a Folder')

        if folder_path:
            self.path_display.setText(folder_path)