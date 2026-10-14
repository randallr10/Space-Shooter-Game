from flask import Flask,render_template, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
@app.route('/leaderboard')
def participants():
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM LEADERBOARD')

    data = cursor.fetchall()
    return render_template("leaderboard.html", data=data)

@app.route('/submit_score', methods=['POST'])
def submit_score():
    username = request.json['username']
    scores = request.json['scores']

    with sqlite3.connect("database.db") as users:
        cursor = users.cursor()
        cursor.execute("INSERT INTO LEADERBOARD \
        (username, scores) VALUES (?,?)",
                       (username, scores))
        users.commit()
        return {'Username': username, 'Score': scores}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)