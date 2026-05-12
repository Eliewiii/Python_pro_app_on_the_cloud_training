"""
Test file for the FileProcessor class in core/processor.py.
"""

import logging
import pytest
from pathlib import Path
from core import FileProcessor

# --- CONFIGURATION ---
DATA_DIR = Path(__file__).parent.parent / "data"

# --- 1. GENERATED FIXTURES (Dynamic) ---


@pytest.fixture
def simple_file(tmp_path):
    """A clean file with standard integers and commas generated on the fly."""
    f = tmp_path / "simple.txt"
    f.write_text("10, 20, 30", encoding="utf-8")
    return f


@pytest.fixture
def multi_line(tmp_path):
    """A generated file withd multiple lines."""
    f = tmp_path / "complex.txt"
    # Triple quotes handle multiple lines naturally
    content = "10, 20.5; 30\n" "40.2 \n" " 5, 5\n"
    f.write_text(content, encoding="utf-8")
    return f


@pytest.fixture
def complex_scientif_notation(tmp_path):
    """A generated file with number in scientific notation."""
    f = tmp_path / "scientif_notation.txt"
    # Triple quotes handle multiple lines naturally
    content = "10e-1, 2.5E0; 3.0e+1"
    f.write_text(content, encoding="utf-8")
    return f


@pytest.fixture
def forbidden_separator_file(tmp_path):
    """A generated file with a forbidden separator '@'."""
    f = tmp_path / "forbidden_separator.txt"
    content = "10 @ 20 @ 30"
    f.write_text(content, encoding="utf-8")
    return f


@pytest.fixture
def invalid_values_file(tmp_path):
    """A clean file with standard integers and commas generated on the fly."""
    f = tmp_path / "simple.txt"
    f.write_text("10, Robert, Jose , 30", encoding="utf-8")
    return f


# --- 2. PHYSICAL FIXTURES (Static files in tests/data/) ---


@pytest.fixture
def wrong_extension_file():
    """Points to a hand-written file with an unsupported extension."""
    return DATA_DIR / "data.pdf"


# --- TEST CASES ---


def test_sum_simple(simple_file):
    with FileProcessor.session():
        assert FileProcessor.sum_file(simple_file) == 60.0


def test_sum_multi_line(multi_line):
    with FileProcessor.session():
        # 10 + 20.5 + 30 + 40.2 + 5 + 5 = 110.7
        assert FileProcessor.sum_file(multi_line) == 110.7


def test_sum_scientific_notation(complex_scientif_notation):
    with FileProcessor.session():
        # 10e-1 + 2.5E0 + 3.0e+1 = 0.1 + 2.5 + 30 = 33.5
        assert FileProcessor.sum_file(complex_scientif_notation) == 33.5


def test_forbidden_separator(forbidden_separator_file):
    """
    Since '@' isn't in our regex, the whole '10 @ 20 @ 30'
    will be treated as one invalid string.
    """
    with FileProcessor.session():
        with pytest.raises(ValueError):
            FileProcessor.sum_file(forbidden_separator_file, ignore_invalid=False)


def test_invalid_values(invalid_values_file):
    with FileProcessor.session():
        assert FileProcessor.sum_file(invalid_values_file, ignore_invalid=True) == 40.0
    with FileProcessor.session():
        with pytest.raises(ValueError):
            FileProcessor.sum_file(invalid_values_file, ignore_invalid=False)


def test_wrong_extension(wrong_extension_file):
    with FileProcessor.session():
        with pytest.raises(ValueError, match="Unsupported extension"):
            FileProcessor.sum_file(wrong_extension_file)


def test_invalid_path():
    """Testing a path that simply does not exist."""
    fake_path = Path("/tmp/this_is_a_ghost_file.txt")
    with FileProcessor.session():
        with pytest.raises(FileNotFoundError):
            FileProcessor.sum_file(fake_path)


# --- LOGGING TESTS ---


def test_logging_triggers_on_first_error(caplog, invalid_values_file):
    """Verifies that the warning is captured during the first encounter."""
    # We explicitly look for WARNING level logs
    with caplog.at_level(logging.WARNING):
        with FileProcessor.session():
            FileProcessor.sum_file(invalid_values_file, ignore_invalid=True)

            # Filter records to find our specific warning
            warnings = [
                r
                for r in caplog.records
                if "The file contains invalid numeric data. These will be skipped" in r.message
            ]

            assert len(warnings) == 1
            assert warnings[0].levelname == "WARNING"


def test_logging_is_suppressed_after_first_warning(caplog, invalid_values_file):
    """Verifies the ContextVar logic: only one log per session."""
    with caplog.at_level(logging.WARNING):
        with FileProcessor.session():
            # Process the same 'dirty' file twice
            FileProcessor.sum_file(invalid_values_file, ignore_invalid=True)
            FileProcessor.sum_file(invalid_values_file, ignore_invalid=True)

            # Even though two files were processed, we only expect one warning
            warnings = [
                r
                for r in caplog.records
                if "The file contains invalid numeric data. These will be skipped" in r.message
            ]
            assert len(warnings) == 1
        # Check the value is indeed reset after the session
        with FileProcessor.session():
            # Process the same 'dirty' file twice
            FileProcessor.sum_file(invalid_values_file, ignore_invalid=True)

            # Even though two files were processed, we only expect one warning
            warnings = [
                r
                for r in caplog.records
                if "The file contains invalid numeric data. These will be skipped" in r.message
            ]
            assert len(warnings) == 2


def test_no_warnings_on_clean_data(caplog, simple_file):
    """Ensures that perfect data produces zero warning logs."""
    with caplog.at_level(logging.WARNING):
        with FileProcessor.session():
            FileProcessor.sum_file(simple_file)

            # There should be no records at the WARNING level
            assert len(caplog.records) == 0
