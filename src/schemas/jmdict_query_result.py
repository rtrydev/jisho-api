from typing import List, TypedDict


class JMdictQueryResult(TypedDict):
    entries: List[str]
    glossary: List[str]
    reading: str
    