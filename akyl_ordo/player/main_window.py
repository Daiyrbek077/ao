from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QMessageBox, QStackedWidget

from akyl_ordo.common.models import GameData
from akyl_ordo.common.sound import SoundSystem
from akyl_ordo.common.storage import load_game
from akyl_ordo.common.styles import APP_STYLE
from akyl_ordo.player.screens.game_board import GameBoardScreen
from akyl_ordo.player.screens.load_game import LoadGameScreen
from akyl_ordo.player.screens.login import LoginScreen
from akyl_ordo.player.screens.question import QuestionScreen
from akyl_ordo.player.screens.results import ResultsScreen
from akyl_ordo.player.screens.score_adjust import ScoreAdjustScreen
from akyl_ordo.player.screens.settings import SettingsScreen


class PlayerWindow(QMainWindow):
    def __init__(self, sounds_dir: Path) -> None:
        super().__init__()
        self.setWindowTitle("Акыл Ордо Player")
        self.setMinimumSize(1280, 720)
        self.setStyleSheet(APP_STYLE)

        self._sound = SoundSystem(sounds_dir)
        self._game: GameData | None = None

        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)

        self.login_screen = LoginScreen()
        self.load_screen = LoadGameScreen()
        self.settings_screen = SettingsScreen()
        self.game_board = GameBoardScreen()
        self.question_screen = QuestionScreen()
        self.score_adjust = ScoreAdjustScreen()
        self.results_screen = ResultsScreen()

        for screen in (
            self.login_screen,
            self.load_screen,
            self.settings_screen,
            self.game_board,
            self.question_screen,
            self.score_adjust,
            self.results_screen,
        ):
            self._stack.addWidget(screen)

        self.login_screen.login_success.connect(self.show_load_screen)
        self.load_screen.game_selected.connect(self.load_game)
        self.settings_screen.start_game.connect(self.start_game)
        self.game_board.question_selected.connect(self.open_question)
        self.question_screen.answer_completed.connect(self.return_to_board)
        self.game_board.open_score_adjust.connect(self.open_score_adjust)
        self.score_adjust.done.connect(self.return_to_board)
        self.game_board.show_results.connect(self.show_results)

    @Slot()
    def show_load_screen(self) -> None:
        self._stack.setCurrentWidget(self.load_screen)

    @Slot(str)
    def load_game(self, folder: str) -> None:
        main_json = Path(folder) / "main.json"
        if not main_json.exists():
            QMessageBox.warning(self, "Ошибка", "main.json не найден")
            return
        self._game = load_game(main_json)
        self.settings_screen.load_game(self._game)
        self._stack.setCurrentWidget(self.settings_screen)

    @Slot(dict)
    def start_game(self, settings: dict) -> None:
        if not self._game:
            return
        self.game_board.load_game(self._game, settings)
        self._stack.setCurrentWidget(self.game_board)
        if settings.get("sound", True):
            self._sound.play("bg_music.mp3")

    @Slot(object)
    def open_question(self, payload: dict) -> None:
        self.question_screen.load_question(payload)
        self._stack.setCurrentWidget(self.question_screen)

    @Slot(dict)
    def return_to_board(self, result: dict | None = None) -> None:
        if result:
            self.game_board.apply_result(result)
        self._stack.setCurrentWidget(self.game_board)

    @Slot()
    def open_score_adjust(self) -> None:
        self.score_adjust.load_state(self.game_board.teams)
        self._stack.setCurrentWidget(self.score_adjust)

    @Slot()
    def show_results(self) -> None:
        self.results_screen.load_results(self.game_board.teams)
        self._stack.setCurrentWidget(self.results_screen)
