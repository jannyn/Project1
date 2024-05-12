from logic import *


def main() -> None:
    """
    main program that loads the UI
    """
    application = QApplication([])
    window = Logic()
    window.show()
    application.exec()


if __name__ == '__main__':
    main()