from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ExampleSentence:
    sentence: str
    reading_hints: List[Dict]
    translation: str
