from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import cv2
import base64
from io import BytesIO
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
db = SQLAlchemy(app)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    class_type = db.Column(db.String(50))
    status = db.Column(db.Integer)
    image_data = db.Column(db.String)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    latitude_str = request.form.get('latitude')
    longitude_str = request.form.get('longitude')

    try:
        latitude = float(latitude_str)
        longitude = float(longitude_str)
    except ValueError:
        return "Invalid latitude or longitude. Please enter numeric values."

    class_type = request.form.get('class_type')
    status = request.form.get('status')

    # Capture image from webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    # Convert image to base64 for storage
    _, buffer = cv2.imencode('.jpg', frame)
    image_data = base64.b64encode(buffer).decode('utf-8')

    new_image = Image(latitude=latitude, longitude=longitude, class_type=class_type, status=status, image_data=image_data)
    db.session.add(new_image)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return f"Error: {str(e)}"

    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=5001)

