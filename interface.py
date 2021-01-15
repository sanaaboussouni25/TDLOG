from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets
import sql


def create_button(window, layout, name, y):
    """Creates a button in the window, having a given name and height

    :param window:
    :param name: the name of the button, like "Maths"
    :param y: the height of the button (depends on the total number of buttons)
    :return: the button in the right shape with the right name
    """
    button = QtWidgets.QPushButton(name, window)
    button.setGeometry(QtCore.QRect(150, y, 300, 30))
    layout.addWidget(button)

    button.show()
    return button


def create_line_edit(window, layout, label, y):
    """Creates a line edit in the window and its label, having a given name and height

        :param label: the name of the button, like "New window"
        :param window:
        :param y: the height of the button (depends on the total number of buttons)
        :return: the button in the right shape with the right name
        """
    line_edit = QtWidgets.QLineEdit(window)
    line_edit_label = QtWidgets.QLabel(label, window)
    line_edit_label.setGeometry(QtCore.QRect(150, y, 300, 30))
    line_edit_label.show()
    line_edit.show()
    line_edit.setGeometry(QtCore.QRect(150, y + 30, 300, 30))
    layout.addWidget(line_edit_label)
    layout.addWidget(line_edit)

    return line_edit, line_edit_label


def create_text(window, layout, text, x, y):
    text_label = QtWidgets.QLabel(text, window)
    layout.addWidget(text_label)
    text_label.setGeometry(QtCore.QRect(x, y, 250, 30))

    return text_label


def HomePage():
    """ Creates the homepage of the game.

    :return: nothing
    """

    homepage = QtWidgets.QMainWindow()
    wid = QtWidgets.QWidget()
    homepage.setCentralWidget(wid)
    layout = QtWidgets.QVBoxLayout()
    play = QtWidgets.QPushButton("Jouer", homepage)
    play.setGeometry(QtCore.QRect(150, 50, 300, 30))
    layout.addWidget(play)
    new_card = QtWidgets.QPushButton("Nouvelle carte", homepage)
    new_card.setGeometry(QtCore.QRect(150, 100, 300, 30))
    layout.addWidget(new_card)
    see_cards = QtWidgets.QPushButton("Voir les cartes", homepage)
    see_cards.setGeometry(QtCore.QRect(150, 150, 300, 30))
    layout.addWidget(see_cards)
    wid.setLayout(layout)

    new_card.clicked.connect(partial(HometoCreate))
    play.clicked.connect(partial(HometoGame))
    see_cards.clicked.connect(partial(HometoCards))

    return homepage


def HometoCreate():
    """ Creates another window, using the class ... Seeks the existing subjects in database and shows the new window.

    :return:
    """
    subject_list = sql.subjects_in_database()
    window_create = QtWidgets.QMainWindow()
    wid = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout()
    wid.setLayout(layout)
    scroll = QtWidgets.QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setObjectName("scrollArea")
    scroll.setEnabled(True)
    scroll.setWidget(wid)
    window_create.setCentralWidget(scroll)
    creation_manager = ManageCreation(window_create, layout,
                                      DisplayChoices(window_create, layout, subject_list, True, True))
    creation_manager.action_subject()
    CreateWindow = creation_manager.display.window
    CreateWindow.show()


def HometoGame():
    """ Creates another window, using the class ... Seeks the existing subjects in database and shows the new window.

        :return:
    """
    subject_list = sql.subjects_in_database()
    window_game = QtWidgets.QMainWindow()
    wid = QtWidgets.QWidget()

    window_game.setCentralWidget(wid)
    layout = QtWidgets.QVBoxLayout()
    wid.setLayout(layout)
    game_manager = ManageGame(window_game, layout, DisplayChoices(window_game, layout, subject_list, False, False))
    game_manager.event_display_lesson()

    assert isinstance(game_manager.display.window, QtWidgets.QMainWindow)
    GameWindow = game_manager.display.window
    GameWindow.show()


