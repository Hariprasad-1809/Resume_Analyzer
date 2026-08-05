"use client";
import React, { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useDropzone } from "react-dropzone";
import axios from "axios";
import { UploadCloud, FileText, AlertCircle, Sparkles } from "lucide-react";

export default function UploadPage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [jobTitle, setJobTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [roles, setRoles] = useState<string[]>([]);
  const [customRole, setCustomRole] = useState("");

  const getApiUrl = () => {
    if (typeof window !== "undefined") {
      return localStorage.getItem("settings_api_url") || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    }
    return process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  };

  useEffect(() => {
    const fetchRoles = async () => {
      try {
        const res = await axios.get(`${getApiUrl()}/api/v1/resume/roles`);
        setRoles(res.data);
      } catch (err) {
        setRoles(["Software Engineer", "Frontend Developer", "Backend Developer", "Data Scientist", "DevOps Engineer"]);
      }
    };
    fetchRoles();
  }, []);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setError(null);
    if (acceptedFiles.length > 0) {
      const selected = acceptedFiles[0];
      if (selected.type !== "application/pdf") {
        setError("Only PDF files are supported.");
        return;
      }
      if (selected.size > 5 * 1024 * 1024) {
        setError("File size exceeds 5MB limit.");
        return;
      }
      setFile(selected);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "application/pdf": [".pdf"] },
    maxFiles: 1
  });

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError("Please upload your resume.");
      return;
    }
    const selectedTitle = jobTitle === "other" ? customRole : jobTitle;
    if (!selectedTitle.trim()) {
      setError("Please specify a target job title.");
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_title", selectedTitle);

    try {
      const res = await axios.post(`${getApiUrl()}/api/v1/resume/analyze`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      router.push(`/dashboard/${res.data.id}`);
    } catch (err: any) {
      const msg = err.response?.data?.detail || "Connection failure or invalid file structure.";
      setError(msg);
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-16 sm:px-6 lg:px-8 animate-fade-in">
      <div className="text-center mb-10">
        <h1 className="text-4xl font-extrabold text-foreground tracking-tight">Upload Resume</h1>
        <p className="mt-2 text-muted-foreground text-sm">
          Select a target job role and upload your resume PDF to begin evaluation.
        </p>
      </div>

      <div className="bg-card border border-border rounded-2xl p-6 sm:p-8 relative">
        {loading ? (
          <div className="flex flex-col items-center justify-center py-16 text-center">
            <div className="h-12 w-12 border-4 border-primary/20 border-t-primary rounded-full animate-spin mb-6"></div>
            <h3 className="text-lg font-bold text-foreground flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-primary animate-pulse" />
              <span>Analyzing Resume Profile...</span>
            </h3>
            <p className="text-xs text-muted-foreground mt-2 max-w-sm">
              Parsing PDF layout structure, matching skills models, and running embedding alignments.
            </p>
          </div>
        ) : (
          <form onSubmit={handleAnalyze} className="space-y-6">
            {error && (
              <div className="p-4 bg-accent/10 border border-accent/20 rounded-lg text-accent text-sm flex items-center gap-3">
                <AlertCircle className="h-5 w-5 flex-shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <div className="space-y-2">
              <label className="text-sm font-medium text-muted-foreground">Target Job Title</label>
              <select
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
                className="w-full px-4 py-2 border border-border rounded-lg bg-background text-foreground text-sm focus:outline-none focus:border-primary transition-colors"
                required
              >
                <option value="">-- Choose Job Role --</option>
                {roles.map((role, index) => (
                  <option key={index} value={role}>
                    {role}
                  </option>
                ))}
                <option value="other">Other (Write in...)</option>
              </select>
            </div>

            {jobTitle === "other" && (
              <div className="space-y-2 animate-fade-in">
                <label className="text-sm font-medium text-muted-foreground">Specify Custom Job Title</label>
                <input
                  type="text"
                  value={customRole}
                  onChange={(e) => setCustomRole(e.target.value)}
                  placeholder="e.g. Senior Machine Learning Engineer"
                  className="w-full px-4 py-2 border border-border rounded-lg bg-background text-foreground text-sm focus:outline-none focus:border-primary transition-colors"
                  required
                />
              </div>
            )}

            <div className="space-y-2">
              <label className="text-sm font-medium text-muted-foreground">Resume File (PDF)</label>
              <div
                {...getRootProps()}
                className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all ${
                  isDragActive
                    ? "border-primary bg-primary/5 scale-[0.99]"
                    : "border-border hover:border-primary/50 hover:bg-secondary/40"
                }`}
              >
                <input {...getInputProps()} />
                <div className="flex flex-col items-center">
                  <UploadCloud className="h-12 w-12 text-muted-foreground mb-4" />
                  {file ? (
                    <div className="flex items-center gap-2 text-primary font-semibold text-sm">
                      <FileText className="h-5 w-5" />
                      <span>{file.name}</span>
                    </div>
                  ) : (
                    <>
                      <p className="text-sm text-foreground font-semibold">
                        Drag & Drop or <span className="text-primary underline">Browse File</span>
                      </p>
                      <p className="text-xs text-muted-foreground/80 mt-1">PDF format only. Max 5MB.</p>
                    </>
                  )}
                </div>
              </div>
            </div>

            <button
              type="submit"
              className="w-full inline-flex items-center justify-center px-6 py-3 rounded-lg text-primary-foreground bg-primary hover:bg-primary/90 transition-all font-semibold text-sm shadow cursor-pointer"
            >
              Analyze Resume
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
