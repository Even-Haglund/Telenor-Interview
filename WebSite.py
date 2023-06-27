from flask import *
import sqlite3

#connect the SQLite Database as read-only
db = sqlite3.connect("file:database.db?mode=ro", check_same_thread=False, uri=True)
readCur = db.cursor()

app = Flask(__name__)

#create a simple route to the home page
@app.route("/")
def Home():
    return render_template('Home.html')

@app.route("/Table", methods=["GET", "POST"])
def Table():
    listData = []
    dataSelect = readCur.execute("SELECT * FROM Telenor")
    for lines in dataSelect:
        listData.append(lines)
    return render_template("Search.html", ListData=listData)


if __name__ == "__main__":
    app.secret_key = '9597975'
    app.run(debug=False)