def HometoCards():
    """ Creates another window, using the class ... Seeks the existing subjects in database and shows the new window.

      :return:
      """
    subject_list = sql.subjects_in_database()
    window_card = QtWidgets.QMainWindow()
    wid = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout()
    wid.setLayout(layout)
    scroll = QtWidgets.QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setObjectName("scrollArea")
    scroll.setEnabled(True)
    scroll.setWidget(wid)
    window_card.setCentralWidget(scroll)
    cards_manager = ManageCards(window_card, layout, DisplayChoices(window_card, layout, subject_list, False, False))
    cards_manager.display_subjects()
    assert isinstance(cards_manager.display.window, QtWidgets.QMainWindow)
    CardsWindow = cards_manager.display.window
    CardsWindow.show()


class ManageCards:
    def __init__(self, window, layout, first_display):
        """

        :param first_display: object from the class DisplayChoices
        """
        self.title = create_text(window, layout, "Nouvelle flashcard", 300, 10)
        self.display = first_display
        self.question_data = list()

    def display_subjects(self):
        self.display.buttons_in_window()
        for i in range(len(self.display.list_of_widgets)):
            self.display.list_of_widgets[i].clicked.connect(partial(self.from_subject_to_lesson, i))

    def from_subject_to_lesson(self, i):
        self.title.setText(self.display.list_of_titles[i])
        self.question_data.append(self.display.list_of_titles[i])
        for k in range(len(self.display.list_of_widgets)):
            self.display.list_of_widgets[k].hide()
        new_display = DisplayChoices(self.display.window, self.display.layout,
                                     sql.lessons_in_subject(self.display.list_of_titles[i]), False,
                                     False)
        self.display = new_display
        self.action_lessons()

    def action_lessons(self):
        self.display.buttons_in_window()
        for k in range(len(self.display.list_of_widgets)):
            self.display.list_of_widgets[k].show()
        for i in range(len(self.display.list_of_widgets)):
            self.display.list_of_widgets[i].clicked.connect(partial(self.from_lesson_to_questions, i))

    def from_lesson_to_questions(self, i):
        self.title.setText(self.display.list_of_titles[i])
        self.question_data.append(self.display.list_of_titles[i])
        for k in range(len(self.display.list_of_widgets)):
            self.display.list_of_widgets[k].hide()
        questions_list = sql.get_all_questions(self.question_data[0], self.question_data[1])
        print(questions_list)

        answers_list = sql.get_all_answers(self.question_data[0], self.question_data[1])
        print(answers_list)
        new_display = DisplayCards(self.display.window, self.display.layout,
                                   questions_list, answers_list)
        self.display = new_display
        self.display.display_all_cards()
        self.action_questions()

    def action_questions(self):
        self.display.list_of_widgets[-1].clicked.connect(self.display.window.close)


class ManageCreation:
    def __init__(self, window, layout, first_display):
        """

        :param first_display: object from the class DisplayChoices
        """
        self.title = create_text(window, layout, "Nouvelle flashcard", 300, 10)
        self.display = first_display
        self.new_question_data = list()

    def action_subject(self):
        self.display.buttons_in_window()
        for i in range(len(self.display.list_of_widgets)):
            if i < len(self.display.list_of_widgets) - 1:
                self.display.list_of_widgets[i].clicked.connect(partial(self.from_subject_to_lesson, i))
            if i == len(self.display.list_of_widgets) - 1:
                self.display.list_of_widgets[i].clicked.connect(partial(self.new_subject))

    def new_subject(self):
        for k in range(len(self.display.list_of_widgets)):
            self.display.list_of_widgets[k].hide()
        self.title.setText("Nouvelle matière")
        new_display = EnterText(self.display.window, self.display.layout, "Entrer une nouvelle matière")
        self.display = new_display
        self.display.enter_text_button()
        self.display.assert_button()
        self.display.list_of_widgets[2].clicked.connect(partial(self.add_subject))

    def add_subject(self):
        self.display.content = self.display.list_of_widgets[0].text()
        self.new_question_data.append(self.display.content)
        for k in range(len(self.display.list_of_widgets)):
            self.display.list_of_widgets[k].hide()
        self.new_lesson()

    def new_lesson(self):
        for k in range(len(self.display.list_of_widgets)):
            self.display.list_of_widgets[k].hide()
        self.title.setText("Nouvelle leçon")
        new_display = EnterText(self.display.window, self.display.layout, "Entrer une nouvelle leçon")
        self.display = new_display

        self.display.enter_text_button()
        self.display.assert_button()
        self.display.list_of_widgets[2].clicked.connect(partial(self.add_lesson))

    def add_lesson(self):
        self.display.content = self.display.list_of_widgets[0].text()
        print(self.display.content)
        self.new_question_data.append(self.display.content)
        for k in range(len(self.display.list_of_widgets)):
            self.display.list_of_widgets[k].hide()
        self.new_question()

    def new_question(self):
        for k in range(len(self.display.list_of_widgets)):
            self.display.list_of_widgets[k].hide()
        self.title.setText("Nouvelle question")
        new_display = EnterText(self.display.window, self.display.layout, "Entrer une nouvelle question")
        self.display = new_display
        self.display.enter_text_button()
        self.display.assert_button()
        self.display.list_of_widgets[2].clicked.connect(partial(self.add_question))

    def add_question(self):
        self.display.content = self.display.list_of_widgets[0].text()
        self.new_question_data.append(self.display.content)
        for k in range(len(self.display.list_of_widgets)):
            self.display.list_of_widgets[k].hide()

        self.new_answer()

    def last_step(self):
        for k in range(len(self.display.list_of_widgets)):
            self.display.list_of_widgets[k].hide()
        self.title.setText("Continuer ? ")
        new_display = DisplayChoices(self.display.window, self.display.layout,
                                     ["Nouvelle question dans " + self.new_question_data[1], "Terminé"], False, False)
        self.display = new_display
        self.display.buttons_in_window()
        self.display.list_of_widgets[0].clicked.connect(partial(self.redo))
        self.display.list_of_widgets[1].clicked.connect(partial(self.display.window.close))

    def redo(self):
        self.new_question_data.pop()
        self.new_question_data.pop()
        self.new_question()

    def new_answer(self):

        self.title.setText("Nouvelle réponse pour la question:  " + self.display.content)
        print(self.new_question_data)
        new_display = EnterText(self.display.window, self.display.layout, "Entrer une nouvelle réponse")
        self.display = new_display

        self.display.enter_text_button()
        self.display.assert_button()
        self.display.list_of_widgets[2].clicked.connect(partial(self.add_answer))

    def add_answer(self):
        self.display.content = self.display.list_of_widgets[0].text()

        self.new_question_data.append(self.display.content)
        sql.insert_question(self.new_question_data)
        for k in range(len(self.display.list_of_widgets)):
            self.display.list_of_widgets[k].hide()
        self.last_step()

    def from_subject_to_lesson(self, i):
        self.title.setText(self.display.list_of_titles[i])
        self.new_question_data.append(self.display.list_of_titles[i])
        for k in range(len(self.display.list_of_widgets)):
            self.display.list_of_widgets[k].hide()
        new_display = DisplayChoices(self.display.window, self.display.layout,
                                     sql.lessons_in_subject(self.display.list_of_titles[i]), True,
                                     False)
        self.display = new_display
        self.action_lessons()

    def new_question_i(self, i):
        self.new_question_data.append(self.display.list_of_titles[i])
        for k in range(len(self.display.list_of_widgets)):
            self.display.list_of_widgets[k].hide()
        self.title.setText("Nouvelle question")
        new_display = EnterText(self.display.window, self.display.layout, "Entrer une nouvelle question")
        self.display = new_display
        self.display.enter_text_button()
        self.display.assert_button()
        self.display.list_of_widgets[2].clicked.connect(partial(self.add_question))

    def action_lessons(self):
        self.display.buttons_in_window()
        for k in range(len(self.display.list_of_widgets)):
            self.display.list_of_widgets[k].show()
        for i in range(len(self.display.list_of_widgets)):
            if i < len(self.display.list_of_widgets) - 1:
                self.display.list_of_widgets[i].clicked.connect(partial(self.new_question_i, i))
            if i == len(self.display.list_of_widgets) - 1:
                self.display.list_of_widgets[i].clicked.connect(partial(self.new_lesson))


