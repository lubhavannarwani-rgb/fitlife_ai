import math
import random

from food_database import (
    FOOD_DATABASE,
    FOOD_ALLERGENS,
    resolve_allergies
)


# ==================================================
# 1. MEAL TEMPLATES
# All ingredient quantities use the database unit
# (grams, or ml for liquids).
# ==================================================

MEAL_TEMPLATES = {

    "breakfast": [

        {
            "name": "Oats and milk bowl",
            "diet": ["vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "oats_dry": 50,
                "milk_toned": 200,
                "banana": 100
            }
        },

        {
            "name": "Vegan oats bowl",
            "diet": ["vegan", "vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "oats_dry": 50,
                "banana": 100,
                "almonds": 10
            }
        },

        {
            "name": "Paneer roti breakfast",
            "diet": ["vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "whole_wheat_roti": 60,
                "low_fat_paneer": 100,
                "tomato": 50
            }
        },

        {
            "name": "Egg and bread breakfast",
            "diet": ["eggetarian", "non_vegetarian"],
            "ingredients": {
                "whole_egg_boiled": 100,
                "brown_bread": 60,
                "tomato": 50
            }
        },

        # NEW: gluten-free / nut-free vegan breakfasts
        {
            "name": "Vegetable poha",
            "diet": ["vegan", "vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "poha_cooked": 200,
                "peas_green": 50,
                "tomato": 50
            }
        },

        {
            "name": "Banana and seeds bowl",
            "diet": ["vegan", "vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "banana": 120,
                "chia_seeds": 15,
                "pumpkin_seeds": 15
            }
        }
    ],

    "morning_snack": [

        {
            "name": "Fruit and curd",
            "diet": ["vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "apple": 150,
                "curd": 100
            }
        },

        {
            "name": "Fruit and nuts",
            "diet": ["vegan", "vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "banana": 100,
                "almonds": 10
            }
        },

        {
            "name": "Sprouts bowl",
            "diet": ["vegan", "vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "moong_sprouts": 100,
                "cucumber": 50,
                "tomato": 50
            }
        },

        {
            "name": "Guava and seeds",
            "diet": ["vegan", "vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "guava": 100,
                "pumpkin_seeds": 15
            }
        },

        {
            "name": "Buttermilk and papaya",
            "diet": ["vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "buttermilk": 200,
                "papaya": 100
            }
        }
    ],

    "lunch": [

        {
            "name": "Dal rice meal",
            "diet": ["vegan", "vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "rice_cooked": 150,
                "moong_dal_cooked": 150,
                "cucumber": 100
            }
        },

        {
            "name": "Rajma rice meal",
            "diet": ["vegan", "vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "rice_cooked": 150,
                "rajma_cooked": 150,
                "carrot": 50
            }
        },

        {
            "name": "Chicken rice meal",
            "diet": ["non_vegetarian"],
            "ingredients": {
                "rice_cooked": 150,
                "chicken_breast_cooked": 120,
                "broccoli": 100
            }
        },

        {
            "name": "Paneer roti meal",
            "diet": ["vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "whole_wheat_roti": 100,
                "low_fat_paneer": 100,
                "spinach": 100
            }
        },

        # NEW
        {
            "name": "Masoor dal rice meal",
            "diet": ["vegan", "vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "rice_cooked": 150,
                "masoor_dal_cooked": 150,
                "tomato": 100
            }
        },

        {
            "name": "Fish rice meal",
            "diet": ["non_vegetarian"],
            "ingredients": {
                "rice_cooked": 150,
                "fish_cooked": 120,
                "spinach": 100
            }
        },

        {
            "name": "Chicken roti meal",
            "diet": ["non_vegetarian"],
            "ingredients": {
                "whole_wheat_roti": 100,
                "chicken_breast_cooked": 120,
                "cucumber": 100
            }
        }
    ],

    "evening_snack": [

        {
            "name": "Greek yogurt bowl",
            "diet": ["vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "greek_yogurt_plain": 150,
                "banana": 80
            }
        },

        {
            "name": "Chickpea bowl",
            "diet": ["vegan", "vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "chickpeas_cooked": 100,
                "cucumber": 50
            }
        },

        {
            "name": "Egg snack",
            "diet": ["eggetarian", "non_vegetarian"],
            "ingredients": {
                "whole_egg_boiled": 100,
                "tomato": 50
            }
        },

        # NEW
        {
            "name": "Sweet potato snack",
            "diet": ["vegan", "vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "sweet_potato_boiled": 150,
                "cucumber": 50
            }
        },

        {
            "name": "Tuna salad",
            "diet": ["non_vegetarian"],
            "ingredients": {
                "tuna_canned_in_water": 80,
                "tomato": 50,
                "cucumber": 50
            }
        }
    ],

    "dinner": [

        {
            "name": "Dal roti dinner",
            "diet": ["vegan", "vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "whole_wheat_roti": 100,
                "moong_dal_cooked": 150,
                "spinach": 100
            }
        },

        {
            "name": "Tofu rice dinner",
            "diet": ["vegan", "vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "brown_rice_cooked": 150,
                "tofu": 150,
                "broccoli": 100
            }
        },

        {
            "name": "Chicken and vegetables",
            "diet": ["non_vegetarian"],
            "ingredients": {
                "chicken_breast_cooked": 120,
                "brown_rice_cooked": 150,
                "broccoli": 100
            }
        },

        {
            "name": "Paneer rice dinner",
            "diet": ["vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "brown_rice_cooked": 150,
                "low_fat_paneer": 100,
                "spinach": 100
            }
        },

        # NEW
        {
            "name": "Chana dal rice dinner",
            "diet": ["vegan", "vegetarian", "eggetarian", "non_vegetarian"],
            "ingredients": {
                "brown_rice_cooked": 150,
                "chana_dal_cooked": 150,
                "cauliflower": 100
            }
        },

        {
            "name": "Fish and rice dinner",
            "diet": ["non_vegetarian"],
            "ingredients": {
                "fish_cooked": 120,
                "brown_rice_cooked": 150,
                "spinach": 100
            }
        }
    ]
}


