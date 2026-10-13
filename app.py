from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
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
    app.run(debug=True)