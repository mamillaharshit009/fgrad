from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Sample in-memory task list
tasks = []

@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/assignment', methods=['GET'])
def assignment_page():
    return render_template('assignment/index.html', tasks=tasks)

@app.route('/assignment', methods=['POST'])
def add_task():
    task_content = request.form.get('content')
    if task_content:
        tasks.append({'id': len(tasks) + 1, 'content': task_content, 'date_created': datetime.now()})
    return redirect(url_for('assignment_page'))

@app.route('/assignment/delete/<int:task_id>')
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return redirect(url_for('assignment_page'))

@app.route('/assignment/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if not task:
        return "Task not found", 404
    if request.method == 'POST':
        task_content = request.form.get('content')
        if task_content:
            task['content'] = task_content
        return redirect(url_for('assignment_page'))
    return render_template('assignment/update.html', task=task)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
