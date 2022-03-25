import random
from tempfile import mkdtemp
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
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


@app.route('/', endpoint='index')
def index():
    # much faster than random.sample from a SET
    if not request.args.get('cat_id'):
        cat_id = random.choice(tuple(AVAILABLE_IMAGE_IDS))
        # check if user already voted for image
        if session.get("user_id") and session.get("user_id") < 10000000000:
            rows = con.execute(
                "SELECT ImageId FROM Ratings WHERE UserId = ?", session["user_id"])
            # parse database rows into a set
            if len(rows) > 0:
                voted_imgs = {int(rows[x]['ImageId'])
                              for x in range(len(rows))}
                # exclude voted images from appearing again
                remaining_ids = AVAILABLE_IMAGE_IDS - voted_imgs
                # generate new image from remaining
                cat_id = random.choice(tuple(remaining_ids))
    else:
        cat_id = request.args.get('cat_id')

    if not session.get("user_id"):
        # if user is not logged in, give him a UserId of a large random number to store their votes
        session["user_id"] = random.randrange(1000000000, 10000000000)

    if request.args.get('chonkness'):
        user_chonkness = int(request.args.get('chonkness'))
        con.execute('INSERT INTO Ratings (UserId, ImageId, Score) VALUES (?, ?, ?)',
                    session['user_id'], cat_id, user_chonkness)
        user_chonk_message = CHONK_SCALE[user_chonkness]
        # get average of community voted chonkness
        community_chonkness = con.execute(
            "SELECT AVG(Score) as chonk FROM Ratings WHERE ImageId = ?", cat_id)
        # round average chonkness to nearest integer value
        community_chonkness = round(community_chonkness[0]['chonk'])
        # assign text to int value
        community_chonk_message = CHONK_SCALE[community_chonkness]
        # print(chonk_message)
    else:
        user_chonk_message = ""
        community_chonk_message = ""
    return render_template('index.html',
                           cat_id=cat_id, user_chonk=user_chonk_message,
                           community_chonk=community_chonk_message)


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
        form_pw = request.form.get("password")
        if len(rows) != 1 or not check_password_hash(rows[0]["Password"], form_pw):
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

        if len(con.execute("SELECT * FROM Users WHERE Username = ?",
                           request.form.get("username"))) != 0:
            return apology("Username already exists, please choose another", 400)

        pw_hash = generate_password_hash(request.form.get("password"))

        con.execute("INSERT INTO Users (Username, Password) VALUES (?, ?)",
                    request.form.get("username"), pw_hash)

        return redirect("/login")

    return render_template("register.html")


@app.route('/skip', methods=["GET", "POST"])
def skip():
    return redirect(url_for('index'))


@app.route('/leaderboard')
def leaderboard():
    row = con.execute(
        "SELECT COUNT(DISTINCT ImageId) as votes, Username as name\
            FROM Ratings INNER JOIN Users ON Ratings.UserId = Users.UserId \
            GROUP BY Ratings.UserId \
            ORDER BY votes DESC LIMIT 10")
    row_range_zip = zip(row, range(1, 11))
    return render_template('leaderboard.html', z=row_range_zip)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    pw_change = False

    if request.method == "POST":

        pw_hash = generate_password_hash(request.form.get("new_password"))

        con.execute("UPDATE Users SET Password = ? WHERE UserId = ?",
                    pw_hash, session["user_id"])
        pw_change = True
        return render_template('profile.html', pw_changed=pw_change)

    return render_template('profile.html', pw_changed=pw_change)


if __name__ == '__main__':
    app.run()
