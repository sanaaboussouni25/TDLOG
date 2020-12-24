from PyQt5 import QtCore, QtGui, QtWidgets
import main
import interface_new_card


class Ui_MainWindow(object):
    def __init__(self):
        # Building the homepage

        self.window_size = [800, 600]  # Size of the main window
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        # Layout containing the buttons
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.layout_size = [60, 80, 681, 401]

        # Main title
        self.main_title = QtWidgets.QLabel(self.centralwidget)
        self.title_size = [370, 30, 58, 16]
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        # 3 main buttons that constitute the homepage
        self.play = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.see_cards = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.create_cards = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.maximum_size = [16777215, 16777215]

        self.enter_subject_label = QtWidgets.QLabel(MainWindow)
        self.enter_subject = QtWidgets.QLineEdit(MainWindow)
        self.new_subject = QtWidgets.QPushButton(MainWindow)
        self.button_list = list()
        self.title = QtWidgets.QLabel(MainWindow)

    def setupUiHomepage(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.window_size[0], self.window_size[1])
        self.centralwidget.setObjectName("Central Widget")
        self.main_title.setGeometry(QtCore.QRect(self.title_size[0], self.title_size[1], self.title_size[2],
                                                 self.title_size[3]))
        self.main_title.setObjectName("Main Title")
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(self.layout_size[0], self.layout_size[1],
                                                             self.layout_size[2], self.layout_size[3]))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("Horizontal Layout")
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.create_cards.sizePolicy().hasHeightForWidth())
        self.create_cards.setSizePolicy(size_policy)
        self.create_cards.setMaximumSize(QtCore.QSize(self.maximum_size[0], self.maximum_size[1]))
        self.create_cards.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.create_cards.setAutoFillBackground(True)
        self.create_cards.setObjectName("Create Cards")
        self.horizontalLayout.addWidget(self.create_cards)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.see_cards.sizePolicy().hasHeightForWidth())
        self.see_cards.setSizePolicy(size_policy)
        self.see_cards.setMaximumSize(QtCore.QSize(self.maximum_size[0], self.maximum_size[1]))
        self.see_cards.setAutoFillBackground(True)
        self.see_cards.setObjectName("See Cards")
        self.horizontalLayout.addWidget(self.see_cards)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.play.sizePolicy().hasHeightForWidth())
        self.play.setSizePolicy(size_policy)
        self.play.setAutoFillBackground(True)
        self.play.setObjectName("play")
        self.horizontalLayout.addWidget(self.play)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.retranslateUi(MainWindow)
        openWindow(self.create_cards, interface_new_card.Dialog)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.main_title.setText(_translate("MainWindow", "Hello !"))
        self.create_cards.setText(_translate("MainWindow", "Create cards"))
        self.see_cards.setText(_translate("MainWindow", "See the cards"))
        self.play.setText(_translate("MainWindow", "Play"))

    def homepageChoice(self, MainWindow):
        self.play.clicked.connect(self.create_cards.close)


def closeWindow(button, window):
    button.clicked.connect(window.close())


def openWindow(button, window):
    button.cliked.connect(window.show())


def hideWidget(button, widget):
    button.cliked.connect(widget.hide())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUiHomepage(MainWindow)
    Dialog = QtWidgets.QDialog()
    ui = interface_new_card.Ui_Dialog()
    ui.interface_new_card.setupUi(Dialog)
    MainWindow.show()
    sys.exit(app.exec_())
