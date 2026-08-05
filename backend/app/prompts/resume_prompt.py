import json
from typing import Tuple


class ResumeAnalysisPrompt:
    """Generates structured prompts for resume analysis using OpenRouter."""

    SYSTEM_PROMPT: str = (
        "You are an experienced Technical Recruiter and Resume Reviewer with expertise in "
        "matching candidates to roles. Your task is to analyze structured resume data against "
        "a target job title. Provide accurate, data-driven insights based only on the provided "
        "information. Never hallucinate or assume information not present in the resume. "
        "If information is missing, explicitly state that it was not found. Always return valid JSON."
    )

    ANALYSIS_INSTRUCTIONS: str = (
        "Analyze the resume against the target job role and provide comprehensive feedback on:\n"
        "1. Overall Match Score (0-100)\n"
        "2. Candidate Strengths (list top 5-8 strengths)\n"
        "3. Weaknesses (areas that need improvement)\n"
        "4. Missing Skills (critical skills not present in resume)\n"
        "5. Recommended Skills (skills to develop for career growth)\n"
        "6. Resume Improvements (actionable recommendations to strengthen resume)\n"
        "7. Project Analysis (analyze each project's relevance and impact)\n"
        "8. Experience Analysis (evaluate work history relevance and achievements)\n"
        "9. ATS Recommendations (suggestions for ATS optimization)\n"
        "10. Interview Readiness (assessment with specific preparation areas)\n"
        "11. Learning Roadmap (personalized skill development plan)\n"
        "12. Suitable Roles (other roles this candidate is well-suited for)"
    )

    OUTPUT_FORMAT: str = (
        "Return ONLY valid JSON without any markdown formatting or extra text. "
        "Use this exact structure:\n"
        "{\n"
        '  "overall_match": <number 0-100>,\n'
        '  "summary": "<brief high-level summary>",\n'
        '  "strengths": [<array of strings>],\n'
        '  "weaknesses": [<array of strings>],\n'
        '  "missing_skills": [<array of strings>],\n'
        '  "recommended_skills": [<array of strings>],\n'
        '  "project_analysis": [\n'
        '    {\n'
        '      "project_name": "<name>",\n'
        '      "relevance": "<high/medium/low>",\n'
        '      "impact": "<description>",\n'
        '      "skills_demonstrated": [<array of skills>],\n'
        '      "improvement_suggestions": [<array of suggestions>]\n'
        "    }\n"
        "  ],\n"
        '  "experience_analysis": [\n'
        '    {\n'
        '      "company": "<name>",\n'
        '      "role": "<title>",\n'
        '      "duration": "<period>",\n'
        '      "relevance": "<high/medium/low>",\n'
        '      "key_achievements": [<array of achievements>],\n'
        '      "transferable_skills": [<array of skills>]\n'
        "    }\n"
        "  ],\n"
        '  "resume_improvements": [<array of actionable suggestions>],\n'
        '  "learning_roadmap": [\n'
        '    {\n'
        '      "skill": "<skill name>",\n'
        '      "priority": "<high/medium/low>",\n'
        '      "timeframe": "<timeframe>",\n'
        '      "resources": [<array of resource suggestions>]\n'
        "    }\n"
        "  ],\n"
        '  "interview_readiness": "<comprehensive assessment>",\n'
        '  "suitable_roles": [<array of role suggestions>]\n'
        "}"
    )

    @staticmethod
    def build_system_prompt() -> str:
        """Build and return the system prompt."""
        return ResumeAnalysisPrompt.SYSTEM_PROMPT

    @staticmethod
    def build_user_prompt(job_title: str, resume_data: dict) -> str:
        """
        Build and return the user prompt with job title and resume data.

        Args:
            job_title: Target job title for analysis
            resume_data: Structured resume data from parser

        Returns:
            Formatted user prompt string
        """
        prompt_parts = [
            "ANALYSIS REQUEST",
            "=" * 50,
            f"Target Job Title: {job_title}\n",
            "Resume Data (JSON):",
            json.dumps(resume_data, indent=2),
            "\n" + "=" * 50,
            ResumeAnalysisPrompt.ANALYSIS_INSTRUCTIONS,
            "\n" + "=" * 50,
            ResumeAnalysisPrompt.OUTPUT_FORMAT,
        ]

        return "\n".join(prompt_parts)

    @staticmethod
    def get_prompts(job_title: str, resume_data: dict) -> Tuple[str, str]:
        """
        Get both system and user prompts.

        Args:
            job_title: Target job title for analysis
            resume_data: Structured resume data from parser

        Returns:
            Tuple of (system_prompt, user_prompt)
        """
        return (
            ResumeAnalysisPrompt.build_system_prompt(),
            ResumeAnalysisPrompt.build_user_prompt(job_title, resume_data),
        )
