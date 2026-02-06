from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget


class LoadGameScreen(QWidget):
    game_selected = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        title = QLabel("Загрузить игру")
        title.setStyleSheet("font-size: 24px; font-weight: 700;")
        select_button = QPushButton("Выбрать папку игры")
        select_button.clicked.connect(self.select_game)

        layout.addWidget(title)
        layout.addWidget(select_button)
        layout.addStretch()

    def select_game(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку игры")
        if folder:
            self.game_selected.emit(folder)
