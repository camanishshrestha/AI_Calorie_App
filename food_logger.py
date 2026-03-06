import csv
import os
from datetime import datetime

FOOD_DATABASE = {
    "apple": 52,
    "banana": 89,
    "rice": 130,
    "chicken breast": 165,
    "egg": 155,
    "bread": 265,
    "milk": 42,
    "cheese": 402,
    "broccoli": 55,
    "tomato": 18,
    "potato": 77,
    "salmon": 208,
}

CSV_FILE = "daily_food_log.csv"

def get_calories(food_name, grams):
    food_name = food_name.lower()
    if food_name in FOOD_DATABASE:
        calories_per_100g = FOOD_DATABASE[food_name]
        return round(calories_per_100g * grams / 100)
    else:
        return None

def save_food_to_csv(food_name, grams, calories, meal="Other"):
    file_exists = os.path.isfile(CSV_FILE)
    today = datetime.now().strftime("%Y-%m-%d")
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["date", "meal", "food", "grams", "calories"])
        writer.writerow([today, meal, food_name, grams, calories])

def load_foods_from_csv():
    foods = []
    if os.path.isfile(CSV_FILE):
        with open(CSV_FILE, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                foods.append({
                    "date": row["date"],
                    "meal": row["meal"],
                    "food": row["food"],
                    "grams": float(row["grams"]),
                    "calories": float(row["calories"])
                })
    return foods

def calculate_food_macros(food_name, grams):
    """
    Returns protein, carbs, fat (grams) per portion size
    Using approximate standard macro ratios
    """
    macros_database = {
        "apple": (0.3, 14, 0.2),
        "banana": (1.1, 23, 0.3),
        "rice": (2.7, 28, 0.3),
        "chicken breast": (31, 0, 3.6),
        "egg": (13, 1.1, 11),
        "bread": (9, 49, 3.2),
        "milk": (3.4, 5, 1),
        "cheese": (25, 1.3, 33),
        "broccoli": (2.8, 7, 0.4),
        "tomato": (0.9, 3.9, 0.2),
        "potato": (2, 17, 0.1),
        "salmon": (20, 0, 13)
    }

    food_name = food_name.lower()
    if food_name in macros_database:
        p, c, f = macros_database[food_name]
        factor = grams / 100
        return round(p*factor), round(c*factor), round(f*factor)
    else:
        return 0,0,0