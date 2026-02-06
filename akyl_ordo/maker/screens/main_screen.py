from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MainScreen(QWidget):
    new_game_requested = Signal(str, str)
    open_game_requested = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(24)

        title = QLabel("Акыл Ордо Maker")
        title.setStyleSheet("font-size: 28px; font-weight: 700;")

        form_layout = QHBoxLayout()
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название игры")
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Папка для сохранения")
        browse_button = QPushButton("Выбрать папку")
        browse_button.clicked.connect(self.select_folder)
        form_layout.addWidget(self.title_input)
        form_layout.addWidget(self.folder_input)
        form_layout.addWidget(browse_button)

        create_button = QPushButton("➕ Создать игру")
        create_button.clicked.connect(self.create_game)

        open_button = QPushButton("📂 Открыть игру")
        open_button.clicked.connect(self.open_game)

        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addWidget(create_button)
        layout.addWidget(open_button)
        layout.addStretch()

    def select_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder:
            self.folder_input.setText(folder)

    def create_game(self) -> None:
        self.new_game_requested.emit(self.title_input.text(), self.folder_input.text())

    def open_game(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку игры")
        if folder:
            self.open_game_requested.emit(folder)
