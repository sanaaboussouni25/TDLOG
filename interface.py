from PyQt5 import QtCore, QtGui, QtWidgets
import main

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

def HomePage():
    """ Creates the homepage of the game.

    :return: nothing
    """
    homepage = QtWidgets.QMainWindow()
    play = QtWidgets.QPushButton("Jouer", homepage)
    play.setGeometry(QtCore.QRect(150, 50, 300, 30))
    new_card = QtWidgets.QPushButton("Nouvelle carte", homepage)
    new_card.setGeometry(QtCore.QRect(150, 100, 300, 30))
    see_cards = QtWidgets.QPushButton("Voir les cartes", homepage)
    see_cards.setGeometry(QtCore.QRect(150, 150, 300, 30))

    new_card.clicked.connect(lambda: HometoCreate())
    play.clicked.connect(lambda: HometoGame())
    # see_cards.clicked.connect(HometoDisplay)

    return homepage


def HometoCreate():
    """ Creates another window, using the class ... Seeks the existing subjects in database and shows the new window.

    :return:
    """
    subject_list = main.subjects_in_database()
    creation_manager = ManageCreation(DisplayChoices(QtWidgets.QMainWindow(), subject_list, True))
    CreateWindow = creation_manager.display.window
    CreateWindow.show()


def HometoGame():
    """ Creates another window, using the class ... Seeks the existing subjects in database and shows the new window.

        :return:
    """
    subject_list = main.subjects_in_database()
    GameWindow = QtWidgets.QMainWindow()
    ManageGame(DisplayChoices(GameWindow, subject_list, False))
    GameWindow.show()


class ManageCreation:
    def __init__(self, first_display):
        """

        :param first_display: object from the class DisplayChoices
        """
        self.title = "FLASHCARDS"
        self.display = first_display

    def setupUiHomepage(self, MainWindow):
        self.display.buttons_in_window()
        self.display.new_button_func()


class DisplayChoices:
    def __init__(self, window, list_of_titles, is_subject):
        self.window = window
        self.is_subject = is_subject
        self.list_of_buttons = list()
        self.list_of_titles = list_of_titles

    def buttons_in_window(self):
        i = 0
        for title in self.list_of_titles:
            self.list_of_buttons.append(create_button(self.window, title, i * 50))
            i += 1
        if self.is_subject:
            self.list_of_buttons.append(create_button(self.window, "Nouvelle matière", len(self.list_of_titles) * 50))
        else:
            self.list_of_buttons.append(create_button(self.window, "Nouvelle leçon", len(self.list_of_titles) * 50))


class ManageGame:
    def __init__(self, window_display):
        self.title = "Choix de la matière"

        self.display = window_display


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    homepage = HomePage()
    homepage.show()
    sys.exit(app.exec_())
