from flask import Flask ,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join('A:/Flask_Task/', 'test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)  # Changed nullable to False
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Corrected db.Datetime to db.DateTime
    def __repr__(self):
        return "<Task %r>" % self.id
#In Python, __repr__ is a special method (also known as a "magic" or "dunder" method) that you can define within a class to provide a string representation of the object. This method is used to generate a human-readable and unambiguous representation of an object, typically for debugging or informative purposes.
@app.route('/', methods=['POST','GET'])
def index():
    if request.method =='POST':
        task_content=request.form['content']
        new_task=Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"

    else:
        tasks=Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    id_to_delete=Todo.query.get_or_404(id)


    try:
        db.session.delete(id_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting the task"

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    id_to_update=Todo.query.get_or_404(id)
    if request.method == 'POST':
        id_to_update.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating the task"
    else:
        return render_template('update.html',task=id_to_update)


if __name__=="__main__":
    app.run(debug=True)