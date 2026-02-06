from __future__ import annotations

from typing import List

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from akyl_ordo.player.screens.game_board import TeamState


class ScoreAdjustScreen(QWidget):
    done = Signal()

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Команда", "Баллы"])
        self.adjust_input = QSpinBox()
        self.adjust_input.setRange(-1000, 1000)
        self.adjust_input.setSingleStep(50)

        apply_button = QPushButton("Применить")
        apply_button.clicked.connect(self.apply_adjustment)
        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.done.emit)

        layout.addWidget(QLabel("Ручная корректировка"))
        layout.addWidget(self.table)
        layout.addWidget(QLabel("Изменение"))
        layout.addWidget(self.adjust_input)
        layout.addWidget(apply_button)
        layout.addWidget(back_button)

        self._teams: List[TeamState] = []

    def load_state(self, teams: List[TeamState]) -> None:
        self._teams = teams
        self.refresh_table()

    def refresh_table(self) -> None:
        self.table.setRowCount(len(self._teams))
        for row, team in enumerate(self._teams):
            self.table.setItem(row, 0, QTableWidgetItem(team.name))
            self.table.setItem(row, 1, QTableWidgetItem(str(team.score)))

    def apply_adjustment(self) -> None:
        row = self.table.currentRow()
        if row < 0:
            return
        self._teams[row].score += self.adjust_input.value()
        self.refresh_table()
