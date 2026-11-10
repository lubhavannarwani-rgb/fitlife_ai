import math
import random

ALL_GOALS = ["weight_loss", "muscle_gain", "maintenance", "general_fitness"]
NON_MUSCLE_GOALS = ["weight_loss", "maintenance", "general_fitness"]
STRENGTH_GOALS = ["muscle_gain", "maintenance", "general_fitness"]


# ==================================================
# 1. EXERCISE DATABASE
# FIX: "maintenance" was missing from every exercise, so a
# maintenance user always got an empty workout. Weight loss
# also only matched 3 exercises. More exercises were added.
# "timed" exercises use seconds instead of reps.
# ==================================================

EXERCISE_DATABASE = [

    # ---------- Bodyweight, beginner ----------
    {"name": "Push-ups", "muscle": "chest", "equipment": [],
     "goals": ALL_GOALS, "difficulty": "beginner", "minutes": 5},

    {"name": "Bodyweight Squats", "muscle": "legs", "equipment": [],
     "goals": ALL_GOALS, "difficulty": "beginner", "minutes": 5},

    {"name": "Lunges", "muscle": "legs", "equipment": [],
     "goals": ALL_GOALS, "difficulty": "beginner", "minutes": 5},

    {"name": "Plank", "muscle": "core", "equipment": [],
     "goals": ALL_GOALS, "difficulty": "beginner", "minutes": 3,
     "timed": True, "time_range": "20-40 seconds"},

    {"name": "Glute Bridge", "muscle": "glutes", "equipment": [],
     "goals": ALL_GOALS, "difficulty": "beginner", "minutes": 4},

    {"name": "Superman Hold", "muscle": "back", "equipment": [],
     "goals": ALL_GOALS, "difficulty": "beginner", "minutes": 3,
     "timed": True, "time_range": "20-30 seconds"},

    {"name": "Jumping Jacks", "muscle": "cardio", "equipment": [],
     "goals": NON_MUSCLE_GOALS, "difficulty": "beginner", "minutes": 4,
     "timed": True, "time_range": "30-45 seconds"},

    {"name": "High Knees", "muscle": "cardio", "equipment": [],
     "goals": NON_MUSCLE_GOALS, "difficulty": "beginner", "minutes": 4,
     "timed": True, "time_range": "30-45 seconds"},

    {"name": "Mountain Climbers", "muscle": "core", "equipment": [],
     "goals": NON_MUSCLE_GOALS, "difficulty": "beginner", "minutes": 4,
     "timed": True, "time_range": "30-45 seconds"},

    # ---------- Dumbbells, beginner ----------
    {"name": "Dumbbell Shoulder Press", "muscle": "shoulders",
     "equipment": ["dumbbells"], "goals": STRENGTH_GOALS,
     "difficulty": "beginner", "minutes": 5},

    {"name": "Dumbbell Rows", "muscle": "back",
     "equipment": ["dumbbells"], "goals": STRENGTH_GOALS,
     "difficulty": "beginner", "minutes": 5},

    {"name": "Dumbbell Bicep Curls", "muscle": "biceps",
     "equipment": ["dumbbells"], "goals": STRENGTH_GOALS,
     "difficulty": "beginner", "minutes": 4},

    {"name": "Dumbbell Triceps Extension", "muscle": "triceps",
     "equipment": ["dumbbells"], "goals": STRENGTH_GOALS,
     "difficulty": "beginner", "minutes": 4},

    {"name": "Dumbbell Goblet Squat", "muscle": "legs",
     "equipment": ["dumbbells"], "goals": ALL_GOALS,
     "difficulty": "beginner", "minutes": 5},

    # ---------- Resistance band, beginner ----------
    {"name": "Resistance Band Rows", "muscle": "back",
     "equipment": ["resistance band"], "goals": STRENGTH_GOALS,
     "difficulty": "beginner", "minutes": 5},

    {"name": "Resistance Band Squats", "muscle": "legs",
     "equipment": ["resistance band"], "goals": ALL_GOALS,
     "difficulty": "beginner", "minutes": 5},

    {"name": "Resistance Band Chest Press", "muscle": "chest",
     "equipment": ["resistance band"], "goals": STRENGTH_GOALS,
     "difficulty": "beginner", "minutes": 5},

    {"name": "Resistance Band Pull-Apart", "muscle": "shoulders",
     "equipment": ["resistance band"], "goals": STRENGTH_GOALS,
     "difficulty": "beginner", "minutes": 4},

    # ---------- Intermediate ----------
    {"name": "Burpees", "muscle": "cardio", "equipment": [],
     "goals": ALL_GOALS, "difficulty": "intermediate", "minutes": 5},

    {"name": "Jump Squats", "muscle": "legs", "equipment": [],
     "goals": NON_MUSCLE_GOALS, "difficulty": "intermediate", "minutes": 5},

    {"name": "Pike Push-ups", "muscle": "shoulders", "equipment": [],
     "goals": STRENGTH_GOALS, "difficulty": "intermediate", "minutes": 5},

    {"name": "Bulgarian Split Squats", "muscle": "legs", "equipment": [],
     "goals": ALL_GOALS, "difficulty": "intermediate", "minutes": 6},

    {"name": "Dumbbell Romanian Deadlift", "muscle": "glutes",
     "equipment": ["dumbbells"], "goals": ALL_GOALS,
     "difficulty": "intermediate", "minutes": 5},

    # ---------- Advanced ----------
    {"name": "Archer Push-ups", "muscle": "chest", "equipment": [],
     "goals": STRENGTH_GOALS, "difficulty": "advanced", "minutes": 5},

    {"name": "Diamond Push-ups", "muscle": "triceps", "equipment": [],
     "goals": STRENGTH_GOALS, "difficulty": "advanced", "minutes": 5},

    {"name": "Pistol Squats (assisted)", "muscle": "legs", "equipment": [],
     "goals": ALL_GOALS, "difficulty": "advanced", "minutes": 6},

    {"name": "Hollow Body Hold", "muscle": "core", "equipment": [],
     "goals": ALL_GOALS, "difficulty": "advanced", "minutes": 4,
     "timed": True, "time_range": "20-40 seconds"}
]


