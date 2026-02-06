from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from akyl_ordo.player.main_window import PlayerWindow


def main() -> None:
    app = QApplication(sys.argv)
    sounds_dir = Path.cwd() / "sounds"
    window = PlayerWindow(sounds_dir)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
