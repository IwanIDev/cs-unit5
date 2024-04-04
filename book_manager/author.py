from dataclasses import dataclass, field


@dataclass
class Author:
    name: str
    id: int = field(default=0)
