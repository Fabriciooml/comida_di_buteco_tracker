from dataclasses import dataclass, field


@dataclass
class Bar:
    name: str
    detail_url: str
    address: str | None = field(default=None)
    street: str | None = field(default=None)
    street_number: str | None = field(default=None)
    complement: str | None = field(default=None)
    neighborhood: str | None = field(default=None)
    city: str | None = field(default=None)
    state: str | None = field(default=None)
    food_name: str | None = field(default=None)
    food_image_url: str | None = field(default=None)
    food_description: str | None = field(default=None)
    food_category: str | None = field(default=None)
    is_vegan: bool | None = field(default=None)
    is_vegetarian: bool | None = field(default=None)
    working_hours: str | None = field(default=None)
