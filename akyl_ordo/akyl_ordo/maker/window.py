from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QSplitter,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..common.constants import MAKER_CONFIG
from ..common.models import GameData, Media, Question
from ..common.sound import SoundManager

SCORES = [100, 200, 300, 400, 500]


class NewGameDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("New Game")
        self.setModal(True)
        self.resize(420, 200)

        self.title_input = QLineEdit()
        self.location_input = QLineEdit()
        self.location_input.setReadOnly(True)
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self._browse)

        form = QFormLayout()
        form.addRow("Game Title", self.title_input)

        location_layout = QHBoxLayout()
        location_layout.addWidget(self.location_input)
        location_layout.addWidget(browse_button)

        location_container = QWidget()
        location_container.setLayout(location_layout)
        form.addRow("Parent Folder", location_container)

        self.create_button = QPushButton("Create")
        self.create_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        self.create_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.create_button)
        self.setLayout(layout)

    def _browse(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "Select Parent Folder")
        if directory:
            self.location_input.setText(directory)

    def game_title(self) -> str:
        return self.title_input.text().strip()

    def parent_folder(self) -> str:
        return self.location_input.text().strip()


class MakerWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Akyл Ordo Maker")
        self.resize(1200, 720)

        self.sound = SoundManager()
        self.sound.start_background()

        self.current_game_path: Optional[Path] = None
        self.game_data: Optional[GameData] = None

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home_screen = self._build_home_screen()
        self.editor_screen = self._build_editor_screen()

        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.editor_screen)

        self._load_recent_games()

    def _build_home_screen(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Akyл Ordo Maker")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        new_button = QPushButton("➕ New Game")
        open_button = QPushButton("📂 Open Existing Game")
        for button in (new_button, open_button):
            button.setStyleSheet(
                "padding: 12px; border-radius: 16px; background-color: #3F51B5; color: white;"
            )

        new_button.clicked.connect(self._create_new_game)
        open_button.clicked.connect(self._open_game)

        recent_label = QLabel("Recent Games")
        recent_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.recent_list = QListWidget()
        self.recent_list.itemDoubleClicked.connect(self._open_recent)

        layout.addWidget(title)
        layout.addWidget(new_button)
        layout.addWidget(open_button)
        layout.addWidget(recent_label)
        layout.addWidget(self.recent_list)

        widget.setLayout(layout)
        return widget

    def _build_editor_screen(self) -> QWidget:
        container = QWidget()
        outer_layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        self.game_title_label = QLabel("Game: -")
        self.game_title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        save_button = QPushButton("💾 Save")
        save_button.setStyleSheet("padding: 10px; background-color: #4CAF50; color: white;")
        save_button.clicked.connect(self._save_game)

        header_layout.addWidget(self.game_title_label)
        header_layout.addStretch()
        header_layout.addWidget(save_button)

        splitter = QSplitter()

        self.category_list = QListWidget()
        self.category_list.itemSelectionChanged.connect(self._filter_questions)

        self.question_table = QTableWidget(0, 3)
        self.question_table.setHorizontalHeaderLabels(["Category", "Score", "Question"])
        self.question_table.horizontalHeader().setStretchLastSection(True)
        self.question_table.itemSelectionChanged.connect(self._load_question_to_form)

        form_widget = QWidget()
        form_layout = QFormLayout()

        self.category_input = QLineEdit()
        self.score_input = QComboBox()
        self.score_input.addItems([str(score) for score in SCORES])
        self.timer_input = QComboBox()
        self.timer_input.addItems(["auto", "10", "15", "20", "30", "45", "60"])
        self.question_input = QTextEdit()
        self.answer_input = QTextEdit()

        self.media_buttons = {}
        for key, label in (
            ("img_question", "Add Image (Question)"),
            ("img_answer", "Add Image (Answer)"),
            ("audio_question", "Add Audio (Question)"),
            ("audio_answer", "Add Audio (Answer)"),
            ("video_question", "Add Video (Question)"),
            ("video_answer", "Add Video (Answer)"),
        ):
            button = QPushButton(label)
            button.clicked.connect(lambda _, k=key: self._select_media(k))
            self.media_buttons[key] = button

        form_layout.addRow("Category", self.category_input)
        form_layout.addRow("Score", self.score_input)
        form_layout.addRow("Timer", self.timer_input)
        form_layout.addRow("Question", self.question_input)
        form_layout.addRow("Answer", self.answer_input)
        for button in self.media_buttons.values():
            form_layout.addRow(button)

        form_widget.setLayout(form_layout)

        editor_buttons_layout = QHBoxLayout()
        add_button = QPushButton("➕ Add Question")
        update_button = QPushButton("✏ Update")
        delete_button = QPushButton("🗑 Delete")
        for button in (add_button, update_button, delete_button):
            button.setStyleSheet("padding: 8px; border-radius: 12px; background-color: #2196F3; color: white;")

        add_button.clicked.connect(self._add_question)
        update_button.clicked.connect(self._update_question)
        delete_button.clicked.connect(self._delete_question)

        editor_buttons_layout.addWidget(add_button)
        editor_buttons_layout.addWidget(update_button)
        editor_buttons_layout.addWidget(delete_button)

        right_container = QWidget()
        right_layout = QVBoxLayout()
        right_layout.addWidget(form_widget)
        right_layout.addLayout(editor_buttons_layout)
        right_container.setLayout(right_layout)

        splitter.addWidget(self.category_list)
        splitter.addWidget(self.question_table)
        splitter.addWidget(right_container)
        splitter.setSizes([200, 500, 400])

        outer_layout.addLayout(header_layout)
        outer_layout.addWidget(splitter)
        container.setLayout(outer_layout)

        return container

    def _create_new_game(self) -> None:
        dialog = NewGameDialog(self)
        if dialog.exec() != QDialog.Accepted:
            return
        title = dialog.game_title()
        parent_folder = dialog.parent_folder()
        if not title or not parent_folder:
            QMessageBox.warning(self, "Missing Info", "Please provide a title and parent folder.")
            return

        game_folder = Path(parent_folder) / title
        content_folder = game_folder / "content"
        for sub in ("images", "videos", "audio"):
            (content_folder / sub).mkdir(parents=True, exist_ok=True)

        game_data = GameData(title=title)
        game_data.save(game_folder / "main.json")
        self._open_game_folder(game_folder)

    def _open_game(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "Select Game Folder")
        if directory:
            self._open_game_folder(Path(directory))

    def _open_recent(self, item: QListWidgetItem) -> None:
        path = Path(item.data(Qt.UserRole))
        if path.exists():
            self._open_game_folder(path)

    def _open_game_folder(self, game_folder: Path) -> None:
        main_json = game_folder / "main.json"
        if not main_json.exists():
            QMessageBox.warning(self, "Invalid Game", "main.json not found in this folder.")
            return
        self.current_game_path = game_folder
        self.game_data = GameData.load(main_json)
        self.game_title_label.setText(f"Game: {self.game_data.title}")
        self._refresh_tables()
        self._update_recent_games(game_folder)
        self.stack.setCurrentWidget(self.editor_screen)

    def _refresh_tables(self) -> None:
        self.category_list.clear()
        self.question_table.setRowCount(0)
        if not self.game_data:
            return
        categories = sorted({question.category for question in self.game_data.questions})
        for category in categories:
            self.category_list.addItem(category)
        for question in self.game_data.questions:
            self._add_question_row(question)

    def _add_question_row(self, question: Question) -> None:
        row = self.question_table.rowCount()
        self.question_table.insertRow(row)
        self.question_table.setItem(row, 0, QTableWidgetItem(question.category))
        self.question_table.setItem(row, 1, QTableWidgetItem(str(question.score)))
        self.question_table.setItem(row, 2, QTableWidgetItem(question.question))

    def _filter_questions(self) -> None:
        if not self.game_data:
            return
        selected = self.category_list.selectedItems()
        if not selected:
            self._refresh_tables()
            return
        category = selected[0].text()
        self.question_table.setRowCount(0)
        for question in self.game_data.questions:
            if question.category == category:
                self._add_question_row(question)

    def _load_question_to_form(self) -> None:
        if not self.game_data:
            return
        selected = self.question_table.selectedItems()
        if not selected:
            return
        row = self.question_table.currentRow()
        category = self.question_table.item(row, 0).text()
        score = int(self.question_table.item(row, 1).text())
        question_text = self.question_table.item(row, 2).text()

        for question in self.game_data.questions:
            if question.category == category and question.score == score and question.question == question_text:
                self.category_input.setText(question.category)
                self.score_input.setCurrentText(str(question.score))
                self.timer_input.setCurrentText(question.timer)
                self.question_input.setPlainText(question.question)
                self.answer_input.setPlainText(question.answer)
                self.current_media = question.media
                return

    def _select_media(self, key: str) -> None:
        if not self.current_game_path:
            return
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Media")
        if not file_path:
            return
        file_path = Path(file_path)
        if key.startswith("img"):
            folder = self.current_game_path / "content" / "images"
        elif key.startswith("video"):
            folder = self.current_game_path / "content" / "videos"
        else:
            folder = self.current_game_path / "content" / "audio"
        folder.mkdir(parents=True, exist_ok=True)
        destination = folder / file_path.name
        shutil.copy(file_path, destination)
        if not hasattr(self, "current_media"):
            self.current_media = Media()
        setattr(self.current_media, key, str(destination.relative_to(self.current_game_path)))

    def _build_question_from_form(self) -> Question:
        media = getattr(self, "current_media", Media())
        return Question(
            category=self.category_input.text().strip(),
            score=int(self.score_input.currentText()),
            question=self.question_input.toPlainText().strip(),
            answer=self.answer_input.toPlainText().strip(),
            timer=self.timer_input.currentText(),
            media=media,
        )

    def _add_question(self) -> None:
        if not self.game_data:
            return
        question = self._build_question_from_form()
        if not question.category or not question.question or not question.answer:
            QMessageBox.warning(self, "Missing Fields", "Category, question and answer are required.")
            return
        if any(q.category == question.category and q.score == question.score for q in self.game_data.questions):
            QMessageBox.warning(self, "Duplicate Score", "Each category must have unique scores.")
            return
        self.game_data.questions.append(question)
        self._refresh_tables()
        self._clear_form()

    def _update_question(self) -> None:
        if not self.game_data:
            return
        selected = self.question_table.selectedItems()
        if not selected:
            return
        row = self.question_table.currentRow()
        category = self.question_table.item(row, 0).text()
        score = int(self.question_table.item(row, 1).text())
        question_text = self.question_table.item(row, 2).text()
        updated = self._build_question_from_form()
        for idx, question in enumerate(self.game_data.questions):
            if question.category == category and question.score == score and question.question == question_text:
                self.game_data.questions[idx] = updated
                break
        self._refresh_tables()

    def _delete_question(self) -> None:
        if not self.game_data:
            return
        selected = self.question_table.selectedItems()
        if not selected:
            return
        row = self.question_table.currentRow()
        category = self.question_table.item(row, 0).text()
        score = int(self.question_table.item(row, 1).text())
        question_text = self.question_table.item(row, 2).text()
        self.game_data.questions = [
            q for q in self.game_data.questions if not (q.category == category and q.score == score and q.question == question_text)
        ]
        self._refresh_tables()
        self._clear_form()

    def _clear_form(self) -> None:
        self.category_input.clear()
        self.score_input.setCurrentIndex(0)
        self.timer_input.setCurrentIndex(0)
        self.question_input.clear()
        self.answer_input.clear()
        self.current_media = Media()

    def _save_game(self) -> None:
        if not self.current_game_path or not self.game_data:
            return
        for question in self.game_data.questions:
            if not question.question or not question.answer or not question.category:
                QMessageBox.warning(self, "Validation", "All questions must have category, question, and answer.")
                return
        main_json = self.current_game_path / "main.json"
        self.game_data.save(main_json)
        QMessageBox.information(self, "Saved", "Game saved successfully.")

    def _load_recent_games(self) -> None:
        if MAKER_CONFIG.exists():
            data = json.loads(MAKER_CONFIG.read_text(encoding="utf-8"))
            for path in data.get("recent", []):
                self._add_recent_item(Path(path))

    def _update_recent_games(self, game_folder: Path) -> None:
        existing = [self.recent_list.item(i).data(Qt.UserRole) for i in range(self.recent_list.count())]
        if str(game_folder) in existing:
            return
        self._add_recent_item(game_folder)
        MAKER_CONFIG.write_text(
            json.dumps({"recent": [self.recent_list.item(i).data(Qt.UserRole) for i in range(self.recent_list.count())]}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _add_recent_item(self, path: Path) -> None:
        item = QListWidgetItem(path.name)
        item.setData(Qt.UserRole, str(path))
        self.recent_list.addItem(item)
