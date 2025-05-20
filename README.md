# Course Recommendation API

This is a FastAPI-based project that recommends courses for both new and existing students based on their profile or input.

## Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Usage

POST to `/get_recommendations` with either:

### For new/existing student:

```json
{
  "student_id": "A001",
  "student_type": "new"
}
```

### For custom input:

```json
{
  "student_type": "custom",
  "interests": ["ai", "programming"],
  "skill_level": "beginner",
  "preferred_mode": "online",
  "career_goals": "research",
  "available_time": "part-time",
  "budget": 500
}
```