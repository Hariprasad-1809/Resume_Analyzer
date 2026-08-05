import fitz
import re

class ParserService:
    def clean_text(self, text: str) -> str:
        text = re.sub(r'[ \t\xa0\u200b\u200c\u200d\ufeff]+', ' ', text)
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        text = re.sub(r'\n+', '\n', text)
        return text.strip()

    def extract_text_from_pdf(self, file_path: str) -> str:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return self.clean_text(text)

    def analyze_formatting(self, file_path: str) -> dict:
        doc = fitz.open(file_path)
        page_count = len(doc)
        issues = []
        if page_count > 2:
            issues.append(f"Resume exceeds 2 pages (currently {page_count} pages). Try to condense your content.")
        
        font_sizes = []
        font_names = []
        for page in doc:
            try:
                blocks = page.get_text("dict")["blocks"]
                for b in blocks:
                    if "lines" in b:
                        for l in b["lines"]:
                            for s in l["spans"]:
                                font_sizes.append(s["size"])
                                font_names.append(s["font"])
            except Exception:
                pass
        doc.close()

        avg_size = sum(font_sizes) / len(font_sizes) if font_sizes else 11.0
        if avg_size < 9.5:
            issues.append(f"Average font size is too small ({round(avg_size, 1)}pt). Standard is 10-12pt for readability.")
        elif avg_size > 13.5:
            issues.append(f"Average font size is unusually large ({round(avg_size, 1)}pt). Standard body size is 10-12pt.")

        unprofessional_fonts = ["comic", "impact", "papyrus", "chiller", "curlz"]
        found_fonts = set()
        for font in font_names:
            font_lower = font.lower()
            for uf in unprofessional_fonts:
                if uf in font_lower:
                    found_fonts.add(font)
        
        for f in found_fonts:
            issues.append(f"Detected non-standard font: {f}. Use professional fonts like Arial, Calibri, or Times New Roman.")

        score = max(0, 100 - len(issues) * 20)
        feedback = "Formatting is excellent and matches standard guidelines." if score >= 90 else "Formatting has issues that could affect visual scanning."
        
        return {
            "issues": issues,
            "score": score,
            "feedback": feedback
        }
