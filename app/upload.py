from flask import (
    request,
    redirect,
    url_for,
    send_from_directory,
    current_app,
    Blueprint,
)
from flask_jwt_extended import jwt_optional, jwt_required, get_jwt_identity
import os
import uuid

from model.common import db
from model.image import Image
from responses import error_response, success_response
import util


# Responses
NO_FILE_UPLOADED = "No file uploaded"
INVALID_FILE = "Invalid file type"
NOT_PERMITTED = "Access not permitted"
IMAGE_NOT_EXIST = "Image does not exist"
ERROR_DURING_SAVING = "Error encountered when saving image"
ERROR_DURING_DELETION = "Error encountered when deleting image"
IMAGE_DELETED = "Image deleted"

upload = Blueprint('upload', __name__)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    _, file_extension = os.path.splitext(filename)
    if file_extension[0] == ".":
        file_extension = file_extension[1:]
    return file_extension in ALLOWED_EXTENSIONS


# Random filename in base 62, generated from uuid
def random_file_name():
    uuid_int = uuid.uuid1().int
    return util.int_to_base62(uuid_int)


@upload.route("/upload", methods=["POST"])
@jwt_required
def upload_file():
    if "file" not in request.files:
        return error_response(NO_FILE_UPLOADED)

    f = request.files["file"]
    if f.filename == "":
        return error_response(NO_FILE_UPLOADED)
    is_public = request.form.get("is_public", "False").lower() == 'true'

    if f and allowed_file(f.filename):
        user = get_jwt_identity()
        _, file_extension = os.path.splitext(f.filename)
        filename = random_file_name() + file_extension

        image = Image(name=filename, owner_id=user, is_public=is_public)
        db.session.add(image)
        try:
            f.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
            db.session.commit()
        except Exception:
            return error_response(ERROR_DURING_SAVING, 500)
        return redirect(url_for("upload.get_file", filename=filename))
    else:
        return error_response(INVALID_FILE)


@upload.route("/uploads/<filename>", methods=["GET"])
@jwt_optional
def get_file(filename):
    current_user = get_jwt_identity()
    f = Image.query.filter_by(name=filename).first()
    if not f:
        return error_response(IMAGE_NOT_EXIST)
    if not f.is_public and f.owner_id != current_user:
        return error_response(NOT_PERMITTED)
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@upload.route("/uploads/<filename>", methods=["DELETE"])
@jwt_required
def delete_file(filename):
    current_user = get_jwt_identity()
    f = Image.query.filter_by(name=filename).first()
    if not f:
        return error_response(IMAGE_NOT_EXIST)
    if f.owner_id != current_user:
        return error_response(NOT_PERMITTED)
    image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], f.name)

    db.session.delete(f)
    try:
        os.remove(image_path)
        db.session.commit()
    except Exception:
        return error_response(ERROR_DURING_DELETION, 500)
    return success_response(IMAGE_DELETED)
