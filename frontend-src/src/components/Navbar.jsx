import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Languages, Sun, Moon, Info, Shield, HelpCircle, Code } from 'lucide-react';

const GithubIcon = ({ className }) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4" />
    <path d="M9 18c-4.51 2-5-2-7-2" />
  </svg>
);

export default function Navbar({ theme, setTheme }) {
  const [hoveredLink, setHoveredLink] = useState(null);

  const links = [
    { name: 'Translator', href: '#translator', icon: Languages },
    { name: 'About', href: '#about', icon: Info },
    { name: 'GitHub', href: 'https://github.com/vardhan30016/EEnadu_Translator', icon: GithubIcon, external: true }
  ];

  return (
    <header className="sticky top-0 z-40 w-full bg-white/40 dark:bg-slate-950/40 border-b border-white/10 dark:border-slate-900/40 backdrop-blur-xl transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-18 flex items-center justify-between">
        
        {/* Brand Logo */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center text-white shadow-lg shadow-blue-500/25">
            <Languages className="w-5 h-5" />
          </div>
          <div>
            <h1 className="font-sans font-bold text-base leading-tight tracking-tight text-slate-900 dark:text-white">
              Eenadu 4C Lipika
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">
              High-fidelity newsroom translator • Developed by Vardhan Naidu
            </p>
          </div>
        </div>

        {/* Navigation Actions */}
        <div className="flex items-center gap-2 sm:gap-4">
          <nav className="hidden md:flex items-center gap-1">
            {links.map((link) => {
              const Icon = link.icon;
              return (
                <a
                  key={link.name}
                  href={link.href}
                  target={link.external ? '_blank' : '_self'}
                  rel={link.external ? 'noopener noreferrer' : ''}
                  onMouseEnter={() => setHoveredLink(link.name)}
                  onMouseLeave={() => setHoveredLink(null)}
                  className="relative px-3.5 py-2 text-sm font-semibold text-slate-600 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 flex items-center gap-1.5 transition-colors duration-200"
                >
                  <Icon className="w-4 h-4" />
                  <span>{link.name}</span>

                  {/* Active background hover pill */}
                  {hoveredLink === link.name && (
                    <motion.span
                      layoutId="navHover"
                      className="absolute inset-0 rounded-xl bg-slate-200/50 dark:bg-slate-800/50 -z-10"
                      transition={{ type: 'spring', stiffness: 350, damping: 25 }}
                    />
                  )}
                </a>
              );
            })}
          </nav>

          <div className="h-5 w-[1px] bg-slate-200 dark:bg-slate-800 hidden md:block" />

          {/* Theme Toggle */}
          <button
            onClick={() => setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'))}
            className="p-2.5 rounded-xl border border-slate-200 dark:border-slate-850 bg-white/60 dark:bg-slate-900/60 text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/80 hover:text-slate-900 dark:hover:text-white shadow-sm hover:scale-105 active:scale-95 transition-all duration-200 cursor-pointer"
            aria-label="Toggle theme"
          >
            {theme === 'dark' ? <Sun className="w-4.5 h-4.5" /> : <Moon className="w-4.5 h-4.5" />}
          </button>
        </div>
      </div>
    </header>
  );
}
