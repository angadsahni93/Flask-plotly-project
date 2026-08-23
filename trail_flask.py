# To see run in browser, run >python Flask.py< in terminal and go to 'http://' provided.

from flask import Flask, redirect, url_for

app = Flask(__name__)

# Defines the route to the def function immediately beneath it.
@app.route("/home") 
def home(): # blank () = takes no arguments (i.e. no input values from user)
    return "<h1>Welcome to the Home Page!</h1>"

@app.route("/user:<name>") # <name> = takes input value from user, ensuring the user/ route is taken.
def user(name): # uses 'name' argument and incorporates it into the return string below.
    return f"Hello <h1>{name}</h1> Welcome to YOUR page!"


@app.route("/admin") # when at /admin page...
def admin(): # function for admin page
    return redirect(url_for("user", name="Admin!")) 
# redirect to user page as defined by 'def user()' function above.
# name="Admin!" is the argument used by user function in th place of <name>.

if __name__ == "__main__":
    app.run(debug=True)
