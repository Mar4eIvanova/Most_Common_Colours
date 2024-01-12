from flask import Flask, render_template, request, send_from_directory,url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_bootstrap import Bootstrap5
import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster
import sklearn.cluster


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] ="lksndkjfgsi"
app.config["UPLOADED_PHOTOS_DEST"] = "uploads"
Bootstrap5(app)

photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)

class UploadForm(FlaskForm):
    photo = FileField(
        validators=[FileAllowed(photos, 'Only images are allowed'),
                    FileRequired('File field should not be empty')
                    ]
    )
    submit = SubmitField('Upload')

@app.route('/uploads/<file>')
def get_file(file):
    return send_from_directory(app.config["UPLOADED_PHOTOS_DEST"], file)



@app.route('/', methods=['GET', 'POST'])
def home():
    form = UploadForm()
    if form.validate_on_submit() and request.method == "POST":
        file = photos.save(form.photo.data)
        file_url = url_for("get_file", file=file)
        img = plt.imread(f"uploads/{file}")
        color_file = np.array(img)
        print(color_file.shape)
        print(color_file)

        unic_color, color_count = np.unique(color_file.reshape(-1, color_file.shape[-1]), axis=0, return_counts=True)
        top_10 = np.argpartition(color_count, -10)[-10:]
        print(unic_color[top_10], color_count[top_10])
        print(unic_color[top_10][0], color_count[top_10][0])
        u_col = unic_color[top_10]

    else:
        file_url = None
        u_col = []

    return render_template("index.html", form=form, file_url=file_url, u_col=u_col)


@app.route('/img', methods=['GET', 'POST'])
def image():
    if request.method == "POST":
        photo = request.files['imgFile']

        return render_template("photo.html", img=photo)
    return render_template("photo.html")



if __name__ == "__main__":
    app.run(debug=True)

