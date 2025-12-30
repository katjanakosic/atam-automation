from pathlib import Path
from typing import List

from pydantic import TypeAdapter

from atam.datatypes import Scenario
from atam.io_utils import read_json

def _load_scenarios(scenarios_path: Path) -> List[Scenario]:
    raw = read_json(scenarios_path)
    return TypeAdapter(List[Scenario]).validate_python(raw)