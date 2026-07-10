from flask import Flask, render_template, request, redirect
import sqlite3
from database import create_database

app = Flask(__name__)
create_database()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?", (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            return redirect("/dashboard")
        else:
            return "Invalid Email or Password"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            """
        INSERT INTO users(fullname,email,password)
        VALUES(?,?,?)
        """,
            (fullname, email, password),
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
