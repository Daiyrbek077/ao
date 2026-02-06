from PySide6.QtWidgets import QApplication

from .window import PlayerWindow


def main() -> None:
    app = QApplication([])
    window = PlayerWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
