def make_food(
    calories, protein, carbs, fat, fibre,
    diet, allergens, serving_size, serving_unit,
    food_state="ready_to_eat",
    allergen_status="ingredient_based_unverified",
    source="USDA_IFCT_REFERENCE_PENDING"
):
    return {
        "calories": float(calories),
        "protein": float(protein),
        "carbs": float(carbs),
        "fat": float(fat),
        "fibre": float(fibre),

        "diet": list(diet),
        "allergens": list(allergens),

        "allergen_status": allergen_status,

        "serving_size": serving_size,
        "serving_unit": serving_unit,

        "nutrition_basis": (
            "per_100_ml"
            if serving_unit == "ml"
            else "per_100_g"
        ),

        "food_state": food_state,
        "source": source,
        "verified": False
    }


ALL_DIETS = [
    "vegan",
    "vegetarian",
    "eggetarian",
    "non_vegetarian"
]

VEGAN = ALL_DIETS.copy()

VEGETARIAN = [
    "vegetarian",
    "eggetarian",
    "non_vegetarian"
]

EGG_FOODS = [
    "eggetarian",
    "non_vegetarian"
]

NON_VEG = [
    "non_vegetarian"
]


FOOD_DATABASE = {

    # ==================================================
    # 1. GRAINS AND CEREALS
    # ==================================================

    # FIX: oats are commonly cross-contaminated with gluten,
    # so a "gluten" allergy now also excludes oats.
    "oats_dry": make_food(
        389, 16.9, 66.3, 6.9, 10.6,
        VEGAN, ["oats", "gluten"], 40, "g", "raw"
    ),

    "rice_raw": make_food(
        365, 7.1, 80.0, 0.7, 1.3,
        VEGAN, [], 50, "g", "raw"
    ),

    "rice_cooked": make_food(
        130, 2.7, 28.2, 0.3, 0.4,
        VEGAN, [], 150, "g", "cooked"
    ),

    "brown_rice_raw": make_food(
        370, 7.5, 77.2, 2.7, 3.5,
        VEGAN, [], 50, "g", "raw"
    ),

    "brown_rice_cooked": make_food(
        123, 2.7, 25.6, 1.0, 1.6,
        VEGAN, [], 150, "g", "cooked"
    ),

    "wheat_flour": make_food(
        340, 13.2, 72.0, 2.5, 10.7,
        VEGAN, ["wheat", "gluten"], 30, "g", "raw"
    ),

    "whole_wheat_roti": make_food(
        297, 9.0, 55.0, 7.0, 8.0,
        VEGAN, ["wheat", "gluten"], 40, "g", "cooked"
    ),

    "white_bread": make_food(
        265, 9.0, 49.0, 3.2, 2.7,
        VEGAN, ["wheat", "gluten"], 30, "g"
    ),

    "brown_bread": make_food(
        250, 9.0, 43.0, 3.5, 6.0,
        VEGAN, ["wheat", "gluten"], 30, "g"
    ),

    "poha_dry": make_food(
        350, 6.7, 77.0, 1.0, 1.0,
        VEGAN, [], 50, "g", "raw"
    ),

    "poha_cooked": make_food(
        130, 2.5, 25.0, 2.5, 1.5,
        VEGAN, [], 150, "g", "cooked"
    ),

    # ==================================================
    # 2. DAIRY PRODUCTS
    # ==================================================

    "milk_full_fat": make_food(
        61, 3.2, 4.8, 3.3, 0,
        VEGETARIAN, ["milk"], 250, "ml"
    ),

    "milk_toned": make_food(
        58, 3.0, 4.8, 3.0, 0,
        VEGETARIAN, ["milk"], 250, "ml"
    ),

    "milk_skimmed": make_food(
        34, 3.4, 5.0, 0.1, 0,
        VEGETARIAN, ["milk"], 250, "ml"
    ),

    "curd": make_food(
        61, 3.5, 4.7, 3.3, 0,
        VEGETARIAN, ["milk"], 150, "g"
    ),

    "greek_yogurt_plain": make_food(
        97, 9.0, 3.9, 5.0, 0,
        VEGETARIAN, ["milk"], 150, "g"
    ),

    "paneer": make_food(
        265, 18.3, 1.2, 20.8, 0,
        VEGETARIAN, ["milk"], 100, "g"
    ),

    "low_fat_paneer": make_food(
        170, 23.0, 4.0, 7.0, 0,
        VEGETARIAN, ["milk"], 100, "g"
    ),

    "cheese": make_food(
        350, 22.0, 2.0, 28.0, 0,
        VEGETARIAN, ["milk"], 30, "g"
    ),

    "buttermilk": make_food(
        40, 3.0, 4.0, 1.0, 0,
        VEGETARIAN, ["milk"], 250, "ml"
    ),

    "ghee": make_food(
        900, 0, 0, 100, 0,
        VEGETARIAN, ["milk"], 10, "g"
    ),

    # ==================================================
    # 3. PULSES AND LEGUMES
    # ==================================================

    "moong_dal_raw": make_food(
        347, 24.0, 63.0, 1.2, 16.0,
        VEGAN, [], 50, "g", "raw"
    ),

    "moong_dal_cooked": make_food(
        105, 7.0, 19.0, 0.4, 7.0,
        VEGAN, [], 150, "g", "cooked"
    ),

    "masoor_dal_raw": make_food(
        352, 24.6, 63.1, 1.1, 10.7,
        VEGAN, [], 50, "g", "raw"
    ),

    "masoor_dal_cooked": make_food(
        116, 9.0, 20.0, 0.4, 7.9,
        VEGAN, [], 150, "g", "cooked"
    ),

    "chana_dal_raw": make_food(
        360, 20.0, 60.0, 5.0, 12.0,
        VEGAN, [], 50, "g", "raw"
    ),

    "chana_dal_cooked": make_food(
        164, 8.9, 27.4, 2.6, 7.6,
        VEGAN, [], 150, "g", "cooked"
    ),

    "rajma_raw": make_food(
        333, 23.6, 60.0, 0.8, 24.9,
        VEGAN, [], 50, "g", "raw"
    ),

    "rajma_cooked": make_food(
        127, 8.7, 22.8, 0.5, 6.4,
        VEGAN, [], 150, "g", "cooked"
    ),

    "chickpeas_raw": make_food(
        378, 20.5, 63.0, 6.0, 12.2,
        VEGAN, [], 50, "g", "raw"
    ),

    "chickpeas_cooked": make_food(
        164, 8.9, 27.4, 2.6, 7.6,
        VEGAN, [], 100, "g", "cooked"
    ),

    "black_chana_cooked": make_food(
        164, 8.9, 27.4, 2.6, 7.6,
        VEGAN, [], 100, "g", "cooked"
    ),

    "soy_chunks_dry": make_food(
        345, 52.0, 33.0, 0.5, 13.0,
        VEGAN, ["soy"], 30, "g", "raw"
    ),

    "tofu": make_food(
        76, 8.0, 1.9, 4.8, 0.3,
        VEGAN, ["soy"], 100, "g"
    ),

    "moong_sprouts": make_food(
        30, 3.0, 6.0, 0.2, 1.8,
        VEGAN, [], 100, "g", "sprouted"
    ),

    # ==================================================
    # 4. EGGS AND NON-VEGETARIAN FOODS
    # ==================================================

    "whole_egg_boiled": make_food(
        155, 12.6, 1.1, 10.6, 0,
        EGG_FOODS, ["egg"], 50, "g", "cooked"
    ),

    "egg_white_boiled": make_food(
        52, 10.9, 0.7, 0.2, 0,
        EGG_FOODS, ["egg"], 33, "g", "cooked"
    ),

    "chicken_breast_raw": make_food(
        120, 22.5, 0, 2.6, 0,
        NON_VEG, [], 100, "g", "raw"
    ),

    "chicken_breast_cooked": make_food(
        165, 31.0, 0, 3.6, 0,
        NON_VEG, [], 100, "g", "cooked"
    ),

    "chicken_thigh_cooked": make_food(
        209, 26.0, 0, 10.9, 0,
        NON_VEG, [], 100, "g", "cooked"
    ),

    "fish_cooked": make_food(
        128, 26.0, 0, 2.7, 0,
        NON_VEG, ["fish"], 100, "g", "cooked"
    ),

    "tuna_canned_in_water": make_food(
        116, 25.5, 0, 0.8, 0,
        NON_VEG, ["fish"], 100, "g", "canned"
    ),

    "prawns_cooked": make_food(
        99, 24.0, 0.2, 0.3, 0,
        NON_VEG, ["crustacean_shellfish"], 100, "g", "cooked"
    ),

    # ==================================================
    # 5. FRUITS
    # ==================================================

    "banana": make_food(
        89, 1.1, 22.8, 0.3, 2.6,
        VEGAN, [], 120, "g"
    ),

    "apple": make_food(
        52, 0.3, 13.8, 0.2, 2.4,
        VEGAN, [], 150, "g"
    ),

    "orange": make_food(
        47, 0.9, 11.8, 0.1, 2.4,
        VEGAN, [], 130, "g"
    ),

    "mango": make_food(
        60, 0.8, 15.0, 0.4, 1.6,
        VEGAN, [], 150, "g"
    ),

    "papaya": make_food(
        43, 0.5, 10.8, 0.3, 1.7,
        VEGAN, [], 150, "g"
    ),

    "guava": make_food(
        68, 2.6, 14.3, 1.0, 5.4,
        VEGAN, [], 100, "g"
    ),

    "watermelon": make_food(
        30, 0.6, 7.6, 0.2, 0.4,
        VEGAN, [], 200, "g"
    ),

    "pomegranate": make_food(
        83, 1.7, 18.7, 1.2, 4.0,
        VEGAN, [], 100, "g"
    ),

    "grapes": make_food(
        69, 0.7, 18.1, 0.2, 0.9,
        VEGAN, [], 100, "g"
    ),

    # ==================================================
    # 6. VEGETABLES
    # ==================================================

    "potato_raw": make_food(
        77, 2.0, 17.5, 0.1, 2.2,
        VEGAN, [], 150, "g", "raw"
    ),

    "potato_boiled": make_food(
        87, 1.9, 20.1, 0.1, 1.8,
        VEGAN, [], 150, "g", "boiled"
    ),

    "sweet_potato_boiled": make_food(
        76, 1.4, 17.7, 0.1, 2.5,
        VEGAN, [], 150, "g", "boiled"
    ),

    "broccoli": make_food(
        34, 2.8, 6.6, 0.4, 2.6,
        VEGAN, [], 100, "g"
    ),

    "spinach": make_food(
        23, 2.9, 3.6, 0.4, 2.2,
        VEGAN, [], 100, "g"
    ),

    "carrot": make_food(
        41, 0.9, 9.6, 0.2, 2.8,
        VEGAN, [], 80, "g"
    ),

    "cucumber": make_food(
        15, 0.7, 3.6, 0.1, 0.5,
        VEGAN, [], 100, "g"
    ),

    "tomato": make_food(
        18, 0.9, 3.9, 0.2, 1.2,
        VEGAN, [], 100, "g"
    ),

    "cauliflower": make_food(
        25, 1.9, 5.0, 0.3, 2.0,
        VEGAN, [], 100, "g"
    ),

    "peas_green": make_food(
        81, 5.4, 14.5, 0.4, 5.1,
        VEGAN, [], 100, "g"
    ),

    # ==================================================
    # 7. NUTS AND SEEDS
    # ==================================================

    "almonds": make_food(
        579, 21.2, 21.6, 49.9, 12.5,
        VEGAN, ["tree_nuts"], 30, "g", "raw"
    ),

    "peanuts": make_food(
        567, 25.8, 16.1, 49.2, 8.5,
        VEGAN, ["peanut"], 30, "g", "raw"
    ),

    "walnuts": make_food(
        654, 15.2, 13.7, 65.2, 6.7,
        VEGAN, ["tree_nuts"], 30, "g", "raw"
    ),

    "cashews": make_food(
        553, 18.2, 30.2, 43.9, 3.3,
        VEGAN, ["tree_nuts"], 30, "g", "raw"
    ),

    "chia_seeds": make_food(
        486, 16.5, 42.1, 30.7, 34.4,
        VEGAN, [], 15, "g", "raw"
    ),

    "flax_seeds": make_food(
        534, 18.3, 28.9, 42.2, 27.3,
        VEGAN, [], 15, "g", "raw"
    ),

    "pumpkin_seeds": make_food(
        559, 30.2, 10.7, 49.1, 6.0,
        VEGAN, [], 20, "g", "raw"
    ),

    "peanut_butter": make_food(
        588, 25.0, 20.0, 50.0, 6.0,
        VEGAN, ["peanut"], 30, "g"
    ),

    # ==================================================
    # 8. OTHER FOODS
    # ==================================================

    "dark_chocolate": make_food(
        598, 7.8, 45.9, 42.6, 10.9,
        VEGETARIAN, ["milk", "soy"], 20, "g"
    ),

    "honey": make_food(
        304, 0.3, 82.4, 0, 0,
        VEGETARIAN, [], 15, "g"
    ),

    "coconut_fresh": make_food(
        354, 3.3, 15.2, 33.5, 9.0,
        VEGAN, ["tree_nuts"], 30, "g"
    ),

    "olive_oil": make_food(
        884, 0, 0, 100, 0,
        VEGAN, [], 10, "g"
    )
}


