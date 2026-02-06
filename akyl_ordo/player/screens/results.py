from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from akyl_ordo.player.screens.game_board import TeamState


class ResultsScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        self.title = QLabel("Итоги")
        self.title.setStyleSheet("font-size: 24px; font-weight: 700;")
        self.results_label = QLabel("")
        self.results_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(self.title)
        layout.addWidget(self.results_label)
        layout.addStretch()

    def load_results(self, teams: list[TeamState]) -> None:
        sorted_teams = sorted(teams, key=lambda t: t.score, reverse=True)
        lines = [f"{idx + 1}. {team.name} — {team.score}" for idx, team in enumerate(sorted_teams)]
        self.results_label.setText("\n".join(lines))
