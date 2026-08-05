import React from "react";
import Link from "next/link";
import { AlertCircle, ArrowLeft } from "lucide-react";

export default function NotFound() {
  return (
    <div className="flex-1 flex flex-col items-center justify-center min-h-[60vh] px-4 text-center animate-fade-in">
      <div className="p-8 max-w-md w-full rounded-2xl glass border border-border flex flex-col items-center">
        <div className="p-3 bg-accent/10 rounded-full mb-6">
          <AlertCircle className="h-12 w-12 text-accent" />
        </div>
        <h1 className="text-4xl font-extrabold text-foreground tracking-tight mb-2">404</h1>
        <h2 className="text-lg font-bold text-foreground mb-4">Page Not Found</h2>
        <p className="text-sm text-muted-foreground leading-relaxed mb-8">
          The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.
        </p>
        <Link
          href="/"
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg text-primary-foreground bg-primary hover:bg-primary/90 font-semibold text-sm shadow transition-all"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Back to Home</span>
        </Link>
      </div>
    </div>
  );
}
