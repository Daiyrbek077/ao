from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from akyl_ordo.common.models import BonusQuestion, GameData


class BonusEditor(QWidget):
    back_requested = Signal()
    save_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Название", "Категория", "Баллы", "Тип"])

        form = QGroupBox("Добавить бонус")
        form_layout = QFormLayout(form)

        self.name_input = QComboBox()
        self.name_input.addItems(["Алтын казына", "Поле чудес", "Тобокел"])
        self.category_input = QComboBox()
        self.score_input = QSpinBox()
        self.score_input.setRange(100, 500)
        self.score_input.setSingleStep(100)
        self.type_input = QComboBox()
        self.type_input.addItems(["gold", "deal", "risk"])

        form_layout.addRow("Название", self.name_input)
        form_layout.addRow("Категория", self.category_input)
        form_layout.addRow("Баллы", self.score_input)
        form_layout.addRow("Тип", self.type_input)

        add_button = QPushButton("Добавить")
        add_button.clicked.connect(self.add_bonus)
        save_button = QPushButton("💾 Сохранить")
        save_button.clicked.connect(self.save_requested.emit)
        back_button = QPushButton("⬅️ Назад")
        back_button.clicked.connect(self.back_requested.emit)

        layout.addWidget(self.table)
        layout.addWidget(form)
        layout.addWidget(add_button)
        layout.addWidget(save_button)
        layout.addWidget(back_button)

        self._game: GameData | None = None

    def load_game(self, game: GameData) -> None:
        self._game = game
        categories = sorted({q.category for q in game.questions}) or ["Математика"]
        self.category_input.clear()
        self.category_input.addItems(categories)
        self.refresh_table()

    def refresh_table(self) -> None:
        if not self._game:
            return
        self.table.setRowCount(len(self._game.bonusQuestions))
        for row, (name, bonus) in enumerate(self._game.bonusQuestions.items()):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(bonus.category))
            self.table.setItem(row, 2, QTableWidgetItem(str(bonus.score)))
            self.table.setItem(row, 3, QTableWidgetItem(bonus.type))

    def add_bonus(self) -> None:
        if not self._game:
            return
        name = self.name_input.currentText()
        bonus = BonusQuestion(
            category=self.category_input.currentText(),
            score=self.score_input.value(),
            type=self.type_input.currentText(),
        )
        self._game.bonusQuestions[name] = bonus
        self.refresh_table()

    def update_game(self, game: GameData) -> None:
        game.bonusQuestions = self._game.bonusQuestions if self._game else {}
