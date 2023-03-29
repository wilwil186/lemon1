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
    return jsonify({'tasks': tasks})

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
    task = {
        'id': tasks[-1]['id'] + 1,
        'description': request.json['description'],
        'priority': request.json.get('priority', 'Baja')
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

# Ruta para actualizar una tarea existente
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['priority'] = request.json.get('priority', task[0]['priority'])
    return jsonify({'task': task[0]})

# Ruta para eliminar una tarea existente
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
