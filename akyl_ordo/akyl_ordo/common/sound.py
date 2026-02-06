from __future__ import annotations

from pathlib import Path
from typing import Optional

from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer

from .constants import SOUNDS_DIR


class SoundManager:
    def __init__(self) -> None:
        self._audio_output = QAudioOutput()
        self._audio_output.setVolume(0.3)
        self._player = QMediaPlayer()
        self._player.setAudioOutput(self._audio_output)
        self._bg_player = QMediaPlayer()
        self._bg_output = QAudioOutput()
        self._bg_output.setVolume(0.2)
        self._bg_player.setAudioOutput(self._bg_output)
        self._bg_player.setLoops(QMediaPlayer.Infinite)

    def set_volume(self, value: float) -> None:
        self._audio_output.setVolume(value)
        self._bg_output.setVolume(max(0.05, value * 0.6))

    def _play_file(self, filename: str, player: QMediaPlayer) -> None:
        path = SOUNDS_DIR / filename
        if not path.exists():
            return
        player.setSource(QUrl.fromLocalFile(str(path)))
        player.play()

    def play_click(self) -> None:
        self._play_file("click.wav", self._player)

    def play_correct(self) -> None:
        self._play_file("correct.wav", self._player)

    def play_wrong(self) -> None:
        self._play_file("wrong.wav", self._player)

    def play_bonus(self) -> None:
        self._play_file("bonus.wav", self._player)

    def play_bonus_gold(self) -> None:
        self._play_file("bonus_gold.wav", self._player)

    def start_background(self) -> None:
        self._play_file("bg_music.mp3", self._bg_player)

    def stop_background(self) -> None:
        self._bg_player.stop()

    def set_enabled(self, enabled: bool) -> None:
        volume = 0.3 if enabled else 0.0
        self.set_volume(volume)
