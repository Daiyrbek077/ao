from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
)

from akyl_ordo.common.models import Question


class QuestionScreen(QWidget):
    answer_completed = Signal(dict)

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.title = QLabel("Вопрос")
        self.title.setStyleSheet("font-size: 22px; font-weight: 700;")
        self.question_text = QTextEdit()
        self.question_text.setReadOnly(True)
        self.answer_text = QTextEdit()
        self.answer_text.setReadOnly(True)
        self.answer_text.hide()

        show_answer = QPushButton("Показать ответ")
        show_answer.clicked.connect(self.toggle_answer)

        buttons = QHBoxLayout()
        correct_button = QPushButton("✅ Правильно")
        wrong_button = QPushButton("❌ Неправильно")
        correct_button.clicked.connect(lambda: self.emit_result(True))
        wrong_button.clicked.connect(lambda: self.emit_result(False))
        buttons.addWidget(correct_button)
        buttons.addWidget(wrong_button)

        layout.addWidget(self.title)
        layout.addWidget(self.question_text)
        layout.addWidget(self.answer_text)
        layout.addWidget(show_answer)
        layout.addLayout(buttons)

        self._question: Question | None = None
        self._team_index = 0

    def load_question(self, payload: dict) -> None:
        question: Question = payload["question"]
        self._question = question
        self._team_index = payload.get("team_index", 0)
        self.title.setText(f"{question.category} · {question.score}")
        self.question_text.setPlainText(question.question)
        self.answer_text.setPlainText(question.answer)
        self.answer_text.hide()

    def toggle_answer(self) -> None:
        self.answer_text.setVisible(not self.answer_text.isVisible())

    def emit_result(self, correct: bool) -> None:
        if not self._question:
            return
        score = self._question.score if correct else -self._question.score
        self.answer_completed.emit({"team_index": self._team_index, "score_delta": score})