# Share of the daily calorie target given to each meal.
MEAL_CALORIE_SPLIT = {
    "breakfast": 0.25,
    "morning_snack": 0.10,
    "lunch": 0.30,
    "evening_snack": 0.10,
    "dinner": 0.25
}

# Portions are never scaled outside this range,
# so meals stay realistic.
MIN_PORTION_SCALE = 0.6
MAX_PORTION_SCALE = 2.3


# ==================================================
# 2. INPUT VALIDATION
# ==================================================

VALID_DIETS = {
    "vegan",
    "vegetarian",
    "eggetarian",
    "non_vegetarian"
}


def validate_inputs(diet_type, allergies):

    diet_type = str(diet_type).lower().strip()

    if diet_type not in VALID_DIETS:
        raise ValueError("Invalid diet type")

    if isinstance(allergies, str):
        allergies = [allergies]

    if not isinstance(allergies, (list, tuple, set)):
        raise ValueError("Allergies must be a list")

    allergies = [
        str(item).lower().strip()
        for item in allergies
        if str(item).strip()
    ]

    return diet_type, allergies


# ==================================================
# 3. CALCULATE FOOD NUTRITION
# ==================================================

def calculate_food_nutrition(food_name, quantity):

    if food_name not in FOOD_DATABASE:
        raise ValueError(f"Food not found: {food_name}")

    if isinstance(quantity, bool) or not isinstance(quantity, (int, float)):
        raise ValueError("Quantity must be numeric")

    if quantity <= 0:
        raise ValueError("Quantity must be positive")

    food = FOOD_DATABASE[food_name]

    factor = quantity / 100

    return {
        "calories": round(food["calories"] * factor, 2),
        "protein": round(food["protein"] * factor, 2),
        "carbs": round(food["carbs"] * factor, 2),
        "fat": round(food["fat"] * factor, 2),
        "fibre": round(food["fibre"] * factor, 2)
    }


# ==================================================
# 4. CALCULATE MEAL NUTRITION
# ==================================================

