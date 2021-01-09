from PyQt5 import QtCore, QtGui, QtWidgets
import main
from functools import partial
import interface

def create_button(window, name, y):
    """Creates a button in the window, having a given name and height

    :param window:
    :param name: the name of the button, like "Maths"
    :param y: the height of the button (depends on the total number of buttons)
    :return: the button in the right shape with the right name
    """
    button = QtWidgets.QPushButton(name, window)
    button.setGeometry(QtCore.QRect(150, y, 300, 30))
    return button

class ManageWindow:
    def __init__(self, subject_list):
        self.title = "FLASHCARDS"
        self.main_window = QtWidgets.QMainWindow()
        self.choice_window = QtWidgets.QMainWindow()
        self.game_window = QtWidgets.QMainWindow()
        self.subject_names = subject_list
        self.subject_buttons = []
        self.lesson_buttons = []
        self.lesson_names_in_subject = []

    def buttons_in_window(self, is_lesson):
        """Creates the buttons corresponding to the list of subjects or lessons we have, and updates the list of buttons

        :return: nothing
        """
        i = 0
        if is_lesson:
            for name in self.lesson_names_in_subject:
                self.lesson_buttons.append(create_button(self.choice_window, name, i * 50))
                i += 1
            self.lesson_buttons.append(create_button(self.choice_window, "Nouvelle leçon",
                                                     len(self.lesson_names_in_subject) * 50))
        else:
            for name in self.subject_names:
                self.subject_buttons.append(create_button(self.choice_window, name, i * 50))
                i += 1
            self.subject_buttons.append(create_button(self.choice_window, "Nouvelle matière",
                                                      len(self.subject_names) * 50))

    def changing_button_list(self, lesson_names_in_subject):
        """ From displaying subjects to displaying lessons

        :param lesson_names_in_subject:
        :return:
        """
        for i in range(len(self.subject_buttons)):
            self.subject_buttons[i].hide()
        self.lesson_names_in_subject = lesson_names_in_subject
        is_lesson = True
        self.lesson_buttons = list()
        self.buttons_in_window(is_lesson)
        for i in range(len(self.lesson_buttons)):
            self.lesson_buttons[i].show()

    def setupUiHomePage(self):
        """ Creates the home page.

        :return:
        """
        play = QtWidgets.QPushButton("Jouer", self.main_window)
        play.setGeometry(QtCore.QRect(150, 50, 300, 30))
        new_card = QtWidgets.QPushButton("Nouvelle carte", self.main_window)
        new_card.setGeometry(QtCore.QRect(150, 100, 300, 30))
        see_cards = QtWidgets.QPushButton("Voir les cartes", self.main_window)
        see_cards.setGeometry(QtCore.QRect(150, 150, 300, 30))

        new_card.clicked.connect(self.HometoChoice)

    def setupUiChoicePage(self):
        """ Creates the window allowing the user to choose the subject he wants to add a flashcard to (after entering
        creation mode)

        :return:
        """
        self.buttons_in_window(False)
        for i, name in enumerate(self.subject_names):
            self.subject_buttons[i].clicked.connect(partial(self.changing_button_list,
                                                            main.lessons_in_subject(name)))

    def HometoChoice(self):
        self.setupUiChoicePage()
        self.choice_window.show()

    def setupUiParamPage(self):
        """ Creates the window allowing the user to choose the subject he wants to work on (after entering game mode)

        :return:
        """
        self.main_window.buttons_in_window()
        self.main_window.new_button_func()

    def setupUiGamePage(self):
        """ Creates the window allowing the user to choose the subject he wants add a flashcard to (after entering
        creation mode)

        :return:
        """
        print("ok")


if __name__ == "__main__":
    import sys

    Subject_list = main.subjects_in_database()
    app = QtWidgets.QApplication(sys.argv)
    ui = ManageWindow(Subject_list)
    ui.setupUiHomePage()
    ui.main_window.window().show()

    sys.exit(app.exec_())
