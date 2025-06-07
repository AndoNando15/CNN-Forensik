from flask import Blueprint, render_template, request
import os
from werkzeug.utils import secure_filename
from app.utils.predict import predict_document  # pastikan ini benar

routes = Blueprint("routes", __name__)
UPLOAD_FOLDER = 'app/static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@routes.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'document' not in request.files:
            return "Tidak ada file yang dikirim", 400

        file = request.files["document"]
        if file.filename == "":
            return "File tidak dipilih", 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        prediction_result = predict_document(file_path)
        return render_template("index.html", prediction=prediction_result, filename=filename)

    return render_template("index.html")

@routes.route("/upload-dataset", methods=["GET", "POST"])
def upload_dataset():
    if request.method == "POST":
        label = request.form.get("label")
        file = request.files.get("document")

        if not label or label not in ["real", "fake"]:
            return "Label tidak valid", 400

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            save_dir = os.path.join("dataset", label)
            os.makedirs(save_dir, exist_ok=True)
            file.save(os.path.join(save_dir, filename))
            message = f"File berhasil diunggah ke dataset '{label}'."
        else:
            message = "Tidak ada file yang dipilih."

        return render_template("upload_dataset.html", message=message)

    return render_template("upload_dataset.html")
