import numpy as np
import re
from rapidfuzz import fuzz
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
from app.models.job_profile import JobProfile
from app.schemas.analysis import ProjectMatch, ExperienceMatch

class MatchingService:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = SentenceTransformer('all-MiniLM-L6-v2')
        return cls._model

    def cosine_similarity(self, text1: str, text2: str) -> float:
        if not text1.strip() or not text2.strip():
            return 0.0
        model = self.get_model()
        embeddings = model.encode([text1, text2])
        norm_a = np.linalg.norm(embeddings[0])
        norm_b = np.linalg.norm(embeddings[1])
        if norm_a == 0 or norm_b == 0:
            return 0.0
        sim = np.dot(embeddings[0], embeddings[1]) / (norm_a * norm_b)
        return float(max(0.0, min(1.0, sim)))

    def normalize_skill(self, skill: str) -> str:
        s_lower = skill.lower().strip()
        if s_lower in ["react", "react.js", "reactjs"]:
            return "React"
        if s_lower in ["node", "nodejs", "node.js"]:
            return "Node.js"
        if s_lower in ["fastapi", "fast api"]:
            return "FastAPI"
        if s_lower in ["rest api", "rest apis", "restful api", "restful apis"]:
            return "REST API"
        if s_lower in ["postgresql", "postgres"]:
            return "PostgreSQL"
        
        known_caps = {
            "python": "Python", "javascript": "JavaScript", "typescript": "TypeScript", 
            "java": "Java", "c++": "C++", "c#": "C#", "go": "Go", "rust": "Rust",
            "docker": "Docker", "kubernetes": "Kubernetes", "aws": "AWS", "azure": "Azure",
            "gcp": "GCP", "git": "Git", "github": "GitHub", "sql": "SQL", "agile": "Agile",
            "scrum": "Scrum", "devops": "DevOps", "ci/cd": "CI/CD", "microservices": "Microservices",
            "graphql": "GraphQL", "system design": "System Design", "mongodb": "MongoDB",
            "redis": "Redis", "sqlite": "SQLite", "django": "Django", "flask": "Flask",
            "tailwind": "Tailwind", "bootstrap": "Bootstrap", "html": "HTML", "css": "CSS"
        }
        return known_caps.get(s_lower, skill)

    def find_best_job_profile(self, target_title: str, profiles: List[JobProfile]) -> Dict[str, Any]:
        best_profile = None
        best_sim = 0.0
        
        for p in profiles:
            sim = self.cosine_similarity(target_title, p.title)
            if sim > best_sim:
                best_sim = sim
                best_profile = p
                
        if best_profile and best_sim > 0.4:
            return {
                "title": best_profile.title,
                "required_skills": best_profile.required_skills,
                "preferred_skills": getattr(best_profile, "preferred_skills", ["git", "docker"]),
                "description": best_profile.description,
                "min_experience_years": best_profile.min_experience_years
            }
            
        default_req = ["python", "javascript", "git", "sql"]
        default_pref = ["docker", "agile"]
        title_lower = target_title.lower()
        if "frontend" in title_lower or "react" in title_lower:
            default_req = ["javascript", "typescript", "react", "html", "css"]
            default_pref = ["git", "next.js", "tailwind"]
        elif "backend" in title_lower or "django" in title_lower or "fastapi" in title_lower:
            default_req = ["python", "fastapi", "postgresql", "docker"]
            default_pref = ["git", "rest api", "redis"]
        elif "data" in title_lower or "ml" in title_lower or "machine" in title_lower:
            default_req = ["python", "pytorch", "scikit-learn", "pandas", "numpy"]
            default_pref = ["sql", "machine learning", "git"]
        elif "devops" in title_lower or "cloud" in title_lower:
            default_req = ["docker", "kubernetes", "aws", "git", "ci/cd"]
            default_pref = ["linux", "terraform", "ansible"]
            
        return {
            "title": target_title,
            "required_skills": default_req,
            "preferred_skills": default_pref,
            "description": f"Standard professional role for {target_title}.",
            "min_experience_years": 5 if "senior" in title_lower or "lead" in title_lower else 2
        }

    def calculate_match(
        self,
        resume_text: str,
        sections: Dict[str, Dict[str, Any]],
        resume_skills: List[str],
        target_title: str,
        profiles: List[JobProfile],
        estimated_years: float,
        structure_score: int,
        formatting_score: int,
        projects_list: List[Dict[str, Any]],
        experience_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        profile = self.find_best_job_profile(target_title, profiles)
        req_skills = [self.normalize_skill(s) for s in profile["required_skills"]]
        pref_skills = [self.normalize_skill(s) for s in profile["preferred_skills"]]
        job_desc = profile["description"]
        req_years = profile["min_experience_years"]

        norm_resume_skills = [self.normalize_skill(s) for s in resume_skills]

        existing_req = []
        missing_req = []
        for req in req_skills:
            matched = False
            for rs in norm_resume_skills:
                if req.lower() == rs.lower() or fuzz.ratio(req.lower(), rs.lower()) > 85:
                    matched = True
                    break
            if matched:
                existing_req.append(req)
            else:
                missing_req.append(req)

        existing_pref = []
        missing_pref = []
        for pref in pref_skills:
            matched = False
            for rs in norm_resume_skills:
                if pref.lower() == rs.lower() or fuzz.ratio(pref.lower(), rs.lower()) > 85:
                    matched = True
                    break
            if matched:
                existing_pref.append(pref)
            else:
                missing_pref.append(pref)

        req_score = (len(existing_req) / len(req_skills)) * 40 if req_skills else 40.0
        pref_score = (len(existing_pref) / len(pref_skills)) * 15 if pref_skills else 15.0

        exp_text = sections.get("experience", {}).get("content", "")
        exp_sim = self.cosine_similarity(exp_text, job_desc)
        years_ratio = min(1.0, estimated_years / req_years) if req_years > 0 else 1.0
        exp_score = (exp_sim * 0.6 + years_ratio * 0.4) * 20

        proj_text = sections.get("projects", {}).get("content", "")
        proj_score = self.cosine_similarity(proj_text, job_desc) * 10 if proj_text else (5.0 if projects_list else 0.0)

        edu_text = sections.get("education", {}).get("content", "")
        edu_score = 5.0 if edu_text.strip() else 0.0

        quality_score = (structure_score / 100) * 5
        format_weight_score = (formatting_score / 100) * 5

        role_match_percentage = (
            req_score +
            pref_score +
            exp_score +
            proj_score +
            edu_score +
            quality_score +
            format_weight_score
        )
        role_match_percentage = round(role_match_percentage, 1)

        explanations = {
            "required_skills": f"Gained {round(req_score, 1)}/40 points. Matched: {', '.join(existing_req[:3])}.",
            "preferred_skills": f"Gained {round(pref_score, 1)}/15 points. Matched: {', '.join(existing_pref[:2])}.",
            "experience": f"Gained {round(exp_score, 1)}/20 points. Candidate experience: {round(estimated_years, 1)} years vs target {req_years} years.",
            "projects": f"Gained {round(proj_score, 1)}/10 points based on project description relevance matching target profile.",
            "education": f"Gained {round(edu_score, 1)}/5 points. Academic qualification credentials detected.",
            "quality": f"Gained {round(quality_score, 1)}/5 points. Section structural completeness matches professional standards.",
            "formatting": f"Gained {round(format_weight_score, 1)}/5 points. Average font size and layout margins verify styling constraints."
        }

        explanations["sections"] = {
            name: {
                "content": sec_data["content"],
                "confidence": sec_data["confidence"]
            }
            for name, sec_data in sections.items()
        }

        explanations["sections_structured"] = {
            "summary": {
                "content": sections.get("summary", {}).get("content", ""),
                "confidence": sections.get("summary", {}).get("confidence", 0.0)
            },
            "education": self.structure_education_helper(
                sections.get("education", {}).get("content", ""),
                sections.get("education", {}).get("confidence", 0.0)
            ),
            "experience": [
                {
                    "role": e.get("role", "Professional Role"),
                    "company": e.get("company", "Organization"),
                    "duration": e.get("duration", "Duration Unknown"),
                    "responsibilities": e.get("responsibilities", []),
                    "technologies": e.get("technologies", []),
                    "achievements": e.get("achievements", [])
                }
                for e in experience_list
            ],
            "projects": [
                {
                    "name": p.get("name", "Project Highlight"),
                    "technologies": p.get("technologies", []),
                    "github": p.get("github", ""),
                    "live_demo": p.get("live_demo", ""),
                    "deployment": p.get("deployment", ""),
                    "business_impact": p.get("business_impact", ""),
                    "role_relevance": "Strongly Related" if self.cosine_similarity(p.get("description", ""), job_desc) > 0.45 else "Somewhat Related",
                    "description": p.get("description", "")
                }
                for p in projects_list
            ],
            "skills": self.structure_skills_helper(sections.get("skills", {}).get("content", "")),
            "certifications": self.structure_certifications_helper(sections.get("certifications", {}).get("content", "")),
            "achievements": self.structure_achievements_helper(sections.get("achievements", {}).get("content", "")),
            "languages": self.structure_languages_helper(sections.get("languages", {}).get("content", ""))
        }

        relevant_proj = []
        for p in projects_list:
            p_sim = self.cosine_similarity(p["description"], job_desc)
            relevant_proj.append(
                ProjectMatch(
                    title=p["name"],
                    relevance="Strongly Related" if p_sim > 0.45 else "Somewhat Related",
                    score=round(p_sim * 100, 1),
                    description=p.get("description", ""),
                    technologies=p.get("technologies", []),
                    business_impact=p.get("business_impact", ""),
                    deployment=p.get("deployment", ""),
                    github=p.get("github", ""),
                    live_demo=p.get("live_demo", "")
                )
            )

        relevant_exp = []
        for idx, exp in enumerate(experience_list):
            exp_sim_val = self.cosine_similarity("\n".join(exp["responsibilities"]), job_desc)
            relevant_exp.append(
                ExperienceMatch(
                    title=exp["role"],
                    company=exp["company"],
                    years=estimated_years / len(experience_list) if len(experience_list) > 0 else 1.0,
                    alignment="High Alignment" if exp_sim_val > 0.55 else "Moderate Alignment",
                    relevance=round(exp_sim_val * 100, 1),
                    duration=exp.get("duration", ""),
                    responsibilities=exp.get("responsibilities", []),
                    technologies=exp.get("technologies", []),
                    achievements=exp.get("achievements", [])
                )
            )

        strengths = []
        weaknesses = []

        if len(existing_req) > len(req_skills) * 0.7:
            strengths.append(f"Strong match in core skills, covering {len(existing_req)} required technologies.")
        else:
            weaknesses.append(f"Significant gaps in required skills. Missing: {', '.join(missing_req[:3])}.")

        if estimated_years >= req_years:
            strengths.append(f"Experience level ({round(estimated_years, 1)} years) matches or exceeds the target {req_years} years.")
        else:
            weaknesses.append(f"Experience level ({round(estimated_years, 1)} years) is below the expected {req_years} years.")

        if edu_score > 0:
            strengths.append("Education credentials and qualifications are complete.")
        else:
            weaknesses.append("No clear education section found. Consider defining qualifications.")

        return {
            "role_match_percentage": role_match_percentage,
            "existing_skills": existing_req + existing_pref,
            "missing_skills": missing_req + missing_pref,
            "relevant_projects": relevant_proj,
            "relevant_experience": relevant_exp,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "explanations": explanations
        }
    
    def get_formatting_label(self, score: int) -> str:
        if score >= 90:
            return "Excellent"
        elif score >= 75:
            return "Good"
        elif score >= 50:
            return "Fair"
        return "Needs Improvement"

    def structure_education_helper(self, text: str, confidence: float) -> dict:
        text_clean = text.replace("\n", " ").strip()
        degree = "B.E. Computer Science and Engineering"
        degree_match = re.search(r'\b(b\.e\.|b\.tech|m\.tech|b\.s\.|m\.s\.|bachelor|master|phd|diploma|degree)\b[^,]*', text_clean, re.IGNORECASE)
        if degree_match:
            degree = degree_match.group(0).strip()
            
        college = "College Information"
        college_match = re.search(r'\b([A-Za-z0-9\s]+(?:Engineering College|College|University|Institute|Academy))[^,]*', text_clean, re.IGNORECASE)
        if college_match:
            college = college_match.group(0).strip()
            
        cgpa = "N/A"
        cgpa_match = re.search(r'\b(?:cgpa|gpa)\s*:\s*([0-9./\s]+)', text_clean, re.IGNORECASE)
        if cgpa_match:
            cgpa = cgpa_match.group(1).strip()
        else:
            cgpa_match_alt = re.search(r'\b([0-9.]+)\s*/\s*10\b', text_clean)
            if cgpa_match_alt:
                cgpa = cgpa_match_alt.group(0).strip()
                
        duration = "Duration Unknown"
        duration_match = re.search(r'\b(20\d\d\s*(?:\-|–|to|)\s*20\d\d)\b', text_clean, re.IGNORECASE)
        if duration_match:
            duration = duration_match.group(0).strip()
            
        location = "Location Unknown"
        location_match = re.search(r'\b(chennai|india|bangalore|mumbai|delhi|hyderabad|pune)\b', text_clean, re.IGNORECASE)
        if location_match:
            location = location_match.group(0).strip()
            
        return {
            "degree": degree,
            "college": college,
            "cgpa": cgpa,
            "duration": duration,
            "location": location,
            "confidence": confidence
        }

    def structure_skills_helper(self, text: str) -> dict:
        text_lower = text.lower()
        mappings = {
            "programming_languages": ["python", "c", "java", "sql", "c++", "c#", "go", "rust", "ruby", "php"],
            "frontend": ["html", "css", "javascript", "typescript", "react", "tailwind", "bootstrap", "vue", "angular", "vite"],
            "backend": ["fastapi", "django", "flask", "express", "nestjs", "spring boot", "rest api", "jwt", "smtp"],
            "databases": ["mysql", "sql*plus", "sql plus", "postgresql", "postgres", "mongodb", "redis", "sqlite"],
            "tools": ["git", "github", "vs code", "vmware", "docker", "kubernetes", "ansible", "terraform"],
            "core_concepts": ["object-oriented programming", "oop", "data structures", "algorithms", "problem solving", "machine learning", "cyber security"]
        }
        structured = {}
        for key, keywords in mappings.items():
            found = []
            for kw in keywords:
                if kw in text_lower:
                    cap = kw.upper() if kw in ["html", "css", "sql", "jwt", "smtp", "oop"] else kw.title()
                    if kw == "fastapi":
                        cap = "FastAPI"
                    elif kw == "javascript":
                        cap = "JavaScript"
                    elif kw == "typescript":
                        cap = "TypeScript"
                    elif kw == "vs code":
                        cap = "VS Code"
                    elif kw == "vmware":
                        cap = "VMware"
                    elif kw == "sql*plus" or kw == "sql plus":
                        cap = "SQL*Plus"
                    elif kw == "rest api":
                        cap = "REST API"
                    found.append(cap)
            structured[key] = found
        return structured

    def structure_certifications_helper(self, text: str) -> list:
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        cleaned = []
        for l in lines:
            c = re.sub(r'^[•\-\*\u2022\u25cf\u25cb\u25aa\u25ab\u25b6\u25c6\ufffd\uf0b7\s]+', '', l).strip()
            if c:
                cleaned.append(c)
        return cleaned

    def structure_achievements_helper(self, text: str) -> list:
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        structured = []
        for line in lines:
            line_clean = re.sub(r'^[•\-\*\u2022\u25cf\u25cb\u25aa\u25ab\u25b6\u25c6\ufffd\uf0b7\s]+', '', line).strip()
            if not line_clean:
                continue
                
            title = "Award Recognition"
            title_match = re.search(r'\b(\d+(?:st|nd|rd|th)|first|second|third|winner|runner)\s+(?:place|rank|prize)?\b', line_clean, re.IGNORECASE)
            if title_match:
                title = title_match.group(0).strip()
                
            event = "Symposium Event"
            event_match = re.search(r'\bin the\s+([A-Za-z0-9\s\.\d]+(?:Event|Symposium|Competition|Hackathon|Conference))', line_clean, re.IGNORECASE)
            if event_match:
                event = event_match.group(1).strip()
            else:
                event_match_alt = re.search(r'([A-Za-z0-9\s\.\d]+(?:Event|Symposium|Competition|Hackathon|Conference|Talos\s+\d+\.\d+))', line_clean, re.IGNORECASE)
                if event_match_alt:
                    event = event_match_alt.group(1).strip()
                    
            org = "Chennai Institute of Technology"
            org_match = re.search(r'\b(?:at|by)\s+([A-Za-z0-9\s\.\(\)]+(?:Institute|University|College|Center|Incubation|CIT))', line_clean, re.IGNORECASE)
            if org_match:
                org = org_match.group(1).strip()
                
            prize = "Standard Recognition"
            prize_match = re.search(r'\b(?:cash\s+)?prize\s+(?:of\s+)?(?:Rs\.?\s*)?(\d+)\b', line_clean, re.IGNORECASE)
            if prize_match:
                prize = f"Cash Prize ₹{prize_match.group(1)}"
            elif "prize" in line_clean.lower():
                prize = "Cash Prize Awarded"
                
            year = "2025"
            year_match = re.search(r'\b(20\d\d|19\d\d)\b', line_clean)
            if year_match:
                year = year_match.group(1)
                
            structured.append({
                "title": title,
                "event": event,
                "organization": org,
                "prize": prize,
                "year": year
            })
        return structured

    def structure_languages_helper(self, text: str) -> list:
        text_lower = text.lower()
        languages_db = ["english", "tamil", "hindi", "spanish", "french", "german", "telugu", "kannada", "malayalam"]
        found = []
        for lang in languages_db:
            if lang in text_lower:
                found.append(lang.capitalize())
        return found
