"""
Builds the structured plan (report + meals + workout + checks).

No web or AI code in here, so it is fast, free to run, and easy to test.
The AI chat is separate (see api.py), so a plan always works even if
the AI service is down.
"""

import random

from fitness_calculator import generate_fitness_report
from meal_planner import generate_meal_plan
from workout_generator import generate_workout


FIBRE_WARNING_GRAMS = 45


def _insight(level, message):
    # level: "ok", "info" or "warning"
    return {"level": level, "message": message}


# ==================================================
# CHECKS (run in code, so they are never "forgotten")
# ==================================================

def check_profile(user, report):

    insights = []

    category = report["BMI Category"]

    if category in ("Underweight", "Obesity"):
        insights.append(_insight(
            "warning",
            f"Your BMI is in the '{category}' range. Please talk to a "
            "doctor or dietitian before starting a new diet or "
            "exercise plan."
        ))

    if (
        user.activity_level.value == "very_active"
        and user.workout_minutes <= 60
    ):
        insights.append(_insight(
            "info",
            "You chose 'very active', which assumes hard physical "
            "work most of the day. If you mostly sit and only train "
            "for a short time, 'active' or 'moderate' may give a more "
            "realistic calorie target."
        ))

    if report.get("Note"):
        insights.append(_insight("info", report["Note"]))

    return insights


def check_meals(meal_plan):

    insights = []

    targets = meal_plan.get("targets", {})
    totals = meal_plan["daily_totals"]

    calories = targets.get("calories")

    if calories and calories["percent_of_target"] is not None:

        percent = calories["percent_of_target"]

        if percent < 95 or percent > 105:
            direction = "below" if percent < 100 else "above"
            insights.append(_insight(
                "info",
                f"Meals give {calories['actual']:.0f} kcal, "
                f"{abs(100 - percent):.0f}% {direction} your "
                f"{calories['target']:.0f} kcal target. "
                "Adjust a snack or a portion to close the gap."
            ))
        else:
            insights.append(_insight(
                "ok",
                "Meals are within about 5% of your calorie target."
            ))

    protein = targets.get("protein_g")

    if protein and protein["percent_of_target"] is not None:

        percent = protein["percent_of_target"]

        if percent < 90:
            insights.append(_insight(
                "info",
                f"Protein is {percent:.0f}% of target. Consider adding "
                "a protein-rich food."
            ))

        elif percent > 130:
            insights.append(_insight(
                "info",
                f"Protein is {percent:.0f}% of target. That is more than "
                "needed, so you could swap some for carbs or fat."
            ))

    if totals["fibre"] > FIBRE_WARNING_GRAMS:
        insights.append(_insight(
            "warning",
            f"Fibre is {totals['fibre']:.0f} g, above the usual "
            "25-38 g range. Very high fibre can cause bloating. "
            "Increase fibre gradually and drink enough water."
        ))

    return insights


def check_workout(user, workout):

    insights = []

    exercises = workout.get("exercises", [])

    if not exercises:
        insights.append(_insight(
            "warning",
            "No exercises fit your goal, equipment, limitations and "
            "time. Try a longer session or add equipment."
        ))
        return insights

    total = (
        workout["warmup"]["minutes"]
        + workout["estimated_exercise_minutes"]
        + workout["cooldown"]["minutes"]
    )

    insights.append(_insight(
        "ok" if total <= user.workout_minutes else "warning",
        f"Estimated session length: {total} min "
        f"(you have {user.workout_minutes} min)."
    ))

    for note in workout.get("notes", []):
        insights.append(_insight("info", note))

    return insights


# ==================================================
# BUILDERS
# ==================================================

MEAL_PLAN_ATTEMPTS = 40


def score_meal_plan(plan):
    """Lower is better: close to calorie and protein target, sane fibre."""

    targets = plan["targets"]
    totals = plan["daily_totals"]

    score = 0.0

    calories = targets.get("calories")
    if calories and calories["percent_of_target"] is not None:
        score += abs(100 - calories["percent_of_target"])

    protein = targets.get("protein_g")
    if protein and protein["percent_of_target"] is not None:
        score += max(0, abs(100 - protein["percent_of_target"]) - 15) * 0.3

    # Heavy penalty for very high fibre
    score += max(0, totals["fibre"] - 40) * 1.0

    return score


def build_meals(user, report):
    """
    Generate several candidate meal plans and keep the best one
    (closest to calorie and protein targets, lowest fibre).
    Note: very high fibre can still appear, because the food database
    lists cooked pulses with whole-bean fibre values. The fix for that
    is better data and more low-fibre meal templates, not more tries.
    """

    best_plan = None
    best_score = None

    for _ in range(MEAL_PLAN_ATTEMPTS):

        plan = generate_meal_plan(
            diet_type=user.diet_type.value,
            allergies=user.allergies,
            calorie_target=report["Daily Calories"],
            macro_targets=report["Macros"],
            seed=random.randrange(1_000_000)
        )

        score = score_meal_plan(plan)

        if best_score is None or score < best_score:
            best_plan, best_score = plan, score

    return best_plan


def build_workout(user):

    return generate_workout(
        user=user,
        experience_level=user.experience_level.value,
        limitations=user.limitations
    )


def build_plan(user):

    report = generate_fitness_report(user)
    meal_plan = build_meals(user, report)
    workout = build_workout(user)

    return {
        "profile": user.model_dump(mode="json"),
        "report": report,
        "meal_plan": meal_plan,
        "workout": workout,
        "insights": {
            "general": check_profile(user, report),
            "meals": check_meals(meal_plan),
            "workout": check_workout(user, workout)
        }
    }


def regenerate_meals(user):

    report = generate_fitness_report(user)
    meal_plan = build_meals(user, report)

    return {
        "meal_plan": meal_plan,
        "insights": check_meals(meal_plan)
    }


def regenerate_workout(user):

    workout = build_workout(user)

    return {
        "workout": workout,
        "insights": check_workout(user, workout)
    }