from study_gui import *
import sys
from PyQt6 import QtWidgets


def main() -> None:
    """
    start the best application of all time and show the main window
    """
    app: QtWidgets.QApplication = QtWidgets.QApplication(sys.argv)
    MainWindow: QtWidgets.QMainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
