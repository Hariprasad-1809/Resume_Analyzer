import os
from sqlalchemy.orm import Session
from app.services.parser_service import ParserService
from app.services.extractor_service import ExtractorService
from app.services.matching_service import MatchingService
from app.services.recommendation_service import RecommendationService
from app.models.resume import Resume
from app.models.analysis import Analysis
from app.models.job_profile import JobProfile

class AnalysisService:
    def __init__(self):
        self.parser = ParserService()
        self.extractor = ExtractorService()
        self.matcher = MatchingService()
        self.recommender = RecommendationService()

    def run_analysis(self, db: Session, file_path: str, filename: str, target_title: str) -> Analysis:
        raw_text = self.parser.extract_text_from_pdf(file_path)
        formatting = self.parser.analyze_formatting(file_path)
        
        sections = self.extractor.extract_sections(raw_text)
        skills = self.extractor.extract_skills(raw_text)
        contact = self.extractor.extract_contact_info(raw_text)
        est_years = self.extractor.estimate_experience_years(raw_text)
        
        print("----- DETECTED HEADINGS AUDIT -----")
        for name, sec_data in sections.items():
            status = "Detected" if sec_data["content"].strip() else "Missing"
            print(f"{status:12} | Section: {name:15} | Confidence: {sec_data['confidence']}% | Len: {len(sec_data['content'])}")
        print("-----------------------------------")

        sections_found = [k for k, v in sections.items() if v["content"].strip()]
        
        required = ["contact_info", "education", "experience", "skills"]
        optional = ["summary", "projects", "certifications", "achievements", "languages"]
        
        missing_required = [r for r in required if r not in sections_found]
        missing_optional = [o for o in optional if o not in sections_found]
        
        structure_score = 100 - len(missing_required) * 20 - len(missing_optional) * 5
        structure_score = max(0, structure_score)
        
        feedback = "Perfect layout coverage!" if structure_score == 100 else f"Core missing: {', '.join(missing_required)}"
        structure = {
            "sections_found": sections_found,
            "missing_sections": missing_required + missing_optional,
            "score": structure_score,
            "feedback": feedback
        }

        proj_content = sections.get("projects", {}).get("content", "")
        projects_list = self.extractor.extract_projects_details(proj_content)
        
        exp_content = sections.get("experience", {}).get("content", "")
        experience_list = self.extractor.extract_experience_details(exp_content)
        
        profiles = db.query(JobProfile).all()
        
        match_data = self.matcher.calculate_match(
            resume_text=raw_text,
            sections=sections,
            resume_skills=skills,
            target_title=target_title,
            profiles=profiles,
            estimated_years=est_years,
            structure_score=structure_score,
            formatting_score=formatting["score"],
            projects_list=projects_list,
            experience_list=experience_list
        )
        
        formatting["rating"] = self.matcher.get_formatting_label(formatting["score"])
        
        recs = self.recommender.generate_recommendations(
            missing_skills=match_data["missing_skills"],
            structure=structure,
            formatting=formatting,
            contact=contact,
            target_title=target_title,
            analysis_context={
                "overall_match": match_data["role_match_percentage"],
                "strengths": match_data["strengths"],
                "weaknesses": match_data["weaknesses"],
                "project_analysis": [p.model_dump() for p in match_data["relevant_projects"]],
                "experience_analysis": [e.model_dump() for e in match_data["relevant_experience"]],
                "sections": sections,
                "summary_text": sections.get("summary", {}).get("content", ""),
                "projects_text": sections.get("projects", {}).get("content", ""),
                "experience_text": sections.get("experience", {}).get("content", ""),
                "education_text": sections.get("education", {}).get("content", ""),
                "achievements_text": sections.get("achievements", {}).get("content", ""),
                "certifications_text": sections.get("certifications", {}).get("content", ""),
            }
        )
        
        resume_record = Resume(
            filename=filename,
            file_path=file_path,
            raw_text=raw_text
        )
        db.add(resume_record)
        db.flush()
        
        analysis_record = Analysis(
            resume_id=resume_record.id,
            job_title=target_title,
            role_match_percentage=match_data["role_match_percentage"],
            existing_skills=match_data["existing_skills"],
            missing_skills=match_data["missing_skills"],
            relevant_projects=[p.model_dump() for p in match_data["relevant_projects"]],
            relevant_experience=[e.model_dump() for e in match_data["relevant_experience"]],
            strengths=match_data["strengths"],
            weaknesses=match_data["weaknesses"],
            structure_analysis=structure,
            formatting_analysis=formatting,
            keyword_recommendations=recs["keyword_recommendations"],
            improvement_suggestions=recs["improvement_suggestions"],
            learning_recommendations=[l.model_dump() for l in recs["learning_recommendations"]],
            suitable_job_roles=recs["suitable_job_roles"],
            explanations=match_data["explanations"]
        )
        db.add(analysis_record)
        db.commit()
        db.refresh(analysis_record)
        
        return analysis_record
