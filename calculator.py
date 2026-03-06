def calculate_bmr(weight, height, age, gender):
    if gender == "male":
        return 10*weight + 6.25*height - 5*age + 5
    else:
        return 10*weight + 6.25*height - 5*age - 161

def calculate_tdee(bmr, activity_level):
    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very active": 1.9
    }
    return bmr * activity_multipliers.get(activity_level, 1.2)

def calorie_goal(tdee, goal):
    if goal == "lose":
        return tdee - 500
    elif goal == "gain":
        return tdee + 500
    return tdee

def macro_split(calories):
    # Simple macro split: protein 30%, fat 25%, carbs 45%
    protein = (calories * 0.3) / 4
    fat = (calories * 0.25) / 9
    carbs = (calories * 0.45) / 4
    return {"protein": round(protein), "fat": round(fat), "carbs": round(carbs)}