import sqlite3
import textwrap

from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_groq import ChatGroq

from fitness_calculator import generate_fitness_report
from meal_planner import generate_meal_plan
from Rag import get_knowledge_base
from workout_generator import generate_workout


MEMORY_DB_FILE = "fitlife_memory.db"


# =========================================
# MEMORY
# =========================================

_checkpointer = None


def get_checkpointer():
    """
    Memory store for conversations.

    Uses SQLite so the conversation is remembered even after the
    program is closed (needs: pip install langgraph-checkpoint-sqlite).
    If that package is missing, falls back to in-memory storage,
    which is forgotten when the program ends.
    """

    global _checkpointer

    if _checkpointer is not None:
        return _checkpointer

    try:
        from langgraph.checkpoint.sqlite import SqliteSaver

        connection = sqlite3.connect(
            MEMORY_DB_FILE,
            check_same_thread=False
        )

        _checkpointer = SqliteSaver(connection)

    except ImportError:
        from langgraph.checkpoint.memory import InMemorySaver

        print(
            "Note: langgraph-checkpoint-sqlite is not installed, so "
            "memory will be lost when the program closes."
        )

        _checkpointer = InMemorySaver()

    return _checkpointer


def _safe_call(function):
    """Return a tool's result, or an error dict if it fails."""

    try:
        return function()

    except Exception as error:
        return {"error": f"{type(error).__name__}: {error}"}


def build_fitlife_agent(user):

    # =========================================
    # TOOL 1: FITNESS REPORT
    # =========================================

    @tool
    def fitness_report_tool() -> dict:
        """Calculate BMI, BMR, TDEE, daily calories
        and macronutrients using the user's profile."""

        return _safe_call(lambda: generate_fitness_report(user))

    # =========================================
    # TOOL 2: NUTRITION PLAN
    # =========================================

    @tool
    def nutrition_plan_tool() -> dict:
        """Generate a one-day meal plan using the user's diet
        preference and allergies. Portions are scaled to the
        user's calorie target, and the result includes a
        comparison of actual totals against targets. Call again
        to get a different plan."""

        def run():

            report = generate_fitness_report(user)

            return generate_meal_plan(
                diet_type=user.diet_type.value,
                allergies=user.allergies,
                calorie_target=report["Daily Calories"],
                macro_targets=report["Macros"]
            )

        return _safe_call(run)

    # =========================================
    # TOOL 3: WORKOUT PLAN
    # =========================================

    @tool
    def workout_plan_tool() -> dict:
        """Generate a workout based on the user's fitness goal,
        equipment, experience level, limitations and workout
        duration. Call again to get a different workout."""

        return _safe_call(
            lambda: generate_workout(
                user=user,
                experience_level=user.experience_level.value,
                limitations=user.limitations
            )
        )

    # =========================================
    # TOOL 4: KNOWLEDGE SEARCH (RAG)
    # =========================================

    @tool
    def knowledge_search_tool(query: str) -> dict:
        """Search the FitLife knowledge base for general fitness,
        nutrition, training, recovery and safety information.
        Use this for general questions such as protein needs,
        fibre, rest between sets, hydration or sleep. The query
        should be a short question or keywords."""

        def run():

            results = get_knowledge_base().search(query, top_k=3)

            if not results:
                return {
                    "found": False,
                    "message": "No relevant information found "
                               "in the knowledge base."
                }

            return {
                "found": True,
                "results": [
                    {
                        "source": result["source"],
                        "topic": result["title"],
                        "text": result["text"]
                    }
                    for result in results
                ]
            }

        return _safe_call(run)

    # =========================================
    # USER PROFILE FOR LLM
    # =========================================

    profile_information = f"""
USER PROFILE:

Name: {user.name}
Age: {user.age}
Sex: {user.sex.value}
Height: {user.height_cm} cm
Weight: {user.weight_kg} kg

Fitness Goal: {user.fitness_goal.value}
Diet Type: {user.diet_type.value}
Activity Level: {user.activity_level.value}
Experience Level: {user.experience_level.value}

Workout Duration: {user.workout_minutes} minutes
Equipment: {user.equipment}
Allergies: {user.allergies}
Limitations: {user.limitations}
"""

    # =========================================
    # GROQ MODEL
    # =========================================

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0
    )

    # =========================================
    # SYSTEM PROMPT
    # =========================================

    system_prompt = textwrap.dedent(f"""
        You are FitLife AI, a personalized fitness assistant.

        {profile_information}

        GENERAL RULES:

        1. The user profile is already available. Never ask for
           the same information again.
        2. Use actual tool outputs. Never invent calculations,
           nutrition numbers or exercises.
        3. Explain results in simple language.
        4. If a tool returns an "error", explain which tool failed
           and why. Do not pretend that a plan was generated.
        5. You remember this conversation. Use earlier messages
           (plans you already made, what the user liked or
           disliked) instead of starting over.

        WHEN THE USER ASKS FOR A COMPLETE PLAN:

        6. Call fitness_report_tool, nutrition_plan_tool and
           workout_plan_tool.
        7. Show the fitness report (BMI, BMR, TDEE, daily calories,
           macros), the meal plan (meals, ingredients with
           quantities and units, nutrition), the daily totals with
           the "targets" comparison, and the workout (warm-up,
           exercises, sets, reps, rest, cooldown, notes).
        8. Say honestly if calories, protein, carbs or fat are above
           or below target. Mention the fitness report "Note" and the
           meal plan "warnings" if present.

        WHEN THE USER ASKS A FOLLOW-UP QUESTION:

        9. Answer from the earlier plan in this conversation when
           possible. Call a plan tool again only if the user wants
           a new or changed plan (for example "give me a different
           dinner plan" or "new workout").
        10. For general fitness, nutrition, training, recovery or
            safety questions, call knowledge_search_tool first and
            base your answer on what it returns. Mention the source
            file name, for example (source: fibre_and_digestion.md).
        11. If knowledge_search_tool finds nothing relevant, say you
            do not have reliable information on that in your
            knowledge base. Do not answer from guesswork, and
            suggest a doctor or dietitian for medical questions.

        SAFETY:

        12. Allergy filtering cannot guarantee protection against
            allergens. Remind the user to check food labels.
        13. You are not a doctor. For medical conditions, injuries,
            pregnancy or medication, advise consulting a
            professional.
    """)

    # =========================================
    # CREATE AGENT (with memory)
    # =========================================

    agent = create_agent(
        model=llm,
        tools=[
            fitness_report_tool,
            nutrition_plan_tool,
            workout_plan_tool,
            knowledge_search_tool
        ],
        system_prompt=system_prompt,
        checkpointer=get_checkpointer()
    )

    return agent