import React from "react";
import { Cpu, Terminal, FileText, CheckCircle2, ShieldCheck, HelpCircle } from "lucide-react";

export default function FeaturesPage() {
  const list = [
    {
      icon: <FileText className="h-6 w-6 text-primary" />,
      title: "PDF Text Parsing",
      desc: "Uses PyMuPDF to extract plain text and structural formatting. Validates magic header signatures to ensure clean processing."
    },
    {
      icon: <Cpu className="h-6 w-6 text-primary" />,
      title: "Semantic Embedding Vectors",
      desc: "Generates 384-dimensional dense vectors using Hugging Face's Sentence Transformers to compute exact cosine similarity metrics."
    },
    {
      icon: <Terminal className="h-6 w-6 text-primary" />,
      title: "Skills Gap Analysis",
      desc: "Uses RapidFuzz algorithms to fuzzy-match resume keywords against job roles, identifying critical technological overlaps."
    },
    {
      icon: <CheckCircle2 className="h-6 w-6 text-primary" />,
      title: "Visual Formatting Check",
      desc: "Reviews page limitations, font sizes, and flags unprofessional font styles to optimize visual appeal for recruiters."
    },
    {
      icon: <ShieldCheck className="h-6 w-6 text-primary" />,
      title: "Secure Processing",
      desc: "Runs entirely in-memory on the backend. No external APIs or third-party crawlers receive your personal details."
    },
    {
      icon: <HelpCircle className="h-6 w-6 text-primary" />,
      title: "Explainable Output",
      desc: "Every score is broken down by its components (experience, skills, projects) with complete structural feedback details."
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-16 sm:px-6 lg:px-8 animate-fade-in">
      <div className="text-center max-w-3xl mx-auto mb-16">
        <h1 className="text-4xl font-extrabold text-foreground tracking-tight">
          Application Core Capabilities
        </h1>
        <p className="mt-4 text-lg text-muted-foreground leading-relaxed">
          Deep NLP matching and structural layout checks built for high-performance candidate evaluations.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {list.map((item, idx) => (
          <div
            key={idx}
            className="p-6 rounded-xl border border-border bg-card hover:border-primary/50 hover:shadow-md transition-all group"
          >
            <div className="p-3 w-fit rounded-lg bg-primary/10 mb-4 transition-colors group-hover:bg-primary/20">
              {item.icon}
            </div>
            <h3 className="text-lg font-bold text-foreground mb-2 group-hover:text-primary transition-colors">
              {item.title}
            </h3>
            <p className="text-sm text-muted-foreground leading-relaxed">
              {item.desc}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