def calculate_meal_nutrition(ingredients):

    total = {
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0,
        "fibre": 0
    }

    for food_name, quantity in ingredients.items():

        nutrition = calculate_food_nutrition(
            food_name,
            quantity
        )

        for key in total:
            total[key] += nutrition[key]

    return {
        key: round(value, 2)
        for key, value in total.items()
    }


# ==================================================
# 5. ALLERGY AND DIET CHECKING
# ==================================================

def is_food_safe(food_name, canonical_allergens, raw_terms):

    food_allergens = {
        item.lower()
        for item in FOOD_ALLERGENS.get(food_name, [])
    }

    # Allergen match (e.g. "dairy" -> "milk")
    if canonical_allergens.intersection(food_allergens):
        return False

    # Ingredient-name match (e.g. allergy to "banana")
    if any(term in food_name for term in raw_terms):
        return False

    return True


def is_meal_suitable(meal, diet_type, canonical_allergens, raw_terms):

    # Meal-level diet compatibility
    if diet_type not in meal["diet"]:
        return False

    for food_name in meal["ingredients"]:

        if food_name not in FOOD_DATABASE:
            return False

        food = FOOD_DATABASE[food_name]

        # Ingredient-level diet compatibility
        if diet_type not in food["diet"]:
            return False

        if not is_food_safe(
            food_name,
            canonical_allergens,
            raw_terms
        ):
            return False

    return True


# ==================================================
# 6. PORTION SCALING
# ==================================================

def scale_ingredients(ingredients, factor):

    scaled = {}

    for food_name, quantity in ingredients.items():

        new_quantity = int(round((quantity * factor) / 5) * 5)

        scaled[food_name] = max(5, new_quantity)

    return scaled


def choose_meal(suitable_meals, meal_calorie_target, rng):
    """
    Pick a meal and the factor needed to reach its calorie share.
    Without a calorie target the template is used as written.
    """

    if meal_calorie_target is None:
        return rng.choice(suitable_meals), 1.0

    options = []

    for meal in suitable_meals:

        base = calculate_meal_nutrition(
            meal["ingredients"]
        )["calories"]

        factor = meal_calorie_target / base if base > 0 else 1.0

        options.append((meal, factor))

    in_range = [
        option for option in options
        if MIN_PORTION_SCALE <= option[1] <= MAX_PORTION_SCALE
    ]

    if in_range:
        meal, factor = rng.choice(in_range)

    else:
        # Nothing fits the range: take the closest and clamp it
        meal, factor = min(
            options,
            key=lambda option: abs(math.log(option[1]))
        )

    factor = min(max(factor, MIN_PORTION_SCALE), MAX_PORTION_SCALE)

    return meal, factor


# ==================================================
# 7. GENERATE MEAL PLAN
# ==================================================

