from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import Optional, List

app = FastAPI()

# Load course and student data
courses_df = pd.read_csv("courses.csv")
students_new_df = pd.read_csv("students_new.csv")
students_existing_df = pd.read_csv("students_existing.csv")

# Define user input model
class UserInput(BaseModel):
    student_id: Optional[str] = None
    student_type: str  # 'new' or 'existing'
    interests: Optional[List[str]] = None
    skill_level: Optional[str] = None
    preferred_mode: Optional[str] = None  # e.g., online, offline
    career_goals: Optional[str] = None
    available_time: Optional[str] = None  # e.g., part-time, full-time
    budget: Optional[float] = None

# Helper function to recommend courses

def recommend_courses(user_input: UserInput):
    recommendations = courses_df.copy()

    # For existing students, fetch their profile
    if user_input.student_type == "existing" and user_input.student_id:
        student_record = students_existing_df[students_existing_df["student_id"] == user_input.student_id]
        if not student_record.empty:
            interests = student_record.iloc[0]["interests"].split(",")
            skill_level = student_record.iloc[0]["skill_level"]
            preferred_mode = student_record.iloc[0]["preferred_mode"]
            career_goals = student_record.iloc[0]["career_goals"]
            available_time = student_record.iloc[0]["available_time"]
            budget = float(student_record.iloc[0]["budget"])
        else:
            raise HTTPException(status_code=404, detail="Student ID not found in existing students.")
    elif user_input.student_type == "new" and user_input.student_id:
        student_record = students_new_df[students_new_df["student_id"] == user_input.student_id]
        if not student_record.empty:
            interests = student_record.iloc[0]["interests"].split(",")
            skill_level = student_record.iloc[0]["skill_level"]
            preferred_mode = student_record.iloc[0]["preferred_mode"]
            career_goals = student_record.iloc[0]["career_goals"]
            available_time = student_record.iloc[0]["available_time"]
            budget = float(student_record.iloc[0]["budget"])
        else:
            raise HTTPException(status_code=404, detail="Student ID not found in new applicants.")
    else:
        interests = user_input.interests or []
        skill_level = user_input.skill_level
        preferred_mode = user_input.preferred_mode
        career_goals = user_input.career_goals
        available_time = user_input.available_time
        budget = user_input.budget

    # Apply filters
    if interests:
        keyword_filter = recommendations["keywords"].apply(lambda x: any(interest.lower() in x.lower() for interest in interests))
        recommendations = recommendations[keyword_filter]

    if skill_level:
        recommendations = recommendations[recommendations["level"].str.lower() == skill_level.lower()]

    if preferred_mode:
        recommendations = recommendations[recommendations["mode"].str.lower() == preferred_mode.lower()]

    if available_time:
        recommendations = recommendations[recommendations["time_commitment"].str.lower() == available_time.lower()]

    if budget is not None:
        recommendations = recommendations[recommendations["cost"] <= budget]

    if "rating" in recommendations.columns:
        recommendations = recommendations.sort_values(by="rating", ascending=False)

    return recommendations.head(10).to_dict(orient="records")

# API endpoint
@app.post("/get_recommendations")
def get_course_recommendations(user_input: UserInput):
    try:
        recommendations = recommend_courses(user_input)
        if not recommendations:
            raise HTTPException(status_code=404, detail="No matching courses found.")
        return {"recommended_courses": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
