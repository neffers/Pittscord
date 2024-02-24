from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def default():
    return render_template("templates/theButton.html")


@app.route("/post", methods=["POST"])
def say_hello():
    print("Hello World")
    return ""


if __name__ == "__main__":
    app.run()