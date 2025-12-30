import json
import time
from pathlib import Path
from typing import Any

def read_json(path: str | Path) -> Any:
    """Read and parse a JSON file, return its contents.

    :param path: Path to the JSON file as string or Path object
    :return: Parsed JSON content (dict, list, str, int, float, bool, or None)

    """
    path = Path(path)
    # Open file in read mode with UTF-8 encoding
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
