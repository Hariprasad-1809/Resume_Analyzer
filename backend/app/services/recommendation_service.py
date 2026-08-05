import json
import logging
import re
from typing import Any, Dict, List, Optional, Tuple

import httpx

from app.core.config import settings
from app.schemas.analysis import LearningResource

logger = logging.getLogger(__name__)

TECH_MAP = {
    "react": {
        "prep": ["React Hooks (useEffect, useMemo, useCallback)", "State management (Context API, Redux/Zustand)", "Performance Optimization (Virtual DOM, code splitting, memoization)"],
        "cert": "Meta Front-End Developer Certificate",
        "resource": ("React Docs", "https://react.dev/learn")
    },
    "fastapi": {
        "prep": ["JWT authentication & Security", "Dependency Injection System", "Asynchronous endpoints (async/await & Pydantic validation)"],
        "cert": "Python Institute Certified Professional",
        "resource": ("FastAPI Docs", "https://fastapi.tiangolo.com/")
    },
    "python": {
        "prep": ["Decorators, generators, and context managers", "Memory management & GIL", "Multithreading vs. Multiprocessing"],
        "cert": "PCEP/PCAP Certification",
        "resource": ("Python Tutorial", "https://docs.python.org/3/tutorial/")
    },
    "typescript": {
        "prep": ["Advanced Types (Generics, Union/Intersection, Mapped Types)", "Type narrowing & Type guards", "TSConfig configuration & strict compilation"],
        "cert": "Microsoft Certified: JavaScript/TypeScript",
        "resource": ("TypeScript Handbook", "https://www.typescriptlang.org/docs/")
    },
    "javascript": {
        "prep": ["Event Loop, Microtasks & Macrotasks", "Closures, Prototypes, and Scope chain", "Promises, Async/Await & ES6+ features"],
        "cert": "OpenJS Node.js Application Developer (JSNAD)",
        "resource": ("MDN JavaScript Guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript")
    },
    "next.js": {
        "prep": ["App Router vs Pages Router", "Server Components vs Client Components", "Data fetching strategies (SSR, SSG, ISR)"],
        "cert": "Vercel Next.js Certification",
        "resource": ("Next.js Docs", "https://nextjs.org/docs")
    },
    "nextjs": {
        "prep": ["App Router vs Pages Router", "Server Components vs Client Components", "Data fetching strategies (SSR, SSG, ISR)"],
        "cert": "Vercel Next.js Certification",
        "resource": ("Next.js Docs", "https://nextjs.org/docs")
    },
    "node.js": {
        "prep": ["Event Loop & Non-blocking I/O", "Buffer, Stream, and Cluster modules", "Middleware patterns & Async error handling"],
        "cert": "OpenJS Node.js Services Developer (JSNSD)",
        "resource": ("Node.js Docs", "https://nodejs.org/en/docs/")
    },
    "nodejs": {
        "prep": ["Event Loop & Non-blocking I/O", "Buffer, Stream, and Cluster modules", "Middleware patterns & Async error handling"],
        "cert": "OpenJS Node.js Services Developer (JSNSD)",
        "resource": ("Node.js Docs", "https://nodejs.org/en/docs/")
    },
    "docker": {
        "prep": ["Dockerfile optimization (multi-stage builds)", "Docker volumes and networking", "Docker Compose for multi-container services"],
        "cert": "Docker Certified Associate (DCA)",
        "resource": ("Docker Docs", "https://docs.docker.com/")
    },
    "kubernetes": {
        "prep": ["K8s Pod lifecycle & deployment strategies", "Service types & Ingress controllers", "ConfigMaps, Secrets, & Persistent Volumes"],
        "cert": "Certified Kubernetes Administrator (CKA)",
        "resource": ("Kubernetes Docs", "https://kubernetes.io/docs/home/")
    },
    "postgresql": {
        "prep": ["Query performance tuning (Explain, Analyze)", "Index types (B-Tree, GIN, Hash) and usage", "Database transactions (ACID, isolation levels)"],
        "cert": "PostgreSQL Certified Associate",
        "resource": ("PostgreSQL Docs", "https://www.postgresql.org/docs/")
    },
    "postgres": {
        "prep": ["Query performance tuning (Explain, Analyze)", "Index types (B-Tree, GIN, Hash) and usage", "Database transactions (ACID, isolation levels)"],
        "cert": "PostgreSQL Certified Associate",
        "resource": ("PostgreSQL Docs", "https://www.postgresql.org/docs/")
    },
    "sql": {
        "prep": ["Joins, Subqueries, & Common Table Expressions (CTEs)", "Window functions & Aggregations", "Query optimization"],
        "cert": "Oracle Database SQL Certified Associate",
        "resource": ("PostgreSQL Docs", "https://www.postgresql.org/docs/")
    },
    "aws": {
        "prep": ["IAM policies and security best practices", "VPC routing, subnets, & security groups", "Compute/Serverless (EC2, ECS, Lambda)"],
        "cert": "AWS Certified Solutions Architect - Associate",
        "resource": ("AWS Documentation", "https://docs.aws.amazon.com/")
    },
    "git": {
        "prep": ["Git branching strategies (GitFlow, trunk-based)", "Rebase vs. Merge & conflict resolution", "Stashing, cherry-picking, & reflog"],
        "cert": "GitLab Certified Git Associate",
        "resource": ("Git Docs", "https://git-scm.com/doc")
    },
    "graphql": {
        "prep": ["Schema definition & type system", "Query vs. Mutation vs. Subscription", "N+1 query problem and DataLoader resolver pattern"],
        "cert": "Apollo GraphQL Professional",
        "resource": ("GraphQL Learn", "https://graphql.org/learn/")
    },
    "redis": {
        "prep": ["Redis data structures (strings, hashes, lists, sets, sorted sets)", "Caching strategies (Cache-Aside, Write-Through)", "Pub/Sub mechanism and rate limiting"],
        "cert": "Redis Certified Developer",
        "resource": ("Redis Docs", "https://redis.io/docs/latest/")
    },
    "celery": {
        "prep": ["Task queues and message brokers (RabbitMQ/Redis)", "Asynchronous workers & event loops", "Celery chord, group, & chain workflows"],
        "cert": "Python Celery Specialist",
        "resource": ("Celery Documentation", "https://docs.celeryq.dev/")
    },
    "terraform": {
        "prep": ["Infrastructure as Code (IaC) principles", "Terraform state files & locking", "Modules, input/output variables, & workspace"],
        "cert": "HashiCorp Certified: Terraform Associate",
        "resource": ("Terraform Docs", "https://developer.hashicorp.com/terraform/docs")
    },
    "ci/cd": {
        "prep": ["Build, Test, and Deploy pipelines", "GitHub Actions workflows & runners", "Automated release management & semantic versioning"],
        "cert": "GitHub Actions Certification",
        "resource": ("GitHub Actions Docs", "https://docs.github.com/actions")
    },
    "system design": {
        "prep": ["Horizontal vs Vertical Scaling", "Load balancing algorithms & reverse proxies", "Sharding & Replication patterns"],
        "cert": "Senior Architect System Design",
        "resource": ("System Design Primer", "https://github.com/donnemartin/system-design-primer")
    },
    "java": {
        "prep": ["Garbage Collection tuning & JVM internals", "Multithreading & Concurrency Utilities", "Spring Framework & Dependency Injection"],
        "cert": "Oracle Certified Professional: Java SE Developer",
        "resource": ("Oracle Java Documentation", "https://docs.oracle.com/en/java/")
    },
    "spring boot": {
        "prep": ["Spring Boot Auto-configuration & Starter modules", "Spring Data JPA & Hibernate ORM", "Spring Security & OAuth2 JWT integration"],
        "cert": "Spring Certified Professional",
        "resource": ("Spring Boot Reference", "https://spring.io/projects/spring-boot")
    },
    "go": {
        "prep": ["Goroutines, Channels & CSP Concurrency", "Interfaces & Duck Typing", "Memory management & Garbage Collector"],
        "cert": "Google Go Certified Developer",
        "resource": ("Go Documentation", "https://go.dev/doc/")
    },
    "django": {
        "prep": ["Django ORM & QuerySet optimization", "Authentication, Sessions & Middleware", "REST Framework (DRF) Serializers & Views"],
        "cert": "Django Software Foundation Certified",
        "resource": ("Django Docs", "https://docs.djangoproject.com/")
    },
    "express": {
        "prep": ["Middleware pipeline & error handling", "Route handlers & controllers", "Security headers (Helmet) & Rate limiting"],
        "cert": "OpenJS Node.js Application Developer",
        "resource": ("Express Docs", "https://expressjs.com/")
    },
    "mongodb": {
        "prep": ["Aggregation Framework & Pipelines", "Indexing strategies (Compound, Text, Geospatial)", "Sharding & Replica sets"],
        "cert": "MongoDB Certified Developer Associate",
        "resource": ("MongoDB Docs", "https://www.mongodb.com/docs/")
    }
}


