import React from "react";
import Link from "next/link";
import { Sparkles } from "lucide-react";

export default function Footer() {
  return (
    <footer className="border-t border-border bg-card text-muted-foreground mt-auto">
      <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-foreground font-semibold">
            <Sparkles className="h-5 w-5 text-primary" />
            <span>RoleMatch AI</span>
          </div>
          <p className="text-xs text-muted-foreground/60">
            &copy; 2026 RoleMatch AI. All rights reserved. Built for professional portfolios.
          </p>
          <div className="flex gap-6 text-sm">
            <Link href="/about" className="hover:text-foreground transition-colors">
              About
            </Link>
            <Link href="/features" className="hover:text-foreground transition-colors">
              Features
            </Link>
            <a href="/#" className="hover:text-foreground transition-colors">
              Privacy
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
