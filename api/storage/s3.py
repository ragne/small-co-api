from flask import Blueprint, request, send_file, abort, current_app
from werkzeug.utils import secure_filename

from api.storage.storage import upload_file, get_file, delete_file, file_exists
from api.utils import make_error

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
s3storage = Blueprint("s3storage", __name__, url_prefix="/")


def get_s3_bucket() -> str:
    return current_app.config["S3_BUCKET"]


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@s3storage.route("/upload", methods=["GET", "POST"])
def do_upload():
    if request.method == "GET":
        abort(405)
    # @TODO: handle file in body, like --data-binary in curl
    if "file" not in request.files:  # file is a form parameter
        return make_error("No file was uploaded!")
    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return make_error(f"File {file.filename} is not allowed!", 400)
    filename = secure_filename(file.filename)
    upload_file(file.stream, filename, get_s3_bucket())
    return {"message": f"File {filename} was uploaded successfully!"}, 200


@s3storage.route("/<filename>")
def do_get(filename):
    filename = secure_filename(filename)
    if not file_exists(filename, get_s3_bucket()):
        return make_error(f"File {filename} doesn't exist", 404)
    try:
        mime, file = get_file(filename, get_s3_bucket())
    except Exception:
        return make_error(f"Cannot get file {filename}!", 500)
    return send_file(file, mimetype=mime)


@s3storage.route("/<filename>", methods=["DELETE"])
def do_delete(filename):
    filename = secure_filename(filename)
    if not file_exists(filename, get_s3_bucket()):
        return make_error(f"File {filename} doesn't exist", 404)
    try:
        delete_file(filename, get_s3_bucket())
        return {"message": f"File {filename} was deleted successfully!"}
    except Exception as e:
        print(e)
        return make_error(f"File {filename} cannot be deleted")