# ==================================================
# 2. INPUT NORMALISATION
# ==================================================

LEVEL_RANK = {
    "beginner": 0,
    "intermediate": 1,
    "advanced": 2
}

# FIX: users type "dumbbell" or "resistance bands", but exercises
# use "dumbbells" and "resistance band".
EQUIPMENT_ALIASES = {
    "dumbbell": "dumbbells",
    "dumbbells": "dumbbells",
    "resistance band": "resistance band",
    "resistance bands": "resistance band",
    "band": "resistance band",
    "bands": "resistance band"
}

NO_EQUIPMENT_WORDS = {
    "", "none", "no", "nothing", "no equipment", "bodyweight"
}

# Body parts / injuries -> muscle groups to avoid
LIMITATION_ALIASES = {
    "knee": {"legs", "cardio"},
    "knees": {"legs", "cardio"},
    "leg": {"legs", "cardio"},
    "legs": {"legs", "cardio"},
    "ankle": {"legs", "cardio"},
    "hip": {"legs", "glutes"},
    "back": {"back"},
    "lower back": {"back", "glutes"},
    "back pain": {"back", "glutes"},
    "shoulder": {"shoulders", "chest"},
    "shoulders": {"shoulders", "chest"},
    "wrist": {"chest", "shoulders", "biceps", "triceps"},
    "chest": {"chest"},
    "core": {"core"},
    "glutes": {"glutes"},
    "biceps": {"biceps"},
    "triceps": {"triceps"},
    "cardio": {"cardio"},
    "arm": {"biceps", "triceps"},
    "arms": {"biceps", "triceps"}
}

# Which muscle groups come first for each goal
GOAL_MUSCLE_PRIORITY = {
    "weight_loss": ["cardio", "legs", "core", "glutes",
                    "chest", "back", "shoulders", "biceps", "triceps"],
    "muscle_gain": ["legs", "chest", "back", "shoulders",
                    "glutes", "core", "biceps", "triceps", "cardio"],
    "maintenance": ["legs", "chest", "back", "core",
                    "shoulders", "glutes", "cardio", "biceps", "triceps"],
    "general_fitness": ["legs", "chest", "back", "core",
                        "cardio", "shoulders", "glutes", "biceps", "triceps"]
}

WARMUP_ACTIVITIES = [
    "March in place",
    "Arm circles",
    "Hip circles",
    "Slow bodyweight squats",
    "Shoulder rolls"
]

COOLDOWN_ACTIVITIES = [
    "Hamstring stretch",
    "Quadriceps stretch",
    "Chest and shoulder stretch",
    "Child's pose",
    "Slow deep breathing"
]


def normalize_equipment(items):

    equipment = set()

    for item in items:

        text = str(item).lower().strip()

        if text in NO_EQUIPMENT_WORDS:
            continue

        equipment.add(EQUIPMENT_ALIASES.get(text, text))

    return equipment


def normalize_limitations(items):
    """Returns (muscles_to_avoid, unrecognised_limitations)."""

    blocked = set()
    unknown = []

    for item in items:

        text = str(item).lower().strip()

        if not text:
            continue

        if text in LIMITATION_ALIASES:
            blocked.update(LIMITATION_ALIASES[text])
        else:
            unknown.append(text)

    return blocked, unknown


# ==================================================
# 3. EXERCISE SELECTION
# ==================================================

