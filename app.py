# app.py
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from food_logger import get_calories, save_food_to_csv
from calculator import calculate_bmr, calculate_tdee, calorie_goal, macro_split
from food_ai import predict_food
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Calorie Tracker", layout="wide")
st.title("AI Calorie Tracker")
st.write("Welcome to the smartest calorie tracker ever built.")

# --- User Profile & Daily Target ---
st.subheader("User Profile")
age = st.number_input("Age", min_value=1, value=25)
weight = st.number_input("Weight (kg)", min_value=1, value=70)
height = st.number_input("Height (cm)", min_value=1, value=170)
gender = st.selectbox("Gender", ["male", "female"])
goal = st.selectbox("Goal", ["maintain", "lose", "gain"])
activity_level = st.selectbox(
    "Activity Level",
    ["sedentary", "light", "moderate", "active", "very active"]
)

if st.button("Calculate Daily Calories"):
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity_level)
    target = calorie_goal(tdee, goal)
    st.session_state["daily_target"] = target
    st.write(f"**Daily Calorie Target:** {target} cal")
    macros = macro_split(target)
    st.write("**Recommended Macros:**")
    st.write(f"Protein: {macros['protein']}g | Fat: {macros['fat']}g | Carbs: {macros['carbs']}g")

# --- Initialize daily foods ---
if "daily_foods" not in st.session_state:
    st.session_state["daily_foods"] = []

# --- Food Logging ---
st.subheader("Food Logging")
food_name = st.text_input("Enter food name (e.g., apple, rice, chicken breast)")
grams = st.number_input("Portion size in grams", min_value=1, value=100)

if st.button("Add Food"):
    calories = get_calories(food_name, grams)
    if calories is not None:
        st.session_state.daily_foods.append({"food": food_name, "grams": grams, "calories": calories})
        save_food_to_csv(food_name, grams, calories)
        st.success(f"Added {grams}g of {food_name} = {calories} cal")
    else:
        st.error("Food not found in database. Try another name.")

# --- AI Meal Photo Upload ---
st.subheader("AI Meal Photo Upload")
uploaded_file = st.file_uploader("Upload a meal photo", type=["jpg", "png"])
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Meal", use_column_width=True)
    st.success("Photo uploaded successfully!")

    # --- Predict food ---
    predictions = predict_food(uploaded_file)
    st.subheader("AI Predictions")
    for label, prob in predictions:
        st.write(f"{label}: {prob*100:.2f}%")

    # Auto-log top match found in database
    for label, _ in predictions:
        calories = get_calories(label.lower(), 100)
        if calories is not None:
            st.session_state.daily_foods.append({"food": label.lower(), "grams": 100, "calories": calories})
            save_food_to_csv(label.lower(), 100, calories)
            st.success(f"Auto-logged {label} = {calories} cal")
            break

# --- Daily Log & Progress ---
if st.session_state.daily_foods:
    st.subheader("Today's Food Log")
    total_calories = sum(entry["calories"] for entry in st.session_state.daily_foods)
    for entry in st.session_state.daily_foods:
        st.write(f"{entry['grams']}g {entry['food']} = {entry['calories']} cal")

    st.write(f"**Total Calories Today:** {total_calories} cal")

    if "daily_target" in st.session_state:
        progress = min(total_calories / st.session_state.daily_target, 1)
        st.progress(progress)

        # Macro pie chart
        macros = macro_split(st.session_state.daily_target)
        labels = list(macros.keys())
        sizes = list(macros.values())
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)