from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)

#flask routing
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/html")
def html():
    return render_template("new.html")

@app.route("/<name>")
def user(name):
    return f"Hello, {name}! How can I help you?"

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run()