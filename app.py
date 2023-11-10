from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///image_database.db'
db = SQLAlchemy(app)

# Define the database models
class Image(db.Model):
    image_id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255))
    upload_date = db.Column(db.TIMESTAMP)
    classifications = db.relationship('Classification', backref='image', lazy=True)
    locations = db.relationship('Location', backref='image', lazy=True)

class Classification(db.Model):
    classification_id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.image_id'), nullable=False)
    coral = db.Column(db.Boolean)
    seaweeds = db.Column(db.Boolean)
    seagrass = db.Column(db.Boolean)

class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.image_id'), nullable=False)
    latitude = db.Column(db.DECIMAL(9,6))
    longitude = db.Column(db.DECIMAL(9,6))

# Create the tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        # Save the image to the server
        image_path = f"uploads/{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        file.save(image_path)

        # Create a new image record in the database
        new_image = Image(image_path=image_path, upload_date=datetime.now())
        db.session.add(new_image)
        db.session.commit()

        # Retrieve image_id for the new image
        image_id = new_image.image_id

        # Retrieve classification and location details from the form
        coral = request.form.get('coral') == 'on'
        seaweeds = request.form.get('seaweeds') == 'on'
        seagrass = request.form.get('seagrass') == 'on'
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        # Create classification record
        new_classification = Classification(image_id=image_id, coral=coral, seaweeds=seaweeds, seagrass=seagrass)
        db.session.add(new_classification)

        # Create location record
        new_location = Location(image_id=image_id, latitude=latitude, longitude=longitude)
        db.session.add(new_location)

        # Commit changes to the database
        db.session.commit()

        return redirect(url_for('index'))

    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
