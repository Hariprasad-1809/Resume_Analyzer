import React from "react";
import { ShieldCheck, Target, Eye } from "lucide-react";

export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-16 sm:px-6 lg:px-8 animate-fade-in">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-extrabold text-foreground tracking-tight">Our Mission</h1>
        <p className="mt-4 text-lg text-muted-foreground leading-relaxed">
          Democratizing recruitment metrics through explainable AI models.
        </p>
      </div>

      <div className="space-y-12">
        <section className="prose dark:prose-invert max-w-none text-muted-foreground leading-relaxed text-sm">
          <p>
            Traditional Applicant Tracking Systems (ATS) reject up to 75% of qualified candidates due to arbitrary keyword counts and parsing formats. We believe candidate selection should be clear, explainable, and accessible.
          </p>
          <p className="mt-4">
            RoleMatch AI was created to solve this problem. Our platform utilizes local Sentence Transformer models and Named Entity Recognition to analyze resumes contextually rather than matching exact keywords, providing deep, explainable insights into how your projects and experiences align with target jobs.
          </p>
        </section>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 pt-8 border-t border-border">
          <div className="p-4 rounded-lg bg-card border border-border">
            <Target className="h-6 w-6 text-primary mb-2" />
            <h4 className="font-semibold text-foreground mb-1">Semantic Match</h4>
            <p className="text-xs text-muted-foreground">Contextual experience matching over raw keywords.</p>
          </div>
          <div className="p-4 rounded-lg bg-card border border-border">
            <Eye className="h-6 w-6 text-primary mb-2" />
            <h4 className="font-semibold text-foreground mb-1">Explainable AI</h4>
            <p className="text-xs text-muted-foreground">Every analysis metric is transparent and explainable.</p>
          </div>
          <div className="p-4 rounded-lg bg-card border border-border">
            <ShieldCheck className="h-6 w-6 text-primary mb-2" />
            <h4 className="font-semibold text-foreground mb-1">Privacy First</h4>
            <p className="text-xs text-muted-foreground">Processes documents locally and safely in-memory.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
