# 🎓 AI Course Recommendation API

This project provides course recommendations for both new applicants and existing students based on academic performance, interests, and career goals.

## 🚀 Run the API Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit: http://127.0.0.1:8000/docs

## 📁 Data Files

- `students_new.csv`: New applicants with academic scores and interests
- `students_existing.csv`: Existing students with GPA and career goals
- `courses.csv`: Course catalog with eligibility criteria

## 📤 API Endpoint

### POST `/recommend`

#### Request JSON
```json
{
  "student_id": "A001",
  "student_type": "new"
}
```

#### Response
```json
[
  {
    "course_code": "CSE101",
    "title": "Intro to AI",
    "score": 4
  }
]
```
