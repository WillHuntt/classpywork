from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = []

@app.route('/')
def home():
    return render_template('task.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form.get('task')

    tasks.append({'task': task, 'completed': False})

    return redirect(url_for('home'))

@app.route('/complete_task', methods=['POST'])
def complete_task():
    task_index = int(request.form.get('task_index'))

    tasks[task_index]['completed'] = True

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)