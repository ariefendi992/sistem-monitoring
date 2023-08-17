import os
from flask import Blueprint, send_from_directory, request

download = Blueprint('download', __name__, url_prefix='/download')

# @download.route('/file/<name>')
# def download_file(name):
#     base_url = request.full_path
#     print(base_url)
#     folder_download = os.getcwd() +'/app/static/'
#     download = send_from_directory(folder_download +'doc/', path=name )
#     return download
@download.route('/file/<path:name>', methods=['GET','POST'])
def image(name):
    # return f'foto: {name}'
    folder_path = os.getcwd() + '/app/backend/static/img/'
    return send_from_directory(folder_path + 'siswa/foto/', path=name)