"""Represents the entities used in the application."""

import datetime
import re
from typing import Literal, Optional, List
from pydantic import BaseModel, Field, PositiveFloat, PositiveInt, field_validator


class Supplier(BaseModel):
    id: Optional[int] = None
    name: str
    default_min_processing_days: Optional[int] = 3
    default_max_processing_days: Optional[int] = 5
    reliability: Optional[Literal["high", "medium", "low"]] = "medium"
    is_internal: Optional[bool] = False
    is_dropshipper: Optional[bool] = False


class Brand(BaseModel):
    """Represents a Brand."""

    id: Optional[PositiveInt] = None
    name: str


class Taxonomy(BaseModel):
    """Represents a Taxonomy."""

    id: Optional[PositiveInt] + None
    path: str


class Product(BaseModel):
    """Common data between a Simple and a Variant product."""

    id: Optional[str] = None
    type: Literal["simple", "variant"] = "simple"
    brand: Optional[Brand] = None
    title: Optional[str] = None
    micro_description: Optional[str] = None
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    taxonomy: Optional[Taxonomy] = None
    raw_specs: Optional[dict] = None


class Attribute(BaseModel):
    """Represents a Product Attribute."""

    id: Optional[PositiveInt] = 0
    name: str
    type: Literal["string", "integer", "float"]


class AttributeValue(BaseModel):
    """Represents a Product Attribute Value."""

    value: str | PositiveInt | PositiveFloat
    attribute: Attribute


class Variant(BaseModel):
    """Variant-specific data linked to a parent `Product`."""

    id: Optional[str] = None
    parent_product: Product
    ean: str
    title: Optional[str] = None
    images: List[str] = Field(default_factory=list)
    weight_grams: Optional[PositiveFloat] = None
    height_centimeters: Optional[PositiveFloat] = None
    width_centimeters: Optional[PositiveFloat] = None
    depth_centimeters: Optional[PositiveFloat] = None
    attributes: Optional[list[AttributeValue]] = None
    raw_specs: Optional[dict] = None

    @field_validator("ean")
    @classmethod
    def ean_must_be_valid(cls, v):
        """Validates the EAN."""

        digit_regex = r"^\d+{13}$"
        if not re.match(digit_regex, v):
            raise ValueError("Invalid EAN.")
        return v


class Task(BaseModel):
    """Represents a Task."""

    id: Optional[PositiveInt] = None
    error_count: PositiveInt = 0
    completed_count: PositiveInt = 0
    success_count: PositiveInt = 0
    tasks_number: PositiveInt = 0
    done: bool = False
    error_data: Optional[dict] = None
    output_urls: list = Field(default_factory=list)


class Offer(BaseModel):
    """Represents a supplier offer."""

    price: float
    quantity: Optional[int] = 0
    supplier: Supplier
    variant: Variant
    currency: Optional[Literal["eur", "usd"]] = "eur"
    min_processing_days: Optional[int] = 3
    max_processing_days: Optional[int] = 5
    is_preferred: Optional[bool] = False
    is_locked: Optional[bool] = False


class Price(BaseModel):
    """Represents a price."""

    price: float
    quantity: Optional[int] = 0
    supplier: Optional[Supplier] = None
    variant: Optional[Variant] = None
    updated_at: str = Field(default_factory=lambda _: datetime.now().isoformat())
