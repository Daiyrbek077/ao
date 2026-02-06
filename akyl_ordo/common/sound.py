from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer


class SoundSystem:
    def __init__(self, sounds_dir: Path) -> None:
        self.sounds_dir = sounds_dir
        self._audio_output = QAudioOutput()
        self._audio_output.setVolume(0.5)
        self._player = QMediaPlayer()
        self._player.setAudioOutput(self._audio_output)

    def set_volume(self, volume: float) -> None:
        self._audio_output.setVolume(volume)

    def play(self, filename: str) -> None:
        file_path = self.sounds_dir / filename
        if not file_path.exists():
            return
        self._player.setSource(QUrl.fromLocalFile(str(file_path)))
        self._player.play()
