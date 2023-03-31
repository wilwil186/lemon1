from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Crear instancia de SQLAlchemy
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    tags = db.relationship('Tag', backref='task', lazy=True)
    assignee_id = db.Column(db.Integer, db.ForeignKey('assignee.id'))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

class Assignee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    tasks = db.relationship('Task', backref='assignee', lazy=True)
    
# Definir una lista de tareas como una variable global
tasks = [
    {
        'id': 1,
        'description': 'Comprar leche',
        'priority': 'Alta'
    },
    {
        'id': 2,
        'description': 'Ir al gimnasio',
        'priority': 'Baja'
    }
]

# Ruta para obtener todas las tareas
@app.route('/api/tasks', methods=['GET'])

def get_tasks():
    tasks = Task.query.all()
    task_list = []
    for task in tasks:
        task_dict = {
            'id': task.id,
            'description': task.description,
            'priority': task.priority,
            'completed': task.completed,
            'assignee': task.assignee.name if task.assignee else None,
            'tags': [tag.name for tag in task.tags]
        }
        task_list.append(task_dict)
    return jsonify({'tasks': task_list})


# Ruta para obtener una tarea por su id
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

# Ruta para crear una nueva tarea
@app.route('/api/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'description' in request.json:
        abort(400)
    description = request.json['description']
    priority = request.json.get('priority', 'Baja')
    assignee_id = request.json.get('assignee_id')
    tags = request.json.get('tags', [])

    assignee = None
    if assignee_id:
        assignee = Assignee.query.get(assignee_id)

    task = Task(description=description, priority=priority, assignee=assignee)

    for tag_name in tags:
        tag = Tag(name=tag_name, task=task)
        db.session.add(tag)

    db.session.add(task)
    db.session.commit()

    task_dict = {
        'id': task.id,
        'description': task.description,
        'priority': task.priority,
        'completed': task.completed,
        'assignee': task.assignee.name if task.assignee else None,
        'tags': [tag.name for tag in task.tags]
    }

    return jsonify({'task': task_dict}), 201


# Ruta para actualizar una tarea existente
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        abort(404)

    if not request.json:
        abort(400)

    task.description = request.json.get('description', task.description)
    task.priority = request.json.get('priority', task.priority)

    assignee_id = request.json.get('assignee_id')
    if assignee_id:
        assignee = Assignee.query.get(assignee_id)
        task.assignee = assignee
    else:
        task.assignee = None

    tags = request.json.get('tags', [])
    task.tags = []
    for tag_name in tags:
        tag = Tag(name=tag_name, task=task)
        db.session.add(tag)

    db.session.commit()

    task_dict = {
        'id': task.id,
        'description': task.description,
        'priority': task.priority,
        'completed': task.completed,
        'assignee': task.assignee.name if task.assignee else None,
        'tags': [tag.name for tag in task.tags]
    }

    return jsonify({'task': task_dict})


# Ruta para eliminar una tarea existente
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    tags = db.relationship('Tag', backref='task', lazy=True)

    def __repr__(self):
        return '<Task %r>' % self.title

@app.route('/tasks')
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.__dict__ for task in tasks])


if __name__ == '__main__':
    app.run(debug=True)
