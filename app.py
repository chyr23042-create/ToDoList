from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_done = db.Column(db.Boolean, nullable=False, default=False)
    priority = db.Column(db.Integer, nullable=False, default=2) 
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.id} {self.title}>"

@app.before_request
def create_tables_once():
    db.create_all()

@app.get("/")
def index():
    filter_mode = request.args.get("filter", "すべて") 
    q = Task.query

    if filter_mode == "未完了":
        q = q.filter_by(is_done=False)
    elif filter_mode == "完了":
        q = q.filter_by(is_done=True)

    tasks = q.order_by(Task.is_done.asc(), Task.priority.asc(), Task.due_date.is_(None), Task.due_date.asc(), Task.created_at.desc()).all()
    return render_template("index.html", tasks=tasks, filter_mode=filter_mode)

@app.post("/add")
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip() or None
    priority = int(request.form.get("priority", "2"))

    due_raw = request.form.get("due_date", "").strip()
    due = date.fromisoformat(due_raw) if due_raw else None

    if not title:
        return redirect(url_for("index"))

    task = Task(title=title, description=description, priority=priority, due_date=due)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for("index"))

@app.post("/toggle/<int:task_id>")
def toggle_task(task_id: int):
    task = Task.query.get_or_404(task_id)
    task.is_done = not task.is_done
    db.session.commit()
    return redirect(url_for("index", filter=request.args.get("filter", "all")))

@app.post("/delete/<int:task_id>")
def delete_task(task_id: int):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index", filter=request.args.get("filter", "all")))

if __name__ == "__main__":
    app.run(debug=True)
