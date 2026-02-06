from __future__ import annotations

from typing import List

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from akyl_ordo.common.models import GameData, Question


class QuestionEditor(QWidget):
    back_requested = Signal()
    save_requested = Signal()
    open_bonus_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setSpacing(16)

        self.categories = QListWidget()
        self.categories.setMinimumWidth(200)
        self.categories.itemSelectionChanged.connect(self.on_category_selected)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Категория", "Баллы", "Вопрос"])
        self.table.itemSelectionChanged.connect(self.on_question_selected)

        form_box = QGroupBox("Редактор вопроса")
        form_layout = QFormLayout(form_box)

        self.category_input = QComboBox()
        self.score_input = QSpinBox()
        self.score_input.setRange(100, 500)
        self.score_input.setSingleStep(100)
        self.question_input = QTextEdit()
        self.answer_input = QTextEdit()
        self.timer_input = QComboBox()
        self.timer_input.addItems(["auto", "30", "45", "60"])

        form_layout.addRow("Категория", self.category_input)
        form_layout.addRow("Баллы", self.score_input)
        form_layout.addRow("Вопрос", self.question_input)
        form_layout.addRow("Ответ", self.answer_input)
        form_layout.addRow("Таймер", self.timer_input)

        add_button = QPushButton("Добавить вопрос")
        add_button.clicked.connect(self.add_question)
        update_button = QPushButton("Обновить")
        update_button.clicked.connect(self.update_question)
        save_button = QPushButton("💾 Сохранить")
        save_button.clicked.connect(self.save_requested.emit)
        bonus_button = QPushButton("✨ Бонусы")
        bonus_button.clicked.connect(self.open_bonus_requested.emit)
        back_button = QPushButton("⬅️ Назад")
        back_button.clicked.connect(self.back_requested.emit)

        buttons = QHBoxLayout()
        buttons.addWidget(add_button)
        buttons.addWidget(update_button)
        buttons.addWidget(save_button)
        buttons.addWidget(bonus_button)
        buttons.addWidget(back_button)

        right_layout = QVBoxLayout()
        right_layout.addWidget(form_box)
        right_layout.addLayout(buttons)
        right_layout.addStretch()

        layout.addWidget(self.categories)
        layout.addWidget(self.table, 1)
        layout.addLayout(right_layout)

        self._game: GameData | None = None

    def load_game(self, game: GameData) -> None:
        self._game = game
        self.refresh_categories()
        self.refresh_table()

    def refresh_categories(self) -> None:
        if not self._game:
            return
        categories = sorted({q.category for q in self._game.questions})
        if not categories:
            categories = ["Математика", "Логика", "История", "Биология"]
        self.categories.clear()
        self.categories.addItems(categories)
        self.category_input.clear()
        self.category_input.addItems(categories)

    def refresh_table(self, category: str | None = None) -> None:
        if not self._game:
            return
        questions = self._game.questions
        if category:
            questions = [q for q in questions if q.category == category]
        self.table.setRowCount(len(questions))
        for row, question in enumerate(questions):
            self.table.setItem(row, 0, QTableWidgetItem(question.category))
            self.table.setItem(row, 1, QTableWidgetItem(str(question.score)))
            self.table.setItem(row, 2, QTableWidgetItem(question.question))

    def on_category_selected(self) -> None:
        selected = self.categories.currentItem()
        if selected:
            self.refresh_table(selected.text())

    def add_question(self) -> None:
        if not self._game:
            return
        question = Question(
            category=self.category_input.currentText(),
            score=self.score_input.value(),
            question=self.question_input.toPlainText().strip(),
            answer=self.answer_input.toPlainText().strip(),
            timer=self.timer_input.currentText(),
        )
        self._game.questions.append(question)
        self.refresh_table(self.category_input.currentText())
        self.refresh_categories()

    def update_question(self) -> None:
        if not self._game:
            return
        row = self.table.currentRow()
        if row < 0:
            return
        category = self.categories.currentItem().text() if self.categories.currentItem() else None
        questions = self._filter_questions(category)
        question = questions[row]
        question.category = self.category_input.currentText()
        question.score = self.score_input.value()
        question.question = self.question_input.toPlainText().strip()
        question.answer = self.answer_input.toPlainText().strip()
        question.timer = self.timer_input.currentText()
        self.refresh_table(category)
        self.refresh_categories()

    def on_question_selected(self) -> None:
        row = self.table.currentRow()
        category = self.categories.currentItem().text() if self.categories.currentItem() else None
        questions = self._filter_questions(category)
        if row < 0 or row >= len(questions):
            return
        question = questions[row]
        self.category_input.setCurrentText(question.category)
        self.score_input.setValue(question.score)
        self.question_input.setPlainText(question.question)
        self.answer_input.setPlainText(question.answer)
        self.timer_input.setCurrentText(question.timer)

    def _filter_questions(self, category: str | None) -> List[Question]:
        if not self._game:
            return []
        if not category:
            return self._game.questions
        return [q for q in self._game.questions if q.category == category]

    def validate_questions(self) -> bool:
        if not self._game:
            return False
        for question in self._game.questions:
            if not question.question.strip() or not question.answer.strip():
                return False
        return True