FOOD_ALLERGENS = {
    food_name: details["allergens"]
    for food_name, details in FOOD_DATABASE.items()
}


# ==================================================
# 9. ALLERGEN NAMES AND ALIASES
# ==================================================
# FIX: users type things like "dairy", "nuts", "eggs" or "shellfish",
# but the database uses "milk", "tree_nuts", "egg" and
# "crustacean_shellfish". Without this mapping, those allergies
# were silently ignored.

KNOWN_ALLERGENS = {
    allergen
    for allergens in FOOD_ALLERGENS.values()
    for allergen in allergens
}

ALLERGEN_ALIASES = {
    "milk": ["milk"],
    "dairy": ["milk"],
    "lactose": ["milk"],
    "milk products": ["milk"],

    "egg": ["egg"],
    "eggs": ["egg"],

    "peanut": ["peanut"],
    "peanuts": ["peanut"],
    "groundnut": ["peanut"],
    "groundnuts": ["peanut"],

    "nut": ["tree_nuts", "peanut"],
    "nuts": ["tree_nuts", "peanut"],
    "tree nut": ["tree_nuts"],
    "tree nuts": ["tree_nuts"],
    "almond": ["tree_nuts"],
    "almonds": ["tree_nuts"],
    "walnut": ["tree_nuts"],
    "walnuts": ["tree_nuts"],
    "cashew": ["tree_nuts"],
    "cashews": ["tree_nuts"],

    "soy": ["soy"],
    "soya": ["soy"],
    "soybean": ["soy"],
    "soybeans": ["soy"],

    "gluten": ["gluten", "wheat"],
    "wheat": ["wheat", "gluten"],
    "oat": ["oats"],
    "oats": ["oats"],

    "fish": ["fish"],
    "seafood": ["fish", "crustacean_shellfish"],
    "shellfish": ["crustacean_shellfish"],
    "crustacean": ["crustacean_shellfish"],
    "crustaceans": ["crustacean_shellfish"],
    "prawn": ["crustacean_shellfish"],
    "prawns": ["crustacean_shellfish"],
    "shrimp": ["crustacean_shellfish"]
}