def generate_meal_plan(
    diet_type,
    allergies=None,
    calorie_target=None,
    macro_targets=None,
    seed=None
):
    """
    Build a one-day meal plan.

    diet_type      : vegan / vegetarian / eggetarian / non_vegetarian
    allergies      : list of allergies (aliases such as "dairy" work)
    calorie_target : optional daily calories; portions are scaled to it
    macro_targets  : optional {"protein_g":..., "carbs_g":..., "fat_g":...}
                     used only to report how close the plan is
    seed           : optional number for a repeatable plan
    """

    if allergies is None:
        allergies = []

    if calorie_target is not None:

        if (
            isinstance(calorie_target, bool)
            or not isinstance(calorie_target, (int, float))
            or calorie_target <= 0
        ):
            raise ValueError("Calorie target must be a positive number")

    diet_type, allergies = validate_inputs(
        diet_type,
        allergies
    )

    canonical_allergens, raw_terms, unknown = resolve_allergies(allergies)

    rng = random.Random(seed)

    meals = {}

    for meal_type, templates in MEAL_TEMPLATES.items():

        suitable_meals = [
            meal for meal in templates
            if is_meal_suitable(
                meal,
                diet_type,
                canonical_allergens,
                raw_terms
            )
        ]

        if not suitable_meals:
            raise ValueError(
                f"No suitable {meal_type} found for diet "
                f"'{diet_type}' with allergies {allergies}"
            )

        meal_target = (
            calorie_target * MEAL_CALORIE_SPLIT[meal_type]
            if calorie_target is not None
            else None
        )

        selected_meal, factor = choose_meal(
            suitable_meals,
            meal_target,
            rng
        )

        ingredients = scale_ingredients(
            selected_meal["ingredients"],
            factor
        )

        meals[meal_type] = {
            "name": selected_meal["name"],

            "ingredients": [
                {
                    "food": food_name,
                    "quantity": quantity,
                    "unit": FOOD_DATABASE[food_name]["serving_unit"]
                }
                for food_name, quantity in ingredients.items()
            ],

            "nutrition": calculate_meal_nutrition(ingredients)
        }

    daily_totals = calculate_daily_totals(meals)

    warnings = [
        "Allergy filtering uses an unverified ingredient list and "
        "cannot guarantee safety. Always check food labels."
    ]

    if unknown:
        warnings.append(
            "These allergies are not in the food database and could "
            f"not be filtered: {', '.join(unknown)}"
        )

    return {
        "meals": meals,
        "daily_totals": daily_totals,
        "targets": compare_with_targets(
            daily_totals,
            calorie_target,
            macro_targets
        ),
        "warnings": warnings
    }


# ==================================================
# 8. DAILY TOTALS AND TARGET COMPARISON
# ==================================================

def calculate_daily_totals(meals):

    totals = {
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0,
        "fibre": 0
    }

    for meal in meals.values():

        nutrition = meal["nutrition"]

        for key in totals:
            totals[key] += nutrition[key]

    return {
        key: round(value, 2)
        for key, value in totals.items()
    }


def compare_with_targets(daily_totals, calorie_target, macro_targets):
    """
    Compare actual totals with targets so the result is verified
    rather than assumed. Returns {} when no targets were given.
    """

    pairs = []

    if calorie_target is not None:
        pairs.append(("calories", calorie_target, daily_totals["calories"]))

    if macro_targets:

        mapping = {
            "protein_g": "protein",
            "carbs_g": "carbs",
            "fat_g": "fat"
        }

        for target_key, total_key in mapping.items():

            if target_key in macro_targets:
                pairs.append((
                    target_key,
                    macro_targets[target_key],
                    daily_totals[total_key]
                ))

    comparison = {}

    for name, target, actual in pairs:

        comparison[name] = {
            "target": round(target, 2),
            "actual": round(actual, 2),
            "difference": round(actual - target, 2),
            "percent_of_target": (
                round(actual / target * 100, 1) if target else None
            )
        }

    return comparison


# ==================================================
# 9. DISPLAY MEAL PLAN
# ==================================================

def display_meal_plan(plan):

    for meal_type, meal in plan["meals"].items():

        print("\n" + "=" * 40)
        print(meal_type.upper().replace("_", " "))
        print("Meal:", meal["name"])

        print("\nIngredients:")

        for item in meal["ingredients"]:
            print(f"  {item['food']}: {item['quantity']} {item['unit']}")

        print("\nNutrition:")

        for key, value in meal["nutrition"].items():
            print(f"  {key}: {value}")

    print("\n" + "=" * 40)
    print("DAILY TOTALS")

    for key, value in plan["daily_totals"].items():
        print(f"  {key}: {value}")

    if plan["targets"]:

        print("\nTARGET CHECK")

        for name, data in plan["targets"].items():
            print(
                f"  {name}: {data['actual']} / {data['target']} "
                f"({data['percent_of_target']}%)"
            )

    for warning in plan["warnings"]:
        print("\nNOTE:", warning)


# ==================================================
# 10. TEST
# ==================================================

if __name__ == "__main__":

    plan = generate_meal_plan(
        diet_type="vegetarian",
        allergies=["dairy"],
        calorie_target=2000,
        macro_targets={
            "protein_g": 110,
            "carbs_g": 250,
            "fat_g": 55
        }
    )

    display_meal_plan(plan)