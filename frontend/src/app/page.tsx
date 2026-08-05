"use client";
import React, { useState } from "react";
import Link from "next/link";
import { ArrowRight, CheckCircle2, Target, Cpu, ShieldCheck, ChevronDown, Award } from "lucide-react";

export default function LandingPage() {
  const [faqOpen, setFaqOpen] = useState<number | null>(null);

  const faqs = [
    {
      q: "Does this calculate an ATS score?",
      a: "No, this is not an ATS calculator. ATS scoring is often arbitrary. Instead, we use semantic embeddings and named entity recognition to detail skills gap analysis, project matching, and formatting issues based on the target job profile."
    },
    {
      q: "How does the semantic role match score work?",
      a: "The score is calculated using an explainable formula: 40% skills coverage, 20% overall semantic description similarity, 25% experience seniority matching, and 15% project keyword relevance. Each component gives a detailed textual breakdown."
    },
    {
      q: "Are my resumes stored securely?",
      a: "Yes. Resumes are processed in-memory and validation checks ensure only legitimate, safe PDFs are accepted. No third-party API receives your files."
    },
    {
      q: "Can I use it offline or locally?",
      a: "Absolutely. The backend includes SQLite database fallback support and loads small local Hugging Face transformer models so it runs on any standard laptop without external API tokens."
    }
  ];

  return (
    <div className="flex flex-col w-full min-h-screen py-12 px-4 sm:px-6 lg:px-8 bg-background">
      <section className="text-center max-w-4xl mx-auto py-16 sm:py-24 animate-fade-in">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold text-primary bg-primary/10 border border-primary/20 mb-6">
          <Award className="h-4 w-4" />
          <span>Explainable AI Evaluation</span>
        </div>
        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-foreground leading-tight">
          Match Your Resume Against Any <span className="text-primary">Target Job Role</span>
        </h1>
        <p className="mt-6 text-lg sm:text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
          Skip black-box ATS percentages. Upload your PDF and get deep semantic similarity, project highlights, skills gap recommendations, and customized learning plans.
        </p>
        <div className="mt-10 flex flex-wrap justify-center gap-4">
          <Link
            href="/upload"
            className="inline-flex items-center gap-2 px-6 py-3 text-base font-semibold rounded-lg text-primary-foreground bg-primary hover:bg-primary/90 shadow-lg hover:shadow-xl transition-all"
          >
            <span>Analyze Resume</span>
            <ArrowRight className="h-5 w-5" />
          </Link>
          <Link
            href="/features"
            className="inline-flex items-center px-6 py-3 text-base font-semibold rounded-lg border border-border bg-card text-foreground hover:bg-secondary transition-all"
          >
            View Features
          </Link>
        </div>
      </section>

      <section className="max-w-7xl mx-auto py-16 border-t border-border">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold tracking-tight text-foreground">Advanced Semantic Features</h2>
          <p className="mt-4 text-muted-foreground">Why professional developers use RoleMatch AI.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="p-6 rounded-xl border border-border bg-card hover:shadow-md transition-all">
            <Target className="h-10 w-10 text-primary mb-4" />
            <h3 className="text-xl font-bold text-foreground mb-2">No Raw ATS Scoring</h3>
            <p className="text-muted-foreground text-sm leading-relaxed">
              We look beyond keywords. Our NLP extracts semantic concepts to match your experiences against real-world job profiles.
            </p>
          </div>
          <div className="p-6 rounded-xl border border-border bg-card hover:shadow-md transition-all">
            <Cpu className="h-10 w-10 text-primary mb-4" />
            <h3 className="text-xl font-bold text-foreground mb-2">Transformer Embeddings</h3>
            <p className="text-muted-foreground text-sm leading-relaxed">
              Using the all-MiniLM-L6-v2 transformer model to analyze semantic similarity of projects, roles, and experience profiles.
            </p>
          </div>
          <div className="p-6 rounded-xl border border-border bg-card hover:shadow-md transition-all">
            <ShieldCheck className="h-10 w-10 text-primary mb-4" />
            <h3 className="text-xl font-bold text-foreground mb-2">Structure & Fonts Audit</h3>
            <p className="text-muted-foreground text-sm leading-relaxed">
              Checks page count, average font sizes, font families, and visual parsing cues to ensure your document looks immaculate.
            </p>
          </div>
        </div>
      </section>

      <section className="max-w-5xl mx-auto py-16 border-t border-border">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold tracking-tight text-foreground">How It Works</h2>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 text-center">
          <div className="flex flex-col items-center">
            <div className="w-12 h-12 rounded-full bg-primary/10 border border-primary/20 text-primary font-bold flex items-center justify-center text-lg mb-4">1</div>
            <h3 className="font-bold text-foreground mb-2">Upload Resume</h3>
            <p className="text-sm text-muted-foreground">Drag and drop your resume in PDF format. We check signature headers and size limits.</p>
          </div>
          <div className="flex flex-col items-center">
            <div className="w-12 h-12 rounded-full bg-primary/10 border border-primary/20 text-primary font-bold flex items-center justify-center text-lg mb-4">2</div>
            <h3 className="font-bold text-foreground mb-2">Input Target Title</h3>
            <p className="text-sm text-muted-foreground">Specify the role (e.g. Frontend Developer). We dynamically match it to database profiles.</p>
          </div>
          <div className="flex flex-col items-center">
            <div className="w-12 h-12 rounded-full bg-primary/10 border border-primary/20 text-primary font-bold flex items-center justify-center text-lg mb-4">3</div>
            <h3 className="font-bold text-foreground mb-2">Review Analytics</h3>
            <p className="text-sm text-muted-foreground">Examine interactive match scores, learning resources, and formatting fixes immediately.</p>
          </div>
        </div>
      </section>

      <section className="max-w-3xl mx-auto py-16 border-t border-border">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold tracking-tight text-foreground">Frequently Asked Questions</h2>
        </div>
        <div className="space-y-4">
          {faqs.map((faq, idx) => (
            <div key={idx} className="border border-border bg-card rounded-lg overflow-hidden transition-all">
              <button
                onClick={() => setFaqOpen(faqOpen === idx ? null : idx)}
                className="w-full flex items-center justify-between p-4 font-semibold text-left text-foreground hover:bg-secondary transition-colors"
              >
                <span>{faq.q}</span>
                <ChevronDown className={`h-5 w-5 transition-transform ${faqOpen === idx ? "rotate-180" : ""}`} />
              </button>
              {faqOpen === idx && (
                <div className="p-4 border-t border-border text-sm text-muted-foreground leading-relaxed bg-background/50">
                  {faq.a}
                </div>
              )}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
