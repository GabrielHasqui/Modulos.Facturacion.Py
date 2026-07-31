from pathlib import Path


def project_root():
    return Path(__file__).resolve().parents[1]


def data_path(filename):
    return project_root() / "data" / filename