class ManageGame:
    def __init__(self, window, layout, window_display):
        self.title = create_text(window, layout, "Choisissez la matière à travailler", 200, 10)
        self.layout = layout
        self.display = window_display
        self.chosen_subject = ""
        self.chosen_lesson = ""
        self.game_mode = -1
        self.question_list = []
        self.current_question = 0
        self.score = 0

    def display_lesson(self, i):
        """ Switch the display from showing the subjects to showing the lessons associated to the subject i chosen by
        the user and updates chosen_subject and the title of the window. At the end, it calls the next event.

        :param i: the index of the subject the user has clicked on
        """

        self.chosen_subject = self.display.list_of_titles[i]
        self.title.setText("Choisissez la leçon à travailler")

        for k in range(len(self.display.list_of_widgets)):
            # We need to first hide the existing buttons in the window
            self.display.list_of_widgets[k].hide()
        # We can now create a new display containing the list of lessons
        new_list_of_titles = sql.lessons_in_subject(self.display.list_of_titles[i])
        new_display = DisplayChoices(self.display.window, self.display.layout, new_list_of_titles, False,
                                     False)
        # Updating the display
        self.display = new_display
        self.display.buttons_in_window()

        self.event_display_game_mode()  # A call to the next event in the game

    def event_display_lesson(self):
        """ Activate the first display and creates the following event: clicking on the button of a subject i makes a
        call to the method from_subject_to_lesson(i). """

        self.display.buttons_in_window()  # Activating the first display
        for i in range(len(self.display.list_of_widgets)):
            self.display.list_of_widgets[i].clicked.connect(partial(self.display_lesson, i))

    def display_game_mode(self, i):
        """ Switch the display from showing the lessons to showing the game modes, and updates chosen_lesson and the
        title of the window.

        :param i: the index of the lesson the user has clicked on
        """

        self.chosen_lesson = self.display.list_of_titles[i]
        self.title.setText("Choisissez votre mode de jeu")

        for k in range(len(self.display.list_of_widgets)):
            # We need to first hide the existing buttons in the window
            self.display.list_of_widgets[k].hide()

        # We can now create a new display containing the list of lessons
        new_list_of_titles = ["Aléatoire", "25% les moins réussies", "25% les moins travaillées"]
        new_display = DisplayChoices(self.display.window, self.display.layout, new_list_of_titles, False, False)

        # Updating the display
        self.display = new_display
        self.display.buttons_in_window()

        self.event_display_first_question()  # A call to the next event in the game

    def event_display_game_mode(self):
        """ Creates the following event: clicking on the button of a lesson i makes a call to the method
        display_game_mode(i). """

        for i in range(len(self.display.list_of_widgets)):
            self.display.list_of_widgets[i].clicked.connect(partial(self.display_game_mode, i))

    def creating_question_list(self):
        """ Creates the question list according to the chosen game mode"""
        if self.game_mode == 0:
            self.question_list = sql.random_questions(self.chosen_lesson)
        if self.game_mode == 1:
            self.question_list = sql.missed_questions(self.chosen_lesson)
        if self.game_mode == 2:
            self.question_list = sql.least_asked_questions(self.chosen_lesson)

    def display_first_question(self, i):
        """ Switch the display from showing the game modes to showing the first question, and updates the game mode and
        the title of the window.

        :param i: the index of the game mode the user has clicked on
        """
        self.game_mode = i
        # Initializing
        self.score = 0
        self.current_question = 0
        self.creating_question_list()

        self.title.setText(self.chosen_subject + " - " + self.chosen_lesson + " - Question 1/"
                           + str(len(self.question_list)) + "\n" + "Score : 0/" + str(len(self.question_list)))

        for k in range(len(self.display.list_of_widgets)):
            # We need to first hide the existing buttons in the window
            self.display.list_of_widgets[k].hide()

        new_display = EnterText(self.display.window, self.display.layout, self.question_list[0])
        self.display = new_display
        self.display.enter_text_button()
        self.display.assert_button()

        # Makes a call to the next event by clicking on "Valider"
        self.display.list_of_widgets[2].clicked.connect(partial(self.display_verify_answer))

    def event_display_first_question(self):
        """ Creates the following event: clicking on the button of a game mode i makes a call to the method
        display_first_question(i). """

        for i in range(len(self.display.list_of_widgets)):
            self.display.list_of_widgets[i].clicked.connect(partial(self.display_first_question, i))

    def display_verify_answer(self):
        """ Collects the answer given by the user and compare it with the answer in the database. If it is the same, it
        calls display_next_question. If not, it creates a display where the user is asked if he/she were right (in order
        to manage typo errors).

        :return: nothing
        """

        self.display.text = self.display.list_of_widgets[0].text()  # Collecting the answer given by the user
        is_right, answer = sql.is_answer_right(self.question_list[self.current_question], self.display.text)

        if is_right:
            self.display_next_question(True)

        else:
            for k in range(len(self.display.list_of_widgets)):
                self.display.list_of_widgets[k].hide()

            self.title.setText("La réponse était : " + str(answer) + ". Aviez-vous juste ?")
            new_display = DisplayChoices(self.display.window, self.display.layout, ["Oui", "Non"], False, False)
            # Updating the display
            self.display = new_display
            self.display.buttons_in_window()

            # Makes a call to the next event by clicking on Yes or No
            self.display.list_of_widgets[0].clicked.connect(partial(self.display_next_question, True))
            self.display.list_of_widgets[1].clicked.connect(partial(self.display_next_question, False))

    def display_next_question(self, is_right):
        """ Updates in the database the number of correct answers of the previous question, updates the title of the
        window and the display to show the next question. At the end, makes a call to the method display_verify_answer.
        If it is the last question, it updates the score and calls the method display_finish_quiz.

        :param is_right: boolean indicating if the user was right about the previous question
        :return: nothing
        """
        if self.current_question >= len(self.question_list) - 1:
            if is_right:
                sql.update_nb_rights(self.question_list[self.current_question])
                self.score += 1
            self.display_finish_quiz()

        else:
            for k in range(len(self.display.list_of_widgets)):
                self.display.list_of_widgets[k].hide()

            if is_right:
                sql.update_nb_rights(self.question_list[self.current_question])
                self.score += 1
            self.current_question += 1
            self.title.setText(self.chosen_subject + " - " + self.chosen_lesson + " - " + "Question "
                               + str(self.current_question + 1) + "/" + str(len(self.question_list))
                               + "\n" + "Score : " + str(self.score) + "/"
                               + str(len(self.question_list)))

            new_display = EnterText(self.display.window, self.display.layout, self.question_list[self.current_question])
            self.display = new_display
            self.display.enter_text_button()
            self.display.assert_button()

            self.display.list_of_widgets[2].clicked.connect(partial(self.display_verify_answer))  # Makes a call to the
            # next event by clicking on "Valider"

    def display_finish_quiz(self):
        """ Print the final score, and allows the user to restart a quiz with the same parameters or to close the game
        window.

        :return:
        """
        for k in range(len(self.display.list_of_widgets)):
            self.display.list_of_widgets[k].hide()

        self.title.setText("Votre score final : " + str(self.score) + "/" + str(len(self.question_list))
                           + " . Voulez-vous recommencer ?")
        new_display = DisplayChoices(self.display.window, self.display.layout, ["Recommencer", "Terminer"],
                                     False, False)
        # Updating the display
        self.display = new_display
        self.display.buttons_in_window()

        # Makes a call to the next event by clicking on Yes or No
        self.display.list_of_widgets[0].clicked.connect(partial(self.display_first_question, self.game_mode))
        self.display.list_of_widgets[1].clicked.connect(partial(self.display.window.close))


