from flask import Flask, render_template

app = Flask(__name__)

# a decorator which tells the application
# which URL should call the associated function.
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/new")
def new():
    return render_template("notes/new.html")

if __name__ == "__main__":
    # run the application on the local dev server
    app.run(debug=True)
