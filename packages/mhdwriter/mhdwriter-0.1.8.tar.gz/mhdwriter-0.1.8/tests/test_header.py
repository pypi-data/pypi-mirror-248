import pytest

from mhdwriter.args import WriteType
from mhdwriter.header import generate_header, WriteArgs


@pytest.fixture
def basic_args():
    args = WriteArgs(
        write_type=WriteType.RAW,
        fov="C",
        series_description="test series",
        study_description="test study",
        protocol="test protocol",
        date_time="2021-01-01 00:00:00",
        root_site_id="12345567",
        downsample_factor=0,
        height=0,
        width=0,
        length=0,
        is_rgb=False,
    )

    yield args


def test_generate_header_should_require_args():
    with pytest.raises(AssertionError) as excinfo:
        generate_header(1)
    assert "Invalid WriteArgs" in str(excinfo.value)


def test_generate_header_should_generate_uuids(basic_args):
    header = generate_header(basic_args)
    assert header["StudyInstanceUID"] == "12345567.7189148.32749.210101.0.1"
    assert header["SeriesInstanceUID"] == "12345567.7189148.8134279.210101.0.2"
    assert header["StudyInstanceUID"] == "12345567.7189148.32749.210101.0.1"


def test_generate_header_should_include_all_fields(basic_args):
    header = generate_header(basic_args)
    assert len(header) == 28


def test_generate_header_should_include_pixel_size_by_fov(basic_args):
    header = generate_header(basic_args)
    assert header["ElementSpacing"] == "0.035 0.035 0.035"
    elspacing1 = header["ElementSpacing"]
    basic_args.fov = "A"
    header = generate_header(basic_args)
    assert header["ElementSpacing"] != elspacing1
    assert header["ElementSpacing"] == "0.02 0.02 0.02"


def test_generate_header_should_include_downsampled_pixel_size(basic_args):
    basic_args.downsample_factor = 1
    header = generate_header(basic_args)
    assert header["ElementSpacing"] == "0.07 0.07 0.07"
    basic_args.downsample_factor = 2
    header = generate_header(basic_args)
    assert header["ElementSpacing"] == "0.14 0.14 0.14"
