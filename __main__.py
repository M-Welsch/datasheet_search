from pathlib import Path
import subprocess
from typing import List

from flask import Flask, request
from jinja2 import Environment

app = Flask(__name__)


DEFAULT_DS_DIRECTORY = Path('/home/max/Nextcloud/C_Referenzen/C01_Bauteile/')
DEFAULT_DS_EXTENSION = 'pdf'


FILE_LIST_TEMPLATE = """<head>
    <title>Datasheet search</title>
</head>
<body>
    {% for link in datasheet_files %}
        <a href="open?file={{link}}">{{link}}</a><br>
    {% endfor %}
</body>
"""


def _find_datasheet(search_string: str, search_dir: Path, search_extension: str) -> List[Path]:
    return list(search_dir.glob(f'*/*{search_string}*.{search_extension}'))


@app.route('/open', methods=['GET'])
def open():
    file = request.args.get('file')
    subprocess.call(["evince", file])
    return f"opened {file}"


@app.route('/search', methods=['GET'])
def parse_request():
    search_string = request.args.get('s')
    search_dir = request.args.get('ds_dir') or DEFAULT_DS_DIRECTORY
    search_extension = request.args.get('ds_extension') or DEFAULT_DS_EXTENSION
    files = _find_datasheet(search_string, search_dir, search_extension)
    if len(files) == 1:
        subprocess.call(["evince", files[0].as_posix()])
        return f"opened {files[0].as_posix()}"
    else:
        datasheet_files = [file.as_uri() for file in files]
        env = Environment().from_string(FILE_LIST_TEMPLATE).render(datasheet_files=datasheet_files)
        return env


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1338)
