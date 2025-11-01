from typing import Dict, Any, List

def get_warmup():
    """Returns a list of exercises for the warm-up routine."""
    return [
        "5 min light jogging / marching",
        "Arm circles – 20 reps",
        "Leg swings – 15/leg",
        "Neck rotations – 10 reps",
        "Hip rotations – 10 reps",
    ]

def get_cooldown():
    """Returns a list of stretches for the cool-down routine."""
    return [
        "Hamstring stretch – 30 sec",
        "Shoulder stretch – 30 sec",
        "Cat-Cow – 10 reps",
        "Child pose – 1 min",
        "Deep breathing – 2 min"
    ]

# ------------------ WORKOUT DICTIONARY -------------------- #

home_workouts = {
    "Fat Loss": {
        "Day 1": ["Jumping jacks – 30 sec", "Squats – 15×3", "Push-ups – 10×3", "Mountain climbers – 30 sec × 3", "Burpees – 10×2"],
        "Day 2": ["Brisk walk / jog – 30 min", "Plank – 45 sec × 2", "High knees – 30 sec × 2"],
        "Day 3": ["Lunges – 12×3", "Tricep dips (chair) – 12×3", "Bicycle crunch – 20×3", "Skipping – 2 min × 2"],
        "Day 4": ["REST / Yoga 20 min"],
        "Day 5": ["Squat jumps – 12×3", "Incline push-ups – 12×3", "Side plank – 30 sec each"],
        "Day 6": ["Jog – 30 min", "Glute bridge – 15×3"],
        "Day 7": ["REST / Stretching 15 min"]
    },
    "Muscle Gain": {
        "Day 1": ["Push-ups – 12×4", "Pike push-ups – 10×3", "Tricep dip – 12×3", "Plank – 1 min"],
        "Day 2": ["Bodyweight squats – 15×4", "Reverse lunges – 12×3", "Calf raise – 20×3"],
        "Day 3": ["REST / Yoga"],
        "Day 4": ["Wide push-ups – 12×4", "Diamond push-ups – 10×3", "Superman hold – 30 sec × 2"],
        "Day 5": ["Bulgarian split squat – 10×3", "Glute bridge – 15×3", "Wall sit – 1 min"],
        "Day 6": ["Abs & Core routine – 20 min"],
        "Day 7": ["REST"]
    },
    "Strength": {
        "Day 1": ["Slow push-ups – 8×5", "Slow squats – 8×5", "Wall handstand hold – 30 sec"],
        "Day 2": ["Walk / light run – 30 min"],
        "Day 3": ["Pistol squat progression – 8×3", "Decline push-ups – 8×3"],
        "Day 4": ["REST"],
        "Day 5": ["Decline push-ups – 10×3", "Single-leg glute bridge – 12×3"],
        "Day 6": ["Core strengthening routine – 20 min"],
        "Day 7": ["REST"]
    }
}

gym_workouts = {
    "Fat Loss": {
        "Day 1": ["Treadmill – 20 min HIIT", "Leg press – 12×3", "Lat pull down – 12×3", "Plank – 1 min"],
        "Day 2": ["Cycling – 25 min", "Cable row – 12×3", "Leg curl – 12×3"],
        "Day 3": ["Treadmill walk – 30 min", "Crunch machine – 15×3"],
        "Day 4": ["REST"],
        "Day 5": ["Rowing machine – 10 min", "Chest press – 12×3", "Shoulder press – 12×3"],
        "Day 6": ["Elliptical – 25 min"],
        "Day 7": ["REST"]
    },
    "Muscle Gain": {
        "Day 1": ["Bench press – 8×4", "Incline dumbbell press – 10×3", "Tricep pushdown – 12×3"],
        "Day 2": ["Squats – 8×4", "Leg press – 12×3", "Calf raise – 15×3"],
        "Day 3": ["REST"],
        "Day 4": ["Lat pull-down – 10×4", "Barbell row – 10×3", "Bicep curls – 12×3"],
        "Day 5": ["Deadlift – 6×3", "Hip thrust – 12×3", "Leg curl – 12×3"],
        "Day 6": ["Shoulder press – 10×3", "Lateral raises – 12×3", "Plank – 1 min"],
        "Day 7": ["REST"]
    },
    "Strength": {
        "Day 1": ["Heavy squats – 5×5", "Romanian deadlift – 6×4"],
        "Day 2": ["Bench press – 5×5", "Dips – 8×3"],
        "Day 3": ["Deadlift – 5×3", "Pull-ups – 6×3"],
        "Day 4": ["REST"],
        "Day 5": ["Overhead press – 5×5", "Farmer walk – 2 rounds"],
        "Day 6": ["Sled push / row – 10 min"],
        "Day 7": ["REST"]
    }
}

# ------------------ MAIN FUNCTION -------------------- #

def generate_workout_plan(goal: str, equipment: str) -> Dict[str, Any]:
    """
    Generates a complete workout plan including warm-up, cool-down, and a 
    weekly schedule based on the user's goal and available equipment (Home/Gym).
    """
    warmup = get_warmup()
    cooldown = get_cooldown()

    # Look up the plan based on equipment and goal
    if equipment == "Home":
        plan = home_workouts.get(goal, {})
    else: # Default to Gym
        plan = gym_workouts.get(goal, {})

    return {
        "warmup": warmup,
        "cooldown": cooldown,
        "weekly_plan": plan
    }
