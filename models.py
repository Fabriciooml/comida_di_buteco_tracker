from dataclasses import dataclass, field


@dataclass
class Bar:
    name: str
    detail_url: str
    address: str | None = field(default=None)
    food_name: str | None = field(default=None)
    food_image_url: str | None = field(default=None)
    food_description: str | None = field(default=None)
    working_hours: str | None = field(default=None)
