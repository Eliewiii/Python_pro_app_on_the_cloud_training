"""
FileProcessor class, sample class to sum numbers in a text file.
"""

import logging
import re
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path
from typing import Final

logger = logging.getLogger(__name__)


class FileProcessor:
    """Provides utilities for batch processing and numeric extraction from text files."""

    # --- 1. CONFIGURATION ---
    _SUPPORTED_EXT: tuple[str, ...] = (".txt", ".csv")
    _SUPPORTED_SEPARATORS: tuple[str, ...] = (",", ";", "|", "\t")
    _SEPARATOR_PATTERN: Final[re.Pattern] = re.compile(r"[ ,;|\t]+")

    # Context variable to trigger warning only once
    _warned_var: ContextVar[bool] = ContextVar("warned_var", default=False)

    @classmethod
    @contextmanager
    def session(cls):
        """
        The Context Manager.
        Ensures the 'warned' state is reset before and after a processing run.
        """
        token = cls._warned_var.set(False)
        try:
            yield
        finally:
            cls._warned_var.reset(token)

    @classmethod
    def sum_file(cls, file_path: Path, ignore_invalid: bool = True) -> float:
        """
        Sum the numbers in a file.

        Args:
            file_path (Path): Path object to the target file.
            ignore_invalid (bool): If False, raises ValueError on invalid data.
                If True, logs a warning and skips the element.

        Returns:
            float: Sum of all valid numeric elements in the file.

        Raises:
            FileNotFoundError: If the file_path does not exist on disk.
            ValueError: If an unsupported file extension is provided or if
                ignore_invalid is False and non-numeric data is encountered.
            RuntimeError: If a system-level IO error occurs during file access.
        """
        cls._ensure_valid_path_and_extension(file_path=file_path)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                total = 0.0
                for line in f:
                    parts = cls._SEPARATOR_PATTERN.split(line.strip())
                    for part in parts:
                        if part:
                            total += cls._to_float(value=part, ignore_invalid=ignore_invalid)
        except (OSError, PermissionError) as e:
            logger.error(f"System-level error opening {file_path}: {e}")
            raise RuntimeError(f"Could not access data source: {file_path.name}") from e
        except ValueError:
            raise

        return total

    @classmethod
    def _ensure_valid_path_and_extension(cls, file_path: Path):
        """
        Validates file existence and extension support.

        Args:
            file_path (Path): Path object to the target file.

        Raises:
            FileNotFoundError: If the file is not found at the specified path.
            ValueError: If the file extension is not in the supported list.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        if file_path.suffix.lower() not in cls._SUPPORTED_EXT:
            raise ValueError(
                f"Unsupported extension '{file_path.suffix}'. Supported: {cls._SUPPORTED_EXT}"
            )

    @classmethod
    def _to_float(cls, value: str, ignore_invalid: bool = True) -> float:
        """
        Converts a string to a float with optional error handling.

        Args:
            value (str): String element to convert.
            ignore_invalid (bool): Whether to skip invalid data or raise an error.

        Returns:
            float: The converted value, or 0.0 if invalid and ignore_invalid is True.

        Raises:
            ValueError: If conversion fails and ignore_invalid is False.
        """
        try:
            return float(value)
        except ValueError:
            if not ignore_invalid:
                raise

            if not cls._warned_var.get():
                logger.warning("The file contains invalid numeric data. These will be skipped")
                cls._warned_var.set(True)

            return 0.0
