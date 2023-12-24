import shutil
from pathlib import Path

import pytest

from mhdwriter.writer import write_mhd_raw
from .test_header import basic_args


@pytest.fixture
def test_jpg_dataset(tmp_path):
    test_data_dir = get_test_data_dir()
    for i in range(1, 30):
        source_file = test_data_dir / "example.jpg"
        shutil.copy(source_file, str(Path(tmp_path).joinpath(f"slice_{i:04d}.jpg")))
    yield tmp_path


@pytest.fixture
def test_tiff_dataset(tmp_path):
    test_data_dir = get_test_data_dir()
    for i in range(1, 60):
        source_file = test_data_dir / "example.tif"
        shutil.copy(source_file, str(Path(tmp_path).joinpath(f"slice_{i:04d}.tiff")))

    yield tmp_path


def get_test_data_dir():
    current_file_path = Path(__file__).resolve().parent.parent
    return current_file_path / "test_data"


def test_write_mhd_jpg_raw(test_jpg_dataset, basic_args):
    basic_args.is_rgb = True
    write_mhd_raw(test_jpg_dataset, basic_args)
    assert True


def test_write_mhd_tiff_raw(test_tiff_dataset, basic_args):
    basic_args.is_rgb = False
    write_mhd_raw(test_tiff_dataset, basic_args)
    assert True
