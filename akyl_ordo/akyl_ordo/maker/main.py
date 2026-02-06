from PySide6.QtWidgets import QApplication

from .window import MakerWindow


def main() -> None:
    app = QApplication([])
    window = MakerWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
