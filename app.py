from flask import Flask, redirect, request, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
# Use a local SQLite database file named site.db for this app's data.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Connect SQLAlchemy to this Flask app.
db = SQLAlchemy(app)


def build_task_chart_data(events):
    task_count = 0
    chart_data = []

    for event in events:
        task_count += event.change
        chart_data.append({
            "time": event.date_created.isoformat(),
            "task_count": task_count,
        })

    return chart_data

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


class TaskEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    change = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

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
            db.session.add(TaskEvent(change=1))
            db.session.commit() # commit the session to save the new task to the database.
            return redirect("/") # redirect to the index page to show the updated list of tasks.
        except:
            return "There was an issue adding your task."

    else: # no task entered.
        tasks = Todo.query.order_by(Todo.date_created).all() # get 'all' tasks from the database, ordered by creation date.
        events = TaskEvent.query.order_by(TaskEvent.date_created).all()
        chart_data = build_task_chart_data(events)
        return render_template("index.html", tasks=tasks, chart_data=chart_data) # just load the index.html page.
        ## tasks=tasks passes the list of tasks to the HTML template, so it can display them. 'tasks' variable will be aded to the index.html template.


@app.route("/delete/<int:id>") # <int:id> means that this route expects an integer parameter named 'id'. 
## This page will store the Deleted tasks from table in index.html.
def delete(id):
    task_to_delete = Todo.query.get_or_404(id) #

    try:
        db.session.delete(task_to_delete) # delete task from database session based of ID.
        db.session.add(TaskEvent(change=-1))
        db.session.commit() # commit the session to save the changes to the database.
        return redirect("/") # redirect to the index.html to show the 'updated' list of tasks.
    except:
        return "There was a problem deleting that task."


@app.route("/update/<int:id>", methods=['GET', 'POST']) # GET = show the updated form, POST = submit the updated form.
def update(id):
    task = Todo.query.get_or_404(id) # get the task to update from the database based on ID.

    if request.method == 'POST': # if user submitted the form (defined in update.html)
        task.content = request.form["content"] # update the task content with the new value from the form.
        try:
            db.session.commit() # commit the session to save the changes to the database.
            return redirect("/") # redirect to the index page to show the updated list of tasks.
        except:
            return "There was an issue updating your task."
    else: 
        return render_template("update.html", task=task)


if __name__ == "__main__":
    app.run(debug=True)
