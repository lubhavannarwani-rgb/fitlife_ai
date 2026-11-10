import os
import re

from pydantic import ValidationError

from fitlife_agent import build_fitlife_agent
from models import UserProfile


# ==================================================
# MENU OPTIONS
# ==================================================

fitness_type_dict = {
    1: "weight_loss",
    2: "muscle_gain",
    3: "maintenance",
    4: "general_fitness"
}

diet_type_dict = {
    1: "vegetarian",
    2: "vegan",
    3: "non_vegetarian",
    4: "eggetarian"
}

activity_type_dict = {
    1: "sedentary",
    2: "light",
    3: "moderate",
    4: "active",
    5: "very_active"
}

sex_type_dict = {
    1: "male",
    2: "female"
}

experience_type_dict = {
    1: "beginner",
    2: "intermediate",
    3: "advanced"
}


# ==================================================
# INPUT FUNCTIONS
# ==================================================

def get_choice(message, options):

    print("\n" + message)

    for key, value in options.items():
        print(f"{key}. {value}")

    while True:

        try:
            choice = int(input("Enter your choice: "))

            if choice in options:
                return options[choice]

            print("Invalid choice! Select a valid option.")

        except ValueError:
            print("Please enter a valid number.")


def get_text(message, min_length=2, max_length=50):
    """Ask again until the text length is valid."""

    while True:

        value = input(message).strip()

        if min_length <= len(value) <= max_length:
            return value

        print(
            f"Please enter between {min_length} and "
            f"{max_length} characters."
        )


def get_number(message, number_type, minimum, maximum):
    """
    FIX: previously a typo like "abc" for age crashed the whole
    form. Now the question is repeated until the value is valid.
    """

    while True:

        try:
            value = number_type(input(message))

        except ValueError:
            print("Please enter a valid number.")
            continue

        if minimum <= value <= maximum:
            return value

        print(f"Please enter a value between {minimum} and {maximum}.")


def get_csv_list(message):

    user_input = input(message)

    return list(dict.fromkeys(
        item.strip().lower()
        for item in user_input.split(",")
        if item.strip()
    ))


# ==================================================
# AGENT / MEMORY HELPERS
# ==================================================

PLAN_REQUEST = """
Generate my complete personalized fitness plan.

Include:

1. Fitness report:
   - BMI
   - BMR
   - TDEE
   - Daily calorie target
   - Protein, carbs and fat

2. Complete meal plan:
   - Breakfast
   - Morning snack
   - Lunch
   - Evening snack
   - Dinner
   - Nutrition information
   - Daily totals compared with my targets

3. Complete workout plan:
   - Warm-up
   - Exercises
   - Sets and reps
   - Rest time
   - Cooldown

Explain everything in simple language.
Use the available tools to get the actual results.
"""


def make_thread_id(name):
    """
    Memory is saved per thread id. Using the user's name means the
    same person gets the same memory next time they run the program.
    (Two users with the same name would share memory.)
    """

    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "user"


def has_saved_conversation(agent, config):

    try:
        state = agent.get_state(config)
        return bool(state.values.get("messages"))

    except Exception:
        return False


def ask_agent(agent, config, text):

    response = agent.invoke(
        {"messages": [{"role": "user", "content": text}]},
        config=config
    )

    return response["messages"][-1].content


def chat_loop(agent, config):

    print("\n" + "=" * 45)
    print("   CHAT WITH FITLIFE AI")
    print("   Ask anything, e.g. 'give me a new dinner plan'")
    print("   or 'how much fibre is too much?'")
    print("   Type 'exit' to quit.")
    print("=" * 45)

    while True:

        question = input("\nYou: ").strip()

        if not question:
            continue

        if question.lower() in {"exit", "quit", "q"}:
            break

        try:
            print("\nFitLife AI:\n")
            print(ask_agent(agent, config, question))

        except Exception as error:
            print("\nCould not get an answer:")
            print(type(error).__name__, ":", error)


# ==================================================
# MAIN PROGRAM
# ==================================================

