from flask import Flask, render_template, request, jsonify
import os
import sqlite3

app = Flask(__name__)

# Specify the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize SQLite database
DATABASE = 'database.db'

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id TEXT PRIMARY KEY,
            date TEXT,
            filename TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Function to insert data into the database
def insert_into_database(image_id, image_date, filename):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO images (id, date, filename)
        VALUES (?, ?, ?)
    ''', (image_id, image_date, filename))

    conn.commit()
    conn.close()

# Route to serve the HTML file from the 'templates' folder
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle image uploads
@app.route('/upload', methods=['POST'])
def upload():
    try:
        # Get the file and data from the request
        file = request.files['file']
        image_date = request.form['date']
        image_id = request.form['id']

        # Save the file to the upload folder
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Insert data into the database
        insert_into_database(image_id, image_date, filename)

        return jsonify({'message': 'File uploaded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    create_table()
    app.run(debug=True, port=5001)
