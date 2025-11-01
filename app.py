import streamlit as st
import json
import requests
from workout_planner import generate_workout_plan
from diet_planner import generate_diet_plan, DIET_ACTIVITY_LEVELS # Also import the activity list

st.set_page_config(page_title="AI Fitness Planner", layout="wide")

st.title("AI Fitness Planner 🏋️‍♂️🤖")
st.markdown("---")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- API Configuration ---
# NOTE: The apiKey will be automatically injected by the environment if left as an empty string.
GEMINI_API_KEY = "AIzaSyCH4UIaq0s_0mQtIE6mJxQNPBop1qEXCjE"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={GEMINI_API_KEY}"

# --- Gemini API Call Function ---
@st.cache_data(show_spinner=False)
def call_gemini_api(history):
    """
    Calls the Gemini API to get a chat response.
    History is a list of {'role': str, 'parts': [{'text': str}]}
    """
    # System instruction to guide the model's persona
    system_instruction = "You are a friendly, motivational, and highly knowledgeable AI Fitness Coach. Answer questions concisely and focus on fitness, nutrition, and wellness topics based on the user's current profile. Do not discuss generating code."
    
    # Format the history for the API payload
    contents = [
        {"role": entry["role"], "parts": [{"text": entry["parts"][0]["text"]}]}
        for entry in history
    ]

    payload = {
        "contents": contents,
        "tools": [{"google_search": {}}], # Enable search grounding for real-time fitness info
        "systemInstruction": {"parts": [{"text": system_instruction}]}
    }

    try:
        # Use requests for synchronous API call, as st.cache_data requires it
        response = requests.post(
            GEMINI_API_URL,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(payload)
        )
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        result = response.json()
        
        # Extract text from the response
        text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'Sorry, I encountered an error fetching the response.')
        return text

    except requests.exceptions.RequestException as e:
        st.error(f"API Error: Could not connect to the model. {e}")
        return "I'm sorry, I'm having trouble connecting to my knowledge base right now."
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred."


# ---- Main Layout (Tabs) ----
main_tabs = st.tabs(["🏋️ Plan Generator", "💬 Fitness Chatbot"])


with main_tabs[0]: # Plan Generator Tab

    # ---- User Inputs ----
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Age", 18, 70, value=30, help="Your age in years.")
        gender = st.selectbox("Gender", ["Male", "Female"])
        goal = st.selectbox("Goal", ["Fat Loss", "Muscle Gain", "Strength", "Maintenance"])

    with col2:
        height = st.number_input("Height (cm)", value=175.0, min_value=1.0)
        weight = st.number_input("Weight (kg)", value=75.0, min_value=1.0)
        equipment = st.selectbox("Training Type", ["Gym", "Home"])

    with col3:
        diet_type = st.selectbox("Diet Preference", ["Veg", "Non-veg"])
        # Crucial input for TDEE calculation
        activity_level = st.selectbox("Activity Level", DIET_ACTIVITY_LEVELS, index=2, help="How active are you?")
        st.markdown("<br>", unsafe_allow_html=True) # Spacer

    # ---- Planning Buttons ----
    button_col1, button_col2 = st.columns(2)
    workout_button = button_col1.button("🏋️ Generate Workout Plan", use_container_width=True)
    diet_button = button_col2.button("🍽️ Generate Diet Plan", use_container_width=True)

    st.markdown("---")

    # ==========================================================
    # ============== WORKOUT GENERATION LOGIC ==============
    # ==========================================================
    if workout_button:
        with st.spinner('Generating personalized workout routine...'):
            plan = generate_workout_plan(goal, equipment)

            st.header(f"💪 Your {goal} Workout Plan ({equipment})")
            
            # Display Warm-up
            st.subheader("✅ Warm-up (5-10 mins)")
            warmup_cols = st.columns(len(plan["warmup"]))
            for i, w in enumerate(plan["warmup"]):
                warmup_cols[i].info(f"• {w}")

            # Display Weekly Plan
            st.subheader("📅 Weekly Workout Plan")
            for day, exercises in plan["weekly_plan"].items():
                st.markdown(f"**🗓️ {day}**")
                for ex in exercises:
                    st.write(f"- {ex}")
                st.markdown("---")


            # Display Cool-down
            st.subheader("🧘 Cool-down (5 mins static stretching)")
            cooldown_cols = st.columns(len(plan["cooldown"]))
            for i, c in enumerate(plan["cooldown"]):
                cooldown_cols[i].success(f"• {c}")

    # ==========================================================
    # ============== DIET GENERATION LOGIC ==============
    # ==========================================================
    if diet_button:
        with st.spinner('Calculating nutrient targets and generating meal suggestions...'):
            
            # Pass all required arguments, including the new activity_level
            diet_plan = generate_diet_plan(
                gender=gender, age=age, height=height, weight=weight, 
                goal=goal, diet_type=diet_type, activity_level=activity_level
            )
            
            if "error" in diet_plan:
                st.error(diet_plan["error"])
            else:
                macros = diet_plan['macros']

                st.header(f"🍏 Your {goal} Diet Plan ({diet_plan['calorie_target']} kcal)")
                st.info(f"**Note:** BMI ({diet_plan['bmi']}) | BMR ({diet_plan['bmr']} kcal) | TDEE ({diet_plan['tdee']} kcal)")

                # Display Macros in a nice table
                st.subheader("📊 Macros per Day")
                macro_cols = st.columns(3)
                macro_cols[0].metric("Protein", f"{macros['protein_g']} g")
                macro_cols[1].metric("Carbs", f"{macros['carbs_g']} g")
                macro_cols[2].metric("Fats", f"{macros['fats_g']} g")
                
                # Calorie Check
                st.markdown(f"**Target Calorie Adjustment:** Your TDEE is **{diet_plan['tdee']} kcal**. The target of **{diet_plan['calorie_target']} kcal** is a {abs(diet_plan['tdee'] - diet_plan['calorie_target'])} kcal {'deficit' if diet_plan['calorie_target'] < diet_plan['tdee'] else 'surplus'} for your goal.")
                
                st.subheader("🍱 Suggested Meal Plan (Indian Focus)")
                
                # Display Meal Plan
                meal_tabs = st.tabs(list(diet_plan["meals"].keys()))
                
                for i, (meal_type, options) in enumerate(diet_plan["meals"].items()):
                    with meal_tabs[i]:
                        st.write("Choose one option per meal:")
                        for item in options:
                            st.markdown(f"**-** {item}")

                st.markdown("---")
                st.caption(diet_plan.get("notes", "Rule-based plan provides a strong starting point."))

with main_tabs[1]: # Fitness Chatbot Tab
    st.header("💬 Talk to Your AI Fitness Coach")
    st.write("Ask any question about your workout, diet, nutrition, or general wellness!")
    
    # 1. Display Chat History
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["parts"][0]["text"])

    # 2. Handle User Input
    if prompt := st.chat_input("Ask me about protein intake or workout recovery..."):
        
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "parts": [{"text": prompt}]})
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display AI response
        with st.chat_message("model"):
            with st.spinner("Thinking..."):
                # Call the API with the current history
                response_text = call_gemini_api(st.session_state.chat_history)
            
            st.markdown(response_text)
            
            # Add AI response to chat history
            st.session_state.chat_history.append({"role": "model", "parts": [{"text": response_text}]})
        
        # Rerun the app to update the history instantly
        st.rerun()
