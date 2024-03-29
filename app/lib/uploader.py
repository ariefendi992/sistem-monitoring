from werkzeug.utils import secure_filename
from PIL import Image
import os
import hashlib


ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
UPLOAD_FOLDER = os.getcwd() + "/app/api/static/img/siswa/foto/"
# foto_folder = os.getcwd() + '/app/static/img/siswa/photos/'

# MAX_FILE_SIZE = 2000


def allowed_extension(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_secure_filename(filename):
    return str(secure_filename(filename))


def uploads(f, nama_user, kelas):
    if f and allowed_extension(f.filename):
        fileOrigin = f.filename.rsplit(".", 1)
        fileExt = fileOrigin[1].lower()
        if fileExt == "jpeg" or fileExt == "jpg" or fileExt == "png":
            encFile = hashlib.md5(
                get_secure_filename(f.filename).encode("utf-8")
            ).hexdigest()
            pathFile = (
                UPLOAD_FOLDER + kelas + "_" + nama_user + "_" + encFile + "." + fileExt
            )
            f.save(pathFile)
            return {
                "status": "ok",
                "path_file": pathFile,
                "photo_name": kelas + "_" + nama_user + "_" + encFile + "." + fileExt,
            }
        elif fileExt == "pdf":
            encFile = hashlib.md5(
                get_secure_filename(f.filename).encode("utf-8")
            ).hexdigest()
            pathFile = (
                UPLOAD_FOLDER + "/doc/" + nama_user + "_" + encFile + "." + fileExt
            )
            f.save(pathFile)
            return {
                "status": "ok",
                "path_file": pathFile,
                "berkas_name": nama_user + "_" + encFile + "." + fileExt,
            }
        else:
            return {"status": "error"}


def upload_resize_photo(f, nama_user, kelas):
    if f and allowed_extension(f.filename):
        fileOrign = f.filename.rsplit(".", 1)
        fileExt = fileOrign[1].lower()
        if fileExt == "jpeg" or fileExt == "jpg" or fileExt == "png":
            encryptFile = hashlib.md5(
                get_secure_filename(f.filename).encode("utf-8")
            ).hexdigest()
            filename = f"{kelas}_{nama_user}_{encryptFile}.{fileExt}"
            path_file = UPLOAD_FOLDER + filename
            img = Image.open(f)
            # print(f"IMAGE SIZE == {img.size}")
            if img.size[0] <= 1000 & img.size[1] <= 1000:
                img.save(
                    os.path.join(UPLOAD_FOLDER, filename), optimize=True, quality=95
                )

                response = dict(status="Ok", filename=filename, path=path_file)
                return response
            else:
                width = int(img.size[0] / 10) * 2
                height = int(img.size[1] / 10) * 2

                re_image = img.resize((width, height), Image.ADAPTIVE)
                re_image.save(
                    os.path.join(UPLOAD_FOLDER, filename), optimize=True, quality=95
                )
                response = dict(status="Ok", filename=filename, path=path_file)
                return response
