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
    creation_window = HometoCreate()
    game_window = HometoGame()
    new_card.clicked.connect(lambda: creation_window.show())
    play.clicked.connect(lambda: game_window.show())
    # see_cards.clicked.connect(HometoDisplay)

    return homepage


def HometoCreate():
    """ Creates another window, using the class ... Seeks the existing subjects in database and shows the new window.

    :return:
    """
    subject_list = main.subjects_in_database()
    creation_manager = ManageCreation(DisplayChoices(QtWidgets.QMainWindow(), subject_list, True))
    CreateWindow = creation_manager.display.window
    return CreateWindow


def HometoGame():
    """ Creates another window, using the class ... Seeks the existing subjects in database and shows the new window.

        :return:
    """
    subject_list = main.subjects_in_database()
    game_manager = ManageGame(DisplayChoices(QtWidgets.QMainWindow(), subject_list, False))
    game_manager.display.display_list_buttons()
    GameWindow = game_manager.display.window
    game_manager.play()
    return GameWindow


class ManageGame:
    def __init__(self, first_display):
        self.title = "GAME"
        self.display = first_display

    def changing_button_list(self, lesson_names_in_subject):
        """ From displaying subjects to displaying lessons

                :param lesson_names_in_subject:
                :return:
                """
        for button in self.display.list_of_buttons:
            button.hide()
        self.display.list_of_titles = lesson_names_in_subject
        self.display.list_of_buttons = list()
        self.display.is_subject = False
        self.buttons_in_window()
        for i in range(len(self.lesson_buttons)):
            self.lesson_buttons[i].show()

    def from_subject_to_lessons(self):
        for i, name in enumerate(self.subject_names):
            self.subject_buttons[i].clicked.connect(partial(self.changing_button_list,
                                                            main.lessons_in_subject(name)))

    def play(self):
        self.from_subject_to_lessons()
        self.display.display_list_buttons()

class ManageCreation:
    def __init__(self, first_display):
        """

        :param first_display: object from the class DisplayChoices
        """
        self.title = "FLASHCARDS"
        self.display = first_display

    def setupUiHomepage(self):
        self.display.buttons_in_window()


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

    def display_list_buttons(self):
        i = 0
        for title in self.list_of_titles:
            self.list_of_buttons.append(create_button(self.window, title, i * 50))
            i += 1


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
