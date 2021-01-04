import sqlite3
import datetime
import random as rd
import math

MyData = sqlite3.connect('MyDataBase.db')
cursor = MyData.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS base(
 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
 subject TEXT,
 lesson_name TEXT,
 question TEXT,
 answer TEXT, 
 question_type TEXT,
 nbr_asked INTEGER,
 nbr_right INTEGER)''')


def new_question():
    # Allows the user to add a new question and its answer
    cursor.execute('SELECT DISTINCT subject FROM base ')
    current_subjects = [str(m[0]) for m in cursor.fetchall()]
    print("Your subjects", current_subjects)
    subject = input("Subject: ")
    if subject in current_subjects:
        cursor.execute('SELECT DISTINCT lesson_name FROM base WHERE subject=?', (subject,))
        current_lessons = [str(l[0]) for l in cursor.fetchall()]
        print("Your lessons", current_lessons)
        lesson_name = input("Name of the lesson: ")
        if lesson_name in current_lessons:
            cursor.execute('SELECT DISTINCT question FROM base WHERE subject=? AND lesson_name=?',
                           (subject, lesson_name,))
            current_questions = [str(l[0]) for l in cursor.fetchall()]
            print("Your questions", current_questions)
    else:
        cursor.execute('SELECT DISTINCT lesson_name FROM base WHERE subject=?', (subject,))
        current_lessons = [str(l[0]) for l in cursor.fetchall()]
        print("Your lessons", current_lessons)
        lesson_name = input("Name of the new lesson: ")
    new = input("Do you want to enter a new question ? Answer with yes or no.")
    if new == "no":
        return None
    question = input("Enter the question: ")
    answer = input("Enter the answer: ")

    '''Deviner le type de la question'''
    if type(answer) == int or type(answer) == float:
        question_type = "integer"
    elif type(answer) == datetime.date:
        question_type = "date"
    else:
        question_type = "text"

    q_r = (subject, lesson_name, question, answer, question_type, 0, 0)
    cursor.execute(
        'INSERT INTO base (subject, lesson_name, question, answer, question_type,nbr_asked,nbr_right) VALUES '
        '(?,?,?,?,?,?,?) ',
        q_r)
    MyData.commit()


def choose_game_param():
    cursor.execute('SELECT DISTINCT subject FROM base ')
    current_subjects = [str(m[0]) for m in cursor.fetchall()]
    print("Your subjects", current_subjects)
    subject_select = str(input("Which subject do you want to work on? "))
    while subject_select not in current_subjects:
        print("This subject does not exist.")
        subject_select = input("Which subject do you want to work on? ")
    cursor.execute('SELECT DISTINCT lesson_name FROM base WHERE subject=?', (subject_select,))
    current_lessons = [str(l[0]) for l in cursor.fetchall()]
    print("Your lessons", current_lessons)
    lesson_select = str(input("Which lesson do you want to work on? "))
    while lesson_select not in current_lessons:
        print("This lesson does not exist.")
        lesson_select = str(input("Which lesson do you want to work on? "))
    mode = int(input("Choose your game mode : 1 = random, 2 = 25% most missed questions, "
                     "3 = 25% least asked questions"))
    question_list = []
    if mode == 1:
        number = int(input("How many questions do you want to be asked?"))
        cursor.execute('SELECT DISTINCT question FROM base WHERE lesson_name = ?',
                       (lesson_select,))
        results = cursor.fetchall()
        for i in range(number):
            # results are then randomly chosen
            question_list.append(results.pop(rd.randrange(0, len(results)))[0])

    if mode == 2:
        cursor.execute('SELECT DISTINCT question, nbr_asked, nbr_right FROM base WHERE lesson_name = ?',
                       (lesson_select,))
        results = cursor.fetchall()
        ratios = []
        for i, r in enumerate(results):
            if r[1] == 0:
                ratios.append((0, i))
            else:
                ratios.append((r[2] / r[1], i))
        ratios = sorted(ratios)

        for x in ratios[:math.ceil(len(ratios) / 4)]:
            question_list.append(results[x[1]][0])

    if mode == 3:
        cursor.execute('SELECT DISTINCT question, nbr_asked FROM base WHERE lesson_name = ? ORDER BY nbr_asked ASC',
                       (lesson_select,))
        results = cursor.fetchall()
        for r in results[:math.ceil(len(results) / 4)]:
            question_list.append(r[0])
    return question_list


def is_answer_right(question, answer):
    cursor.execute('SELECT answer, nbr_asked, nbr_right FROM base WHERE question=?', (question,))
    result = cursor.fetchall()
    print(result)
    cursor.execute('UPDATE base SET nbr_asked = nbr_asked +1 WHERE question=?', (question,))
    print("Nb of times asked: " + str(result[0][1]))
    MyData.commit()
    if isinstance(answer, (int, float)):
        if result[0][0] == answer:
            return True
        return 'False, the right answer was ' + str(result[0][0])
    else:
        check = input('The answer was ' + str(result[0][0]) + ', were you right?')
        if check == 'Yes':
            cursor.execute('UPDATE base SET nbr_right = nbr_right +1 WHERE question=?', (question,))
            MyData.commit()
            print("Well done")
        else:
            print("A bit of studying wouldn't hurt you...")
    print("Nb of times you got it right: " + str(result[0][2]))


# Lorsqu'on lui demande si il a eu juste et qu'il répond oui, inclure sa réponse
# comme nouvelle alternative à la question ?

def new_subject(text):
    print(text)


def subjects_nb():
    cursor.execute('SELECT COUNT (DISTINCT subject)  FROM base ')
    result = cursor.fetchall()
    return result[0][0]


def lessons_nb(subject):
    cursor.execute('SELECT COUNT (DISTINCT lesson_name)  FROM base WHERE subject=?', (subject,))
    result = cursor.fetchall()
    return result[0][0]


def subject_name(i):
    cursor.execute('SELECT DISTINCT subject FROM base')
    result = cursor.fetchall()
    return result[i][0]


def lesson_name(i, subject):
    cursor.execute('SELECT DISTINCT lesson_name FROM base WHERE subject=?', (subject,))
    result = cursor.fetchall()
    print(result)
    return result[i][0]


def subjects_in_database():
    cursor.execute('SELECT DISTINCT subject FROM base')
    result = cursor.fetchall()
    return [elem[0] for elem in result]

def lessons_in_subject(subject):
    results = []
    for i in range(lessons_nb(subject)):
        results.append(lesson_name(i, subject))
    return results

if __name__ == "__main__":
    new_question()
    #choose_game_param()
    #subjects_nb = subjects_nb()
    #subjects_list = [subject_name(i) for i in range(subjects_nb)]
