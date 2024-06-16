from dataclasses import dataclass


@dataclass
class ExampleSentenceReadDTO:
    sentence: str
    translation: str
