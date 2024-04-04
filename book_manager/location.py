from dataclasses import dataclass, field


@dataclass
class Location:
    name: str
    id: int = field(default=0)
