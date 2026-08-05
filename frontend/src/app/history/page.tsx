"use client";
import React, { useEffect, useState } from "react";
import Link from "next/link";
import axios from "axios";
import { History, Eye, Search, AlertCircle, FileText } from "lucide-react";

interface HistoryRecord {
  id: string;
  resume_id: string;
  job_title: string;
  role_match_percentage: number;
  created_at: string;
  filename: string;
}

import { getApiBaseUrl } from "@/lib/api";

export default function HistoryPage() {
  const [records, setRecords] = useState<HistoryRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await axios.get(`${getApiBaseUrl()}/api/v1/history`);
        setRecords(res.data);
      } catch (err) {
        setError("Failed to retrieve analysis history.");
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  const filtered = records.filter(
    (r) =>
      r.job_title.toLowerCase().includes(search.toLowerCase()) ||
      r.filename.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="max-w-6xl mx-auto px-4 py-16 sm:px-6 lg:px-8 animate-fade-in w-full">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-10">
        <div>
          <h1 className="text-4xl font-extrabold text-foreground tracking-tight flex items-center gap-2">
            <History className="h-8 w-8 text-primary" />
            <span>Evaluation History</span>
          </h1>
          <p className="mt-2 text-muted-foreground text-sm">
            Access previous resume evaluations and matching metrics profiles.
          </p>
        </div>
        <div className="relative w-full sm:w-80">
          <span className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-muted-foreground">
            <Search className="h-4 w-4" />
          </span>
          <input
            type="text"
            placeholder="Search role or filename..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-4 py-2 border border-border rounded-lg bg-card text-foreground text-sm focus:outline-none focus:border-primary transition-colors"
          />
        </div>
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-20 bg-card border border-border rounded-xl">
          <div className="h-10 w-10 border-4 border-primary/20 border-t-primary rounded-full animate-spin"></div>
        </div>
      ) : error ? (
        <div className="p-6 bg-accent/10 border border-accent/20 rounded-xl text-accent text-sm flex items-center gap-3">
          <AlertCircle className="h-5 w-5" />
          <span>{error}</span>
        </div>
      ) : filtered.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 bg-card border border-border rounded-xl text-center">
          <FileText className="h-12 w-12 text-muted-foreground/60 mb-4" />
          <h3 className="text-lg font-bold text-foreground">No Records Found</h3>
          <p className="text-sm text-muted-foreground mt-1 max-w-xs mx-auto">
            Upload your first resume in the upload panel to see evaluations here.
          </p>
          <Link
            href="/upload"
            className="mt-6 inline-flex items-center justify-center px-4 py-2 text-sm font-semibold rounded-lg text-primary-foreground bg-primary hover:bg-primary/90 transition-all shadow"
          >
            Analyze Resume
          </Link>
        </div>
      ) : (
        <div className="overflow-x-auto border border-border rounded-xl bg-card">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-border bg-secondary/50 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                <th className="px-6 py-4">Target Job Role</th>
                <th className="px-6 py-4">Original Filename</th>
                <th className="px-6 py-4">Match %</th>
                <th className="px-6 py-4">Evaluation Date</th>
                <th className="px-6 py-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border text-sm text-foreground">
              {filtered.map((record) => (
                <tr key={record.id} className="hover:bg-secondary/20 transition-colors">
                  <td className="px-6 py-4 font-semibold">{record.job_title}</td>
                  <td className="px-6 py-4 text-muted-foreground font-mono text-xs">{record.filename}</td>
                  <td className="px-6 py-4">
                    <span
                      className={`inline-flex px-2 py-1 rounded text-xs font-bold ${
                        record.role_match_percentage >= 80
                          ? "bg-green-500/10 text-green-500 border border-green-500/20"
                          : record.role_match_percentage >= 50
                          ? "bg-amber-500/10 text-amber-500 border border-amber-500/20"
                          : "bg-red-500/10 text-red-500 border border-red-500/20"
                      }`}
                    >
                      {record.role_match_percentage}%
                    </span>
                  </td>
                  <td className="px-6 py-4 text-muted-foreground">
                    {new Date(record.created_at).toLocaleDateString(undefined, {
                      year: "numeric",
                      month: "short",
                      day: "numeric"
                    })}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <Link
                      href={`/dashboard/${record.id}`}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-border text-xs font-semibold hover:bg-secondary transition-colors"
                    >
                      <Eye className="h-3.5 w-3.5" />
                      <span>View Report</span>
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
