"use client";
import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Sun, Moon, Sparkles } from "lucide-react";
import { useTheme } from "./ThemeProvider";

export default function Navbar() {
  const pathname = usePathname();
  const { theme, toggleTheme } = useTheme();

  const links = [
    { href: "/features", label: "Features" },
    { href: "/about", label: "About" },
    { href: "/upload", label: "Analyze" },
    { href: "/history", label: "History" },
    { href: "/settings", label: "Settings" }
  ];

  return (
    <header className="sticky top-0 z-50 glass-nav shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex items-center gap-2.5 text-foreground font-bold tracking-tight">
              <img src="/icon.svg" alt="RoleMatch AI Logo" className="h-7 w-7 rounded-lg shadow-sm" />
              <span className="bg-gradient-to-r from-primary to-purple-500 bg-clip-text text-transparent">RoleMatch AI</span>
            </Link>
          </div>
          <nav className="hidden md:flex items-center space-x-8">
            {links.map((link) => {
              const active = pathname === link.href;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`text-sm font-medium transition-colors hover:text-primary ${
                    active ? "text-primary font-semibold" : "text-muted-foreground"
                  }`}
                >
                  {link.label}
                </Link>
              );
            })}
          </nav>
          <div className="flex items-center gap-4">
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
            >
              {theme === "light" ? <Moon className="h-5 w-5" /> : <Sun className="h-5 w-5" />}
            </button>
            <Link
              href="/upload"
              className="hidden sm:inline-flex items-center justify-center px-4 py-2 text-sm font-medium rounded-lg text-primary-foreground bg-primary hover:bg-primary/90 transition-all shadow"
            >
              Analyze Resume
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}
