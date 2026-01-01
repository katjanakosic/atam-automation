import json
import time
from pathlib import Path
from typing import Any

def read_json(path: str | Path) -> Any:
    """
    Read and parse a JSON file, return its contents.

    :param path: Path to the JSON file as string or Path object
    :return: Parsed JSON content (dict, list, str, int, float, bool, or None)

    """
    path = Path(path)
    # Open file in read mode with UTF-8 encoding
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str | Path, obj: Any) -> None:
    """
    Write a Python object to a JSON file with proper formatting.

    :param path: Path to the output JSON file
    :param obj: Python object to serialize to JSON
    :return: None
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


def make_run_dir(out_root: str | Path, domain_name: str) -> Path:
    """
    Create a timestamped run directory for storing analysis results.
    Creates a directory structure: out_root/domain_name/run-YYYYMMDD-HHMMSS/
    This allows organizing multiple runs by domain and timestamp for easier tracking.

    :param out_root: Root directory for all outputs
    :param domain_name: Name of the domain/project being analyzed
    :return: Path object pointing to the created run directory
    """
    out_root = Path(out_root)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    run_dir = out_root / domain_name / f"run-{timestamp}"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir

