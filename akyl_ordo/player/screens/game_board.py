from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from akyl_ordo.common.models import GameData, Question


@dataclass
class TeamState:
    name: str
    score: int = 0


class GameBoardScreen(QWidget):
    question_selected = Signal(dict)
    open_score_adjust = Signal()
    show_results = Signal()

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        header = QHBoxLayout()
        self.current_team_label = QLabel("Ход: Команда 1")
        self.current_team_label.setStyleSheet("font-size: 20px; font-weight: 600;")
        score_adjust_button = QPushButton("✏️ Баллы")
        score_adjust_button.clicked.connect(self.open_score_adjust.emit)
        results_button = QPushButton("🏆 Итоги")
        results_button.clicked.connect(self.show_results.emit)
        header.addWidget(self.current_team_label)
        header.addStretch()
        header.addWidget(score_adjust_button)
        header.addWidget(results_button)

        body = QHBoxLayout()
        self.team_box = QVBoxLayout()
        self.board_box = QGroupBox("Игровое поле")
        self.board_layout = QGridLayout(self.board_box)

        body.addLayout(self.team_box)
        body.addWidget(self.board_box, 1)

        layout.addLayout(header)
        layout.addLayout(body)

        self._game: GameData | None = None
        self.teams: list[TeamState] = []
        self._team_index = 0
        self._question_buttons: dict[tuple[str, int], QPushButton] = {}

    def load_game(self, game: GameData, settings: dict) -> None:
        self._game = game
        self.teams = [TeamState(name=name) for name in settings["teams"]]
        self._team_index = 0
        self.refresh_teams()
        self.build_board()

    def refresh_teams(self) -> None:
        while self.team_box.count():
            item = self.team_box.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for team in self.teams:
            label = QLabel(f"{team.name}: {team.score}")
            label.setStyleSheet("font-size: 18px; font-weight: 600;")
            self.team_box.addWidget(label)
        self.current_team_label.setText(f"Ход: {self.teams[self._team_index].name}")

    def build_board(self) -> None:
        while self.board_layout.count():
            item = self.board_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._question_buttons.clear()
        if not self._game:
            return
        categories = sorted({q.category for q in self._game.questions})
        scores = sorted({q.score for q in self._game.questions})
        for col, category in enumerate(categories):
            self.board_layout.addWidget(QLabel(category), 0, col)
        for row, score in enumerate(scores, start=1):
            for col, category in enumerate(categories):
                button = QPushButton(str(score))
                button.clicked.connect(lambda checked=False, c=category, s=score: self.open_question(c, s))
                self.board_layout.addWidget(button, row, col)
                self._question_buttons[(category, score)] = button

    def open_question(self, category: str, score: int) -> None:
        if not self._game:
            return
        question = next((q for q in self._game.questions if q.category == category and q.score == score), None)
        if not question:
            return
        button = self._question_buttons.get((category, score))
        if button:
            button.setEnabled(False)
        payload = {
            "question": question,
            "team_index": self._team_index,
        }
        self.question_selected.emit(payload)

    def apply_result(self, result: dict) -> None:
        team_index = result.get("team_index", self._team_index)
        delta = result.get("score_delta", 0)
        if 0 <= team_index < len(self.teams):
            self.teams[team_index].score += delta
        self._team_index = (self._team_index + 1) % len(self.teams)
        self.refresh_teams()
