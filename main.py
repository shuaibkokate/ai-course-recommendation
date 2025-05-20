from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Load CSVs as DataFrames
students_new = pd.read_csv("students_new.csv")
students_existing = pd.read_csv("students_existing.csv")
courses = pd.read_csv("courses.csv")

class RecommendationRequest(BaseModel):
    student_id: str
    student_type: str  # "new" or "existing"

class CourseRecommendation(BaseModel):
    course_code: str
    title: str
    score: int

@app.post("/recommend", response_model=list[CourseRecommendation])
def recommend_course(request: RecommendationRequest):
    student_df = students_new if request.student_type == "new" else students_existing
    student = student_df[student_df["student_id"] == request.student_id]
    if student.empty:
        raise HTTPException(status_code=404, detail="Student not found")
    student = student.iloc[0].to_dict()

    results = []
    for _, course in courses.iterrows():
        score = 0
        if request.student_type == "new":
            if course["math_req"] and student["math"] >= course["math_req"]:
                score += 1
            if course["science_req"] and student["science"] >= course["science_req"]:
                score += 1
            if course["english_req"] and student["english"] >= course["english_req"]:
                score += 1
        else:
            if not pd.isna(course["GPA_req"]) and student["GPA"] >= course["GPA_req"]:
                score += 1
        if course["interest_AI"] and student["interest_AI"]:
            score += 1
        if course["interest_business"] and student["interest_business"]:
            score += 1
        if course["career"] == student["goal"]:
            score += 1
        if score >= 2:
            results.append({
                "course_code": course["course_code"],
                "title": course["title"],
                "score": score
            })

    return results
