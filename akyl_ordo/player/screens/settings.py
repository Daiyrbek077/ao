from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
    QCheckBox,
)

from akyl_ordo.common.models import GameData


class SettingsScreen(QWidget):
    start_game = Signal(dict)

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        title = QLabel("Настройки игры")
        title.setStyleSheet("font-size: 24px; font-weight: 700;")

        form_box = QGroupBox("Команды")
        form_layout = QFormLayout(form_box)

        self.team_count = QSpinBox()
        self.team_count.setRange(2, 14)
        self.team_count.setValue(2)
        self.team_inputs = [QLineEdit() for _ in range(14)]
        for idx, input_field in enumerate(self.team_inputs, start=1):
            input_field.setPlaceholderText(f"Команда {idx}")
        form_layout.addRow("Количество команд", self.team_count)
        for idx, input_field in enumerate(self.team_inputs, start=1):
            form_layout.addRow(f"Команда {idx}", input_field)

        options_box = QGroupBox("Опции")
        options_layout = QFormLayout(options_box)
        self.timer_toggle = QCheckBox("Включить таймер")
        self.timer_seconds = QSpinBox()
        self.timer_seconds.setRange(10, 120)
        self.timer_seconds.setValue(30)
        self.sound_toggle = QCheckBox("Звук")
        self.sound_toggle.setChecked(True)
        options_layout.addRow(self.timer_toggle)
        options_layout.addRow("Секунд", self.timer_seconds)
        options_layout.addRow(self.sound_toggle)

        start_button = QPushButton("Начать игру")
        start_button.clicked.connect(self.emit_settings)

        layout.addWidget(title)
        layout.addWidget(form_box)
        layout.addWidget(options_box)
        layout.addWidget(start_button)
        layout.addStretch()

        self._game: GameData | None = None

    def load_game(self, game: GameData) -> None:
        self._game = game
        for idx, input_field in enumerate(self.team_inputs, start=1):
            input_field.setText(f"Команда {idx}")

    def emit_settings(self) -> None:
        count = self.team_count.value()
        teams = [self.team_inputs[idx].text() or f"Команда {idx+1}" for idx in range(count)]
        payload = {
            "teams": teams,
            "timer_enabled": self.timer_toggle.isChecked(),
            "timer_seconds": self.timer_seconds.value(),
            "sound": self.sound_toggle.isChecked(),
        }
        self.start_game.emit(payload)
