"""Shared data models, used by both the command-line app and the web API."""

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FitnessGoal(str, Enum):
    WEIGHT_LOSS = "weight_loss"
    MUSCLE_GAIN = "muscle_gain"
    MAINTENANCE = "maintenance"
    GENERAL_FITNESS = "general_fitness"


class DietType(str, Enum):
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    NON_VEGETARIAN = "non_vegetarian"
    EGGETARIAN = "eggetarian"


class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    ACTIVE = "active"
    VERY_ACTIVE = "very_active"


class Sex(str, Enum):
    MALE = "male"
    FEMALE = "female"


class ExperienceLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


MAX_LIST_ITEMS = 20
MAX_ITEM_LENGTH = 40


def _clean_list(value):
    """Accept a list or a comma separated string; lowercase, trim, dedupe."""

    if value is None:
        return []

    if isinstance(value, str):
        value = value.split(",")

    if not isinstance(value, (list, tuple, set)):
        raise ValueError("must be a list")

    cleaned = (
        str(item).strip().lower()[:MAX_ITEM_LENGTH]
        for item in value
        if str(item).strip()
    )

    return list(dict.fromkeys(cleaned))[:MAX_LIST_ITEMS]


class UserProfile(BaseModel):

    model_config = ConfigDict(
        str_strip_whitespace=True,
        allow_inf_nan=False
    )

    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=18, le=100)
    height_cm: float = Field(gt=100, le=230)
    weight_kg: float = Field(gt=30, le=300)

    fitness_goal: FitnessGoal
    diet_type: DietType
    activity_level: ActivityLevel
    sex: Sex

    experience_level: ExperienceLevel = ExperienceLevel.BEGINNER

    workout_minutes: int = Field(ge=5, le=180)

    equipment: list[str] = Field(default_factory=list)
    allergies: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)

    @field_validator(
        "equipment", "allergies", "limitations", mode="before"
    )
    @classmethod
    def clean_lists(cls, value):
        return _clean_list(value)