from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ExampleSentenceReadDTO:
    sentence: str
    reading_hints: List[Dict]
    translation: str
