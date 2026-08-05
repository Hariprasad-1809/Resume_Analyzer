"use client";
import React, { useEffect, useState } from "react";
import { Sliders, Save, Database, Shield } from "lucide-react";

import { getApiBaseUrl } from "@/lib/api";

export default function SettingsPage() {
  const [apiUrl, setApiUrl] = useState("https://resume-analyzer-gqte.onrender.com");
  const [skillWeight, setSkillWeight] = useState(40);
  const [expWeight, setExpWeight] = useState(25);
  const [projWeight, setProjWeight] = useState(15);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    const url = localStorage.getItem("settings_api_url") || getApiBaseUrl();
    const skill = localStorage.getItem("settings_skill_weight") || "40";
    const exp = localStorage.getItem("settings_exp_weight") || "25";
    const proj = localStorage.getItem("settings_proj_weight") || "15";

    setApiUrl(url);
    setSkillWeight(parseInt(skill));
    setExpWeight(parseInt(exp));
    setProjWeight(parseInt(proj));
  }, []);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    localStorage.setItem("settings_api_url", apiUrl);
    localStorage.setItem("settings_skill_weight", skillWeight.toString());
    localStorage.setItem("settings_exp_weight", expWeight.toString());
    localStorage.setItem("settings_proj_weight", projWeight.toString());

    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-16 sm:px-6 lg:px-8 animate-fade-in">
      <div className="mb-10">
        <h1 className="text-4xl font-extrabold text-foreground tracking-tight">Configuration Settings</h1>
        <p className="mt-2 text-muted-foreground text-sm">
          Customize matching calculation parameters and backend environments.
        </p>
      </div>

      <form onSubmit={handleSave} className="space-y-8 bg-card border border-border rounded-xl p-6 sm:p-8">
        <div className="space-y-4">
          <h3 className="text-lg font-bold text-foreground flex items-center gap-2">
            <Database className="h-5 w-5 text-primary" />
            <span>Connection Profile</span>
          </h3>
          <div className="space-y-2">
            <label className="text-sm font-medium text-muted-foreground">Backend API Endpoint URL</label>
            <input
              type="text"
              value={apiUrl}
              onChange={(e) => setApiUrl(e.target.value)}
              className="w-full px-4 py-2 border border-border rounded-lg bg-background text-foreground text-sm focus:outline-none focus:border-primary transition-colors"
              required
            />
          </div>
        </div>

        <hr className="border-border" />

        <div className="space-y-6">
          <h3 className="text-lg font-bold text-foreground flex items-center gap-2">
            <Sliders className="h-5 w-5 text-primary" />
            <span>Matching Component Weights</span>
          </h3>
          <p className="text-xs text-muted-foreground">Adjust weights for matching logic percentage.</p>

          <div className="space-y-4">
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="font-medium text-muted-foreground">Skill Overlap Weight</span>
                <span className="font-semibold text-primary">{skillWeight}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                value={skillWeight}
                onChange={(e) => setSkillWeight(parseInt(e.target.value))}
                className="w-full accent-primary bg-secondary h-2 rounded-lg cursor-pointer"
              />
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="font-medium text-muted-foreground">Experience Alignment Weight</span>
                <span className="font-semibold text-primary">{expWeight}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                value={expWeight}
                onChange={(e) => setExpWeight(parseInt(e.target.value))}
                className="w-full accent-primary bg-secondary h-2 rounded-lg cursor-pointer"
              />
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="font-medium text-muted-foreground">Projects Relevance Weight</span>
                <span className="font-semibold text-primary">{projWeight}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                value={projWeight}
                onChange={(e) => setProjWeight(parseInt(e.target.value))}
                className="w-full accent-primary bg-secondary h-2 rounded-lg cursor-pointer"
              />
            </div>
          </div>
        </div>

        <hr className="border-border" />

        <div className="space-y-4">
          <h3 className="text-lg font-bold text-foreground flex items-center gap-2">
            <Shield className="h-5 w-5 text-primary" />
            <span>Privacy Compliance</span>
          </h3>
          <p className="text-xs text-muted-foreground leading-relaxed">
            All analysis data is stored locally in SQLite when PostgreSQL connection values are absent.
          </p>
        </div>

        <div className="flex items-center gap-4 pt-4">
          <button
            type="submit"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg text-primary-foreground bg-primary hover:bg-primary/90 transition-all font-semibold text-sm shadow cursor-pointer"
          >
            <Save className="h-4 w-4" />
            <span>Save Preferences</span>
          </button>
          {saved && (
            <span className="text-xs text-green-500 font-semibold animate-pulse">
              Preferences updated successfully!
            </span>
          )}
        </div>
      </form>
    </div>
  );
}
