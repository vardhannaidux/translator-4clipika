import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, FileText, CheckCircle, Database } from 'lucide-react';

export default function AboutSection() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.15 }
    }
  };

  const cardVariants = {
    hidden: { opacity: 0, y: 25 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { type: 'spring', stiffness: 100, damping: 20 }
    }
  };

  return (
    <section id="about" className="py-16 md:py-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      <motion.div
        variants={containerVariants}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: '-100px' }}
        className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center bg-white/40 dark:bg-slate-900/30 rounded-3xl border border-white/20 dark:border-slate-800/80 p-8 md:p-12 backdrop-blur-xl shadow-xl"
      >
        
        {/* Info Column */}
        <div className="flex flex-col gap-5">
          <motion.div variants={cardVariants}>
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-blue-500/10 dark:bg-blue-500/10 border border-blue-500/20 text-blue-600 dark:text-blue-400">
              Technical Overview
            </span>
          </motion.div>
          <motion.h3 variants={cardVariants} className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
            How The Engine Works
          </motion.h3>
          <motion.p variants={cardVariants} className="text-sm sm:text-base text-slate-500 dark:text-slate-400 leading-relaxed font-semibold">
            Historically, newsrooms like *Eenadu* composed content using CP1252-based font layers (like 4C Lipika) that mapped English characters visually onto Telugu glyphs. While this worked for print layouts, the raw text remains unsearchable and unreadable on standard digital platforms.
          </motion.p>
          <motion.p variants={cardVariants} className="text-sm sm:text-base text-slate-500 dark:text-slate-400 leading-relaxed font-semibold">
            This translator executes high-fidelity, bi-directional transdecoding. It translates visual font bytes to and from Telugu Unicode, correcting complex conjunct consonants, trailing loops, and spelling overlaps automatically.
          </motion.p>
        </div>

        {/* Feature Cards Column */}
        <div className="flex flex-col gap-6">
          
          {/* Card 1 */}
          <motion.div
            variants={cardVariants}
            whileHover={{ y: -5, scale: 1.01 }}
            className="p-5 rounded-2xl border border-slate-200/50 dark:border-slate-800 bg-white/60 dark:bg-slate-950/40 backdrop-blur-md shadow-sm transition-all duration-200"
          >
            <div className="flex gap-4">
              <div className="w-11 h-11 rounded-xl bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center flex-shrink-0 shadow-inner">
                <Sparkles className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-slate-900 dark:text-white">Editorial Overrides</h4>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 font-medium leading-relaxed">
                  Integrates dictionary spellcheck mappings explicitly optimized for print typography runs.
                </p>
              </div>
            </div>
          </motion.div>

          {/* Card 2 */}
          <motion.div
            variants={cardVariants}
            whileHover={{ y: -5, scale: 1.01 }}
            className="p-5 rounded-2xl border border-slate-200/50 dark:border-slate-800 bg-white/60 dark:bg-slate-950/40 backdrop-blur-md shadow-sm transition-all duration-200"
          >
            <div className="flex gap-4">
              <div className="w-11 h-11 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center flex-shrink-0 shadow-inner">
                <FileText className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-slate-900 dark:text-white">Word Run Preservation</h4>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 font-medium leading-relaxed">
                  Processes paragraph segments individually inside Microsoft Word `.docx` documents, ensuring that inline styling and colors remain perfectly preserved.
                </p>
              </div>
            </div>
          </motion.div>

          {/* Card 3 */}
          <motion.div
            variants={cardVariants}
            whileHover={{ y: -5, scale: 1.01 }}
            className="p-5 rounded-2xl border border-slate-200/50 dark:border-slate-800 bg-white/60 dark:bg-slate-950/40 backdrop-blur-md shadow-sm transition-all duration-200"
          >
            <div className="flex gap-4">
              <div className="w-11 h-11 rounded-xl bg-purple-500/10 text-purple-600 dark:text-purple-400 flex items-center justify-center flex-shrink-0 shadow-inner">
                <Database className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-slate-900 dark:text-white">Consolidated Mappings</h4>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 font-medium leading-relaxed">
                  Utilizes a single, unified mapping cache file to translate complex syllables, removing random inconsistencies.
                </p>
              </div>
            </div>
          </motion.div>

        </div>

      </motion.div>
    </section>
  );
}
