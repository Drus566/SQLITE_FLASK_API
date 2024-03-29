import sqlite3
from flask import Flask, jsonify, request, g
from enum import Enum

app = Flask(__name__)

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/api/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM table_task WHERE id=?',(task_id,))
    data = cursor.fetchall()
    update_data = [(d[0], d[1], d[2], TaskStatus.getTaskStatusName(d[3])) for d in data]
    return jsonify(update_data)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM table_task')
    data = cursor.fetchall()
    update_data = [(d[0], d[1], d[2], TaskStatus.getTaskStatusName(d[3])) for d in data]
    return jsonify(update_data)

@app.route('/api/task', methods=['POST'])
def create_task():
    name = request.json['name']
    description = request.json['description']
    status = request.json['status']
    update_status = TaskStatus.getTaskStatusValue(status)

    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO table_task (name, description, status) VALUES (?, ?, ?)', (name, description, update_status))

    db.commit()
    return jsonify('success create')

@app.route('/api/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    name = request.json['name']
    description = request.json['description']
    status = request.json['status']
    update_status = TaskStatus.getTaskStatusValue(status)

    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE table_task SET name=?, description=?, status=? WHERE id=?', (name, description, update_status, task_id))

    db.commit()
    return jsonify('success update')

@app.route('/api/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('DELETE FROM table_task WHERE id = ?', (task_id,)) 

    db.commit()
#    return 200
    return jsonify('success delete')

class TaskStatus(Enum):
    ADDED       = 1
    IN_WORK     = 2
    PERFORMED   = 3

    def getTaskStatusName(value):
        if (value == TaskStatus.ADDED.value):
            return TaskStatus.ADDED.name
        elif (value == TaskStatus.IN_WORK.value):
            return TaskStatus.IN_WORK.name
        elif (value == TaskStatus.PERFORMED.value):
            return TaskStatus.PERFORMED.name
        else:
            return 'Not defined'

    def getTaskStatusValue(name):
        if (name == TaskStatus.ADDED.name):
            return TaskStatus.ADDED.value
        elif (name == TaskStatus.IN_WORK.name):
            return TaskStatus.IN_WORK.value
        elif (name == TaskStatus.PERFORMED.name):
            return TaskStatus.PERFORMED.value
        else:
            return 0


if __name__ == '__main__':
    db = sqlite3.connect(DATABASE)
    db.cursor().execute('''

    CREATE TABLE IF NOT EXISTS table_task (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        status TINYINT NOT NULL
    );''')
    app.run()
