from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# create db
conn = sqlite3.connect('notes.db')
conn.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL
    )
''')
conn.close()


@app.route('/')
def index():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes')
    notes = cursor.fetchall()
    conn.close()
    return render_template('index.html', notes=notes)


@app.route('/create', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        content = request.form['content']
        conn = sqlite3.connect('notes.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO notes (content) VALUES (?)', (content,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/note/<int:note_id>')
def view_note(note_id):
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
    note = cursor.fetchone()
    conn.close()
    return render_template('note.html', note=note)


@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)