class DisplayCards:
    """
            :param window: the window where the choices are displayed
            :param layout: the layout where the choices are put
            :param questions: questions to be displayed
            :param answers: answers to be displayed
            :param list_of_widgets: collects all the widgets created
            :param layout2: grid layout (attached to self.layout) that enables us to display cards into a grid
            """

    def __init__(self, window, layout, questions_list, answers_list):
        self.window = window
        self.layout = layout
        self.questions = questions_list
        self.answers = answers_list
        self.list_of_widgets = list()
        self.layout2 = QtWidgets.QGridLayout()

    def display_one_card(self, i):
        question_text = QtWidgets.QLabel(self.questions[i], self.window)
        question_text.setAlignment(QtCore.Qt.AlignCenter)
        question_text.setStyleSheet("""
        QWidget {
            border: 1px solid black;
            border-radius: 5px;
            background-color: rgb(255, 255, 255);
            }
        """)
        answer_text = QtWidgets.QLabel(self.answers[i], self.window)
        answer_text.setAlignment(QtCore.Qt.AlignCenter)
        answer_text.setStyleSheet("""
                QWidget {
                    border: 1px solid black;
                    border-radius: 5px;
                    }
                """)
        delete_button = QtWidgets.QPushButton("Supprimer la question", self.window)
        self.layout2.addWidget(question_text, i, 0)
        self.layout2.addWidget(answer_text, i, 1)
        self.layout2.addWidget(delete_button, i, 2)
        self.list_of_widgets.append(question_text)
        self.list_of_widgets.append(answer_text)
        self.list_of_widgets.append(delete_button)

    def display_all_cards(self):
        self.layout.addLayout(self.layout2)
        for i in range(len(self.questions)):
            self.display_one_card(i)
        end_button = create_button(self.window, self.layout, "Retour à la page d'accueil", 200)
        self.list_of_widgets.append(end_button)


