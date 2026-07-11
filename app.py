from flask import Flask, render_template, request, redirect
import sqlite3
from database import create_database
import os
from werkzeug.utils import secure_filename
from resume_parser import extract_text
from flask import render_template, request, redirect, session
import secrets
from resume_parser import extract_text, extract_email, extract_phone, extract_skills

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
create_database()
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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

            session["user_id"] = user[0]  # id
            session["name"] = user[1]  # name (अगर दूसरा column name है)
            session["email"] = user[2]  # email (अगर तीसरा column email है)

            return redirect("/dashboard")

        else:
            return "Invalid Email or Password"

    return render_template("login.html")


# @app.route("/resume", methods=["GET", "POST"])
# def resume():

#     if request.method == "POST":

#         file = request.files["resume"]

#         if file:

#             filename = secure_filename(file.filename)

#             filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

#             file.save(filepath)

#             text = extract_text(filepath)

#             print(text)

#             return "Resume Uploaded Successfully!"


#     return render_template("resume.html")
@app.route("/resume", methods=["GET", "POST"])
def resume():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        if "resume" not in request.files:
            return "No file uploaded"

        file = request.files["resume"]

        if file.filename == "":
            return "Please select a PDF file"

        filename = secure_filename(file.filename)

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        file.save(filepath)

        # Resume Text
        text = extract_text(filepath)

        # Resume Details
        email = extract_email(text)
        phone = extract_phone(text)
        skills = extract_skills(text)

        return render_template(
            "analysis.html", resume_text=text, email=email, phone=phone, skills=skills
        )

    return render_template("resume.html")


# @app.route("/interview")
# def interview():
#     return "<h1>Interview Page</h1>"


# @app.route("/dashboard")
# def dashboard():
#     return render_template("dashboard.html")
# @app.route("/dashboard")
# def dashboard():

#     resume_uploaded = False

#     interviews = 0

#     score = 0

#     return render_template(
#         "dashboard.html",
#         resume_uploaded=resume_uploaded,
#         interviews=interviews,
#         score=score,
#     )
from flask import session, redirect


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    resume_uploaded = False
    interviews = 0
    score = 0

    return render_template(
        "dashboard.html",
        resume_uploaded=resume_uploaded,
        interviews=interviews,
        score=score,
    )


@app.route("/interview")
def interview():

    return render_template("interview.html")


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
