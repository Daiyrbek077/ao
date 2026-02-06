from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSlider,
    QSpinBox,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QInputDialog,
)

from ..common.constants import PLAYER_CONFIG
from ..common.models import GameData, Question
from ..common.sound import SoundManager


@dataclass
class Team:
    name: str
    score: int = 0


class ScoreAdjustDialog(QDialog):
    def __init__(self, teams: List[Team], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Manual Score Adjustment")
        self.teams = teams
        self.history: List[Tuple[int, int]] = []

        layout = QVBoxLayout()
        self.team_list = QListWidget()
        for team in teams:
            self.team_list.addItem(f"{team.name} ({team.score})")

        controls = QHBoxLayout()
        self.amount_input = QSpinBox()
        self.amount_input.setRange(0, 10000)
        minus_button = QPushButton("- Apply")
        plus_button = QPushButton("+ Apply")
        undo_button = QPushButton("Undo")

        minus_button.clicked.connect(lambda: self._apply(-1))
        plus_button.clicked.connect(lambda: self._apply(1))
        undo_button.clicked.connect(self._undo)

        controls.addWidget(QLabel("Amount"))
        controls.addWidget(self.amount_input)
        controls.addWidget(minus_button)
        controls.addWidget(plus_button)
        controls.addWidget(undo_button)

        self.history_list = QListWidget()

        layout.addWidget(self.team_list)
        layout.addLayout(controls)
        layout.addWidget(QLabel("History"))
        layout.addWidget(self.history_list)
        self.setLayout(layout)

    def _apply(self, sign: int) -> None:
        row = self.team_list.currentRow()
        if row < 0:
            return
        amount = self.amount_input.value() * sign
        self.teams[row].score += amount
        self.history.append((row, amount))
        self.history_list.addItem(f"{self.teams[row].name}: {amount:+}")
        self._refresh()

    def _undo(self) -> None:
        if not self.history:
            return
        row, amount = self.history.pop()
        self.teams[row].score -= amount
        self.history_list.takeItem(self.history_list.count() - 1)
        self._refresh()

    def _refresh(self) -> None:
        self.team_list.clear()
        for team in self.teams:
            self.team_list.addItem(f"{team.name} ({team.score})")


class PlayerWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Akyл Ordo Player")
        self.resize(1280, 720)

        self.sound = SoundManager()
        self.sound.start_background()

        self.game_data: Optional[GameData] = None
        self.game_path: Optional[Path] = None
        self.teams: List[Team] = []
        self.current_team_index = 0
        self.timer_enabled = True
        self.timer_seconds = 30
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.remaining_seconds = 0
        self.current_question: Optional[Question] = None
        self.current_custom_score: Optional[int] = None

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_screen = self._build_login_screen()
        self.load_screen = self._build_load_screen()
        self.settings_screen = self._build_settings_screen()
        self.board_screen = self._build_board_screen()
        self.question_screen = self._build_question_screen()

        for screen in (
            self.login_screen,
            self.load_screen,
            self.settings_screen,
            self.board_screen,
            self.question_screen,
        ):
            self.stack.addWidget(screen)

    def _build_login_screen(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Login")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        login_button = QPushButton("Login")
        login_button.clicked.connect(self._attempt_login)

        layout.addWidget(title)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        widget.setLayout(layout)
        return widget

    def _build_load_screen(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Load Game")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        load_button = QPushButton("Select Game Folder")
        load_button.clicked.connect(self._load_game_folder)

        layout.addWidget(title)
        layout.addWidget(load_button)
        widget.setLayout(layout)
        return widget

    def _build_settings_screen(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Game Settings")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.team_count_input = QSpinBox()
        self.team_count_input.setRange(2, 14)
        self.team_count_input.setValue(2)
        self.team_count_input.valueChanged.connect(self._render_team_inputs)

        self.team_inputs_container = QWidget()
        self.team_inputs_layout = QFormLayout()
        self.team_inputs_container.setLayout(self.team_inputs_layout)

        self.timer_toggle = QCheckBox("Enable Timer")
        self.timer_toggle.setChecked(True)
        self.timer_toggle.stateChanged.connect(lambda state: setattr(self, "timer_enabled", state == Qt.Checked))

        self.timer_seconds_input = QSpinBox()
        self.timer_seconds_input.setRange(5, 120)
        self.timer_seconds_input.setValue(30)
        self.timer_seconds_input.valueChanged.connect(lambda value: setattr(self, "timer_seconds", value))

        self.sound_toggle = QCheckBox("Enable Sound")
        self.sound_toggle.setChecked(True)
        self.sound_toggle.stateChanged.connect(lambda state: self.sound.set_enabled(state == Qt.Checked))

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(30)
        self.volume_slider.valueChanged.connect(lambda value: self.sound.set_volume(value / 100))

        start_button = QPushButton("Start Game")
        start_button.clicked.connect(self._start_game)

        layout.addWidget(title)
        layout.addWidget(QLabel("Teams Count"))
        layout.addWidget(self.team_count_input)
        layout.addWidget(self.team_inputs_container)
        layout.addWidget(self.timer_toggle)
        layout.addWidget(QLabel("Timer Seconds"))
        layout.addWidget(self.timer_seconds_input)
        layout.addWidget(self.sound_toggle)
        layout.addWidget(QLabel("Volume"))
        layout.addWidget(self.volume_slider)
        layout.addWidget(start_button)

        widget.setLayout(layout)
        self._render_team_inputs(self.team_count_input.value())
        return widget

    def _build_board_screen(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()

        self.current_team_label = QLabel("Team: -")
        self.current_team_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.team_scores_list = QListWidget()

        self.board_grid = QGridLayout()
        self.board_container = QWidget()
        self.board_container.setLayout(self.board_grid)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.current_team_label)
        top_layout.addStretch()
        adjust_button = QPushButton("✏ Score Adjust")
        adjust_button.clicked.connect(self._open_score_adjust)
        top_layout.addWidget(adjust_button)

        layout.addLayout(top_layout)
        layout.addWidget(self.team_scores_list)
        layout.addWidget(self.board_container)
        widget.setLayout(layout)
        return widget

    def _build_question_screen(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()

        self.question_title = QLabel("Question")
        self.question_title.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.timer_label = QLabel("Timer")
        self.question_text = QTextEdit()
        self.question_text.setReadOnly(True)
        self.answer_text = QTextEdit()
        self.answer_text.setReadOnly(True)

        show_answer_button = QPushButton("Show Answer")
        show_answer_button.clicked.connect(self._show_answer)

        correct_button = QPushButton("✅ Correct")
        wrong_button = QPushButton("❌ Wrong")
        correct_button.clicked.connect(lambda: self._score_answer(True))
        wrong_button.clicked.connect(lambda: self._score_answer(False))

        buttons = QHBoxLayout()
        buttons.addWidget(show_answer_button)
        buttons.addWidget(correct_button)
        buttons.addWidget(wrong_button)

        layout.addWidget(self.question_title)
        layout.addWidget(self.timer_label)
        layout.addWidget(QLabel("Question"))
        layout.addWidget(self.question_text)
        layout.addWidget(QLabel("Answer"))
        layout.addWidget(self.answer_text)
        layout.addLayout(buttons)

        widget.setLayout(layout)
        return widget

    def _attempt_login(self) -> None:
        password = self.password_input.text().strip()
        if not password:
            return
        hashed = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if PLAYER_CONFIG.exists():
            data = json.loads(PLAYER_CONFIG.read_text(encoding="utf-8"))
            stored_hash = data.get("password_hash")
            if stored_hash and stored_hash != hashed:
                QMessageBox.warning(self, "Login Failed", "Incorrect password.")
                return
        else:
            PLAYER_CONFIG.write_text(json.dumps({"password_hash": hashed}, indent=2), encoding="utf-8")
        self.stack.setCurrentWidget(self.load_screen)

    def _load_game_folder(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "Select Game Folder")
        if not directory:
            return
        game_path = Path(directory)
        main_json = game_path / "main.json"
        if not main_json.exists():
            QMessageBox.warning(self, "Invalid Game", "main.json not found.")
            return
        self.game_path = game_path
        self.game_data = GameData.load(main_json)
        self.stack.setCurrentWidget(self.settings_screen)

    def _render_team_inputs(self, count: int) -> None:
        while self.team_inputs_layout.rowCount():
            self.team_inputs_layout.removeRow(0)
        self.team_name_inputs = []
        for index in range(count):
            input_field = QLineEdit(f"Team {index + 1}")
            self.team_name_inputs.append(input_field)
            self.team_inputs_layout.addRow(f"Team {index + 1}", input_field)

    def _start_game(self) -> None:
        self.teams = [Team(name=input_field.text().strip() or f"Team {i + 1}") for i, input_field in enumerate(self.team_name_inputs)]
        self.current_team_index = 0
        self._refresh_scores()
        self._build_game_board()
        self._update_current_team_label()
        self.stack.setCurrentWidget(self.board_screen)

    def _build_game_board(self) -> None:
        for i in reversed(range(self.board_grid.count())):
            item = self.board_grid.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
        if not self.game_data:
            return
        categories = sorted({q.category for q in self.game_data.questions})
        scores = sorted({q.score for q in self.game_data.questions})

        for col, category in enumerate(categories):
            label = QLabel(category)
            label.setStyleSheet("font-weight: bold; font-size: 16px;")
            self.board_grid.addWidget(label, 0, col)

        for row, score in enumerate(scores, start=1):
            for col, category in enumerate(categories):
                button = QPushButton(str(score))
                button.setEnabled(self._has_question(category, score))
                button.clicked.connect(lambda _, c=category, s=score, b=button: self._select_cell(c, s, b))
                self.board_grid.addWidget(button, row, col)

    def _has_question(self, category: str, score: int) -> bool:
        if not self.game_data:
            return False
        return any(q.category == category and q.score == score for q in self.game_data.questions)

    def _select_cell(self, category: str, score: int, button: QPushButton) -> None:
        if not self.game_data:
            return
        button.setEnabled(False)
        bonus = self._find_bonus(category, score)
        if bonus:
            self._handle_bonus(bonus)
            self._refresh_scores()
            self._advance_team()
            return
        question = next(
            (q for q in self.game_data.questions if q.category == category and q.score == score),
            None,
        )
        if not question:
            return
        self.current_question = question
        self.current_custom_score = None
        self.question_title.setText(f"{question.category} - {question.score}")
        self.question_text.setPlainText(question.question)
        self.answer_text.clear()
        self._start_timer(question.timer)
        self.stack.setCurrentWidget(self.question_screen)

    def _find_bonus(self, category: str, score: int) -> Optional[Dict[str, str]]:
        if not self.game_data:
            return None
        for bonus in self.game_data.bonus_questions.values():
            if bonus.get("category") == category and int(bonus.get("score")) == score:
                return bonus
        return None

    def _handle_bonus(self, bonus: Dict[str, str]) -> None:
        bonus_type = bonus.get("type")
        if bonus_type == "gold":
            self.sound.play_bonus_gold()
            self.teams[self.current_team_index].score += int(bonus.get("score", 0))
            QMessageBox.information(self, "Алтын казына", "Instant bonus added!")
        elif bonus_type == "deal":
            self.sound.play_bonus()
            dialog = ScoreAdjustDialog(self.teams, self)
            dialog.exec()
        elif bonus_type == "risk":
            self.sound.play_bonus()
            custom_score, ok = QInputDialog.getInt(self, "Тобокел", "Enter custom score:", value=200, min=0, max=5000)
            if ok:
                self.current_custom_score = custom_score
                self._show_risk_question(bonus)

    def _show_risk_question(self, bonus: Dict[str, str]) -> None:
        if not self.game_data:
            return
        question = next(
            (q for q in self.game_data.questions if q.category == bonus.get("category") and q.score == int(bonus.get("score"))),
            None,
        )
        if not question:
            return
        self.current_question = question
        self.question_title.setText(f"{question.category} - {self.current_custom_score}")
        self.question_text.setPlainText(question.question)
        self.answer_text.clear()
        self._start_timer(question.timer)
        self.stack.setCurrentWidget(self.question_screen)

    def _start_timer(self, timer_value: str) -> None:
        if not self.timer_enabled:
            self.timer_label.setText("Timer: off")
            return
        if timer_value == "auto":
            self.remaining_seconds = self.timer_seconds
        else:
            self.remaining_seconds = int(timer_value)
        self.timer_label.setText(f"Timer: {self.remaining_seconds}s")
        self.timer.start(1000)

    def _tick(self) -> None:
        self.remaining_seconds -= 1
        self.timer_label.setText(f"Timer: {self.remaining_seconds}s")
        if self.remaining_seconds <= 0:
            self.timer.stop()

    def _show_answer(self) -> None:
        if not self.current_question:
            return
        self.answer_text.setPlainText(self.current_question.answer)

    def _score_answer(self, correct: bool) -> None:
        if not self.current_question:
            return
        self.timer.stop()
        score_value = self.current_custom_score or self.current_question.score
        if correct:
            self.teams[self.current_team_index].score += score_value
            self.sound.play_correct()
        else:
            self.teams[self.current_team_index].score -= score_value
            self.sound.play_wrong()
        self._refresh_scores()
        self._advance_team()
        self.stack.setCurrentWidget(self.board_screen)

    def _advance_team(self) -> None:
        self.current_team_index = (self.current_team_index + 1) % len(self.teams)
        self._update_current_team_label()

    def _refresh_scores(self) -> None:
        self.team_scores_list.clear()
        for team in self.teams:
            self.team_scores_list.addItem(f"{team.name}: {team.score}")

    def _update_current_team_label(self) -> None:
        if not self.teams:
            return
        self.current_team_label.setText(f"Current Team: {self.teams[self.current_team_index].name}")

    def _open_score_adjust(self) -> None:
        dialog = ScoreAdjustDialog(self.teams, self)
        dialog.exec()
        self._refresh_scores()
