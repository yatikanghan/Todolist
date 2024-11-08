from flask import Flask,render_template, url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500), nullable=False)
    datecreated=db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':
        title=request.form.get('todotitle')
        desc=request.form.get('tododesc')
        newtodo=Todo(title=title, desc=desc)
        db.session.add(newtodo)
        db.session.commit()

    alltodo=Todo.query.all()

    return render_template('index.html', alltodo=alltodo)


@app.route('/edit/<int:sno>')
def edit(sno):
    updatetodo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', updatetodo=updatetodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    deltodo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(deltodo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form.get('todotitle')
        desc=request.form.get('tododesc')
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()

    return redirect("/")



def createdatabase():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    createdatabase()
    app.run(debug=True)