def main():

    try:

        # ------------------------------------------
        # 0. CHECK API KEY
        # ------------------------------------------

        if not os.getenv("GROQ_API_KEY"):
            print(
                "GROQ_API_KEY is missing. Create a .env file with:\n"
                "GROQ_API_KEY=your_key_here"
            )
            return

        # ------------------------------------------
        # 1. COLLECT USER INFORMATION
        # ------------------------------------------

        print("\n" + "=" * 45)
        print("          FITLIFE AI USER PROFILE")
        print("=" * 45)

        user = UserProfile(

            name=get_text("Enter your name: "),

            age=get_number("Enter your age (18-100): ", int, 18, 100),

            height_cm=get_number(
                "Enter your height in cm: ", float, 101, 230
            ),

            weight_kg=get_number(
                "Enter your weight in kg: ", float, 31, 300
            ),

            fitness_goal=get_choice(
                "Select your fitness goal:",
                fitness_type_dict
            ),

            diet_type=get_choice(
                "Select your diet type:",
                diet_type_dict
            ),

            activity_level=get_choice(
                "Select your activity level:",
                activity_type_dict
            ),

            sex=get_choice(
                "Select your sex:",
                sex_type_dict
            ),

            experience_level=get_choice(
                "Select your workout experience level:",
                experience_type_dict
            ),

            workout_minutes=get_number(
                "Enter workout duration in minutes (5-180): ",
                int, 5, 180
            ),

            equipment=get_csv_list(
                "Enter equipment separated by commas "
                "(e.g. dumbbells, resistance band; leave empty for none): "
            ),

            allergies=get_csv_list(
                "Enter allergies separated by commas "
                "(e.g. dairy, peanuts; leave empty for none): "
            ),

            limitations=get_csv_list(
                "Enter injuries/limitations separated by commas "
                "(e.g. knee, lower back; leave empty for none): "
            )
        )

        print("\nUser profile created successfully!")

        # ------------------------------------------
        # 2. DISPLAY USER PROFILE
        # ------------------------------------------

        print("\n" + "=" * 45)
        print("              USER PROFILE")
        print("=" * 45)

        for key, value in user.model_dump(mode="json").items():
            print(f"{key.replace('_', ' ').title()}: {value}")

        # ------------------------------------------
        # 3. BUILD FITLIFE AI AGENT (with memory)
        # ------------------------------------------

        print("\n" + "=" * 45)
        print("       STARTING FITLIFE AI AGENT")
        print("=" * 45)

        fitlife_agent = build_fitlife_agent(user)

        config = {
            "configurable": {
                "thread_id": make_thread_id(user.name)
            }
        }

        # ------------------------------------------
        # 4. NEW PLAN OR CONTINUE PREVIOUS CHAT
        # ------------------------------------------

        generate_plan = True

        if has_saved_conversation(fitlife_agent, config):

            print(f"\nWelcome back, {user.name}! I remember our last chat.")

            answer = input(
                "Continue the previous chat (c) or "
                "make a fresh plan (n)? [c/n]: "
            ).strip().lower()

            generate_plan = answer == "n"

        # ------------------------------------------
        # 5. GENERATE PLAN
        # ------------------------------------------

        if generate_plan:

            print("\nGenerating your plan, please wait...")

            report = ask_agent(fitlife_agent, config, PLAN_REQUEST)

            print("\n" + "=" * 45)
            print("       YOUR FITLIFE AI REPORT")
            print("=" * 45)

            print(report)

        # ------------------------------------------
        # 6. CHAT (memory + knowledge base)
        # ------------------------------------------

        chat_loop(fitlife_agent, config)

        print(f"\nGreat work, {user.name}! See you next time.")

    except (ValidationError, ValueError) as e:

        print("\nInvalid user information or input:")
        print(e)

    except KeyboardInterrupt:

        print("\nProgram cancelled by user.")

    except Exception as e:

        print("\nSomething went wrong:")
        print(type(e).__name__, ":", e)


# ==================================================
# ENTRY POINT
# ==================================================

if __name__ == "__main__":
    main()