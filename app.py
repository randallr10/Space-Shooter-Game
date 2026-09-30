
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

connect = sqlite3.connect('database.db')
connect.execute(
    'CREATE TABLE IF NOT EXISTS LEADERBOARD (username TEXT, scores TEXT)')

@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        username = request.form['username']
        scores = request.form['scores']
        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute("INSERT INTO LEADERBOARD \
            (username, scores) VALUES (?,?)",
                           (username, scores))
            users.commit()
        return render_template("index.html")
    else:
        return render_template('join.html')

@app.route('/leaderboard')
def leaderboard():
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM LEADERBOARD')

    data = cursor.fetchall()
    return render_template('leaderboard.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
