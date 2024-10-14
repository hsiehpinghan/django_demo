import base64
import json
import os
import re
from io import BytesIO

import pdfplumber
from PIL import Image
from cachetools import LRUCache, cached
from ruamel.yaml import YAML
from strenum import StrEnum

class FileType(StrEnum):
    PDF = 'pdf'
    DOC = 'doc'
    VISUAL = 'visual'
    AURAL = 'aural'
    VIRTUAL = 'virtual'
    FOLDER = 'folder'
    OTHER = "other"

PROJECT_BASE = os.getenv("RAG_PROJECT_BASE") or os.getenv("RAG_DEPLOY_BASE")
RAG_BASE = os.getenv("RAG_BASE")


def get_project_base_directory(*args):
    global PROJECT_BASE
    if PROJECT_BASE is None:
        PROJECT_BASE = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                os.pardir,
                os.pardir,
            )
        )

    if args:
        return os.path.join(PROJECT_BASE, *args)
    return PROJECT_BASE


def get_rag_directory(*args):
    global RAG_BASE
    if RAG_BASE is None:
        RAG_BASE = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                os.pardir,
                os.pardir,
                os.pardir,
            )
        )
    if args:
        return os.path.join(RAG_BASE, *args)
    return RAG_BASE


def get_rag_python_directory(*args):
    return get_rag_directory("python", *args)


def get_home_cache_dir():
    dir = os.path.join(os.path.expanduser('~'), ".ragflow")
    try:
        os.mkdir(dir)
    except OSError as error:
        pass
    return dir


@cached(cache=LRUCache(maxsize=10))
def load_json_conf(conf_path):
    if os.path.isabs(conf_path):
        json_conf_path = conf_path
    else:
        json_conf_path = os.path.join(get_project_base_directory(), conf_path)
    try:
        with open(json_conf_path) as f:
            return json.load(f)
    except BaseException:
        raise EnvironmentError(
            "loading json file config from '{}' failed!".format(json_conf_path)
        )


def dump_json_conf(config_data, conf_path):
    if os.path.isabs(conf_path):
        json_conf_path = conf_path
    else:
        json_conf_path = os.path.join(get_project_base_directory(), conf_path)
    try:
        with open(json_conf_path, "w") as f:
            json.dump(config_data, f, indent=4)
    except BaseException:
        raise EnvironmentError(
            "loading json file config from '{}' failed!".format(json_conf_path)
        )


def load_json_conf_real_time(conf_path):
    if os.path.isabs(conf_path):
        json_conf_path = conf_path
    else:
        json_conf_path = os.path.join(get_project_base_directory(), conf_path)
    try:
        with open(json_conf_path) as f:
            return json.load(f)
    except BaseException:
        raise EnvironmentError(
            "loading json file config from '{}' failed!".format(json_conf_path)
        )


def load_yaml_conf(conf_path):
    if not os.path.isabs(conf_path):
        conf_path = os.path.join(get_project_base_directory(), conf_path)
    try:
        with open(conf_path) as f:
            yaml = YAML(typ='safe', pure=True)
            return yaml.load(f)
    except Exception as e:
        raise EnvironmentError(
            "loading yaml file config from {} failed:".format(conf_path), e
        )


def rewrite_yaml_conf(conf_path, config):
    if not os.path.isabs(conf_path):
        conf_path = os.path.join(get_project_base_directory(), conf_path)
    try:
        with open(conf_path, "w") as f:
            yaml = YAML(typ="safe")
            yaml.dump(config, f)
    except Exception as e:
        raise EnvironmentError(
            "rewrite yaml file config {} failed:".format(conf_path), e
        )


def rewrite_json_file(filepath, json_data):
    with open(filepath, "w") as f:
        json.dump(json_data, f, indent=4, separators=(",", ": "))
    f.close()


def filename_type(filename):
    filename = filename.lower()
    if re.match(r".*\.pdf$", filename):
        return FileType.PDF.value

    if re.match(
             r".*\.(eml|doc|docx|ppt|pptx|yml|xml|htm|json|csv|txt|ini|xls|xlsx|wps|rtf|hlp|pages|numbers|key|md|py|js|java|c|cpp|h|php|go|ts|sh|cs|kt|html|sql)$", filename):
        return FileType.DOC.value

    if re.match(
            r".*\.(wav|flac|ape|alac|wavpack|wv|mp3|aac|ogg|vorbis|opus|mp3)$", filename):
        return FileType.AURAL.value

    if re.match(r".*\.(jpg|jpeg|png|tif|gif|pcx|tga|exif|fpx|svg|psd|cdr|pcd|dxf|ufo|eps|ai|raw|WMF|webp|avif|apng|icon|ico|mpg|mpeg|avi|rm|rmvb|mov|wmv|asf|dat|asx|wvx|mpe|mpa|mp4)$", filename):
        return FileType.VISUAL.value

    return FileType.OTHER.value


def thumbnail(filename, blob):
    filename = filename.lower()
    if re.match(r".*\.pdf$", filename):
        pdf = pdfplumber.open(BytesIO(blob))
        buffered = BytesIO()
        pdf.pages[0].to_image(resolution=32).annotated.save(buffered, format="png")
        return "data:image/png;base64," + \
            base64.b64encode(buffered.getvalue()).decode("utf-8")

    if re.match(r".*\.(jpg|jpeg|png|tif|gif|icon|ico|webp)$", filename):
        image = Image.open(BytesIO(blob))
        image.thumbnail((30, 30))
        buffered = BytesIO()
        image.save(buffered, format="png")
        return "data:image/png;base64," + \
            base64.b64encode(buffered.getvalue()).decode("utf-8")

def traversal_files(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname
