from functools import partial

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
    button.show()
    return button

def create_line_edit(window, label, y):
    """Creates a line edit in the window and its label, having a given name and height

        :param window:
        :param name: the name of the button, like "New window"
        :param y: the height of the button (depends on the total number of buttons)
        :return: the button in the right shape with the right name
        """
    line_edit = QtWidgets.QLineEdit(window)
    line_edit_label = QtWidgets.QLabel(label,window)
    line_edit_label.setGeometry(QtCore.QRect(150, y, 300, 30))
    line_edit_label.show()
    line_edit.show()
    line_edit.setGeometry(QtCore.QRect(150, y+30, 300, 30))
    return line_edit

def create_text(window, text, x,y):
    text_label = QtWidgets.QLabel(text,window)
    text_label.setGeometry(QtCore.QRect(x, y, 250, 30))
    return text_label




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
    HC = HometoCreate()
    new_card.clicked.connect(partial(HC.show))
    play.clicked.connect(partial(HometoGame))
    # see_cards.clicked.connect(HometoDisplay)

    return homepage


def HometoCreate():
    """ Creates another window, using the class ... Seeks the existing subjects in database and shows the new window.

    :return:
    """
    subject_list = main.subjects_in_database()
    window_create=QtWidgets.QMainWindow()

    creation_manager = ManageCreation(window_create,DisplayChoices(window_create, subject_list, True))

    creation_manager.action_subject()
    CreateWindow = creation_manager.display.window
    return CreateWindow


def HometoGame():
    """ Creates another window, using the class ... Seeks the existing subjects in database and shows the new window.

        :return:
    """
    subject_list = main.subjects_in_database()
    GameWindow = QtWidgets.QMainWindow()
    ManageGame(DisplayChoices(GameWindow, subject_list, False))
    GameWindow.show()


class ManageCreation:
    def __init__(self, window, first_display):
        """

        :param first_display: object from the class DisplayChoices
        """
        self.title =  create_text(window,"Nouvelle flashcard", 300, 10)
        self.display = first_display





    def action_subject(self):
        self.display.buttons_in_window()
        for i in range(len(self.display.list_of_buttons)):
            if i < len(self.display.list_of_buttons) - 1:
                self.display.list_of_buttons[i].clicked.connect(partial(self.from_subject_to_lesson,i))
            if i == len(self.display.list_of_buttons) - 1 :
                self.display.list_of_buttons[i].clicked.connect(partial(self.new_lesson))


    def new_lesson(self):
        for k in range(len(self.display.list_of_buttons)):
            self.display.list_of_buttons[k].hide()
        self.title.setText("Nouvelle leçon")
        new_display= EnterText(self.display.window, "Entrer une nouvelle leçon" )
        self.display= new_display
        self.display.assert_button()
        line_edit= self.display.enter_text_button()


    def from_subject_to_lesson(self,i):
        self.title.setText(self.display.list_of_titles[i])

        for k in range(len(self.display.list_of_buttons)):
            self.display.list_of_buttons[k].hide()
        new_display = DisplayChoices(self.display.window,main.lessons_in_subject(self.display.list_of_titles[i]),False)
        self.display = new_display
        self.display.buttons_in_window()
        #for k in range(len(self.display.list_of_buttons)):
            #self.display.list_of_buttons[k].show()





class EnterText:
    def __init__(self, window, label):
        self.window = window
        self.label= label
        self.content = ""

    def assert_button(self):
        create_button(self.window, "Valider", 400)

    def enter_text_button(self):
        return create_line_edit(self.window, self.label, 100)




class DisplayChoices:
    def __init__(self, window, list_of_titles, is_subject):
        self.window = window
        self.is_subject = is_subject
        self.list_of_buttons = list()
        self.list_of_titles = list_of_titles

    def buttons_in_window(self):
        i = 0

        for title in self.list_of_titles:
            self.list_of_buttons.append(create_button(self.window, title,50+ i * 50))
            i += 1
        if self.is_subject:
            self.list_of_buttons.append(create_button(self.window, "Nouvelle matière", 50+ len(self.list_of_titles) * 50))
        else:
            self.list_of_buttons.append(create_button(self.window, "Nouvelle leçon", 50+ len(self.list_of_titles) * 50))


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
