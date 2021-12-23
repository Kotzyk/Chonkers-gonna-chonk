
from cs50 import SQL
import sqlite3
import random
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

CHONK_SCALE = ["A Fine Boi", "He Chomnk", "A Heckin' Chonker",
               "H E F T Y C H O N K", "M E G A C H O N K E R", "OH LAWD HE COMIN"]
AVAILABLE_IMAGE_IDS = set(range(1, 148))


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database
con = SQL('sqlite:///chonkers.db')


# Error message
def apology(message, code=400):
    return render_template('apology.html', message=message)


@app.route('/', methods=["GET", "POST"])
def index():
    # much faster than random.sample from a SET
    cat_id = random.choice(tuple(AVAILABLE_IMAGE_IDS))
    if request.method == "POST":
        user_chonkness = int(request.form.get('chonkness'))
        if session.get("user_id") is None:
            # if user is not logged in, give him a UserId of a very large random number to store their votes
            session["user_id"] = random.randrange(1000000000, 10000000000)
        con.execute('INSERT INTO Ratings (UserId, ImageId, Score) VALUES (?, ?, ?)',
                    session['user_id'], cat_id, user_chonkness)
        user_chonk_message = CHONK_SCALE[user_chonkness]
       # print(chonk_message)
        # get median of community voted chonkness
        community_chonkness = con.execute(
            "SELECT AVG(Score) as chonk FROM Ratings WHERE ImageId = ?", cat_id)
        # round average chonkness to nearest integer value
        community_chonkness = round(community_chonkness[0]['chonk'])
        # assign text to int value
        community_chonk_message = CHONK_SCALE[community_chonkness]
    # check if user already voted for image
    if session.get("user_id") and session.get("user_id") < 1000000000:
        rows = con.execute(
            "SELECT ImageId FROM Ratings WHERE UserId = ?", session["user_id"])
        # parse database rows into a set
        voted_imgs = set([int(rows[x]['ImageId']) for x in range(len(rows)+1)])
        # exclude voted images from appearing again
        remaining_ids = AVAILABLE_IMAGE_IDS - voted_imgs
        # generate new image from remaining
        cat_id = random.choice(tuple(remaining_ids))

    return render_template('index.html', cat_id=cat_id, user_chonk=user_chonk_message, community_chonkness=community_chonk_message)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = con.execute(
            "SELECT * FROM Users WHERE Username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["Password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["UserId"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        if len(con.execute("SELECT * FROM Users WHERE Username = ?", request.form.get("username"))) != 0:
            return apology("Username already exists, please choose another", 400)

        pw_hash = generate_password_hash(request.form.get("password"))

        con.execute("INSERT INTO Users (Username, Password) VALUES (?, ?)",
                    request.form.get("username"), pw_hash)

        return redirect("/login")
    else:
        return render_template("register.html")


@app.route('/skip', methods=["GET", "POST"])
def skip():
    return redirect('/')


@app.route('/leaderboard')
def leaderboard():
    row = con.execute(
        "SELECT TOP 10 COUNT(DISTINCT ImageId) as votes, Username as name, FROM Ratings INNER JOIN Users ON Ratings.UserId = Users.UserId GROUP BY Ratings.UserId ORDER BY votes DESC")
    return render_template('leaderboard.html', rank=range(1, 11), row=row)


if __name__ == '__main__':
    app.run(debug=True)
