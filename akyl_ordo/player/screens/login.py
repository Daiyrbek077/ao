from __future__ import annotations

import hashlib
from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class LoginScreen(QWidget):
    login_success = Signal()

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        title = QLabel("Вход в Akyl Ordo Player")
        title.setStyleSheet("font-size: 24px; font-weight: 700;")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Пароль")
        toggle_button = QPushButton("Показать")
        toggle_button.clicked.connect(self.toggle_password)
        login_button = QPushButton("Войти")
        login_button.clicked.connect(self.check_password)

        pass_layout = QHBoxLayout()
        pass_layout.addWidget(self.password_input)
        pass_layout.addWidget(toggle_button)

        layout.addWidget(title)
        layout.addLayout(pass_layout)
        layout.addWidget(login_button)
        layout.addStretch()

        self._password_path = Path.home() / ".akyl_ordo_password"
        if not self._password_path.exists():
            self._password_path.write_text(self._hash("admin"), encoding="utf-8")

    def toggle_password(self) -> None:
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def check_password(self) -> None:
        stored = self._password_path.read_text(encoding="utf-8").strip()
        if self._hash(self.password_input.text()) == stored:
            self.login_success.emit()

    @staticmethod
    def _hash(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()
