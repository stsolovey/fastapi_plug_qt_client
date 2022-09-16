"""import os
import requests

#from mainwindow import label

url = 'http://127.0.0.1:9005'


def register(login, passw):
    # login = inputboxLogin.text()
    # passw = inputboxPassword.text()
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
    # login = inputboxLogin.text()
    # passw = inputboxPassword.text()
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
    return False"""