def resolve_allergies(allergies):
    """
    Convert free-text allergies into database allergen names.

    Returns:
        canonical : set of database allergen names (e.g. "milk")
        raw_terms : set of the user's own words as food-name fragments
                    (e.g. "banana"), so an allergy to a specific
                    ingredient still works
        unknown   : list of allergies that could not be matched to
                    anything in the database
    """

    canonical = set()
    raw_terms = set()
    unknown = []

    for item in allergies:

        term = str(item).lower().strip()
        term = term.replace("_", " ").replace("-", " ")
        term = " ".join(term.split())

        if not term:
            continue

        key = term.replace(" ", "_")
        raw_terms.add(key)

        if term in ALLERGEN_ALIASES:
            canonical.update(ALLERGEN_ALIASES[term])

        elif key in KNOWN_ALLERGENS:
            canonical.add(key)

        elif any(key in food_name for food_name in FOOD_DATABASE):
            # Matches an ingredient name, handled by name matching
            pass

        else:
            unknown.append(term)

    return canonical, raw_terms, unknown


# ==================================================
# 10. DATABASE VALIDATION
# ==================================================

REQUIRED_FIELDS = {
    "calories",
    "protein",
    "carbs",
    "fat",
    "fibre",
    "diet",
    "allergens",
    "allergen_status",
    "serving_size",
    "serving_unit",
    "nutrition_basis",
    "food_state",
    "source",
    "verified"
}


