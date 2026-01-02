from flask import Flask

app = Flask(__name__)

# a decorator which tells the application
# which URL should call the associated function.
@app.route("/")
def index():
    return "Hello!"

if __name__ == "__main__":
    # run the application on the local dev server
    app.run(debug=True)
