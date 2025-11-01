import json
from typing import Dict, Any, List

# Activity multipliers for TDEE (Must be defined here for use in calculations)
ACTIVITY_MULTIPLIERS = {
    "Sedentary (little/no exercise)": 1.2,
    "Lightly active (1-3 days/week)": 1.375,
    "Moderately active (3-5 days/week)": 1.55,
    "Very active (6-7 days/week)": 1.725,
    "Extra active (intense daily / physical job)": 1.9
}

# Simple Indian Meal Options (fallback)
VEG_MEALS = {
    "Breakfast": [
        "Oats porridge + milk + banana (approx. 350-400 kcal)",
        "Moong dal cheela (2 pcs) + chutney (approx. 300-350 kcal)",
        "Paneer stuffed paratha (1 pc) + curd (approx. 400-450 kcal)"
    ],
    "Lunch": [
        "Dal (1 katori) + brown rice (1 cup) + mixed sabzi (1 katori) + salad (approx. 500-600 kcal)",
        "Chole (1 katori) + roti (2 pcs) + salad (approx. 450-550 kcal)",
    ],
    "Snacks": [
        "Sprouts salad (1 cup)",
        "Roasted chana (1/2 cup)",
    ],
    "Dinner": [
        "Soya curry (1 katori) + roti (2 pcs) (approx. 450-550 kcal)",
        "Mixed vegetable khichdi (1 bowl) + curd (approx. 400-500 kcal)",
    ]
}

NONVEG_MEALS = {
    "Breakfast": [
        "Oats + 3 boiled egg whites + 1 yolk (approx. 350-400 kcal)",
        "Egg omelette (2 whole eggs) + whole wheat toast (1 pc) (approx. 300-350 kcal)",
    ],
    "Lunch": [
        "Grilled chicken (150g) + brown rice (1 cup) + salad (approx. 550-650 kcal)",
        "Egg curry (2 eggs) + roti (2 pcs) + salad (approx. 500-600 kcal)",
    ],
    "Snacks": [
        "Boiled eggs (2)",
        "Greek yogurt (1 cup) + fruit",
    ],
    "Dinner": [
        "Grilled fish (150g) + steamed vegetables (approx. 400-500 kcal)",
        "Chicken soup + roti (2 pcs) (approx. 450-550 kcal)",
    ]
}

def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    """Calculates Body Mass Index (BMI)."""
    if height_cm <= 0: return 0.0
    h_m = height_cm / 100.0
    return round(weight_kg / (h_m * h_m), 1)

def calculate_bmr_mifflin(gender: str, weight: float, height: float, age: int) -> float:
    """Calculates Basal Metabolic Rate (BMR) using Mifflin-St Jeor."""
    gender = gender.lower()
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else: # female
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    return round(bmr)

def calculate_tdee(bmr: float, activity_level: str) -> int:
    """Calculates Total Daily Energy Expenditure (TDEE)."""
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level, 1.375)
    return round(bmr * multiplier)

def macro_split_by_goal(goal: str, weight_kg: float) -> Dict[str, int]:
    """Generates macro grams/day recommendations based on goal."""
    goal = goal.lower()
    if "fat loss" in goal or "fat" in goal:
        protein = 1.6 * weight_kg
        carbs = 2.0 * weight_kg
        fats = 0.8 * weight_kg
    elif "muscle gain" in goal or "gain" in goal:
        protein = 2.0 * weight_kg
        carbs = 4.0 * weight_kg
        fats = 1.0 * weight_kg
    elif "strength" in goal:
        protein = 1.8 * weight_kg
        carbs = 3.0 * weight_kg
        fats = 1.0 * weight_kg
    else:
        # maintenance
        protein = 1.6 * weight_kg
        carbs = 3.0 * weight_kg
        fats = 0.9 * weight_kg

    return {
        "protein_g": int(round(protein)),
        "carbs_g": int(round(carbs)),
        "fats_g": int(round(fats))
    }

def generate_diet_plan(gender: str, age: int, height: float, weight: float,
                       goal: str, diet_type: str, activity_level: str) -> Dict[str, Any]:
    """Generates a complete rule-based diet plan based on user inputs."""
    
    # Basic data validation
    if height <= 0 or weight <= 0:
        return {
            "error": "Please enter valid height and weight.",
            "calorie_target": 0, "macros": {"protein_g": 0, "carbs_g": 0, "fats_g": 0}, 
            "meals": {"Error": ["Invalid height or weight provided."]}
        }

    bmr = calculate_bmr_mifflin(gender, weight, height, age)
    tdee = calculate_tdee(bmr, activity_level)

    # Adjust calorie target based on goal
    goal_lower = goal.lower()
    if "fat loss" in goal_lower:
        # 400 kcal deficit
        calorie_target = max(1200, tdee - 400)
    elif "muscle gain" in goal_lower:
        # 300 kcal surplus
        calorie_target = tdee + 300
    else:  # strength / maintenance
        calorie_target = tdee

    macros = macro_split_by_goal(goal, weight)

    meals = VEG_MEALS if diet_type.lower() == "veg" else NONVEG_MEALS

    return {
        "bmi": calculate_bmi(height, weight),
        "bmr": bmr,
        "tdee": tdee,
        "calorie_target": calorie_target,
        "macros": macros,
        "meals": meals,
        "notes": f"Plan based on {activity_level}. Adjust portions to hit the exact calorie and macro targets."
    }

# Export the multipliers so Streamlit can use them for the select box
DIET_ACTIVITY_LEVELS = list(ACTIVITY_MULTIPLIERS.keys())
