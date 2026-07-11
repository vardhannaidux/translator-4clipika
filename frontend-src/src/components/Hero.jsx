import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, ArrowRight } from 'lucide-react';
import Scene3D from './Scene3D';

export default function Hero() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15,
        delayChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 30, filter: 'blur(10px)' },
    visible: {
      opacity: 1,
      y: 0,
      filter: 'blur(0px)',
      transition: { type: 'spring', damping: 20, stiffness: 100 },
    },
  };

  return (
    <section className="relative min-h-[85vh] flex items-center justify-center overflow-hidden py-12 md:py-24">
      {/* 3D Scene Viewport */}
      <Scene3D />

      <div className="max-w-4xl mx-auto text-center px-4 z-10 select-none">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="flex flex-col items-center gap-6"
        >
          {/* Sparkles Badge */}
          <motion.div variants={itemVariants}>
            <span className="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-full text-xs font-bold bg-blue-500/10 dark:bg-blue-500/10 border border-blue-500/20 text-blue-600 dark:text-blue-400 backdrop-blur-md shadow-sm">
              <Sparkles className="w-3.5 h-3.5 animate-pulse" /> Newsroom-Grade Translation Engine
            </span>
          </motion.div>

          {/* Large Headline */}
          <motion.h2
            variants={itemVariants}
            className="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight text-slate-900 dark:text-white leading-[1.1] md:leading-[1.15]"
          >
            Cinematic Bi-Directional <br />
            <span className="bg-gradient-to-r from-blue-600 via-indigo-500 to-purple-500 bg-clip-text text-transparent">
              Telugu Font Converter
            </span>
          </motion.h2>

          {/* AI-Inspired Subtitle */}
          <motion.p
            variants={itemVariants}
            className="max-w-2xl text-base sm:text-lg text-slate-500 dark:text-slate-400 leading-relaxed font-semibold"
          >
            A world-class, premium transdecoding system designed to translate legacy Eenadu 4C Lipika visual mapping sequences to Telugu Unicode and back. Preserves styles, runs, and layouts.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div variants={itemVariants} className="flex flex-wrap items-center justify-center gap-4 mt-4">
            <a
              href="#translator"
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-2xl font-bold flex items-center gap-2 shadow-lg shadow-blue-500/25 hover:shadow-indigo-500/30 hover:scale-103 active:scale-97 transition-all duration-200 cursor-pointer"
            >
              Get Started <ArrowRight className="w-4 h-4" />
            </a>
            <a
              href="#about"
              className="px-8 py-4 bg-white/40 dark:bg-slate-900/40 border border-white/10 dark:border-slate-800/80 backdrop-blur-md hover:bg-white/60 dark:hover:bg-slate-800 text-slate-800 dark:text-slate-200 rounded-2xl font-bold hover:scale-103 active:scale-97 transition-all duration-200 cursor-pointer"
            >
              How It Works
            </a>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
