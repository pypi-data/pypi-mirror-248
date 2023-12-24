from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class ApiGwResponse:
    statusCode: int
    headers: Optional[dict]
    body: Optional[str]

    def to_dict(self):
        response_dict = asdict(self)
        return response_dict