class EnterText:
    """
            :param window: the window where the choices are displayed
            :param layout: the layout where the choices are put
            :param label : label displays which indicate the content to be entered by the user
            :param list_of_widgets: collects all the widgets created
            :param content: collects the text entered by the user

            """

    def __init__(self, window, layout, label):
        self.window = window
        self.layout = layout
        self.label = label
        self.list_of_widgets = list()
        self.content = ""

    def assert_button(self):
        self.list_of_widgets.append(create_button(self.window, self.layout, "Valider", 200))

    def enter_text_button(self):
        w1, w2 = create_line_edit(self.window, self.layout, self.label, 100)
        self.list_of_widgets.append(w1)
        self.list_of_widgets.append(w2)


class DisplayChoices:
    def __init__(self, window, layout, list_of_titles, is_new, is_subject):
        """

        :param window: the window where the choices are displayed
        :param layout: the layout where the choices are put
        :param list_of_titles: the list containing the titles of the choices (like the list of subjects)
        :param is_new: allow to choose to create a button "new" (so the class can be used by ManageCreation AND
        ManageGame
        :param is_subject: allow to choose between the button "Nouvelle matière" and the button "Nouvelle leçon"
        """
        self.window = window
        self.layout = layout
        self.is_subject = is_subject
        self.list_of_widgets = list()
        self.list_of_titles = list_of_titles
        self.is_new = is_new

    def buttons_in_window(self):
        i = 0

        for title in self.list_of_titles:
            self.list_of_widgets.append(create_button(self.window, self.layout, title, 50 + i * 50))
            i += 1
        if self.is_new:
            if self.is_subject:
                self.list_of_widgets.append(
                    create_button(self.window, self.layout, "Nouvelle matière", 50 + len(self.list_of_titles) * 50))
            else:
                self.list_of_widgets.append(
                    create_button(self.window, self.layout, "Nouvelle leçon", 50 + len(self.list_of_titles) * 50))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    the_homepage = HomePage()
    the_homepage.show()
    sys.exit(app.exec_())