def select_exercises(candidates, goal, available_minutes, rng, minutes_for):
    """
    Take exercises one muscle group at a time so the workout is
    balanced, instead of filling the time with the first few
    exercises in the list.
    """

    groups = {}

    for exercise in candidates:
        groups.setdefault(exercise["muscle"], []).append(exercise)

    for group in groups.values():
        rng.shuffle(group)

    priority = GOAL_MUSCLE_PRIORITY[goal]

    order = [m for m in priority if m in groups]
    order += [m for m in groups if m not in priority]

    selected = []
    used_minutes = 0
    exercises_left = True

    while exercises_left:

        exercises_left = False

        for muscle in order:

            if not groups[muscle]:
                continue

            exercises_left = True
            exercise = groups[muscle].pop(0)

            if used_minutes + minutes_for(exercise) <= available_minutes:
                selected.append(exercise)
                used_minutes += minutes_for(exercise)

    return selected, used_minutes


def get_prescription(goal, level):
    """Returns sets, reps, rest text and the average rest in seconds."""

    if goal == "muscle_gain":
        sets, reps, rest, rest_seconds = 3, "8-12", "60-120 seconds", 90

    elif goal == "weight_loss":
        sets, reps, rest, rest_seconds = 3, "10-15", "45-60 seconds", 50

    else:
        sets, reps, rest, rest_seconds = 2, "10-12", "45-60 seconds", 50

    if level == "advanced":
        sets += 1

    return sets, reps, rest, rest_seconds


def estimate_exercise_minutes(exercise, sets, rest_seconds):
    """
    FIX: time used to be a fixed 3-6 minutes per exercise, ignoring
    sets and rest, so sessions ran much longer than shown.
    Now: sets x (work time + rest), rounded up.
    """

    work_seconds = 30 if exercise.get("timed") else 40

    return math.ceil(sets * (work_seconds + rest_seconds) / 60)


# ==================================================
# 4. GENERATE WORKOUT
# ==================================================

def generate_workout(
    user,
    experience_level="beginner",
    limitations=None,
    seed=None
):
    """
    Generate a workout from the user's profile.

    Equipment requirements are matched against user.equipment.
    Exercises with [] equipment are bodyweight exercises.
    """

    if limitations is None:
        limitations = []

    if experience_level not in LEVEL_RANK:
        raise ValueError("Invalid experience level")

    goal = user.fitness_goal.value

    available_equipment = normalize_equipment(user.equipment)

    blocked_muscles, unknown_limitations = normalize_limitations(
        limitations
    )

    rng = random.Random(seed)

    notes = []

    if unknown_limitations:
        notes.append(
            "These limitations were not recognised, so no exercises "
            "were removed for them: "
            + ", ".join(unknown_limitations)
            + ". Please check with a doctor or trainer."
        )

    candidates = [
        exercise for exercise in EXERCISE_DATABASE
        if goal in exercise["goals"]
        and set(exercise["equipment"]).issubset(available_equipment)
        and LEVEL_RANK[exercise["difficulty"]] <= LEVEL_RANK[experience_level]
        and exercise["muscle"] not in blocked_muscles
    ]

    # Shorter sessions get shorter warm-up and cool-down
    warmup_minutes = cooldown_minutes = (
        5 if user.workout_minutes >= 20 else 2
    )

    available_minutes = max(
        0,
        user.workout_minutes - warmup_minutes - cooldown_minutes
    )

    sets, reps, rest, rest_seconds = get_prescription(
        goal,
        experience_level
    )

    def minutes_for(exercise):
        return estimate_exercise_minutes(exercise, sets, rest_seconds)

    selected, used_minutes = select_exercises(
        candidates,
        goal,
        available_minutes,
        rng,
        minutes_for
    )

    warmup = {
        "minutes": warmup_minutes,
        "activities": WARMUP_ACTIVITIES
    }

    cooldown = {
        "minutes": cooldown_minutes,
        "activities": COOLDOWN_ACTIVITIES
    }

    if not selected:

        notes.append(
            "No suitable exercises fit this goal, equipment, "
            "limitations and time. Try a longer session or "
            "different equipment."
        )

        return {
            "warmup": warmup,
            "exercises": [],
            "cooldown": cooldown,
            "estimated_exercise_minutes": 0,
            "notes": notes
        }

    workout = []

    for exercise in selected:

        workout.append({
            "exercise": exercise["name"],
            "muscle": exercise["muscle"],
            "sets": sets,
            "reps": exercise.get("time_range", reps),
            "rest": rest,
            "equipment": exercise["equipment"] or ["bodyweight"],
            "estimated_minutes": minutes_for(exercise)
        })

    return {
        "warmup": warmup,
        "exercises": workout,
        "cooldown": cooldown,
        "estimated_exercise_minutes": used_minutes,
        "notes": notes
    }