def validate_food_database(database):

    errors = []

    for food_name, details in database.items():

        missing = REQUIRED_FIELDS - set(details)

        if missing:
            errors.append(
                f"{food_name}: Missing fields {missing}"
            )
            continue

        for nutrient in [
            "calories", "protein", "carbs", "fat", "fibre"
        ]:
            value = details[nutrient]

            if not isinstance(value, (int, float)):
                errors.append(
                    f"{food_name}: Invalid {nutrient}"
                )

            elif value < 0:
                errors.append(
                    f"{food_name}: Negative {nutrient}"
                )

        if not isinstance(details["diet"], list):
            errors.append(f"{food_name}: diet must be a list")

        elif not set(details["diet"]).issubset(ALL_DIETS):
            errors.append(f"{food_name}: Invalid diet category")

        if not isinstance(details["allergens"], list):
            errors.append(f"{food_name}: allergens must be a list")

        if details["serving_size"] <= 0:
            errors.append(
                f"{food_name}: Invalid serving size"
            )

        expected_basis = (
            "per_100_ml"
            if details["serving_unit"] == "ml"
            else "per_100_g"
        )

        if details["nutrition_basis"] != expected_basis:
            errors.append(
                f"{food_name}: Incorrect nutrition basis"
            )

    if errors:
        for error in errors:
            print("ERROR:", error)

        return False

    return True


if __name__ == "__main__":

    if validate_food_database(FOOD_DATABASE):

        print("Food database structure is valid!")

        print(
            "Total food entries:",
            len(FOOD_DATABASE)
        )