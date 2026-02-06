from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from akyl_ordo.maker.main_window import MakerWindow


def main() -> None:
    app = QApplication(sys.argv)
    window = MakerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
