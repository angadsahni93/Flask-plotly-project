from flask import Flask, redirect, request, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
# Use a local SQLite database file named site.db for this app's data.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Connect SQLAlchemy to this Flask app.
db = SQLAlchemy(app)

# Database model for a single task in the to-do list; each to-do task is a row in the database, site.db.
## class Todo defines which components of each task should be stored (i.e. columns in the database table).
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False) # nullable=False means that this column cannot be empty.
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Defines how this task looks when printed/debugged.
    def __repr__(self):
        # Show the task using its database id.
        return '<Task %r>' % self.id

## NOTE: 'templates' folder is an innate name for Flask to look for HTML files.
# GET = browser loads this page.
# POST = browser sends form data to this route, e.g. text from an "add task" input.
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST': # if user submitted the form (defined in index.html)
        task_content = request.form["content"] # get the text from the form input named 'content'.
        new_task = Todo(content=task_content) # create a new task with the text from the form.

        try:
            db.session.add(new_task) # add the new task to the database session.
            db.session.commit() # commit the session to save the new task to the database.
            return redirect("/") # redirect to the index page to show the updated list of tasks.
        except:
            return "There was an issue adding your task."

    else: # no task entered.
        tasks = Todo.query.order_by(Todo.date_created).all() # get 'all' tasks from the database, ordered by creation date.
        return render_template("index.html", tasks=tasks) # just load the index.html page.
        ## tasks=tasks passes the list of tasks to the HTML template, so it can display them. 'tasks' variable will be aded to the index.html template.


@app.route("/delete/<int:id>") # <int:id> means that this route expects an integer parameter named 'id'. 
## This page will store the Deleted tasks from table in index.html.

if __name__ == "__main__":
    app.run(debug=True)
