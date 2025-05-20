from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import Optional, List

app = FastAPI()

# Load data
courses_df = pd.read_csv("courses.csv")
students_new_df = pd.read_csv("students_new.csv")
students_existing_df = pd.read_csv("students_existing.csv")

class UserInput(BaseModel):
    student_id: Optional[str] = None
    student_type: str  # 'new', 'existing', or 'custom'
    interests: Optional[List[str]] = None
    skill_level: Optional[str] = None
    preferred_mode: Optional[str] = None
    career_goals: Optional[str] = None
    available_time: Optional[str] = None
    budget: Optional[float] = None

@app.post("/get_recommendations")
def get_recommendations(user_input: UserInput):
    df = courses_df.copy()

    if user_input.student_type in ["new", "existing"] and user_input.student_id:
        df_students = students_new_df if user_input.student_type == "new" else students_existing_df
        student = df_students[df_students["student_id"] == user_input.student_id]
        if student.empty:
            raise HTTPException(status_code=404, detail="Student ID not found.")
        student = student.iloc[0]
        interests = student["interests"].split(",")
        skill_level = student["skill_level"]
        preferred_mode = student["preferred_mode"]
        career_goals = student["career_goals"]
        available_time = student["available_time"]
        budget = student["budget"]
    else:
        interests = user_input.interests or []
        skill_level = user_input.skill_level
        preferred_mode = user_input.preferred_mode
        career_goals = user_input.career_goals
        available_time = user_input.available_time
        budget = user_input.budget

    if interests:
        df = df[df["keywords"].apply(lambda x: any(i.lower() in x.lower() for i in interests))]
    if skill_level:
        df = df[df["level"].str.lower() == skill_level.lower()]
    if preferred_mode:
        df = df[df["mode"].str.lower() == preferred_mode.lower()]
    if available_time:
        df = df[df["time_commitment"].str.lower() == available_time.lower()]
    if budget is not None:
        df = df[df["cost"] <= budget]

    df = df.sort_values(by="rating", ascending=False)

    return {"recommended_courses": df.head(10).to_dict(orient="records")}