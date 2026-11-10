MIN_CALORIES = {
    "male": 1500,
    "female": 1200
}


def calculate_BMI(weight, height):

    if weight <= 0 or height <= 0:
        raise ValueError("Weight and height must be positive")

    height_in_m = height / 100
    bmi = weight / (height_in_m ** 2)

    return round(bmi, 2)


def get_bmi_category(bmi):

    # FIX: underweight limit was 18.2; the standard WHO limit is 18.5.
    # Category names are now consistently capitalised.
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal range"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obesity"


# BMR = Basal Metabolic Rate: the calories your body uses in 24 hours
# at complete rest (breathing, circulation, temperature regulation).
# Formula used: Mifflin-St Jeor.

def calculate_BMR(weight, height, age, sex):

    if sex == "male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5

    elif sex == "female":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    else:
        raise ValueError("Invalid sex value")

    return round(bmr, 2)


# TDEE = Total Daily Energy Expenditure = BMR x Activity Factor.
# It covers basic body functions, daily movement, exercise and digestion.

ACTIVITY_FACTORS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9
}


def calculate_TDEE(bmr, activity_level):

    if activity_level not in ACTIVITY_FACTORS:
        raise ValueError("Invalid activity level")

    tdee = bmr * ACTIVITY_FACTORS[activity_level]

    return round(tdee, 2)


def calculate_calorie_target(tdee, fitness_goal, sex=None):
    """
    Returns (calories, note). note is None unless a safety minimum
    had to be applied.
    """

    if fitness_goal == "weight_loss":
        calories = tdee - 300

    elif fitness_goal == "muscle_gain":
        calories = tdee + 200

    elif fitness_goal in ["maintenance", "general_fitness"]:
        calories = tdee

    else:
        raise ValueError("Invalid fitness goal")

    note = None

    # NEW: never go below a commonly used safe minimum
    minimum = MIN_CALORIES.get(sex)

    if minimum and calories < minimum:
        calories = minimum
        note = (
            f"Calorie target raised to the safe minimum of "
            f"{minimum} kcal."
        )

    return round(calories), note


def calculate_macros(weight_kg, calorie_target):

    protein = weight_kg * 1.6
    protein_calories = protein * 4

    fat_calories = calorie_target * 0.25
    fat = fat_calories / 9

    carbs_calories = calorie_target - protein_calories - fat_calories

    if carbs_calories < 0:
        raise ValueError(
            "Calorie target is too low for these macro settings"
        )

    carbs = carbs_calories / 4

    return {
        "protein_g": round(protein, 2),
        "carbs_g": round(carbs, 2),
        "fat_g": round(fat, 2)
    }


def generate_fitness_report(user):

    bmi = calculate_BMI(
        user.weight_kg,
        user.height_cm
    )

    bmi_category = get_bmi_category(bmi)

    bmr = calculate_BMR(
        user.weight_kg,
        user.height_cm,
        user.age,
        user.sex.value
    )

    tdee = calculate_TDEE(
        bmr,
        user.activity_level.value
    )

    calorie_target, note = calculate_calorie_target(
        tdee,
        user.fitness_goal.value,
        user.sex.value
    )

    macros = calculate_macros(
        user.weight_kg,
        calorie_target
    )

    report = {
        "BMI": bmi,
        "BMI Category": bmi_category,
        "BMR": bmr,
        "TDEE": tdee,
        "Daily Calories": calorie_target,
        "Macros": macros
    }

    if note:
        report["Note"] = note

    return report