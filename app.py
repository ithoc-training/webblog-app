from flask import Flask, request, render_template_string
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def home():
    return '''
        <h1>Anmeldung</h1>
        <form action="/login" method="POST">
            <label>Benutzername:</label>
            <input type="text" name="username" />
            <label>Kennwort:</label>
            <input type="password" name="password" />
            <input type="submit" value="Los" />
        </form>
    '''


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    headers = {'Content-Type': 'application/json'}
    response = requests.request('POST',
                                'http://localhost:5001/login',
                                json={'username': username, 'password': password},
                                headers=headers)
    logging.debug(f'response: {response}')

    logged_in: bool = response.json()['success']
    if logged_in:
        return render_template_string('''
        <h1>Dashboard</h1>
        <p>Willkommen zurück, {{ username }}</p>
        ''', username=username)
    else:
        return render_template_string('''
        <p>Anmeldung fehlgeschlagen</p>
        ''')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
