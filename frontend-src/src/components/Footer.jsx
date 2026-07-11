import React from 'react';

export default function Footer() {
  return (
    <footer className="w-full bg-white/40 dark:bg-slate-950/40 border-t border-white/10 dark:border-slate-900/40 py-8 backdrop-blur-xl transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-slate-500 dark:text-slate-400 font-semibold">
        <p>© 2026 Eenadu 4C Lipika Translator Suite • Developed by Vardhan Naidu • Production Stable v60.0</p>
        <div className="flex items-center gap-6">
          <a
            href="https://github.com/vardhan30016/EEnadu_Translator"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-slate-850 dark:hover:text-white transition-colors duration-200"
          >
            GitHub Repo
          </a>
          <a
            href="https://github.com/vardhan30016/EEnadu_Translator/blob/main/LICENSE"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-slate-850 dark:hover:text-white transition-colors duration-200"
          >
            MIT License
          </a>
        </div>
      </div>
    </footer>
  );
}
