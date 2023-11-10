from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Elmo912017@localhost/yoloodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable Flask-SQLAlchemy modification tracking
db = SQLAlchemy(app)

class Image2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        file = request.files['image2']

        # Save the image to a folder (you may need to create the folder)
        image_path = f"static/uploads/{file.filename}"
        file.save(image_path)

        # Save the image details to the database
        new_image = Image(title=title, image_path=image_path)
        db.session.add(new_image)
        db.session.commit()

    images = Image.query.all()
    return render_template('index.html', images=images)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
