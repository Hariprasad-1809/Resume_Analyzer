"use client";
import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import axios from "axios";
import { getApiBaseUrl } from "@/lib/api";
import {
  ArrowLeft,
  CheckCircle2,
  XCircle,
  AlertCircle,
  FileText,
  Bookmark,
  Award,
  AlertTriangle,
  Lightbulb,
  ExternalLink,
  BookOpen,
  Layout,
  Layers,
  Sparkles,
  Calendar,
  Briefcase,
  GitBranch,
  Globe,
  Settings,
  TrendingUp,
  Activity,
  ChevronDown,
  ChevronUp,
  Eye,
  CheckSquare,
  Target,
  Clock,
  ShieldCheck,
  Zap,
  UserCheck,
  Flame,
  Compass,
  Code,
  Check,
  FileCheck,
  Wrench,
  GraduationCap,
  Shield,
  HelpCircle,
  Info
} from "lucide-react";
import { ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from "recharts";

interface ProjectMatch {
  title: string;
  relevance: string;
  score: number;
  description?: string;
  technologies?: string[];
  business_impact?: string;
  deployment?: string;
  github?: string;
  live_demo?: string;
}

interface ExperienceMatch {
  title: string;
  company: string;
  years: number;
  alignment: string;
  relevance: number;
  duration?: string;
  responsibilities?: string[];
  technologies?: string[];
  achievements?: string[];
}

interface StructureAnalysis {
  sections_found: string[];
  missing_sections: string[];
  score: number;
  feedback: string;
}

interface FormattingAnalysis {
  issues: string[];
  score: number;
  feedback: string;
  rating?: string;
}

interface LearningResource {
  skill: string;
  resource_name: string;
  resource_url: string;
}

interface SectionEvidence {
  content: string;
  confidence: number;
}

interface RecommendationCard {
  id?: string;
  priority: "High" | "Medium" | "Low" | string;
  category: string;
  title: string;
  reason: string;
  resume_evidence?: string;
  evidence?: string;
  recommendation: string;
  expected_benefit: string;
  estimated_effort?: string;
}

interface RecruiterReview {
  feedback: string;
  strengths: string[];
  concerns: string[];
  decision: "Strong Hire" | "Hire" | "Consider" | "Needs Improvement" | "Reject" | string;
  readiness: string;
}

interface ProjectReview {
  project_name: string;
  strengths: string;
  weaknesses: string;
  missing_business_impact: string;
  missing_metrics: string;
  deployment_improvements: string;
  architecture_improvements: string;
  testing_improvements: string;
  documentation_improvements: string;
  portfolio_improvements: string;
  security_improvements: string;
  performance_improvements: string;
  priority: string;
}

interface ExperienceReview {
  role: string;
  company: string;
  action_verbs: string;
  quantified_achievements: string;
  technical_wording: string;
  business_impact: string;
  ownership: string;
}

interface SkillRecommendation {
  skill: string;
  learning_priority: string;
  difficulty: string;
  estimated_learning_time: string;
  reason: string;
}

interface TopActionItem {
  priority: string;
  reason: string;
  recommendation: string;
  expected_benefit: string;
  estimated_time: string;
}

interface InterviewPrepItem {
  skill: string;
  recommendations: string[];
}

interface LearningRoadmap {
  plan_7_days: string[];
  plan_30_days: string[];
  plan_60_days: string[];
  plan_90_days: string[];
}

interface ParsedRecommendations {
  recruiter_review?: RecruiterReview;
  summary?: {
    status?: string;
    review?: string;
    better_wording?: string;
    missing_keywords?: string[];
    alignment?: string;
    readability?: string;
  };
  projects?: ProjectReview[];
  experience?: ExperienceReview[];
  skills?: SkillRecommendation[];
  education?: {
    has_improvements?: boolean;
    evidence?: string;
    recommendation?: string;
  };
  certifications?: {
    has_improvements?: boolean;
    evidence?: string;
    recommendations?: string[];
  };
  achievements?: {
    evidence?: string;
    stronger_wording?: string;
    measurable_presentation?: string;
  };
  ats?: {
    keywords?: string[];
    section_ordering?: string[];
    bullet_formatting?: string[];
    ats_compatibility?: string;
  };
  interview_preparation?: InterviewPrepItem[];
  learning_roadmap?: LearningRoadmap;
  top_action_plan?: TopActionItem[];
  cards?: RecommendationCard[];
}

interface AnalysisData {
  id: string;
  resume_id: string;
  job_title: string;
  role_match_percentage: number;
  existing_skills: string[];
  missing_skills: string[];
  relevant_projects: ProjectMatch[];
  relevant_experience: ExperienceMatch[];
  strengths: string[];
  weaknesses: string[];
  structure_analysis: StructureAnalysis;
  formatting_analysis: FormattingAnalysis;
  keyword_recommendations: string[];
  improvement_suggestions: string[];
  learning_recommendations: LearningResource[];
  suitable_job_roles: string[];
  explanations?: {
    sections?: Record<string, SectionEvidence>;
    sections_structured?: {
      summary?: { content: string; confidence: number };
      education?: { degree: string; college: string; cgpa: string; duration: string; location?: string; confidence: number };
      experience?: Array<{ role: string; company: string; duration: string; responsibilities: string[]; technologies: string[]; achievements?: string[] }>;
      projects?: Array<{ name: string; technologies: string[]; github: string; live_demo: string; deployment: string; business_impact: string; role_relevance: string; description: string }>;
      skills?: Record<string, string[]>;
      certifications?: string[];
      achievements?: Array<{ title: string; event: string; organization: string; prize: string; year: string }>;
      languages?: string[];
    };
    required_skills?: string;
    preferred_skills?: string;
    experience?: string;
    projects?: string;
    education?: string;
    quality?: string;
    formatting?: string;
  } & Record<string, any>;
  resume_raw_text?: string;
  created_at: string;
}

export default function DashboardPage() {
  const { id } = useParams();
  const router = useRouter();
  const [data, setData] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [openEvidence, setOpenEvidence] = useState<Record<string, boolean>>({});
  const [cardFilter, setCardFilter] = useState<"All" | "High" | "Medium" | "Low">("All");
  const [expandedProjects, setExpandedProjects] = useState<Record<number, boolean>>({});

  useEffect(() => {
    if (!id) return;
    const fetchDetail = async () => {
      try {
        const res = await axios.get(`${getApiBaseUrl()}/api/v1/history/${id}`);
        setData(res.data);
      } catch (err) {
        setError("Failed to load evaluation details.");
      } finally {
        setLoading(false);
      }
    };
    fetchDetail();
  }, [id]);

  const toggleEvidence = (section: string) => {
    setOpenEvidence((prev) => ({ ...prev, [section]: !prev[section] }));
  };

  const toggleProjectExpand = (idx: number) => {
    setExpandedProjects((prev) => ({ ...prev, [idx]: !prev[idx] }));
  };

  // Safely parse recommendations from data.improvement_suggestions
  const parseRecommendations = (): ParsedRecommendations | null => {
    if (!data?.improvement_suggestions || data.improvement_suggestions.length === 0) {
      return null;
    }

    try {
      const raw = data.improvement_suggestions[0];
      if (typeof raw === "string" && raw.trim().startsWith("{")) {
        return JSON.parse(raw);
      } else if (typeof raw === "object") {
        return raw as ParsedRecommendations;
      }
    } catch (err) {
      console.error("Error parsing recommendations JSON:", err);
    }
    return null;
  };

  const recs = parseRecommendations();

  if (loading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center min-h-[70vh] bg-background">
        <div className="h-12 w-12 border-4 border-primary/20 border-t-primary rounded-full animate-spin"></div>
        <p className="mt-4 text-muted-foreground font-medium text-[15px]">Loading candidate evaluation report...</p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="max-w-2xl mx-auto py-20 px-6 text-center">
        <div className="p-8 bg-destructive/10 border border-destructive/20 rounded-2xl text-destructive flex flex-col items-center">
          <AlertTriangle className="h-12 w-12 mb-4" />
          <h2 className="text-[22px] font-bold mb-2">Error Loading Report</h2>
          <p className="text-[15px] mb-6">{error || "Record not found."}</p>
          <Link
            href="/history"
            className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground text-[15px] font-semibold rounded-xl hover:bg-primary/95 transition-all"
          >
            <ArrowLeft className="h-5 w-5" />
            <span>Back to Logs</span>
          </Link>
        </div>
      </div>
    );
  }

  const radarData = [
    { subject: "Core Skills", A: data.existing_skills.length * 10, fullMark: 100 },
    { subject: "Experience", A: data.relevant_experience.length > 0 ? Math.round(data.relevant_experience[0].relevance) : 50, fullMark: 100 },
    { subject: "Projects", A: data.relevant_projects.length > 0 ? Math.round(data.relevant_projects[0].score) : 50, fullMark: 100 },
    { subject: "Structure", A: data.structure_analysis.score, fullMark: 100 },
    { subject: "Formatting", A: data.formatting_analysis.score, fullMark: 100 }
  ];

  const getRoleFit = (pct: number) => {
    if (pct >= 85) return { text: "Outstanding Fit", color: "text-emerald-500 bg-emerald-500/10 border-emerald-500/20" };
    if (pct >= 70) return { text: "Strong Fit", color: "text-indigo-500 bg-indigo-500/10 border-indigo-500/20" };
    if (pct >= 50) return { text: "Moderate Fit", color: "text-amber-500 bg-amber-500/10 border-amber-500/20" };
    return { text: "Needs Improvement", color: "text-rose-500 bg-rose-500/10 border-rose-500/20" };
  };

  const getDecisionBadge = (decision: string) => {
    const d = decision?.toLowerCase() || "";
    if (d.includes("strong hire")) return "bg-emerald-500 text-white border-emerald-600";
    if (d.includes("hire")) return "bg-blue-600 text-white border-blue-700";
    if (d.includes("consider")) return "bg-amber-500 text-white border-amber-600";
    if (d.includes("needs improvement")) return "bg-orange-500 text-white border-orange-600";
    return "bg-rose-600 text-white border-rose-700";
  };

  const getCategoryIcon = (category: string) => {
    const c = category?.toLowerCase() || "";
    if (c.includes("project")) return <GitBranch className="h-5 w-5 text-primary" />;
    if (c.includes("summary")) return <FileText className="h-5 w-5 text-primary" />;
    if (c.includes("experience") || c.includes("internship")) return <Briefcase className="h-5 w-5 text-primary" />;
    if (c.includes("skill")) return <Layers className="h-5 w-5 text-primary" />;
    if (c.includes("ats")) return <Zap className="h-5 w-5 text-primary" />;
    if (c.includes("education")) return <GraduationCap className="h-5 w-5 text-primary" />;
    if (c.includes("certif")) return <Award className="h-5 w-5 text-primary" />;
    if (c.includes("achieve")) return <Sparkles className="h-5 w-5 text-primary" />;
    return <Lightbulb className="h-5 w-5 text-primary" />;
  };

  const getPriorityStyle = (priority: string) => {
    const p = priority?.toLowerCase() || "";
    if (p.includes("high")) return {
      badge: "bg-red-500/10 text-red-600 border-red-500/30 dark:bg-rose-500/20 dark:text-rose-400 dark:border-rose-500/40",
      dot: "🔥 HIGH",
      border: "border-red-500/30 hover:border-red-500/50 dark:border-red-500/30",
      accent: "border-l-4 border-l-red-500"
    };
    if (p.includes("medium")) return {
      badge: "bg-orange-500/10 text-orange-600 border-orange-500/30 dark:bg-amber-500/20 dark:text-amber-400 dark:border-amber-500/40",
      dot: "🟠 MEDIUM",
      border: "border-orange-500/30 hover:border-orange-500/50 dark:border-amber-500/30",
      accent: "border-l-4 border-l-orange-500"
    };
    return {
      badge: "bg-emerald-500/10 text-emerald-600 border-emerald-500/30 dark:bg-emerald-500/20 dark:text-emerald-400 dark:border-emerald-500/40",
      dot: "🟢 LOW",
      border: "border-emerald-500/30 hover:border-emerald-500/50 dark:border-emerald-500/30",
      accent: "border-l-4 border-l-emerald-500"
    };
  };

  // Process recommendation cards - fallback guarantee
  let rawCards: RecommendationCard[] = recs?.cards || [];
  if (rawCards.length === 0) {
    rawCards = [{
      id: "rec-0",
      title: "Resume looks good",
      category: "General",
      priority: "Low",
      reason: "No significant improvements detected.",
      resume_evidence: "All key resume sections and skills align well with standard benchmarks.",
      recommendation: "Continue updating your resume as you gain more experience.",
      expected_benefit: "Keeps the resume current and aligned with career growth."
    }];
  }

  const filteredCards = cardFilter === "All"
    ? rawCards
    : rawCards.filter(c => c.priority.toLowerCase() === cardFilter.toLowerCase());

  const displayCards = filteredCards.length > 0 ? filteredCards : rawCards;

  const sectionsList = [
    { key: "summary", label: "Profile Summary" },
    { key: "education", label: "Education Credentials" },
    { key: "experience", label: "Work Experience" },
    { key: "projects", label: "Projects Details" },
    { key: "skills", label: "Technical Skills" },
    { key: "certifications", label: "Certifications" },
    { key: "achievements", label: "Achievements & Awards" }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-10">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 p-8 rounded-3xl bg-gradient-to-r from-card via-card/80 to-secondary/30 border border-border shadow-sm">
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <Link href="/history" className="p-2 rounded-xl bg-secondary/50 hover:bg-secondary transition-colors text-muted-foreground hover:text-foreground">
              <ArrowLeft className="h-5 w-5" />
            </Link>
            <span className="text-[13px] font-bold text-primary bg-primary/10 px-3 py-1 rounded-full uppercase tracking-wider border border-primary/20">
              {data.job_title}
            </span>
          </div>
          <h1 className="text-[28px] sm:text-[34px] font-extrabold text-foreground tracking-tight">
            Recruiter Match Report
          </h1>
          <p className="text-[15px] text-muted-foreground">
            Analysis evaluated on {new Date(data.created_at).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}
          </p>
        </div>

        <div className="flex items-center gap-6">
          <div className="text-right">
            <span className="text-[13px] font-semibold text-muted-foreground uppercase tracking-wider block">Role Match Score</span>
            <div className="text-[40px] font-black text-primary leading-none mt-1">
              {data.role_match_percentage}%
            </div>
          </div>
          <div className={`px-4 py-2 rounded-2xl text-[14px] font-bold border ${getRoleFit(data.role_match_percentage).color}`}>
            {getRoleFit(data.role_match_percentage).text}
          </div>
        </div>
      </div>

      {/* Recruiter Overview & Hiring Decision */}
      {recs?.recruiter_review && (
        <div className="p-8 rounded-3xl border border-border bg-card shadow-sm space-y-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-border pb-6">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-primary/10 rounded-2xl text-primary border border-primary/20">
                <UserCheck className="h-6 w-6" />
              </div>
              <div>
                <h2 className="text-[22px] font-bold text-foreground">Recruiter Review & Decision</h2>
                <p className="text-[14px] text-muted-foreground">Senior Recruiter Assessment & Candidate Evaluation</p>
              </div>
            </div>
            {recs.recruiter_review.decision && (
              <div className="flex items-center gap-3">
                <span className="text-[13px] font-bold text-muted-foreground uppercase tracking-wider">Hiring Decision:</span>
                <span className={`px-4 py-1.5 rounded-full text-[14px] font-extrabold tracking-wide uppercase border shadow-sm ${getDecisionBadge(recs.recruiter_review.decision)}`}>
                  {recs.recruiter_review.decision}
                </span>
              </div>
            )}
          </div>

          <div className="space-y-4">
            <p className="text-[16px] text-foreground leading-relaxed font-medium bg-secondary/10 p-5 rounded-2xl border border-border/60">
              "{recs.recruiter_review.feedback}"
            </p>

            {recs.recruiter_review.readiness && (
              <div className="flex items-center gap-2 text-[14px] text-muted-foreground font-semibold px-2">
                <ShieldCheck className="h-5 w-5 text-primary flex-shrink-0" />
                <span><strong className="text-foreground">Interview Readiness:</strong> {recs.recruiter_review.readiness}</span>
              </div>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-border/60">
            <div className="space-y-3">
              <span className="text-[13px] font-bold text-emerald-600 bg-emerald-500/10 px-3 py-1 rounded-full uppercase tracking-wider border border-emerald-500/20 inline-flex items-center gap-1.5">
                <CheckCircle2 className="h-4 w-4" /> Candidate Strengths
              </span>
              <ul className="space-y-2 text-[14px] text-foreground">
                {(recs.recruiter_review.strengths || data.strengths).map((s, idx) => (
                  <li key={idx} className="flex items-start gap-2.5 p-3 rounded-xl bg-emerald-500/5 border border-emerald-500/10">
                    <Check className="h-4.5 w-4.5 text-emerald-500 mt-0.5 flex-shrink-0" />
                    <span>{s}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="space-y-3">
              <span className="text-[13px] font-bold text-rose-600 bg-rose-500/10 px-3 py-1 rounded-full uppercase tracking-wider border border-rose-500/20 inline-flex items-center gap-1.5">
                <AlertTriangle className="h-4 w-4" /> Recruiter Concerns / Gaps
              </span>
              <ul className="space-y-2 text-[14px] text-foreground">
                {(recs.recruiter_review.concerns || data.weaknesses).map((w, idx) => (
                  <li key={idx} className="flex items-start gap-2.5 p-3 rounded-xl bg-rose-500/5 border border-rose-500/10">
                    <XCircle className="h-4.5 w-4.5 text-rose-500 mt-0.5 flex-shrink-0" />
                    <span>{w}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Radar Chart & Key Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 p-8 rounded-3xl border border-border bg-card shadow-sm space-y-4">
          <h3 className="text-[20px] font-bold text-foreground flex items-center gap-2">
            <Activity className="h-5 w-5 text-primary" />
            <span>Candidate Skill & Alignment Radar</span>
          </h3>
          <div className="h-[280px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="currentColor" className="text-border" />
                <PolarAngleAxis dataKey="subject" stroke="currentColor" className="text-muted-foreground text-[12px] font-semibold" />
                <PolarRadiusAxis angle={30} domain={[0, 100]} />
                <Radar name="Candidate" dataKey="A" stroke="hsl(var(--primary))" fill="hsl(var(--primary))" fillOpacity={0.3} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="p-8 rounded-3xl border border-border bg-card shadow-sm space-y-6 flex flex-col justify-between">
          <div className="space-y-4">
            <h3 className="text-[20px] font-bold text-foreground flex items-center gap-2">
              <Zap className="h-5 w-5 text-primary" />
              <span>ATS & Layout Audit</span>
            </h3>

            <div className="space-y-4">
              <div className="p-4 rounded-2xl bg-secondary/20 border border-border space-y-1">
                <div className="flex justify-between items-center text-[14px]">
                  <span className="text-muted-foreground font-semibold">Structure Score</span>
                  <span className="font-bold text-foreground">{data.structure_analysis.score}%</span>
                </div>
                <div className="w-full bg-secondary rounded-full h-2 overflow-hidden">
                  <div className="bg-primary h-full rounded-full transition-all" style={{ width: `${data.structure_analysis.score}%` }}></div>
                </div>
                <p className="text-[12px] text-muted-foreground pt-1">{data.structure_analysis.feedback}</p>
              </div>

              <div className="p-4 rounded-2xl bg-secondary/20 border border-border space-y-1">
                <div className="flex justify-between items-center text-[14px]">
                  <span className="text-muted-foreground font-semibold">Formatting Rating</span>
                  <span className="font-bold text-foreground">{data.formatting_analysis.score}% ({data.formatting_analysis.rating || "Good"})</span>
                </div>
                <div className="w-full bg-secondary rounded-full h-2 overflow-hidden">
                  <div className="bg-emerald-500 h-full rounded-full transition-all" style={{ width: `${data.formatting_analysis.score}%` }}></div>
                </div>
                <p className="text-[12px] text-muted-foreground pt-1">{data.formatting_analysis.feedback}</p>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-border">
            <span className="text-[12px] font-bold text-muted-foreground uppercase tracking-wider block mb-2">Suitable Job Roles</span>
            <div className="flex flex-wrap gap-1.5">
              {data.suitable_job_roles.map((role, idx) => (
                <span key={idx} className="text-[12px] font-semibold bg-primary/10 text-primary px-2.5 py-1 rounded-lg border border-primary/20">
                  {role}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* PRIMARY SECTION: Actionable Improvement Advice / AI Resume Recommendations */}
      <div className="p-8 rounded-3xl border border-border bg-card shadow-sm space-y-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-border pb-6">
          <div className="space-y-1">
            <div className="flex items-center gap-2.5">
              <div className="p-2.5 bg-primary/10 rounded-xl text-primary">
                <Lightbulb className="h-6 w-6" />
              </div>
              <h2 className="text-[24px] font-extrabold text-foreground tracking-tight">
                Actionable Improvement Advice
              </h2>
            </div>
            <p className="text-[14px] text-muted-foreground pl-11">
              Personalized recruiter suggestions referencing candidate resume evidence for: <strong className="text-foreground">{data.job_title}</strong>
            </p>
          </div>

          {/* Priority Filters */}
          <div className="flex items-center bg-secondary/30 p-1.5 rounded-2xl border border-border">
            {(["All", "High", "Medium", "Low"] as const).map((filter) => (
              <button
                key={filter}
                onClick={() => setCardFilter(filter)}
                className={`px-4 py-1.5 rounded-xl text-[13px] font-bold transition-all ${
                  cardFilter === filter
                    ? "bg-card text-foreground shadow-sm border border-border"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                {filter === "High" && "🔥 "}
                {filter === "Medium" && "🟠 "}
                {filter === "Low" && "🟢 "}
                {filter}
              </button>
            ))}
          </div>
        </div>

        {/* Vertical Stack of Recommendation Cards */}
        <div className="flex flex-col gap-6">
          {displayCards.map((card, idx) => {
            const priorityStyle = getPriorityStyle(card.priority);
            const cardIcon = getCategoryIcon(card.category);
            const evidenceText = card.resume_evidence || card.evidence || "Resume details evaluated.";

            return (
              <div
                key={card.id || `card-${idx}`}
                className={`p-6 rounded-2xl border ${priorityStyle.border} ${priorityStyle.accent} bg-card hover:-translate-y-1 hover:shadow-xl transition-all duration-300 space-y-5`}
              >
                {/* Top Row: Icon, Category, Title, Priority Badge */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-border/60 pb-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2.5 rounded-xl bg-secondary/50 border border-border">
                      {cardIcon}
                    </div>
                    <div>
                      <span className="text-[12px] font-bold text-muted-foreground uppercase tracking-wider block">
                        {card.category}
                      </span>
                      <h3 className="text-[18px] font-bold text-foreground leading-snug">
                        {card.title}
                      </h3>
                    </div>
                  </div>

                  <div className="self-start sm:self-center flex-shrink-0">
                    <span className={`text-[12px] font-black px-3.5 py-1 rounded-full border shadow-sm ${priorityStyle.badge}`}>
                      {priorityStyle.dot} PRIORITY
                    </span>
                  </div>
                </div>

                {/* Reason & Resume Evidence */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-[14px]">
                  <div className="p-4 rounded-xl bg-secondary/20 border border-border/60 space-y-1">
                    <span className="font-bold text-foreground text-[12px] uppercase tracking-wider block text-primary">
                      Reason:
                    </span>
                    <p className="text-foreground leading-relaxed">
                      {card.reason}
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-secondary/20 border border-border/60 space-y-1">
                    <span className="font-bold text-foreground text-[12px] uppercase tracking-wider block text-primary">
                      Resume Evidence:
                    </span>
                    <p className="italic text-muted-foreground leading-relaxed">
                      "{evidenceText}"
                    </p>
                  </div>
                </div>

                {/* Recommendation Detail */}
                <div className="p-4 rounded-xl bg-primary/5 border border-primary/20 space-y-1.5 text-[14px]">
                  <span className="font-bold text-primary text-[12px] uppercase tracking-wider block">
                    Actionable Recommendation:
                  </span>
                  <p className="text-foreground font-medium leading-relaxed">
                    {card.recommendation}
                  </p>
                </div>

                {/* Expected Benefit */}
                <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-[14px] flex items-start gap-3">
                  <CheckCircle2 className="h-5 w-5 text-emerald-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <span className="font-bold text-emerald-700 dark:text-emerald-400 text-[12px] uppercase tracking-wider block">
                      Expected Benefit:
                    </span>
                    <p className="text-emerald-800 dark:text-emerald-300 font-semibold leading-snug">
                      {card.expected_benefit}
                    </p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Top 10 Action Plan Section */}
      {recs?.top_action_plan && recs.top_action_plan.length > 0 && (
        <div className="p-8 rounded-3xl border border-border bg-card shadow-sm space-y-6">
          <div className="flex items-center gap-3 border-b border-border pb-6">
            <div className="p-3 bg-primary/10 rounded-2xl text-primary border border-primary/20">
              <Target className="h-6 w-6" />
            </div>
            <div>
              <h2 className="text-[22px] font-bold text-foreground">Top 10 High-Impact Action Plan</h2>
              <p className="text-[14px] text-muted-foreground">Prioritized checklist sorted strictly by hiring impact</p>
            </div>
          </div>

          <div className="space-y-4">
            {recs.top_action_plan.map((item, idx) => {
              const priorityStyle = getPriorityStyle(item.priority);
              return (
                <div key={idx} className="p-5 rounded-2xl border border-border/80 bg-secondary/10 hover:bg-secondary/20 transition-all flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                  <div className="flex items-start gap-4">
                    <div className="h-9 w-9 rounded-2xl bg-primary text-primary-foreground font-black text-[16px] flex items-center justify-center flex-shrink-0 shadow-sm">
                      {idx + 1}
                    </div>
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className={`text-[11px] font-extrabold px-2.5 py-0.5 rounded-full border ${priorityStyle.badge}`}>
                          {item.priority} Priority
                        </span>
                        <span className="text-[13px] font-bold text-foreground">{item.reason}</span>
                      </div>
                      <p className="text-[15px] font-semibold text-foreground">{item.recommendation}</p>
                      <p className="text-[13px] text-emerald-600 font-medium">Expected Benefit: {item.expected_benefit}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 text-[13px] font-mono text-muted-foreground bg-secondary px-3 py-1.5 rounded-xl border border-border flex-shrink-0 self-end md:self-center">
                    <Clock className="h-4 w-4" />
                    <span>Est. Time: {item.estimated_time}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Learning Roadmap Section (7, 30, 60, 90 Days) */}
      {recs?.learning_roadmap && (
        <div className="p-8 rounded-3xl border border-border bg-card shadow-sm space-y-6">
          <div className="flex items-center gap-3 border-b border-border pb-6">
            <div className="p-3 bg-primary/10 rounded-2xl text-primary border border-primary/20">
              <Compass className="h-6 w-6" />
            </div>
            <div>
              <h2 className="text-[22px] font-bold text-foreground">Skill Development & Learning Roadmap</h2>
              <p className="text-[14px] text-muted-foreground">Structured timeline to bridge technical gaps for target position</p>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="p-6 rounded-2xl border border-blue-500/20 bg-blue-500/5 space-y-4">
              <span className="text-[13px] font-extrabold text-blue-600 bg-blue-500/10 px-3 py-1 rounded-full border border-blue-500/20 uppercase tracking-wider inline-block">
                Day 1 - 7 (Week 1)
              </span>
              <ul className="space-y-2 text-[14px] text-foreground">
                {(recs.learning_roadmap.plan_7_days || []).map((step, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <CheckSquare className="h-4.5 w-4.5 text-blue-500 mt-0.5 flex-shrink-0" />
                    <span>{step}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="p-6 rounded-2xl border border-indigo-500/20 bg-indigo-500/5 space-y-4">
              <span className="text-[13px] font-extrabold text-indigo-600 bg-indigo-500/10 px-3 py-1 rounded-full border border-indigo-500/20 uppercase tracking-wider inline-block">
                Day 8 - 30 (Month 1)
              </span>
              <ul className="space-y-2 text-[14px] text-foreground">
                {(recs.learning_roadmap.plan_30_days || []).map((step, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <CheckSquare className="h-4.5 w-4.5 text-indigo-500 mt-0.5 flex-shrink-0" />
                    <span>{step}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="p-6 rounded-2xl border border-violet-500/20 bg-violet-500/5 space-y-4">
              <span className="text-[13px] font-extrabold text-violet-600 bg-violet-500/10 px-3 py-1 rounded-full border border-violet-500/20 uppercase tracking-wider inline-block">
                Day 31 - 60 (Month 2)
              </span>
              <ul className="space-y-2 text-[14px] text-foreground">
                {(recs.learning_roadmap.plan_60_days || []).map((step, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <CheckSquare className="h-4.5 w-4.5 text-violet-500 mt-0.5 flex-shrink-0" />
                    <span>{step}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="p-6 rounded-2xl border border-emerald-500/20 bg-emerald-500/5 space-y-4">
              <span className="text-[13px] font-extrabold text-emerald-600 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20 uppercase tracking-wider inline-block">
                Day 61 - 90 (Month 3)
              </span>
              <ul className="space-y-2 text-[14px] text-foreground">
                {(recs.learning_roadmap.plan_90_days || []).map((step, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <CheckSquare className="h-4.5 w-4.5 text-emerald-500 mt-0.5 flex-shrink-0" />
                    <span>{step}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Technical Interview Preparation Section (ONLY for detected skills) */}
      {recs?.interview_preparation && recs.interview_preparation.length > 0 && (
        <div className="p-8 rounded-3xl border border-border bg-card shadow-sm space-y-6">
          <div className="flex items-center gap-3 border-b border-border pb-6">
            <div className="p-3 bg-primary/10 rounded-2xl text-primary border border-primary/20">
              <Code className="h-6 w-6" />
            </div>
            <div>
              <h2 className="text-[22px] font-bold text-foreground">Technical Interview Preparation</h2>
              <p className="text-[14px] text-muted-foreground">Targeted interview questions & topics derived <strong className="text-foreground">ONLY</strong> from detected resume skills</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recs.interview_preparation.map((item, idx) => (
              <div key={idx} className="p-6 rounded-2xl border border-border bg-secondary/10 space-y-4 flex flex-col justify-between">
                <div className="space-y-3">
                  <span className="text-[13px] font-extrabold bg-primary/10 text-primary px-3 py-1 rounded-full border border-primary/20 inline-block">
                    Detected: {item.skill}
                  </span>
                  <div className="space-y-2">
                    <span className="text-[12px] font-bold text-muted-foreground uppercase tracking-wider block">Recommended Prep Topics:</span>
                    <ul className="space-y-2 text-[14px] text-foreground">
                      {item.recommendations.map((rec, rIdx) => (
                        <li key={rIdx} className="flex items-start gap-2">
                          <CheckCircle2 className="h-4 w-4 text-primary mt-0.5 flex-shrink-0" />
                          <span>{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Projects Deep-Dive Recruiter Review (For EVERY project) */}
      {recs?.projects && recs.projects.length > 0 && (
        <div className="p-8 rounded-3xl border border-border bg-card shadow-sm space-y-6">
          <div className="flex items-center gap-3 border-b border-border pb-6">
            <div className="p-3 bg-primary/10 rounded-2xl text-primary border border-primary/20">
              <GitBranch className="h-6 w-6" />
            </div>
            <div>
              <h2 className="text-[22px] font-bold text-foreground">Projects Recruiter Audit ({recs.projects.length})</h2>
              <p className="text-[14px] text-muted-foreground">Individual architectural, deployment, testing, & security reviews for every extracted project</p>
            </div>
          </div>

          <div className="space-y-6">
            {recs.projects.map((proj, idx) => {
              const isExpanded = !!expandedProjects[idx];
              return (
                <div key={idx} className="p-6 rounded-2xl border border-border bg-card space-y-4 shadow-sm">
                  <div className="flex justify-between items-start gap-4">
                    <div>
                      <h3 className="text-[18px] font-bold text-foreground">{proj.project_name}</h3>
                      <p className="text-[14px] text-emerald-600 font-medium pt-0.5"><strong className="text-foreground">Strengths:</strong> {proj.strengths}</p>
                    </div>
                    <button
                      onClick={() => toggleProjectExpand(idx)}
                      className="px-3 py-1.5 rounded-xl text-[13px] font-bold bg-secondary text-foreground hover:bg-secondary/80 transition-colors flex items-center gap-1"
                    >
                      <span>{isExpanded ? "Collapse Audit" : "Full 11-Point Review"}</span>
                      {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                    </button>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-[14px]">
                    <div className="p-3 rounded-xl bg-secondary/15 border border-border">
                      <span className="font-bold text-muted-foreground block text-[11px] uppercase tracking-wider">Business Impact:</span>
                      <p className="text-foreground">{proj.missing_business_impact}</p>
                    </div>
                    <div className="p-3 rounded-xl bg-secondary/15 border border-border">
                      <span className="font-bold text-muted-foreground block text-[11px] uppercase tracking-wider">Metrics to Add:</span>
                      <p className="text-foreground">{proj.missing_metrics}</p>
                    </div>
                  </div>

                  {isExpanded && (
                    <div className="pt-4 border-t border-border/60 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 text-[13px] animate-fade-in">
                      <div className="p-3 rounded-xl bg-secondary/10 border border-border/60">
                        <span className="font-bold text-primary block text-[11px] uppercase tracking-wider mb-1">Deployment</span>
                        <p className="text-foreground">{proj.deployment_improvements}</p>
                      </div>
                      <div className="p-3 rounded-xl bg-secondary/10 border border-border/60">
                        <span className="font-bold text-primary block text-[11px] uppercase tracking-wider mb-1">Architecture</span>
                        <p className="text-foreground">{proj.architecture_improvements}</p>
                      </div>
                      <div className="p-3 rounded-xl bg-secondary/10 border border-border/60">
                        <span className="font-bold text-primary block text-[11px] uppercase tracking-wider mb-1">Testing</span>
                        <p className="text-foreground">{proj.testing_improvements}</p>
                      </div>
                      <div className="p-3 rounded-xl bg-secondary/10 border border-border/60">
                        <span className="font-bold text-primary block text-[11px] uppercase tracking-wider mb-1">Documentation</span>
                        <p className="text-foreground">{proj.documentation_improvements}</p>
                      </div>
                      <div className="p-3 rounded-xl bg-secondary/10 border border-border/60">
                        <span className="font-bold text-primary block text-[11px] uppercase tracking-wider mb-1">Security</span>
                        <p className="text-foreground">{proj.security_improvements}</p>
                      </div>
                      <div className="p-3 rounded-xl bg-secondary/10 border border-border/60">
                        <span className="font-bold text-primary block text-[11px] uppercase tracking-wider mb-1">Performance</span>
                        <p className="text-foreground">{proj.performance_improvements}</p>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Experience Deep-Dive Recruiter Review */}
      {recs?.experience && recs.experience.length > 0 && (
        <div className="p-8 rounded-3xl border border-border bg-card shadow-sm space-y-6">
          <div className="flex items-center gap-3 border-b border-border pb-6">
            <div className="p-3 bg-primary/10 rounded-2xl text-primary border border-primary/20">
              <Briefcase className="h-6 w-6" />
            </div>
            <div>
              <h2 className="text-[22px] font-bold text-foreground">Experience Recruiter Audit ({recs.experience.length})</h2>
              <p className="text-[14px] text-muted-foreground">Action verbs, metric framing, & ownership review for every role</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {recs.experience.map((exp, idx) => (
              <div key={idx} className="p-6 rounded-2xl border border-border bg-card space-y-4 shadow-sm flex flex-col justify-between">
                <div className="space-y-3">
                  <div>
                    <h3 className="text-[18px] font-bold text-foreground">{exp.role}</h3>
                    <p className="text-[14px] text-muted-foreground font-semibold">{exp.company}</p>
                  </div>

                  <div className="space-y-2 text-[13px]">
                    <div className="p-3 rounded-xl bg-secondary/15 border border-border">
                      <strong className="text-foreground block text-[11px] uppercase tracking-wider text-primary">Action Verbs:</strong>
                      <p className="text-foreground">{exp.action_verbs}</p>
                    </div>
                    <div className="p-3 rounded-xl bg-secondary/15 border border-border">
                      <strong className="text-foreground block text-[11px] uppercase tracking-wider text-primary">Quantified Achievements:</strong>
                      <p className="text-foreground">{exp.quantified_achievements}</p>
                    </div>
                    <div className="p-3 rounded-xl bg-secondary/15 border border-border">
                      <strong className="text-foreground block text-[11px] uppercase tracking-wider text-primary">Business Impact & Ownership:</strong>
                      <p className="text-foreground">{exp.business_impact} {exp.ownership}</p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Skills Gap Priority Matrix */}
      {recs?.skills && recs.skills.length > 0 && (
        <div className="p-8 rounded-3xl border border-border bg-card shadow-sm space-y-6">
          <div className="flex items-center gap-3 border-b border-border pb-6">
            <div className="p-3 bg-primary/10 rounded-2xl text-primary border border-primary/20">
              <Layers className="h-6 w-6" />
            </div>
            <div>
              <h2 className="text-[22px] font-bold text-foreground">Skills Gap Learning Matrix</h2>
              <p className="text-[14px] text-muted-foreground">Compare detected skills against missing target requirements</p>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-border text-[12px] font-bold text-muted-foreground uppercase tracking-wider">
                  <th className="py-3 px-4">Missing Skill</th>
                  <th className="py-3 px-4">Priority</th>
                  <th className="py-3 px-4">Difficulty</th>
                  <th className="py-3 px-4">Est. Learning Time</th>
                  <th className="py-3 px-4">Recruiter Rationale</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border text-[14px]">
                {recs.skills.map((s, idx) => {
                  const pStyle = getPriorityStyle(s.learning_priority);
                  return (
                    <tr key={idx} className="hover:bg-secondary/20 transition-colors">
                      <td className="py-3.5 px-4 font-bold text-foreground">{s.skill}</td>
                      <td className="py-3.5 px-4">
                        <span className={`px-2.5 py-0.5 rounded-full text-[12px] font-extrabold border ${pStyle.badge}`}>
                          {s.learning_priority}
                        </span>
                      </td>
                      <td className="py-3.5 px-4 font-medium text-foreground">{s.difficulty}</td>
                      <td className="py-3.5 px-4 font-mono text-muted-foreground">{s.estimated_learning_time}</td>
                      <td className="py-3.5 px-4 text-muted-foreground">{s.reason}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Collapsible Section Evidence Drawer */}
      <div className="space-y-6">
        <h3 className="text-[20px] sm:text-[22px] font-bold flex items-center gap-2">
          <Eye className="h-5.5 w-5.5 text-primary" />
          <span>Extracted Resume Evidence Drawer</span>
        </h3>
        <div className="border border-border rounded-2xl bg-card overflow-hidden divide-y divide-border shadow-sm">
          {sectionsList.map((sec) => {
            const confidence = data.explanations?.sections?.[sec.key]?.confidence || 0;
            const structured = data.explanations?.sections_structured;

            let hasContent = false;
            if (structured) {
              if (sec.key === "summary" && structured.summary?.content) hasContent = true;
              if (sec.key === "education" && structured.education?.degree) hasContent = true;
              if (sec.key === "experience" && structured.experience && structured.experience.length > 0) hasContent = true;
              if (sec.key === "projects" && structured.projects && structured.projects.length > 0) hasContent = true;
              if (sec.key === "skills" && structured.skills && Object.values(structured.skills).some(arr => arr.length > 0)) hasContent = true;
              if (sec.key === "certifications" && structured.certifications && structured.certifications.length > 0) hasContent = true;
              if (sec.key === "achievements" && structured.achievements && structured.achievements.length > 0) hasContent = true;
            }

            if (!hasContent) return null;
            const isOpen = !!openEvidence[sec.key];

            return (
              <div key={sec.key} className="w-full">
                <button
                  onClick={() => toggleEvidence(sec.key)}
                  className="w-full px-6 py-4 flex justify-between items-center text-[15px] font-bold hover:bg-secondary/20 transition-all text-left"
                >
                  <div className="flex items-center gap-3">
                    <span className="capitalize">{sec.label}</span>
                    <span className="px-2.5 py-0.5 rounded text-[11px] font-bold border border-primary/20 bg-primary/10 text-primary">
                      {confidence}% Confidence
                    </span>
                  </div>
                  {isOpen ? <ChevronUp className="h-5 w-5" /> : <ChevronDown className="h-5 w-5" />}
                </button>
                {isOpen && (
                  <div className="px-6 pb-5 pt-2 bg-secondary/5 text-[14px]">
                    {sec.key === "summary" && <p className="text-foreground leading-relaxed">{structured?.summary?.content}</p>}
                    {sec.key === "education" && (
                      <p className="text-foreground">Degree: <strong>{structured?.education?.degree}</strong> | Institution: <strong>{structured?.education?.college}</strong> | GPA: <strong>{structured?.education?.cgpa}</strong></p>
                    )}
                    {sec.key === "experience" && (
                      <ul className="list-disc pl-5 space-y-1 text-muted-foreground">
                        {structured?.experience?.map((e: any, idx: number) => (
                          <li key={idx}><strong>{e.role}</strong> at {e.company} ({e.duration})</li>
                        ))}
                      </ul>
                    )}
                    {sec.key === "projects" && (
                      <ul className="list-disc pl-5 space-y-1 text-muted-foreground">
                        {structured?.projects?.map((p: any, idx: number) => (
                          <li key={idx}><strong>{p.name}</strong> - {p.description}</li>
                        ))}
                      </ul>
                    )}
                    {sec.key === "certifications" && (
                      <ul className="list-disc pl-5 space-y-1 text-muted-foreground">
                        {structured?.certifications?.map((c: string, idx: number) => (
                          <li key={idx}>{c}</li>
                        ))}
                      </ul>
                    )}
                    {sec.key === "achievements" && (
                      <ul className="list-disc pl-5 space-y-1 text-muted-foreground">
                        {structured?.achievements?.map((a: any, idx: number) => (
                          <li key={idx}><strong>{a.title}</strong> - {a.event} ({a.year})</li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Curated Skills Bridge Courses */}
      <div className="rounded-3xl border border-border bg-card p-8 space-y-6 shadow-sm">
        <h3 className="text-[20px] font-bold flex items-center gap-2 text-foreground">
          <BookOpen className="h-5.5 w-5.5 text-primary" />
          <span>Curated Learning Resources</span>
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {data.learning_recommendations.length > 0 ? (
            data.learning_recommendations.map((rec, idx) => (
              <a
                key={idx}
                href={rec.resource_url}
                target="_blank"
                rel="noopener noreferrer"
                className="p-5 bg-secondary/30 hover:bg-secondary/60 border border-border rounded-2xl flex flex-col justify-between items-start gap-4 transition-all group shadow-sm hover:shadow"
              >
                <div className="space-y-1.5">
                  <span className="text-[12px] font-bold text-primary uppercase tracking-wider block">{rec.skill} Path</span>
                  <span className="font-bold text-foreground text-[15px] leading-snug line-clamp-2">{rec.resource_name}</span>
                </div>
                <div className="w-full flex justify-between items-center pt-2.5 border-t border-border/60 text-[13px] font-semibold text-muted-foreground group-hover:text-primary transition-colors">
                  <span>Official Documentation</span>
                  <ExternalLink className="h-4 w-4" />
                </div>
              </a>
            ))
          ) : (
            <div className="col-span-full p-8 text-center border border-dashed border-border rounded-2xl text-muted-foreground text-[15px]">
              Skills coverage matches expectations. No further resources required.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
