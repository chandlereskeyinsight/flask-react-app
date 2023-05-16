from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Tas %r>' % self.id
    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'date_created': self.date_created
        }

@app.route('/getTodos', methods=["GET"])
@cross_origin(supports_credentials=True)
def getTodos():
    tasks = Todo.query.order_by(Todo.date_created).all()
    jsonified = []
    for task in tasks:
        jsonified.append(task.serialize())
    return jsonify(jsonified)

@app.route('/addTodo/<todo>', methods=["POST"])
@cross_origin(supports_credentials=True)
def addTodo(todo):
    print('the todo:', todo)
    new_task = Todo(content=todo)
    print(new_task)
    try:
        db.session.add(new_task)
        db.session.commit()
    except:
        return 'There was an issue adding your task'
    return 'Successfully added todo'

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
    except:
        return 'there was a problem deleting that task'
    return 'Successfully deleted todo'
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try: 
            db.session.commit()
            return redirect('/')
        except:
            return 'failed to update'
    else: 
        return render_template('update.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)