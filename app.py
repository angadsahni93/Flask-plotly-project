from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
# Use a local SQLite database file named site.db for this app's data.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Connect SQLAlchemy to this Flask app.
db = SQLAlchemy(app)

# Database model for a single task in the to-do list.
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
@app.route("/")
def index(): 
    return render_template("index.html") 




if __name__ == "__main__":
    app.run(debug=True)
