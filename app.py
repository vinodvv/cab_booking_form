from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/book_cab")
def book_cab():

    return render_template("book_cab.html")


app.run(debug=True, port=5001)
