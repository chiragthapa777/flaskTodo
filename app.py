from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.sno} - {self.title}'


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)


@app.route("/products")
def products():
    todos = Todo.query.all()
    print(todos)
    return "<p>This is product pages</p>"


@app.route("/delete/<int:sno>")
def deleteProduct(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def updateProduct(sno):
    if request.method == 'POST':
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=7000)