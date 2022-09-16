# This Python file uses the following encoding: utf-8
import sys
import os.path

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit
from PySide6.QtWidgets import QLabel, QFrame, QTextEdit
from PySide6.QtGui import QTextCursor
import requests


url = 'http://127.0.0.1:9005'
token = 'None'
global exercise_id


def register(login, passw):
    path = '/register'
    params = {'login': login, 'password': passw}
    r = requests.get(url+path, params=params)
    data = r.json()
    print(data)

    if data['status'] is True:
        token = data['token']
        write_token_to_file(token)
        write_to_lable(token)
        return token
    return False


def write_token_to_file(token):
    with open('token.dt', 'w') as fp:
        fp.write(token)


def write_to_lable(token):
    c = 0
    for symb in token:
        if c % 50 == 0:
            token = token[:c] + "\n" + token[c:]
        c += 1

    label.setText("token: " + token)


def loginer(login, passw):
    path = '/login'
    params = {'login': login, 'password': passw}
    r = requests.get(url+path, params=params)
    data = r.json()
    print(data)
    if data['status'] is True:
        token = data['token']
        write_token_to_file(token)
        write_to_lable(token)
        return token
    return False


def read_token_from_file():
    if os.path.exists('token.dt') is False:
        write_to_lable("There is no token yet.")
    with open('token.dt', 'r') as fp:
        token = fp.read()
    return token


def get_exercise():
    labelCheckedAnswer.setText("")
    textEditAnswer.setText("")

    token = read_token_from_file()
    print(token)
    path = '/exercise'
    params = {'token': token}
    r = requests.get(url+path, params=params)
    print(r)
    print(r.text)
    data = r.json()
    print(data)
    if data['status'] is True:
        textEditExercise.setText(data['sentence'])
        global exercise_id
        exercise_id = data['exercise_id']
        print('exercise_id: ', exercise_id)
        return data['exercise_id']
    return False


def check_answer(token, exercise_id, sentence):
    print(token)
    print(exercise_id)
    print(sentence)
    path = '/translate'
    params = {'token': token, 'exercise_id': exercise_id, 'translation': sentence}
    r = requests.get(url+path, params=params)
    data = r.json()
    print(data)

    strng = ""
    sentence = "sentence: " + data['sentence']
    translation = "translation: " + data['translation']
    answer = "answer: " + data['answer']
    distanse = "distanse: " + str(data['distanse'])
    time = "time: " + str(data['time'])
    comment = "comment: " + data['comment']
    strng = "\n".join([sentence, translation, answer, distanse, time, comment])
    labelCheckedAnswer.setText(strng)

    return False


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.setWindowTitle("Qt Python Plug-Client")

    window.setMinimumHeight(620)
    window.setMinimumWidth(390)

    buttonReg = QPushButton("Register", window)
    buttonLogin = QPushButton("Login", window)
    buttonGetExercise = QPushButton("Get Exercise", window)
    buttonCheck = QPushButton("Check", window)
    buttonNext = QPushButton("Next", window)

    textEditAnswer = QTextEdit(window)
    textEditAnswer.setPlaceholderText('Translate your exercise')

    textEditExercise = QTextEdit(window)
    textEditExercise.setReadOnly(True)

    font = textEditExercise.font()
    font.setFamily("Courier")
    font.setPointSize(10)
    textEditExercise.moveCursor(QTextCursor.End)
    textEditExercise.setCurrentFont(font)
    textEditExercise.setPlaceholderText('Here will be your exercise')

    labelCheckedAnswer = QLabel(window)

    inputboxLogin = QLineEdit(window)
    inputboxLogin.setPlaceholderText("Login")

    inputboxPassword = QLineEdit(window)
    inputboxPassword.setPlaceholderText("Password")

    label = QLabel(window)
    label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
    label.setWordWrap(True)
    label.setMinimumHeight(80)
    label.setMinimumWidth(350)
    label.setText("token: None")

    buttonReg.move(10, 10)
    buttonLogin.move(10, 50)
    buttonGetExercise.move(10, 180)
    buttonCheck.move(10, 410)
    buttonNext. move(140, 410)

    textEditExercise.move(10, 220)
    textEditExercise.setMinimumHeight(80)
    textEditExercise.setMinimumWidth(350)

    textEditAnswer.move(10, 320)
    textEditAnswer.setMinimumHeight(80)
    textEditAnswer.setMinimumWidth(350)

    labelCheckedAnswer.move(10, 450)
    labelCheckedAnswer.setMinimumHeight(180)
    labelCheckedAnswer.setMinimumWidth(350)
    labelCheckedAnswer.setWordWrap(True)

    inputboxLogin.move(140, 10)
    inputboxLogin.setMinimumWidth(200)
    inputboxPassword.move(140, 50)
    inputboxPassword.setMinimumWidth(200)

    label.move(10, 90)

    buttonReg.clicked.connect(lambda: register(
        inputboxLogin.text(),
        inputboxPassword.text()))

    buttonLogin.clicked.connect(lambda: loginer(
        inputboxLogin.text(),
        inputboxPassword.text()))

    buttonGetExercise.clicked.connect(get_exercise)

    buttonCheck.clicked.connect(lambda: check_answer(
        read_token_from_file(),
        exercise_id,
        textEditAnswer.toPlainText()))

    buttonNext.clicked.connect(get_exercise)

    token = read_token_from_file()
    write_to_lable(token)

    window.show()

    sys.exit(app.exec())
