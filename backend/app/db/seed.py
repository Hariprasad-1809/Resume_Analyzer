from app.core.database import SessionLocal, engine, Base
from app.models.job_profile import JobProfile

def seed_data():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    profiles = [
        {
            "title": "Software Engineer",
            "required_skills": ["python", "javascript", "git", "sql", "data structures", "algorithms", "agile"],
            "preferred_skills": ["docker", "aws", "system design", "ci/cd"],
            "description": "Generalist software engineer responsible for building scalable web platforms, APIs, and backend systems.",
            "min_experience_years": 2
        },
        {
            "title": "Frontend Developer",
            "required_skills": ["javascript", "typescript", "react", "next.js", "html", "css", "tailwind", "git"],
            "preferred_skills": ["redux", "webpack", "jest", "graphql"],
            "description": "Frontend specialist focused on building responsive, highly visual user interfaces and modern web applications.",
            "min_experience_years": 3
        },
        {
            "title": "Backend Developer",
            "required_skills": ["python", "fastapi", "django", "postgresql", "redis", "docker", "git", "rest api"],
            "preferred_skills": ["kubernetes", "aws", "graphql", "gcp"],
            "description": "Backend specialist focused on building highly performant REST APIs, microservices, and managing databases.",
            "min_experience_years": 3
        },
        {
            "title": "Full Stack Developer",
            "required_skills": ["javascript", "typescript", "react", "next.js", "python", "fastapi", "postgresql", "docker", "git"],
            "preferred_skills": ["tailwind", "redis", "aws", "ci/cd"],
            "description": "Generalist engineer working across frontend interfaces, backend APIs, and systems infrastructure.",
            "min_experience_years": 4
        },
        {
            "title": "Data Scientist",
            "required_skills": ["python", "pytorch", "tensorflow", "scikit-learn", "pandas", "numpy", "sql", "machine learning"],
            "preferred_skills": ["deep learning", "nlp", "docker", "git"],
            "description": "Data professional focused on building ML pipelines, exploratory analyses, training models, and generating insights.",
            "min_experience_years": 3
        },
        {
            "title": "DevOps Engineer",
            "required_skills": ["docker", "kubernetes", "aws", "git", "ci/cd", "terraform", "ansible", "linux", "bash"],
            "preferred_skills": ["prometheus", "grafana", "nginx", "azure"],
            "description": "Infrastructure and systems engineer responsible for scaling operations, pipeline automation, and cloud deployments.",
            "min_experience_years": 4
        }
    ]

    for p_data in profiles:
        profile = JobProfile(
            title=p_data["title"],
            required_skills=p_data["required_skills"],
            preferred_skills=p_data["preferred_skills"],
            description=p_data["description"],
            min_experience_years=p_data["min_experience_years"]
        )
        db.add(profile)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_data()
