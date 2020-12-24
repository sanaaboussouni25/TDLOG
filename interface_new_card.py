from PyQt5 import QtCore, QtGui, QtWidgets
import main
from functools import partial


class Ui_MainWindow(object):
    def __init__(self):
        self.title = "FLASHCARDS"

    def setupUiHomepage(self, MainWindow, subject_list):
        first_window = type1(subject_list, True, False)
        first_window.buttons_in_window()
        first_window.new_button_func()


class type1(Ui_MainWindow):
    def __init__(self, list_of_titles, listing=False, subject=True):
        self.list = listing
        self.subject = subject
        self.list_of_buttons = list()
        self.list_of_titles = list_of_titles
        self.new_button = QtWidgets.QPushButton(MainWindow)

    def name_button(self, title, y):
        button = QtWidgets.QPushButton(MainWindow)
        button.setGeometry(QtCore.QRect(150, y, 300, 30))
        button.setText(title)
        return button

    def new_button_func(self):
        self.new_button.setGeometry(QtCore.QRect(150, len(self.list_of_titles) * 50, 300, 30))
        if self.list:
            self.new_button.setText("Nouvelle liste")
        if self.subject:
            self.new_button.setText("Nouvelle matiere")

    def buttons_in_window(self):
        i = 0
        for title in self.list_of_titles:
            self.list_of_buttons.append(self.name_button(title, i * 50))
            i += 1


if __name__ == "__main__":
    import sys

    subject_list = main.subjects_in_database()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUiHomepage(MainWindow, subject_list)
    MainWindow.show()
    sys.exit(app.exec_())

# close database
