from PyQt6 import QtCore, QtWidgets
from logic import FlashcardManager


class Ui_MainWindow(object):
    """
    basic flashcard UI class
    """

    def setupUi(self, MainWindow: QtWidgets.QMainWindow) -> None:
        """
        create widgets, set properties, and wire up signals
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 400)
        MainWindow.setMinimumSize(QtCore.QSize(500, 400))
        MainWindow.setMaximumSize(QtCore.QSize(500, 450))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #  Title
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 20, 250, 41))
        self.label.setObjectName("label")

        #    Input frame

        self.card_insert_frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.card_insert_frame.setGeometry(QtCore.QRect(150, 80, 230, 141))
        self.card_insert_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.card_insert_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.card_insert_frame.setObjectName("card_insert_frame")

        # "Front"

        self.label_2 = QtWidgets.QLabel(parent=self.card_insert_frame)
        self.label_2.setGeometry(QtCore.QRect(30, 20, 80, 50))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.card_insert_frame)
        self.lineEdit.setGeometry(QtCore.QRect(80, 20, 113, 20))
        self.lineEdit.setObjectName("lineEdit")

        # "Back"

        self.label_3 = QtWidgets.QLabel(parent=self.card_insert_frame)
        self.label_3.setGeometry(QtCore.QRect(40, 70, 31, 16))
        self.label_3.setObjectName("label_3")

        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.card_insert_frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 70, 113, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")

        # Add & Remove buttons
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(140, 240, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(260, 240, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")

        # Next &  Previous
        self.prevButton = QtWidgets.QPushButton("Previous", parent=self.centralwidget)
        self.prevButton.setGeometry(QtCore.QRect(10, 260, 75, 23))
        self.nextButton = QtWidgets.QPushButton("Next", parent=self.centralwidget)
        self.nextButton.setGeometry(QtCore.QRect(415, 260, 75, 23))

        # Stack wiget for front/back pages
        self.stackWidget = QtWidgets.QStackedWidget(parent=self.centralwidget)
        self.stackWidget.setGeometry(QtCore.QRect(10, 300, 480, 90))
        self.stackWidget.setObjectName("stackWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.manager = FlashcardManager()

        # Buttons
        self.pushButton.setText("Add")
        self.pushButton.clicked.connect(self.add_flashcard)
        self.pushButton_2.setText("Remove")
        self.pushButton_2.clicked.connect(self.remove_flashcard)
        self.nextButton.clicked.connect(self.next_card)
        self.prevButton.clicked.connect(self.previous_card)

        # Load initial cards into the stack
        self.load_flashcards()
        # ────────────────────────────────

    def retranslateUi(self, MainWindow: QtWidgets.QMainWindow) -> None:
        """
        set static text on labels and buttons
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Flashcards"))
        self.label.setText(_translate(
            "MainWindow",
            "Enter front and back text below,\n"
            "then press Add. Use Remove to delete,\n"
            "and Next/Previous to flip cards."
        ))
        self.label_2.setText(_translate("MainWindow", "Front"))
        self.label_3.setText(_translate("MainWindow", "Back"))

    def load_flashcards(self) -> None:
        """
        clear and rebuild the stack widget with pages for each card
        """
        while self.stackWidget.count():
            w = self.stackWidget.widget(0)
            self.stackWidget.removeWidget(w)
            w.deleteLater()

        cards = self.manager.load_cards()
        for front, back in cards:
            # front page
            page_f = QtWidgets.QWidget(parent=self.stackWidget)
            lbl_f = QtWidgets.QLabel(front, parent=page_f)
            lbl_f.setGeometry(QtCore.QRect(10, 10, 460, 20))
            self.stackWidget.addWidget(page_f)

            # back page
            page_b = QtWidgets.QWidget(parent=self.stackWidget)
            lbl_b = QtWidgets.QLabel(back, parent=page_b)
            lbl_b.setGeometry(QtCore.QRect(10, 10, 460, 20))
            self.stackWidget.addWidget(page_b)

        if self.stackWidget.count():
            self.stackWidget.setCurrentIndex(0)

    def add_flashcard(self) -> None:
        """
        read inputs, add card via manager, then refresh display
        """

        front: str = self.lineEdit.text().strip()
        back: str = self.lineEdit_2.text().strip()
        if not front or not back:
            QtWidgets.QMessageBox.warning(
                None, "Invalid Input", "Please enter both front and back."
            )
            return

        self.manager.add_card(front, back)
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.load_flashcards()

    def remove_flashcard(self) -> None:
        """
        remove the currently shown card by index and refresh
          """

        idx: int = self.stackWidget.currentIndex()
        card_index: int = idx // 2
        self.manager.remove_card(card_index)
        self.load_flashcards()

    def next_card(self) -> None:
        """
        advance to the next flashcard page

        """
        count: int = self.stackWidget.count()
        if count:
            new_idx: int = (self.stackWidget.currentIndex() + 1) % count
            self.stackWidget.setCurrentIndex(new_idx)

    def previous_card(self) -> None:
        """
        go back to the previous flashcard page
        """

        count: int = self.stackWidget.count()
        if count:
            new_idx: int = (self.stackWidget.currentIndex() - 1) % count
            self.stackWidget.setCurrentIndex(new_idx)
