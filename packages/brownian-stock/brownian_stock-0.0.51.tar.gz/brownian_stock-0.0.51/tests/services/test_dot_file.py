import pathlib
import tempfile

import pytest
from brownian_stock.services import dot_file


@pytest.fixture
def config_file() -> pathlib.Path:
    filename = ".brownianrc"
    file_contents = """
    username: test_username
    password: test_password
    """
    with tempfile.TemporaryDirectory() as dirname:
        filepath = pathlib.Path(dirname) / filename
        with open(filepath, "w") as fp:
            fp.write(file_contents)
        yield filepath


def test_dot_file(config_file: pathlib.Path) -> None:
    config = dot_file.load_config(config_file)
    assert config.username == "test_username"
    assert config.password == "test_password"


def test_dot_file_with_args(config_file: pathlib.Path) -> None:
    config = dot_file.load_config(config_file, args_username="args_username", args_password="args_password")
    assert config.username == "args_username"
    assert config.password == "args_password"


def test_dot_file_not_exists() -> None:
    with tempfile.TemporaryDirectory() as dirname:
        path = pathlib.Path(dirname) / "no_exist.txt"
        config = dot_file.load_config(path)
        assert config is None
