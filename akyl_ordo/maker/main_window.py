from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QMessageBox, QStackedWidget

from akyl_ordo.common.models import GameData
from akyl_ordo.common.storage import ensure_game_structure, load_game, write_game
from akyl_ordo.common.styles import APP_STYLE
from akyl_ordo.maker.screens.bonus_editor import BonusEditor
from akyl_ordo.maker.screens.main_screen import MainScreen
from akyl_ordo.maker.screens.question_editor import QuestionEditor


class MakerWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Акыл Ордо Maker")
        self.setMinimumSize(1200, 720)
        self.setStyleSheet(APP_STYLE)

        self._game_path: Path | None = None
        self._game_data: GameData | None = None

        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)

        self.main_screen = MainScreen()
        self.question_editor = QuestionEditor()
        self.bonus_editor = BonusEditor()

        self._stack.addWidget(self.main_screen)
        self._stack.addWidget(self.question_editor)
        self._stack.addWidget(self.bonus_editor)

        self.main_screen.new_game_requested.connect(self.create_new_game)
        self.main_screen.open_game_requested.connect(self.open_existing_game)
        self.question_editor.back_requested.connect(self.show_main)
        self.question_editor.save_requested.connect(self.save_game)
        self.question_editor.open_bonus_requested.connect(self.open_bonus_editor)
        self.bonus_editor.back_requested.connect(self.return_to_questions)
        self.bonus_editor.save_requested.connect(self.save_bonus)

    @Slot(str, str)
    def create_new_game(self, title: str, folder: str) -> None:
        if not title.strip():
            QMessageBox.warning(self, "Требуется название", "Введите название игры.")
            return
        path = ensure_game_structure(Path(folder) / title, title)
        self._game_path = path
        self._game_data = load_game(path / "main.json")
        self.question_editor.load_game(self._game_data)
        self._stack.setCurrentWidget(self.question_editor)

    @Slot(str)
    def open_existing_game(self, folder: str) -> None:
        path = Path(folder)
        main_json = path / "main.json"
        if not main_json.exists():
            QMessageBox.warning(self, "Ошибка", "main.json не найден.")
            return
        self._game_path = path
        self._game_data = load_game(main_json)
        self.question_editor.load_game(self._game_data)
        self._stack.setCurrentWidget(self.question_editor)

    @Slot()
    def show_main(self) -> None:
        self._stack.setCurrentWidget(self.main_screen)

    @Slot()
    def save_game(self) -> None:
        if not self._game_path or not self._game_data:
            return
        if not self.question_editor.validate_questions():
            QMessageBox.warning(self, "Проверка", "Заполните все вопросы и ответы.")
            return
        write_game(self._game_path / "main.json", self._game_data)
        QMessageBox.information(self, "Сохранено", "Игра сохранена.")

    @Slot()
    def open_bonus_editor(self) -> None:
        if not self._game_data:
            return
        self.bonus_editor.load_game(self._game_data)
        self._stack.setCurrentWidget(self.bonus_editor)

    @Slot()
    def return_to_questions(self) -> None:
        if self._game_data:
            self.question_editor.load_game(self._game_data)
        self._stack.setCurrentWidget(self.question_editor)

    @Slot()
    def save_bonus(self) -> None:
        if not self._game_path or not self._game_data:
            return
        self.bonus_editor.update_game(self._game_data)
        write_game(self._game_path / "main.json", self._game_data)
        QMessageBox.information(self, "Сохранено", "Бонусы обновлены.")
        self._stack.setCurrentWidget(self.question_editor)