class RecommendationService:
    OPENROUTER_TIMEOUT = 60.0

    def _section_content(self, sections: Dict[str, Any], name: str) -> str:
        section = sections.get(name, {}) if isinstance(sections, dict) else {}
        if isinstance(section, dict):
            return str(section.get("content", "") or "").strip()
        return ""

    def _coerce_text(self, value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, str):
            return value.strip()
        return str(value).strip()

    def _normalize_list(self, value: Any) -> List[Any]:
        if not isinstance(value, list):
            return []
        return [item for item in value if item not in (None, "", [], {})]

    def _skill_resource(self, skill: str) -> LearningResource:
        skill_lower = skill.lower().strip()
        if skill_lower in TECH_MAP:
            name, url = TECH_MAP[skill_lower]["resource"]
            return LearningResource(skill=skill, resource_name=name, resource_url=url)
        return LearningResource(
            skill=skill,
            resource_name=f"{skill} Docs",
            resource_url=f"https://www.google.com/search?q={skill}+official+documentation"
        )

    def _extract_json_payload(self, text: str) -> Dict[str, Any]:
        if not text:
            raise ValueError("Empty OpenRouter response content")

        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r"\s*```$", "", cleaned)

        first_brace = cleaned.find("{")
        last_brace = cleaned.rfind("}")
        if first_brace != -1 and last_brace != -1:
            cleaned = cleaned[first_brace:last_brace + 1]

        payload = json.loads(cleaned)
        if not isinstance(payload, dict):
            raise ValueError("OpenRouter response was not a JSON object")
        return payload

    def _build_llm_context(
        self,
        missing_skills: List[str],
        structure: Dict[str, Any],
        formatting: Dict[str, Any],
        contact: Dict[str, Any],
        target_title: str,
        analysis_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        context = analysis_context or {}
        sections = context.get("sections", {}) or {}

        project_analysis = self._normalize_list(context.get("project_analysis", []))
        experience_analysis = self._normalize_list(context.get("experience_analysis", []))

        return {
            "target_job_title": target_title,
            "overall_match_score": context.get("overall_match", 0),
            "resume_summary": self._coerce_text(context.get("summary_text", "") or self._section_content(sections, "summary")),
            "extracted_skills": self._normalize_list(context.get("existing_skills", [])),
            "missing_skills": self._normalize_list(missing_skills),
            "strengths": self._normalize_list(context.get("strengths", [])),
            "weaknesses": self._normalize_list(context.get("weaknesses", [])),
            "projects": project_analysis,
            "experience": experience_analysis,
            "education": self._coerce_text(context.get("education_text", "") or self._section_content(sections, "education")),
            "certifications": self._coerce_text(context.get("certifications_text", "") or self._section_content(sections, "certifications")),
            "achievements": self._coerce_text(context.get("achievements_text", "") or self._section_content(sections, "achievements")),
            "resume_structure": structure,
            "formatting_analysis": formatting,
            "contact_analysis": contact,
            "ats_analysis": context.get("ats_analysis", {
                "structure_score": structure.get("score") if isinstance(structure, dict) else None,
                "formatting_score": formatting.get("score") if isinstance(formatting, dict) else None,
                "formatting_issues": self._normalize_list(formatting.get("issues", [])) if isinstance(formatting, dict) else [],
                "missing_sections": self._normalize_list(structure.get("missing_sections", [])) if isinstance(structure, dict) else [],
            }),
        }

    def _build_llm_prompt(self, context_snapshot: Dict[str, Any]) -> Tuple[str, str]:
        system_prompt = (
            "You are a Senior Technical Recruiter and Senior Software Architect. "
            "Analyze the candidate's resume snapshot against the target job title. "
            "Every recommendation MUST reference actual resume evidence. "
            "Never generate generic advice. Never invent experiences or skills. "
            "Return valid JSON only without markdown formatting."
        )

        user_prompt = f"""
Analyze the candidate's resume snapshot against target job title '{context_snapshot.get('target_job_title')}'.

Return a JSON object with EXACTLY these keys:
{{
  "recruiter_review": {{
    "feedback": "Detailed recruiter-style feedback referencing candidate resume evidence.",
    "strengths": ["Key candidate strengths backed by resume evidence"],
    "concerns": ["Key candidate gaps compared to target role"],
    "decision": "Strong Hire / Hire / Consider / Needs Improvement / Reject",
    "readiness": "Interview readiness assessment."
  }},
  "summary": {{
    "status": "strong / weak",
    "review": "Review of current profile summary.",
    "better_wording": "A recommended rewrite of the summary tailored to the target role.",
    "missing_keywords": ["Target job keywords missing from summary"],
    "alignment": "Suggestions for role alignment.",
    "readability": "Suggestions for conciseness and impact."
  }},
  "projects": [
    {{
      "project_name": "Exact project title from resume",
      "strengths": "Observed strengths in this project",
      "weaknesses": "Observed gaps in this project description",
      "missing_business_impact": "Business value/impact to emphasize",
      "missing_metrics": "Quantifiable metrics to add (e.g. latency, user count)",
      "deployment_improvements": "Deployment suggestions (Docker, AWS, Vercel)",
      "architecture_improvements": "Architectural enhancements (MVC, microservices)",
      "testing_improvements": "Testing improvements (Jest, PyTest)",
      "documentation_improvements": "README or API documentation improvements",
      "portfolio_improvements": "GitHub or live demo link improvements",
      "security_improvements": "Security improvements (JWT, HTTPS, CORS)",
      "performance_improvements": "Performance suggestions (Caching, indexing)",
      "priority": "High / Medium / Low"
    }}
  ],
  "experience": [
    {{
      "role": "Role title from resume",
      "company": "Company name from resume",
      "action_verbs": "Stronger action verbs to use",
      "quantified_achievements": "Quantified achievement suggestions",
      "technical_wording": "Better technical terms and tools to mention",
      "business_impact": "How to articulate business impact",
      "ownership": "How to highlight end-to-end ownership"
    }}
  ],
  "skills": [
    {{
      "skill": "Name of missing skill",
      "learning_priority": "High / Medium / Low",
      "difficulty": "Beginner / Intermediate / Advanced",
      "estimated_learning_time": "Estimated time (e.g., 2 weeks)",
      "reason": "Why this skill is required for the target role"
    }}
  ],
  "education": {{
    "has_improvements": true/false,
    "evidence": "Education evidence from resume",
    "recommendation": "Suggested improvements or explanation why no improvements are required"
  }},
  "certifications": {{
    "has_improvements": true/false,
    "evidence": "Certifications evidence",
    "recommendations": ["Advanced certifications worth targeting"]
  }},
  "achievements": {{
    "evidence": "Achievements evidence",
    "stronger_wording": "Stronger verb framing suggestions",
    "measurable_presentation": "Measurable presentation suggestions"
  }},
  "ats": {{
    "keywords": ["Missing ATS keywords"],
    "section_ordering": ["Recommended section sequence"],
    "bullet_formatting": ["Formatting rules for ATS readability"],
    "ats_compatibility": "ATS compatibility summary"
  }},
  "interview_preparation": [
    {{
      "skill": "Detected skill name ONLY",
      "recommendations": ["Core interview topics to prepare"]
    }}
  ],
  "learning_roadmap": {{
    "plan_7_days": ["Actionable goals for Day 1-7"],
    "plan_30_days": ["Actionable goals for Day 8-30"],
    "plan_60_days": ["Actionable goals for Day 31-60"],
    "plan_90_days": ["Actionable goals for Day 61-90"]
  }},
  "top_action_plan": [
    {{
      "priority": "High / Medium / Low",
      "reason": "Why this action is critical",
      "recommendation": "Concrete action step",
      "expected_benefit": "Quantified benefit",
      "estimated_time": "Estimated effort time"
    }}
  ],
  "cards": [
    {{
      "id": "rec-1",
      "title": "Title of recommendation",
      "category": "Projects / Summary / Experience / Skills / ATS / Education / Certifications / Achievements / Structure / Formatting",
      "priority": "High / Medium / Low",
      "reason": "Reason for recommendation",
      "resume_evidence": "Resume evidence snippet",
      "recommendation": "Actionable recommendation details",
      "expected_benefit": "Expected benefit"
    }}
  ]
}}

Snapshot:
{json.dumps(context_snapshot, indent=2)}
"""
        return system_prompt, user_prompt

    def _call_openrouter_recommendations(self, context_snapshot: Dict[str, Any]) -> Dict[str, Any]:
        if not settings.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
        if not settings.openrouter_model:
            raise ValueError("OPENROUTER_MODEL environment variable not set")

        system_prompt, user_prompt = self._build_llm_prompt(context_snapshot)
        payload = {
            "model": settings.openrouter_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
            "max_tokens": 4000,
        }

        headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "RoleMatch AI",
        }

        with httpx.Client(timeout=httpx.Timeout(self.OPENROUTER_TIMEOUT, connect=10.0)) as client:
            response = client.post(settings.openrouter_url, headers=headers, json=payload)
            response.raise_for_status()
            response_json = response.json()

        choices = response_json.get("choices", []) if isinstance(response_json, dict) else []
        if not choices:
            raise ValueError("OpenRouter response did not contain any choices")

        message = choices[0].get("message", {}) if isinstance(choices[0], dict) else {}
        content = message.get("content", "") if isinstance(message, dict) else ""
        return self._extract_json_payload(content)

    def generate_fallback_recommendations(
        self,
        missing_skills: List[str],
        structure: Dict[str, Any],
        formatting: Dict[str, Any],
        contact: Dict[str, Any],
        target_title: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        overall_match = float(context.get("overall_match", 0.0) or 0.0)
        existing_skills = context.get("existing_skills", []) or []
        projects = context.get("project_analysis", []) or []
        experience = context.get("experience_analysis", []) or []

        detected_skills_str = ", ".join(existing_skills[:5]) if existing_skills else "software development"
        missing_skills_str = ", ".join(missing_skills[:3]) if missing_skills else "advanced deployment and monitoring"

        # 1. Recruiter Review
        decision = "Consider"
        if overall_match >= 85:
            decision = "Strong Hire"
        elif overall_match >= 70:
            decision = "Hire"
        elif overall_match >= 50:
            decision = "Consider"
        elif overall_match >= 35:
            decision = "Needs Improvement"
        else:
            decision = "Reject"

        recruiter_feedback = (
            f"Candidate demonstrates functional proficiency in {detected_skills_str}. "
            f"To reach candidate excellence for target role '{target_title}', the resume must directly address gaps in {missing_skills_str} "
            f"and incorporate quantified business impact in project descriptions."
        )

        strengths = context.get("strengths", []) or [f"Active experience utilizing {detected_skills_str}"]
        concerns = context.get("weaknesses", []) or [f"Missing target skill requirements: {missing_skills_str}"]

        recruiter_review = {
            "feedback": recruiter_feedback,
            "strengths": strengths,
            "concerns": concerns,
            "decision": decision,
            "readiness": f"Interview readiness rated at {round(overall_match)}%. Immediate target skill bridge recommended."
        }

        # 2. Summary
        summary_text = context.get("summary_text", "")
        summary_status = "strong" if (summary_text and len(summary_text.split()) >= 15) else "weak"

        better_wording = (
            f"Results-driven Software Professional with proficiency in {detected_skills_str}. "
            f"Proven track record building and deploying web applications. "
            f"Targeting a {target_title} role to engineer scalable backend services, optimize frontend performance, and deliver measurable business value."
        ) if not summary_text else (
            f"Refine summary for {target_title} role: 'Senior-focused Developer specializing in {detected_skills_str}. "
            f"Demonstrated success delivering production applications, looking to advance systems engineering as a {target_title}.'"
        )

        summary_data = {
            "status": summary_status,
            "review": "Summary requires stronger role-targeted keywords and quantified metrics." if summary_status == "weak" else "Summary is present but can better align with target job title keywords.",
            "better_wording": better_wording,
            "missing_keywords": missing_skills[:4],
            "alignment": f"Explicitly include '{target_title}' in your opening summary sentence to immediately pass ATS keyword filters.",
            "readability": "Structure into 3 concise sentences focusing on core stack, major achievements, and career target."
        }

        # 3. Projects (Evaluate EVERY project)
        project_recs = []
        if not projects:
            project_recs.append({
                "project_name": "No projects listed",
                "strengths": "N/A",
                "weaknesses": "Resume lacks a dedicated projects section.",
                "missing_business_impact": "Explain real-world user problems solved by your builds.",
                "missing_metrics": "Include numbers such as database size, API latency reduction, or user adoption count.",
                "deployment_improvements": "Add containerization (Docker) and host on AWS/Vercel with automated GitHub Actions CI/CD pipelines.",
                "architecture_improvements": "Highlight system architecture (e.g., MVC, RESTful Microservices, Event-driven).",
                "testing_improvements": "Incorporate unit and integration test suites using PyTest or Jest with >80% coverage.",
                "documentation_improvements": "Provide comprehensive README.md files with setup commands and API endpoints.",
                "portfolio_improvements": "Include public GitHub repository links and live working URL demos.",
                "security_improvements": "Detail authentication mechanisms like OAuth2 JWT, HTTP-only cookies, and rate limiting.",
                "performance_improvements": "Highlight Redis caching, database indexing, and query optimization.",
                "priority": "High"
            })
        else:
            for idx, p in enumerate(projects):
                p_name = p.get("title") or p.get("project_name") or f"Project #{idx + 1}"
                techs = p.get("technologies") or []
                techs_str = ", ".join(techs) if techs else "core technologies"

                project_recs.append({
                    "project_name": p_name,
                    "strengths": f"Demonstrates hands-on software development experience using {techs_str}.",
                    "weaknesses": "Lacks production operational details and concrete business impact metrics.",
                    "missing_business_impact": f"Specify how {p_name} created value for users or streamlined engineering workflows.",
                    "missing_metrics": "Add concrete figures (e.g., 'served 500+ requests/sec', 'reduced DB query latency by 40%').",
                    "deployment_improvements": "Detail hosting setup (e.g. Docker containerization, AWS EC2/Lambda, or Vercel deployment).",
                    "architecture_improvements": "State exact architecture patterns used (e.g. REST API, Layered Architecture, Microservices).",
                    "testing_improvements": "Specify automated testing tools used (e.g., PyTest, Jest, Cypress) to demonstrate code quality.",
                    "documentation_improvements": "Mention inclusion of API documentation (Swagger/OpenAPI) and setup guidelines.",
                    "portfolio_improvements": "Add direct clickable links to public GitHub repo and live demo URL.",
                    "security_improvements": "Mention security practices: input validation, JWT token rotation, HTTPS, and CORS policies.",
                    "performance_improvements": "Describe backend performance gains achieved via Redis caching, async I/O, or DB indexing.",
                    "priority": "High" if idx == 0 else "Medium"
                })

        # 4. Experience (Evaluate EVERY experience entry)
        exp_recs = []
        if not experience:
            exp_recs.append({
                "role": "No work experience listed",
                "company": "N/A",
                "action_verbs": "Use strong technical action verbs such as 'Architected', 'Engineered', 'Developed', and 'Optimized'.",
                "quantified_achievements": "Quantify outcomes with percentages and metrics (e.g., 'improved page load by 35%').",
                "technical_wording": "Detail frameworks, cloud infrastructure, and database engines used daily.",
                "business_impact": "Connect technical tasks to business ROI and user growth metrics.",
                "ownership": "Emphasize full end-to-end feature ownership from requirement specs to production deploy."
            })
        else:
            for e in experience:
                role = e.get("title") or e.get("role") or "Software Engineering Experience"
                company = e.get("company") or "Organization"
                exp_recs.append({
                    "role": role,
                    "company": company,
                    "action_verbs": "Replace passive verbs ('assisted with', 'worked on') with powerful engineering verbs ('Architected', 'Spearheaded', 'Engineered').",
                    "quantified_achievements": f"Add quantitative results for {role} (e.g., 'reduced API latency by 25%', 'automated deployments saving 8 hours weekly').",
                    "technical_wording": "Explicitly state engineering stack details (e.g. REST endpoints, SQL query optimization, CI/CD pipelines).",
                    "business_impact": "Explain how your engineering deliverables directly improved team velocity, system uptime, or client satisfaction.",
                    "ownership": "Highlight your role as primary owner of features or services across the software lifecycle."
                })

        # 5. Skills Gaps
        skills_recs = []
        for idx, s in enumerate(missing_skills[:6]):
            s_lower = s.lower().strip()
            diff = "Intermediate"
            est_time = "2-3 weeks"
            if any(term in s_lower for term in ["kubernetes", "docker", "aws", "cloud", "system design", "microservices"]):
                diff = "Advanced"
                est_time = "3-4 weeks"
            elif any(term in s_lower for term in ["css", "html", "git", "json"]):
                diff = "Beginner"
                est_time = "1 week"

            skills_recs.append({
                "skill": s,
                "learning_priority": "High" if idx < 2 else ("Medium" if idx < 4 else "Low"),
                "difficulty": diff,
                "estimated_learning_time": est_time,
                "reason": f"Required tool to meet qualification criteria for '{target_title}' positions."
            })
        if not skills_recs:
            skills_recs.append({
                "skill": "High-Scale Distributed Systems Design",
                "learning_priority": "Low",
                "difficulty": "Advanced",
                "estimated_learning_time": "4 weeks",
                "reason": "Core skills are well covered. Distributed systems design review will elevate candidate seniority."
            })

        # 6. Education
        edu_text = context.get("education_text", "")
        missing_sections = structure.get("missing_sections", []) if isinstance(structure, dict) else []
        edu_missing = "education" in missing_sections or not edu_text

        education_data = {
            "has_improvements": edu_missing,
            "evidence": "No education details detected." if edu_missing else (edu_text[:120] if len(edu_text) > 120 else edu_text),
            "recommendation": "Add formal degree, institution name, major, and graduation year." if edu_missing else "Education details are clear and formatted properly. No further improvements required."
        }

        # 7. Certifications
        cert_text = context.get("certifications_text", "")
        cert_missing = "certifications" in missing_sections or not cert_text

        target_lower = target_title.lower()
        if "devops" in target_lower or "cloud" in target_lower or "infrastructure" in target_lower:
            cert_recs = ["Certified Kubernetes Administrator (CKA)", "AWS Certified Solutions Architect - Associate"]
        elif "frontend" in target_lower or "react" in target_lower:
            cert_recs = ["Meta Front-End Developer Professional Certificate", "Vercel Certified Next.js Developer"]
        elif "data" in target_lower or "ai" in target_lower:
            cert_recs = ["AWS Certified Data Analytics", "TensorFlow Developer Certificate"]
        else:
            cert_recs = ["AWS Certified Developer - Associate", "Meta Back-End Developer Professional Certificate"]

        certifications_data = {
            "has_improvements": cert_missing,
            "evidence": "No professional certifications detected." if cert_missing else (cert_text[:120] if len(cert_text) > 120 else cert_text),
            "recommendations": cert_recs
        }

        # 8. Achievements
        ach_text = context.get("achievements_text", "")
        ach_missing = "achievements" in missing_sections or not ach_text

        achievements_data = {
            "evidence": "No achievements section detected." if ach_missing else (ach_text[:120] if len(ach_text) > 120 else ach_text),
            "stronger_wording": "Highlight competitive rankings, hackathons, or engineering milestones (e.g. 'Awarded Top Developer 2024').",
            "measurable_presentation": "Quantify achievement outcomes (e.g. 'Outperformed 50+ competing teams to secure 1st place')."
        }

        # 9. ATS Analysis
        ats_data = {
            "keywords": missing_skills[:6] if missing_skills else ["System Architecture", "Unit Testing", "CI/CD"],
            "section_ordering": [
                "1. Header & Contact Information",
                "2. Professional Summary",
                "3. Technical Skills",
                "4. Professional Experience",
                "5. Projects",
                "6. Education & Certifications"
            ],
            "bullet_formatting": [
                "Use bullet points starting with strong action verbs.",
                "Avoid graphic tables, multi-column text frames, or non-standard symbols.",
                "Keep bullet lengths between 1 and 2 lines max for optimal parsing."
            ],
            "ats_compatibility": "Resume structure is parseable but requires key technical terms added to project descriptions."
        }

        # 10. Interview Preparation (Based ONLY on detected skills)
        interview_prep = []
        for s in existing_skills:
            s_lower = s.lower().strip()
            if s_lower in TECH_MAP:
                interview_prep.append({
                    "skill": s,
                    "recommendations": TECH_MAP[s_lower]["prep"]
                })
            else:
                interview_prep.append({
                    "skill": s,
                    "recommendations": [
                        f"{s} Core Concepts & Architecture",
                        f"Best practices and common design patterns in {s}",
                        f"Performance optimization & debugging techniques in {s}"
                    ]
                })

        interview_prep = interview_prep[:6]
        if not interview_prep:
            interview_prep.append({
                "skill": "Software Engineering Fundamentals",
                "recommendations": ["Data Structures & Algorithms", "System Design Patterns", "Object-Oriented Programming"]
            })

        # 11. Learning Roadmap
        ms_1 = missing_skills[0] if len(missing_skills) > 0 else "Cloud Architecture"
        ms_2 = missing_skills[1] if len(missing_skills) > 1 else "Docker & Containerization"
        ms_3 = missing_skills[2] if len(missing_skills) > 2 else "Automated Testing Frameworks"

        learning_roadmap = {
            "plan_7_days": [
                f"Study fundamentals and documentation for {ms_1}.",
                f"Build a standalone hello-world project utilizing {ms_1}."
            ],
            "plan_30_days": [
                f"Integrate {ms_1} into your primary project portfolio codebase.",
                f"Begin learning {ms_2} and configure basic development environment."
            ],
            "plan_60_days": [
                f"Implement {ms_2} containerization and configure multi-stage builds.",
                f"Add automated test suites using {ms_3} with continuous integration."
            ],
            "plan_90_days": [
                f"Deploy complete application stack featuring {ms_1} and {ms_2} to cloud infrastructure.",
                "Publish project to GitHub with live demo URL and update resume experience bullets."
            ]
        }

        # 12. Top Action Plan (Top 10 items sorted by impact)
        top_action_plan = [
            {
                "priority": "High",
                "reason": "Profile summary is the first section evaluated by recruiters and ATS parsers.",
                "recommendation": f"Rewrite profile summary to explicitly target '{target_title}', featuring skills in {detected_skills_str}.",
                "expected_benefit": "Increases immediate role match relevance score by up to 25%.",
                "estimated_time": "45 mins"
            },
            {
                "priority": "High",
                "reason": f"Missing core technical skill requirement: {ms_1}.",
                "recommendation": f"Complete targeted learning and build a functional project module using {ms_1}.",
                "expected_benefit": "Fulfills hard ATS filter criteria for {target_title} job postings.",
                "estimated_time": "3 days"
            },
            {
                "priority": "High",
                "reason": "Project descriptions lack measurable business impact metrics.",
                "recommendation": "Add quantifiable metrics to every project (e.g. latency numbers, database scaling, active users).",
                "expected_benefit": "Demonstrates engineering competence and production readiness.",
                "estimated_time": "2 hours"
            },
            {
                "priority": "Medium",
                "reason": "Experience bullets utilize passive activity verbs.",
                "recommendation": "Transform experience descriptions using strong action verbs ('Architected', 'Engineered', 'Optimized').",
                "expected_benefit": "Elevates candidate perceived seniority during hiring manager reviews.",
                "estimated_time": "2 hours"
            },
            {
                "priority": "Medium",
                "reason": f"Missing secondary technical skill requirement: {ms_2}.",
                "recommendation": f"Add Docker container configurations and CI/CD pipelines incorporating {ms_2}.",
                "expected_benefit": "Demonstrates modern DevOps and deployment proficiency.",
                "estimated_time": "2 days"
            },
            {
                "priority": "Medium",
                "reason": "Projects lack public code repository links or live links.",
                "recommendation": "Add public GitHub repository URLs and live working demo links to all listed projects.",
                "expected_benefit": "Provides verifiable proof of engineering work to hiring recruiters.",
                "estimated_time": "1 hour"
            },
            {
                "priority": "Medium",
                "reason": "ATS keyword density in project bullet points is low.",
                "recommendation": f"Incorporate target job terms ({', '.join(missing_skills[:3])}) directly into project descriptions.",
                "expected_benefit": "Passes automated resume screeners with high keyword alignment.",
                "estimated_time": "1.5 hours"
            },
            {
                "priority": "Low",
                "reason": "Testing frameworks are not explicitly specified in project stack.",
                "recommendation": "Add automated unit testing details (e.g., PyTest, Jest) to project tech stacks.",
                "expected_benefit": "Proves dedication to software reliability and code quality standards.",
                "estimated_time": "3 hours"
            },
            {
                "priority": "Low",
                "reason": "No specialized role-specific certification listed.",
                "recommendation": f"Target industry-recognized certification: {cert_recs[0]}.",
                "expected_benefit": "Validates expertise for candidate qualification reviews.",
                "estimated_time": "2 weeks"
            },
            {
                "priority": "Low",
                "reason": "Formatting consistency and section ordering optimization.",
                "recommendation": "Standardize bullet points, remove non-standard icons, and use single-column layout.",
                "expected_benefit": "Ensures 100% clean parsing across all commercial ATS engines.",
                "estimated_time": "30 mins"
            }
        ]

        # 13. Recommendation Cards (Exact schema with id, title, category, priority, reason, resume_evidence, recommendation, expected_benefit)
        p_first = projects[0].get("title", "Full-Stack Project") if projects else "Projects section"
        cards = [
            {
                "id": "rec-1",
                "title": "Improve Project Impact",
                "category": "Projects",
                "priority": "High",
                "reason": "Your projects describe technologies but do not mention measurable impact.",
                "resume_evidence": f"\"{p_first}\" describes features without numerical scale or performance metrics.",
                "recommendation": "Mention number of users, API requests handled, database scale, and latency improvements achieved.",
                "expected_benefit": "Recruiters can understand the business value and engineering scale of your project."
            },
            {
                "id": "rec-2",
                "title": f"Align Profile Summary for '{target_title}'",
                "category": "Summary",
                "priority": "High",
                "reason": f"Profile summary does not explicitly target the '{target_title}' position.",
                "resume_evidence": f"\"{summary_text[:75]}\"" if summary_text else "No profile summary section detected in parsed resume.",
                "recommendation": f"Rewrite summary to state: 'Results-driven developer proficient in {detected_skills_str}, targeting a {target_title} role.'",
                "expected_benefit": "Dramatically improves first-stage recruiter review relevance and ATS matching."
            },
            {
                "id": "rec-3",
                "title": f"Bridge Core Technical Skill Gap: {ms_1}",
                "category": "Skills",
                "priority": "High",
                "reason": f"Missing critical technical skill requirement: {ms_1}.",
                "resume_evidence": f"Target role '{target_title}' requires {ms_1}, which was not detected in parsed skills.",
                "recommendation": f"Study {ms_1} fundamentals and build a functional project module showcasing its implementation.",
                "expected_benefit": "Satisfies mandatory ATS keyword checks and screening criteria."
            },
            {
                "id": "rec-4",
                "title": "Quantify Internship & Work Experience",
                "category": "Experience",
                "priority": "Medium",
                "reason": "Experience bullets describe passive daily duties rather than technical wins.",
                "resume_evidence": f"Experience entry at '{experience[0].get('company', 'Company')}' uses generic task descriptions." if experience else "Experience section uses passive task verbs.",
                "recommendation": "Start bullet points with strong action verbs ('Architected', 'Spearheaded', 'Engineered') and quantify results.",
                "expected_benefit": "Enhances candidate positioning during hiring manager evaluation."
            },
            {
                "id": "rec-5",
                "title": "Optimize ATS Keyword Density",
                "category": "ATS",
                "priority": "Medium",
                "reason": f"Resume lacks sufficient term density for target role '{target_title}'.",
                "resume_evidence": f"Missing required terms: {', '.join(missing_skills[:4])}",
                "recommendation": "Weave target technical keywords naturally throughout project descriptions and skill sections.",
                "expected_benefit": "Maximizes resume screening match score across commercial ATS parsers."
            },
            {
                "id": "rec-6",
                "title": "Add Containerization & Deployment Details",
                "category": "Projects",
                "priority": "Medium",
                "reason": "Projects lack clear deployment hosting and containerization specifications.",
                "resume_evidence": "Project descriptions do not state hosting platforms or CI/CD pipelines.",
                "recommendation": "Add Docker container configurations and host links (AWS, Vercel, Netlify) with GitHub URLs.",
                "expected_benefit": "Demonstrates end-to-end full-lifecycle software delivery capability."
            },
            {
                "id": "rec-7",
                "title": "Acquire Specialized Industry Certification",
                "category": "Certifications",
                "priority": "Low",
                "reason": "No specialized role-targeted certification detected on candidate profile.",
                "resume_evidence": cert_text[:80] if cert_text else "No professional certifications section detected.",
                "recommendation": f"Target industry-recognized certification: {cert_recs[0]}.",
                "expected_benefit": "Provides verified proof of technical authority for qualification reviews."
            },
            {
                "id": "rec-8",
                "title": "Standardize Education & Layout Formatting",
                "category": "Education",
                "priority": "Low",
                "reason": "Education and layout formatting can be optimized for automated parsing engines.",
                "resume_evidence": education_data["evidence"],
                "recommendation": education_data["recommendation"],
                "expected_benefit": "Ensures 100% clean data extraction without text truncation."
            }
        ]

        if not cards:
            cards.append({
                "id": "rec-0",
                "title": "Resume looks good",
                "category": "General",
                "priority": "Low",
                "reason": "No significant improvements detected.",
                "resume_evidence": "All key resume sections and skills align well.",
                "recommendation": "Continue updating your resume as you gain more experience.",
                "expected_benefit": "Keeps the resume current."
            })

        return {
            "recruiter_review": recruiter_review,
            "summary": summary_data,
            "projects": project_recs,
            "experience": exp_recs,
            "skills": skills_recs,
            "education": education_data,
            "certifications": certifications_data,
            "achievements": achievements_data,
            "ats": ats_data,
            "interview_preparation": interview_prep,
            "learning_roadmap": learning_roadmap,
            "top_action_plan": top_action_plan,
            "cards": cards
        }

    def generate_recommendations(
        self,
        missing_skills: List[str],
        structure: Dict[str, Any],
        formatting: Dict[str, Any],
        contact: Dict[str, Any],
        target_title: str,
        analysis_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        context = analysis_context or {}
        overall_match = float(context.get("overall_match", 0.0) or 0.0)

        # Prepare context snapshot for LLM
        context_snapshot = self._build_llm_context(
            missing_skills=missing_skills,
            structure=structure,
            formatting=formatting,
            contact=contact,
            target_title=target_title,
            analysis_context=context,
        )

        recommendation_data = None

        # 1. Try LLM Call if key available
        if settings.openrouter_api_key:
            try:
                recommendation_data = self._call_openrouter_recommendations(context_snapshot)
                logger.info("Successfully generated AI recommendations via OpenRouter.")
            except Exception as exc:
                logger.warning("OpenRouter recommendations failed: %s. Falling back to rule-based engine.", exc)
        else:
            logger.info("No OpenRouter API key found. Using rule-based recommendation generator.")

        # 2. Use Fallback if LLM failed or key missing
        if not recommendation_data:
            recommendation_data = self.generate_fallback_recommendations(
                missing_skills=missing_skills,
                structure=structure,
                formatting=formatting,
                contact=contact,
                target_title=target_title,
                context=context
            )

        # Ensure cards is never empty
        if not recommendation_data.get("cards"):
            recommendation_data["cards"] = [{
                "id": "rec-0",
                "title": "Resume looks good",
                "category": "General",
                "priority": "Low",
                "reason": "No significant improvements detected.",
                "resume_evidence": "All key resume sections and skills align well.",
                "recommendation": "Continue updating your resume as you gain more experience.",
                "expected_benefit": "Keeps the resume current."
            }]

        # 3. Format outputs matching AnalysisResponse schema
        keyword_recommendations = []
        if recommendation_data.get("ats") and recommendation_data["ats"].get("keywords"):
            keyword_recommendations = [str(k) for k in recommendation_data["ats"]["keywords"]]
        else:
            keyword_recommendations = missing_skills[:6]

        # Put full JSON payload inside first element of improvement_suggestions list
        improvement_suggestions = [json.dumps(recommendation_data, ensure_ascii=True)]

        # Convert skills learning roadmap back to LearningResource schema list
        learning_recommendations: List[LearningResource] = []
        seen = set()

        if recommendation_data.get("skills"):
            for item in recommendation_data["skills"]:
                skill = item.get("skill")
                if skill:
                    key = skill.lower().strip()
                    if key not in seen:
                        seen.add(key)
                        learning_recommendations.append(self._skill_resource(skill))

        for skill in missing_skills:
            if len(learning_recommendations) >= 4:
                break
            key = skill.lower().strip()
            if key not in seen:
                seen.add(key)
                learning_recommendations.append(self._skill_resource(skill))

        if not learning_recommendations:
            for d_skill in ["System Design", "React", "FastAPI"]:
                learning_recommendations.append(self._skill_resource(d_skill))

        # Suitable job roles mapping
        target_lower = target_title.lower()
        if "full stack" in target_lower:
            suitable_job_roles = ["Full Stack Developer", "Senior Full Stack Engineer", "Backend Engineer", "Frontend Engineer"]
        elif "backend" in target_lower:
            suitable_job_roles = ["Backend Engineer", "Platform Engineer", "API Developer", "Systems Architect"]
        elif "frontend" in target_lower or "react" in target_lower:
            suitable_job_roles = ["Frontend Engineer", "UI Engineer", "Full Stack Developer"]
        elif "devops" in target_lower or "cloud" in target_lower:
            suitable_job_roles = ["DevOps Engineer", "Platform Engineer", "Cloud Engineer"]
        else:
            suitable_job_roles = [target_title, "Full Stack Developer", "Backend Engineer"]

        if overall_match >= 85 and "Senior Full Stack Engineer" not in suitable_job_roles:
            suitable_job_roles.insert(1, "Senior Full Stack Engineer")

        return {
            "keyword_recommendations": keyword_recommendations,
            "improvement_suggestions": improvement_suggestions,
            "learning_recommendations": learning_recommendations[:4],
            "suitable_job_roles": suitable_job_roles,
        }