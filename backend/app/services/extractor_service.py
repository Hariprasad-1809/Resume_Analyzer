import re
from datetime import datetime

class ExtractorService:
    def normalize_text(self, text: str) -> str:
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        text = text.replace('\u2013', '-').replace('\u2014', '-').replace('\u2018', "'").replace('\u2019', "'")
        text = re.sub(r'[\u2022\u25cf\u25cb\u25aa\u25ab\u25b6\u25c6\ufffd\uf0b7]', '-', text)
        return text

    def clean_heading_line(self, line: str) -> str:
        line = re.sub(r'[\xa0\u200b\u200c\u200d\ufeff]', ' ', line)
        line = re.sub(r'\s+', ' ', line).strip()
        line = re.sub(r'^[•\-\*\u2022\u25cf\u25cb\u25aa\u25ab\u25b6\u25c6\ufffd\uf0b7\s]+', '', line)
        line = re.sub(r'^[0-9]+[\.\u2022\-\s]+', '', line)
        line = re.sub(r'[:#\*_\-\s]+$', '', line)
        return line.strip().lower()

    def extract_sections(self, text: str) -> dict:
        normalized_text = self.normalize_text(text)
        
        header_mapping = {
            "education": ["education", "academic background", "academic qualification", "qualification", "qualifications", "academic", "academic credentials", "academic profile"],
            "experience": ["experience", "work experience", "professional experience", "employment", "internship", "career history", "work history", "employment history"],
            "projects": ["projects", "personal projects", "academic projects", "portfolio", "selected projects", "key projects"],
            "skills": ["skills", "technical skills", "technologies", "technology stack", "competencies", "technical expertise", "tech stack", "toolbox", "skills & tools"],
            "certifications": ["certifications", "certification", "courses", "professional certifications", "licenses", "certificates", "credentials", "certifications & licenses"],
            "achievements": ["achievements", "awards", "honors", "accomplishments", "recognition"],
            "summary": ["summary", "profile", "profile summary", "professional summary", "career objective", "objective", "about", "about me", "personal statement"],
            "languages": ["languages", "spoken languages", "language proficiency", "language skills"]
        }
        
        lines = normalized_text.split("\n")
        char_index = 0
        line_mappings = []
        for line in lines:
            line_len = len(line)
            line_mappings.append({
                "text": line,
                "start": char_index,
                "end": char_index + line_len
            })
            char_index += line_len + 1

        found_sections = []
        for line_info in line_mappings:
            line_text = line_info["text"]
            
            trimmed_orig = line_text.strip()
            if trimmed_orig.startswith(("-", "*", "•", "Technologies:")):
                continue
                
            clean = self.clean_heading_line(line_text)
            if not clean:
                continue
                
            if len(clean.split()) > 3:
                continue
                
            for sec_name, aliases in header_mapping.items():
                matched_alias = False
                for alias in aliases:
                    alias_lower = alias.lower()
                    if clean == alias_lower:
                        found_sections.append({
                            "section": sec_name,
                            "header_start": line_info["start"],
                            "header_end": line_info["end"],
                            "confidence": 100.0,
                            "matched_text": line_text
                        })
                        matched_alias = True
                        break
                    elif clean.startswith(alias_lower):
                        alias_len = len(alias_lower)
                        if len(clean) > alias_len:
                            next_char = clean[alias_len]
                            if next_char in [" ", ":", "-", "•"] and len(clean) < 25:
                                found_sections.append({
                                    "section": sec_name,
                                    "header_start": line_info["start"],
                                    "header_end": line_info["start"] + alias_len,
                                    "confidence": 90.0,
                                    "matched_text": line_text
                                })
                                matched_alias = True
                                break
                if matched_alias:
                    break

        found_sections = sorted(found_sections, key=lambda x: x["header_start"])
        unique_sections = []
        seen = set()
        for fs in found_sections:
            if fs["section"] not in seen:
                seen.add(fs["section"])
                unique_sections.append(fs)
                
        segmented = {}
        for idx, sec in enumerate(unique_sections):
            start = sec["header_end"]
            end = len(normalized_text)
            if idx + 1 < len(unique_sections):
                end = unique_sections[idx + 1]["header_start"]
            
            content = normalized_text[start:end].strip()
            segmented[sec["section"]] = {
                "content": content,
                "start_index": start,
                "end_index": end,
                "confidence": sec["confidence"]
            }
            
        all_categories = ["contact_info", "summary", "education", "experience", "projects", "skills", "certifications", "achievements", "languages"]
        final_sections = {}
        
        first_header_pos = unique_sections[0]["header_start"] if unique_sections else len(normalized_text)
        final_sections["contact_info"] = {
            "content": normalized_text[:first_header_pos].strip(),
            "start_index": 0,
            "end_index": first_header_pos,
            "confidence": 100.0
        }

        for cat in all_categories:
            if cat == "contact_info":
                continue
            if cat in segmented:
                final_sections[cat] = segmented[cat]
            else:
                final_sections[cat] = {
                    "content": "",
                    "start_index": -1,
                    "end_index": -1,
                    "confidence": 0.0
                }

        final_sections = self.infer_sections_from_content(normalized_text, final_sections)
        
        print("----- SECTION BOUNDARIES AUDIT -----")
        for sec_name, data in final_sections.items():
            content = data["content"]
            start = data["start_index"]
            end = data["end_index"]
            char_count = len(content)
            preview = content[:80].replace("\n", " ") + "..." if char_count > 0 else "EMPTY"
            print(f"Section: {sec_name:15} | Start: {start:5} | End: {end:5} | Chars: {char_count:5} | Preview: {preview}")
        print("------------------------------------")
        
        return final_sections

    def infer_sections_from_content(self, text: str, sections: dict) -> dict:
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        
        if not sections["education"]["content"].strip():
            edu_lines = []
            for line in lines:
                if re.search(r'\b(b\.e\.|b\.tech|m\.tech|b\.s\.|m\.s\.|bachelor|master|phd|diploma|degree|cgpa|gpa|gpa:|cgpa:|university|college|school|institute)\b', line, re.IGNORECASE) or re.search(r'\b(20\d\d|19\d\d)\b', line):
                    edu_lines.append(line)
            if edu_lines:
                sections["education"] = {
                    "content": "\n".join(edu_lines[:5]),
                    "start_index": 0,
                    "end_index": len(text),
                    "confidence": 75.0
                }
                
        if not sections["experience"]["content"].strip():
            exp_lines = []
            for line in lines:
                if re.search(r'\b(developer|engineer|intern|analyst|manager|designer|architect|programmer|coordinator|lead|specialist|internship|employment)\b', line, re.IGNORECASE) or re.search(r'\b(19\d\d|20\d\d)\s*(?:\-|–|to)\s*(present|current|today|now|\b(19\d\d|20\d\d)\b)', line, re.IGNORECASE):
                    exp_lines.append(line)
            if exp_lines:
                sections["experience"] = {
                    "content": "\n".join(exp_lines[:8]),
                    "start_index": 0,
                    "end_index": len(text),
                    "confidence": 70.0
                }
                
        if not sections["projects"]["content"].strip():
            proj_lines = []
            for line in lines:
                if any(k in line.lower() for k in ["github:", "technologies:", "live demo:", "developed a", "built a", "implemented a"]) or re.search(r'github\.com', line, re.IGNORECASE):
                    proj_lines.append(line)
            if proj_lines:
                sections["projects"] = {
                    "content": "\n".join(proj_lines[:6]),
                    "start_index": 0,
                    "end_index": len(text),
                    "confidence": 75.0
                }
                
        if not sections["skills"]["content"].strip():
            skills = self.extract_skills(text)
            if skills:
                sections["skills"] = {
                    "content": ", ".join(skills),
                    "start_index": 0,
                    "end_index": len(text),
                    "confidence": 70.0
                }

        if not sections["summary"]["content"].strip():
            summary_lines = []
            for l in lines[6:22]:
                if len(l) > 40 and not l.startswith(("-", "*", "•")):
                    summary_lines.append(l)
            if summary_lines:
                sections["summary"] = {
                    "content": "\n".join(summary_lines),
                    "start_index": 0,
                    "end_index": len(text),
                    "confidence": 75.0
                }
                
        if not sections["certifications"]["content"].strip():
            cert_lines = []
            for line in lines:
                if re.search(r'\b(certificat|course|licens|nptel|coursera|udemy|certified|credential|credentials)\b', line, re.IGNORECASE):
                    cert_lines.append(line)
            if cert_lines:
                sections["certifications"] = {
                    "content": "\n".join(cert_lines[:5]),
                    "start_index": 0,
                    "end_index": len(text),
                    "confidence": 75.0
                }
                
        if not sections["achievements"]["content"].strip():
            ach_lines = []
            for line in lines:
                if re.search(r'\b(achiev|award|won|place|prize|scholarship|secured|rank|competition|competitions|recognition|symposium)\b', line, re.IGNORECASE) or re.search(r'\b(1st|2nd|3rd|first|second|third)\b', line, re.IGNORECASE):
                    ach_lines.append(line)
            if ach_lines:
                sections["achievements"] = {
                    "content": "\n".join(ach_lines[:5]),
                    "start_index": 0,
                    "end_index": len(text),
                    "confidence": 75.0
                }
                
        if not sections["languages"]["content"].strip():
            lang_lines = []
            for line in lines:
                if re.search(r'\b(english|tamil|hindi|spanish|french|german|telugu|kannada|malayalam|japanese|mandarin|chinese)\b', line, re.IGNORECASE):
                    lang_lines.append(line)
            if lang_lines:
                sections["languages"] = {
                    "content": "\n".join(lang_lines[:3]),
                    "start_index": 0,
                    "end_index": len(text),
                    "confidence": 75.0
                }
                
        return sections

    def extract_skills(self, text: str) -> list:
        skills_db = [
            "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust", "ruby", "php", "swift", "kotlin", "html", "css", "sql", "r", "matlab", "bash", "shell",
            "react", "angular", "vue", "next.js", "nextjs", "django", "fastapi", "flask", "spring boot", "express", "nestjs", "rails", "flutter", "react native", "pytorch", "tensorflow", "keras", "scikit-learn", "pandas", "numpy", "bootstrap", "tailwind",
            "postgresql", "mysql", "mongodb", "redis", "sqlite", "dynamodb", "oracle", "cassandra", "elasticsearch", "firebase",
            "docker", "kubernetes", "aws", "azure", "gcp", "git", "github", "gitlab", "jenkins", "terraform", "ansible", "prometheus", "grafana", "nginx", "linux",
            "agile", "scrum", "devops", "ci/cd", "microservices", "rest api", "graphql", "system design", "unit testing", "tdd", "oop", "machine learning", "deep learning", "nlp", "data structures", "algorithms"
        ]
        
        found = set()
        text_lower = text.lower()
        
        for skill in skills_db:
            escaped = re.escape(skill)
            pattern = r'\b' + escaped + r'\b'
            if skill.endswith('+') or skill.endswith('#'):
                pattern = r'\b' + escaped
            if skill.startswith('.'):
                pattern = escaped + r'\b'
            
            if re.search(pattern, text_lower):
                found.add(skill)
        return list(found)

    def extract_contact_info(self, text: str) -> dict:
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        phone_pattern = r'\+?[0-9][0-9\-.\s()]{8,15}[0-9]'
        linkedin_pattern = r'linkedin\.com/in/[a-zA-Z0-9_-]+'
        github_pattern = r'github\.com/[a-zA-Z0-9_-]+'
        
        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)
        linkedin = re.findall(linkedin_pattern, text)
        github = re.findall(github_pattern, text)
        
        return {
            "email": emails[0] if emails else "",
            "phone": phones[0] if phones else "",
            "linkedin": f"https://{linkedin[0]}" if linkedin else "",
            "github": f"https://{github[0]}" if github else ""
        }

    def estimate_experience_years(self, text: str) -> float:
        pattern = r'\b(19\d\d|20\d\d)\s*(?:\-|–|to)\s*(present|current|today|now|\b(19\d\d|20\d\d)\b)'
        matches = re.findall(pattern, text, re.IGNORECASE)
        total_years = 0.0
        current_year = datetime.now().year
        
        for start, end, end_year in matches:
            start_yr = float(start)
            if end.lower() in ["present", "current", "today", "now"]:
                end_yr = float(current_year)
            else:
                end_yr = float(end_year) if end_year else float(start_yr)
            
            diff = end_yr - start_yr
            if 0 < diff < 40:
                total_years += diff
                
        if total_years == 0.0:
            exp_text_pattern = r'\b(\d{1,2})\+?\s*years?\s+(?:of\s+)?experience\b'
            matches_text = re.findall(exp_text_pattern, text, re.IGNORECASE)
            if matches_text:
                total_years = max(float(x) for x in matches_text)
                
        return min(total_years if total_years > 0 else 1.0, 30.0)

    def extract_projects_details(self, text: str) -> list:
        if not text.strip():
            return []
        
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        
        tech_indices = []
        for idx, line in enumerate(lines):
            if line.lower().startswith("technologies:") or "technologies:" in line.lower():
                tech_indices.append(idx)
                
        if not tech_indices:
            return self._fallback_projects_extractor(lines, text)
            
        projects_data = []
        for i, tech_idx in enumerate(tech_indices):
            name = "Project Highlight"
            if tech_idx > 0:
                name = lines[tech_idx - 1]
                
            tech_line = lines[tech_idx]
            techs = [t.strip() for t in tech_line.replace("Technologies:", "").replace("technologies:", "").split(",") if t.strip()]
            
            live_demo = "Private Link"
            github_url = "Private Repository"
            
            bullets_start = tech_idx + 1
            for offset in range(1, 4):
                next_idx = tech_idx + offset
                if next_idx < len(lines):
                    next_line = lines[next_idx]
                    if next_line.lower().startswith("live demo:") or "live demo:" in next_line.lower():
                        live_demo = next_line.replace("Live Demo:", "").replace("live demo:", "").strip()
                        bullets_start = max(bullets_start, next_idx + 1)
                    elif next_line.lower().startswith("github:") or "github:" in next_line.lower():
                        github_url = next_line.replace("GitHub:", "").replace("github:", "").strip()
                        bullets_start = max(bullets_start, next_idx + 1)
                        
            bullets_end = len(lines)
            if i + 1 < len(tech_indices):
                bullets_end = tech_indices[i + 1] - 1
                
            desc_lines = lines[bullets_start:bullets_end]
            full_desc = "\n".join(desc_lines)
            
            impact = "General project implementation."
            impact_keywords = ["optimized", "reduced", "improved", "increased", "boosted", "saved", "scaled", "decreased", "latency", "performance"]
            metrics = re.findall(r'\b\d+%\b|\$\d+', full_desc)
            found_keywords = [k for k in impact_keywords if k in full_desc.lower()]
            if metrics or found_keywords:
                impact = f"Optimized performance using {', '.join(found_keywords[:2])} with metrics {', '.join(metrics[:2])}."
                
            deployment = "Standard Environment"
            deploy_keywords = ["vercel", "netlify", "heroku", "aws", "gcp", "azure", "docker", "kubernetes"]
            for dk in deploy_keywords:
                if dk in full_desc.lower() or dk in name.lower() or dk in live_demo.lower():
                    deployment = dk.capitalize()
                    break
                    
            projects_data.append({
                "name": name,
                "technologies": techs if techs else self.extract_skills(full_desc),
                "description": full_desc[:300],
                "business_impact": impact,
                "deployment": deployment,
                "github": github_url,
                "live_demo": live_demo
            })
            
        return projects_data

    def _fallback_projects_extractor(self, lines: list, text: str) -> list:
        project_blocks = []
        current_title = None
        current_lines = []
        
        for line in lines:
            if len(line) < 55 and not line.startswith(("-", "*", "•")) and any(c.isalpha() for c in line) and not any(k in line.lower() for k in ["github:", "live demo:", "developed a"]):
                if current_title:
                    project_blocks.append((current_title, "\n".join(current_lines)))
                current_title = line
                current_lines = []
            else:
                if current_title:
                    current_lines.append(line)
                    
        if current_title:
            project_blocks.append((current_title, "\n".join(current_lines)))
            
        if not project_blocks and lines:
            project_blocks.append(("Project Highlight 1", "\n".join(lines)))
            
        projects_data = []
        for name, desc in project_blocks:
            techs = self.extract_skills(desc)
            
            impact = "General project implementation."
            impact_keywords = ["optimized", "reduced", "improved", "increased", "boosted", "saved", "scaled", "decreased", "latency", "performance"]
            metrics = re.findall(r'\b\d+%\b|\$\d+', desc)
            found_keywords = [k for k in impact_keywords if k in desc.lower()]
            if metrics or found_keywords:
                impact = f"Optimized performance using {', '.join(found_keywords[:2])} with metrics {', '.join(metrics[:2])}."
                
            deployment = "Standard Environment"
            deploy_keywords = ["vercel", "netlify", "heroku", "aws", "gcp", "azure", "docker", "kubernetes"]
            for dk in deploy_keywords:
                if dk in desc.lower():
                    deployment = dk.capitalize()
                    break
                    
            github_match = re.search(r'github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+', desc)
            github_url = f"https://{github_match.group(0)}" if github_match else "Private Repository"
            
            projects_data.append({
                "name": name,
                "technologies": techs,
                "description": desc[:300],
                "business_impact": impact,
                "deployment": deployment,
                "github": github_url,
                "live_demo": "Private Link"
            })
        return projects_data

    def extract_experience_details(self, text: str) -> list:
        if not text.strip():
            return []
        
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        date_pattern = r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|19\d\d|20\d\d)\b.*(present|current|today|now|\b(19\d\d|20\d\d)\b)'
        
        date_indices = []
        for idx, line in enumerate(lines):
            if re.search(date_pattern, line, re.IGNORECASE):
                date_indices.append(idx)
                
        if not date_indices:
            return [{
                "company": "Organization",
                "role": "Professional Role",
                "duration": "Duration Undefined",
                "responsibilities": lines[:4],
                "technologies": self.extract_skills(text),
                "achievements": ["Delivered functional milestones."]
            }]
            
        experience_data = []
        for i, date_idx in enumerate(date_indices):
            duration = lines[date_idx]
            
            role = "Professional Role"
            if date_idx > 0:
                prev_line = lines[date_idx - 1]
                if not prev_line.startswith(("-", "*", "•")) and len(prev_line) < 60:
                    role = prev_line
                    
            company = "Organization"
            if date_idx + 1 < len(lines):
                next_line = lines[date_idx + 1]
                if not next_line.startswith(("-", "*", "•")) and len(next_line) < 60:
                    company = next_line
                    
            bullets_start = date_idx + 2 if company != "Organization" else date_idx + 1
            bullets_end = len(lines)
            if i + 1 < len(date_indices):
                next_date_idx = date_indices[i + 1]
                bullets_end = next_date_idx - 1 if next_date_idx > 1 else next_date_idx
                
            resps = [l for l in lines[bullets_start:bullets_end] if l.startswith(("-", "*", "•")) or len(l) > 15]
            full_desc = "\n".join(lines[bullets_start:bullets_end])
            techs = self.extract_skills(full_desc)
            
            achievements = []
            for l in lines[bullets_start:bullets_end]:
                if any(k in l.lower() for k in ["achieved", "delivered", "awarded", "spearheaded", "designed", "improved", "increased", "reduced"]):
                    achievements.append(l)
                    
            experience_data.append({
                "company": company,
                "role": role,
                "duration": duration,
                "responsibilities": resps[:5],
                "technologies": techs,
                "achievements": achievements[:2] if achievements else ["Delivered key technical milestones."]
            })
            
        return experience_data
