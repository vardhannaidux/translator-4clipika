import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Languages,
  Sun,
  Moon,
  Trash2,
  Copy,
  Check,
  UploadCloud,
  FileText,
  X,
  Sparkles,
  ArrowRightLeft,
  Info,
  BookOpen,
  ArrowRight,
  Download,
  AlertCircle
} from 'lucide-react';

const Github = ({ className, ...props }) => (
  <svg
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
    {...props}
  >
    <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4" />
    <path d="M9 18c-4.51 2-5-2-7-2" />
  </svg>
);


// --- RENDER INTERACTIVE BACKGROUND ---
const AnimatedBackground = ({ theme }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let animationFrameId;

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', handleResize);

    const particles = [];
    const particleCount = Math.min(60, Math.floor((width * height) / 25000));
    const isDark = theme === 'dark';

    class Particle {
      constructor() {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.vx = (Math.random() - 0.5) * 0.4;
        this.vy = (Math.random() - 0.5) * 0.4;
        this.radius = Math.random() * 2 + 1;
      }
      update() {
        this.x += this.vx;
        this.y += this.vy;
        if (this.x < 0 || this.x > width) this.vx = -this.vx;
        if (this.y < 0 || this.y > height) this.vy = -this.vy;
      }
      draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = isDark ? 'rgba(59, 130, 246, 0.4)' : 'rgba(37, 99, 235, 0.2)';
        ctx.fill();
      }
    }

    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle());
    }

    let mouseX = null;
    let mouseY = null;

    const handleMouseMove = (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    };

    const handleMouseLeave = () => {
      mouseX = null;
      mouseY = null;
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseleave', handleMouseLeave);

    const animate = () => {
      ctx.clearRect(0, 0, width, height);

      particles.forEach((p) => {
        p.update();
        p.draw();
      });

      const maxDistance = 140;
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < maxDistance) {
            const alpha = (1 - dist / maxDistance) * 0.15;
            ctx.strokeStyle = isDark
              ? `rgba(99, 102, 241, ${alpha})`
              : `rgba(59, 130, 246, ${alpha})`;
            ctx.lineWidth = 0.8;
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.stroke();
          }
        }

        if (mouseX !== null && mouseY !== null) {
          const dx = particles[i].x - mouseX;
          const dy = particles[i].y - mouseY;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 180) {
            const alpha = (1 - dist / 180) * 0.25;
            ctx.strokeStyle = isDark
              ? `rgba(147, 51, 234, ${alpha})`
              : `rgba(99, 102, 241, ${alpha})`;
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(mouseX, mouseY);
            ctx.stroke();
          }
        }
      }

      animationFrameId = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseleave', handleMouseLeave);
      cancelAnimationFrame(animationFrameId);
    };
  }, [theme]);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none -z-20 w-full h-full"
    />
  );
};


function App() {
  // --- STATE ---
  const [theme, setTheme] = useState(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('theme');
      if (saved) return saved;
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    return 'light';
  });

  const [direction, setDirection] = useState('unicode_to_legacy'); // 'unicode_to_legacy' | 'legacy_to_unicode'
  const [activeTab, setActiveTab] = useState('text'); // 'text' | 'file'
  
  // Text translation states
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [editorialMode, setEditorialMode] = useState(false);
  const [isTranslating, setIsTranslating] = useState(false);
  const [stats, setStats] = useState({ chars: 0, words: 0, speedMs: 0 });

  // File translation states
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStatus, setUploadStatus] = useState('idle'); // 'idle' | 'uploading' | 'processing' | 'success' | 'error'
  const [errorMessage, setErrorMessage] = useState('');

  // Toasts
  const [toasts, setToasts] = useState([]);
  const fileInputRef = useRef(null);

  // --- EFFECT: Theme Management ---
  useEffect(() => {
    const root = window.document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
      root.setAttribute('data-theme', 'dark');
    } else {
      root.classList.remove('dark');
      root.setAttribute('data-theme', 'light');
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  // --- TOAST HELPER ---
  const showToast = (message, type = 'info') => {
    const id = Date.now().toString();
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4000);
  };

  // --- TEXT TRANSLATION HANDLING ---
  const handleTranslate = async () => {
    const text = inputText.trim();
    if (!text) {
      showToast('Please enter some text to translate', 'error');
      return;
    }

    setIsTranslating(true);
    try {
      const response = await fetch('/api/translate/text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          direction: direction,
          editorial_mode: direction === 'unicode_to_legacy' ? editorialMode : false,
        }),
      });

      if (response.status === 429) {
        showToast('Rate limit exceeded. Please wait 60 seconds.', 'error');
        return;
      }

      const data = await response.json();
      if (response.ok) {
        setOutputText(data.translated_text);
        setStats({
          chars: data.stats.chars,
          words: text.split(/\s+/).filter(Boolean).length,
          speedMs: data.stats.time_ms,
        });
        showToast('Translation completed', 'success');
      } else {
        showToast(data.detail || 'Translation failed', 'error');
      }
    } catch (error) {
      console.error(error);
      showToast('Network connection error', 'error');
    } finally {
      setIsTranslating(false);
    }
  };

  const handleClearText = () => {
    setInputText('');
    setOutputText('');
    setStats({ chars: 0, words: 0, speedMs: 0 });
    showToast('Text cleared', 'info');
  };

  const handleCopyOutput = () => {
    if (!outputText) {
      showToast('Nothing to copy', 'error');
      return;
    }
    navigator.clipboard.writeText(outputText)
      .then(() => showToast('Copied output to clipboard', 'success'))
      .catch(() => showToast('Failed to copy text', 'error'));
  };

  // --- FILE HANDLING ---
  const handleFileChange = (file) => {
    if (!file) return;
    const ext = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    if (ext !== '.txt' && ext !== '.docx') {
      showToast('Unsupported extension. Only .txt and .docx are permitted.', 'error');
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      showToast('File is too large. Max size is 5MB.', 'error');
      return;
    }
    setSelectedFile(file);
    setUploadStatus('idle');
    setUploadProgress(0);
    setErrorMessage('');
    showToast(`File selected: ${file.name}`, 'info');
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files.length > 0) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    setUploadStatus('idle');
    setUploadProgress(0);
    if (fileInputRef.current) fileInputRef.current.value = '';
    showToast('File removed', 'info');
  };

  const handleTranslateFile = () => {
    if (!selectedFile) return;

    setUploadStatus('uploading');
    setUploadProgress(0);

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('direction', direction);
    formData.append('editorial_mode', direction === 'unicode_to_legacy' ? editorialMode : false);

    const xhr = new XMLHttpRequest();

    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable) {
        const percent = Math.round((e.loaded / e.total) * 100);
        setUploadProgress(percent);
        if (percent >= 100) {
          setUploadStatus('processing');
        }
      }
    });

    xhr.addEventListener('load', () => {
      if (xhr.status === 200) {
        setUploadStatus('success');
        const blob = new Blob([xhr.response], { type: xhr.getResponseHeader('Content-Type') });
        
        let outFilename = `translated_${selectedFile.name}`;
        const disp = xhr.getResponseHeader('Content-Disposition');
        if (disp && disp.indexOf('filename=') !== -1) {
          outFilename = disp.substring(disp.indexOf('filename=') + 9).replace(/['"]/g, '');
        }

        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = outFilename;
        link.click();

        showToast('Document translated and downloaded!', 'success');

        setTimeout(() => {
          handleRemoveFile();
        }, 1500);
      } else if (xhr.status === 429) {
        setUploadStatus('error');
        setErrorMessage('Rate limit exceeded. Please wait a minute.');
        showToast('Rate limit exceeded', 'error');
      } else {
        setUploadStatus('error');
        setErrorMessage('Failed to parse or translate the file.');
        showToast('File translation failed', 'error');
      }
    });

    xhr.addEventListener('error', () => {
      setUploadStatus('error');
      setErrorMessage('Network upload error.');
      showToast('Network error occurred', 'error');
    });

    xhr.open('POST', '/api/translate/file');
    xhr.responseType = 'blob';
    xhr.send(formData);
  };

  // --- STATS LOGIC FOR INPUT ---
  const inputCharCount = inputText.length;
  const inputWordCount = inputText.trim() ? inputText.trim().split(/\s+/).length : 0;

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-800 dark:bg-slate-950 dark:text-slate-200 transition-colors duration-300 relative overflow-hidden">
      <AnimatedBackground theme={theme} />
      
      {/* Toast Notification Stack */}
      <div className="fixed top-4 right-4 z-50 flex flex-col gap-2 max-w-sm w-full pointer-events-none">
        <AnimatePresence>
          {toasts.map((toast) => (
            <motion.div
              key={toast.id}
              initial={{ opacity: 0, y: -20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95, transition: { duration: 0.2 } }}
              className={`p-4 rounded-xl shadow-lg backdrop-blur-md flex items-center gap-3 pointer-events-auto border ${
                toast.type === 'success'
                  ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-600 dark:text-emerald-400'
                  : toast.type === 'error'
                  ? 'bg-rose-500/10 border-rose-500/20 text-rose-600 dark:text-rose-400'
                  : 'bg-blue-500/10 border-blue-500/20 text-blue-600 dark:text-blue-400'
              }`}
            >
              {toast.type === 'error' ? (
                <AlertCircle className="w-5 h-5 flex-shrink-0" />
              ) : (
                <Sparkles className="w-5 h-5 flex-shrink-0" />
              )}
              <span className="text-sm font-medium">{toast.message}</span>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {/* Top Header / Navigation */}
      <header className="sticky top-0 z-30 w-full bg-white/70 dark:bg-slate-900/70 border-b border-slate-100 dark:border-slate-800 backdrop-blur-md transition-colors">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20">
              <Languages className="w-5 h-5" />
            </div>
            <div>
              <h1 className="font-sans font-bold text-lg leading-tight tracking-tight text-slate-900 dark:text-white">
                Eenadu 4C Lipika
              </h1>
              <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">
                High-fidelity newsroom translator • Developed by Vardhan Naidu
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <a
              href="#about"
              className="hidden md:inline-flex items-center gap-1.5 text-sm font-semibold text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white transition-colors"
            >
              <Info className="w-4 h-4" /> About
            </a>
            <a
              href="https://github.com/vardhan30016/EEnadu_Translator"
              target="_blank"
              rel="noopener noreferrer"
              className="hidden md:inline-flex items-center gap-1.5 text-sm font-semibold text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white transition-colors"
            >
              <Github className="w-4 h-4" /> GitHub
            </a>

            <div className="h-4 w-[1px] bg-slate-200 dark:bg-slate-800 hidden md:block" />

            {/* Theme Toggle */}
            <button
              onClick={() => setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'))}
              className="p-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-850 hover:text-slate-900 dark:hover:text-white shadow-sm transition-all"
              aria-label="Toggle theme"
            >
              {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </button>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12 relative overflow-visible">
        
        {/* Animated Aurora Mesh Gradient Blobs */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-[450px] overflow-hidden pointer-events-none -z-10 select-none">
          <div className="absolute -top-12 left-[15%] w-72 h-72 rounded-full bg-blue-500/20 dark:bg-blue-600/10 blur-[100px] animate-blob-1" />
          <div className="absolute -top-4 right-[15%] w-80 h-80 rounded-full bg-emerald-400/15 dark:bg-emerald-600/10 blur-[100px] animate-blob-2" />
          <div className="absolute top-[120px] left-[35%] w-96 h-96 rounded-full bg-sky-400/20 dark:bg-indigo-600/10 blur-[120px] animate-blob-3" />
        </div>
        
        {/* Hero Section */}
        <section className="text-center max-w-3xl mx-auto mb-10 md:mb-14">
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 mb-4 border border-blue-100 dark:border-blue-900/50">
              <Sparkles className="w-3.5 h-3.5" /> Newsroom-Grade Translation Engine
            </span>
            <h2 className="text-4xl md:text-5xl font-extrabold tracking-tight text-slate-900 dark:text-white mb-4 leading-tight">
              State-of-the-Art <br className="hidden sm:inline" /> Telugu Font Converter
            </h2>
            <p className="text-base md:text-lg text-slate-500 dark:text-slate-400 leading-relaxed font-medium">
              A premium, bi-directional transdecoding system designed to translate legacy Eenadu 4C Lipika visual mapping sequences into clean Telugu Unicode, and vice versa.
            </p>
          </motion.div>
        </section>

        {/* Translation Card Workspace */}
        <div className="bg-white/80 dark:bg-slate-900/80 border border-slate-100 dark:border-slate-800/80 rounded-3xl shadow-xl shadow-slate-100/50 dark:shadow-none p-6 md:p-8 backdrop-blur-xl mb-12 transition-all">
          
          {/* Top Controls: Translation Direction & Switcher */}
          <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4 pb-6 border-b border-slate-100 dark:border-slate-800">
            
            {/* Direction Selector */}
            <div className="bg-slate-100/80 dark:bg-slate-950/60 p-1.5 rounded-2xl flex gap-1.5 self-start md:self-auto w-full md:w-auto">
              <button
                onClick={() => {
                  setDirection('unicode_to_legacy');
                  setOutputText('');
                }}
                className={`flex-grow md:flex-grow-0 px-4 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                  direction === 'unicode_to_legacy'
                    ? 'bg-white dark:bg-slate-800 text-blue-600 dark:text-blue-400 shadow-sm'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'
                }`}
              >
                Unicode → 4C Lipika
              </button>
              <button
                onClick={() => {
                  setDirection('legacy_to_unicode');
                  setOutputText('');
                  setEditorialMode(false); // Default disable in reverse mode
                }}
                className={`flex-grow md:flex-grow-0 px-4 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                  direction === 'legacy_to_unicode'
                    ? 'bg-white dark:bg-slate-800 text-blue-600 dark:text-blue-400 shadow-sm'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'
                }`}
              >
                4C Lipika → Unicode
              </button>
            </div>

            {/* Tab switchers: Text vs File */}
            <div className="bg-slate-100/80 dark:bg-slate-950/60 p-1.5 rounded-2xl flex gap-1.5 w-full md:w-auto">
              <button
                onClick={() => setActiveTab('text')}
                className={`flex-grow md:flex-grow-0 px-5 py-2.5 rounded-xl text-sm font-semibold flex items-center justify-center gap-2 transition-all ${
                  activeTab === 'text'
                    ? 'bg-white dark:bg-slate-800 text-slate-800 dark:text-white shadow-sm'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'
                }`}
              >
                <Languages className="w-4 h-4" /> Text
              </button>
              <button
                onClick={() => setActiveTab('file')}
                className={`flex-grow md:flex-grow-0 px-5 py-2.5 rounded-xl text-sm font-semibold flex items-center justify-center gap-2 transition-all ${
                  activeTab === 'file'
                    ? 'bg-white dark:bg-slate-800 text-slate-800 dark:text-white shadow-sm'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'
                }`}
              >
                <FileText className="w-4 h-4" /> Documents
              </button>
            </div>

          </div>

          {/* Core Content Area */}
          <div className="pt-6">
            
            {/* Tab 1: Text Translator */}
            {activeTab === 'text' && (
              <div>
                
                {/* 2-column input/output block */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">
                  
                  {/* Left Column: Input Panel */}
                  <div className="flex flex-col border border-slate-100 dark:border-slate-800 rounded-2xl overflow-hidden bg-slate-50/50 dark:bg-slate-950/30 transition-all focus-within:ring-2 focus-within:ring-blue-500/20 focus-within:border-blue-500">
                    <div className="px-4 py-3 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between bg-white dark:bg-slate-900/50">
                      <span className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                        {direction === 'unicode_to_legacy' ? 'Telugu Unicode' : '4C Lipika Legacy'}
                      </span>
                      {inputText && (
                        <button
                          onClick={handleClearText}
                          className="text-xs font-semibold text-slate-500 hover:text-rose-500 flex items-center gap-1.5 px-2 py-1 rounded-md hover:bg-slate-100 dark:hover:bg-slate-800 transition-all"
                          title="Clear input"
                        >
                          <Trash2 className="w-3.5 h-3.5" /> Clear
                        </button>
                      )}
                    </div>
                    <textarea
                      value={inputText}
                      onChange={(e) => setInputText(e.target.value)}
                      placeholder={
                        direction === 'unicode_to_legacy'
                          ? 'Type or paste Telugu Unicode text here...'
                          : 'Paste legacy 4C Lipika visual character strings (e.g. ë¯yô¢í£²) here...'
                      }
                      className="w-full min-h-[220px] md:min-h-[260px] p-4 bg-transparent outline-none border-none resize-y text-slate-800 dark:text-slate-200 placeholder-slate-400 text-sm leading-relaxed"
                    />
                    <div className="px-4 py-2 bg-white dark:bg-slate-900/50 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-xs text-slate-400 font-medium">
                      <span>Characters: {inputCharCount}</span>
                      <span>Words: {inputWordCount}</span>
                    </div>
                  </div>

                  {/* Right Column: Output Panel */}
                  <div className="flex flex-col border border-slate-100 dark:border-slate-800 rounded-2xl overflow-hidden bg-slate-50/50 dark:bg-slate-950/30 transition-all">
                    <div className="px-4 py-3 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between bg-white dark:bg-slate-900/50">
                      <span className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                        {direction === 'unicode_to_legacy' ? '4C Lipika Legacy' : 'Telugu Unicode'}
                      </span>
                      {outputText && (
                        <button
                          onClick={handleCopyOutput}
                          className="text-xs font-semibold text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/30 flex items-center gap-1.5 px-2 py-1 rounded-md transition-all"
                        >
                          <Copy className="w-3.5 h-3.5" /> Copy
                        </button>
                      )}
                    </div>
                    <textarea
                      readOnly
                      value={outputText}
                      placeholder={
                        direction === 'unicode_to_legacy'
                          ? 'Translated legacy visual bytes will appear here...'
                          : 'Standard Telugu Unicode text will appear here...'
                      }
                      className="w-full min-h-[220px] md:min-h-[260px] p-4 bg-transparent outline-none border-none resize-y text-slate-800 dark:text-slate-200 placeholder-slate-450 text-sm leading-relaxed"
                    />
                    <div className="px-4 py-2 bg-white dark:bg-slate-900/50 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-xs text-slate-400 font-medium">
                      <span>Translated Chars: {stats.chars}</span>
                      <span>Speed: {stats.speedMs ? `${stats.speedMs.toFixed(1)} ms` : '0 ms'}</span>
                    </div>
                  </div>

                </div>

                {/* Bottom Action panel: Settings & Translate Button */}
                <div className="mt-6 flex flex-col sm:flex-row items-center justify-between gap-4 pt-6 border-t border-slate-100 dark:border-slate-800">
                  
                  {/* Settings section */}
                  <div>
                    {direction === 'unicode_to_legacy' ? (
                      <label className="inline-flex items-center gap-2.5 cursor-pointer group">
                        <input
                          type="checkbox"
                          checked={editorialMode}
                          onChange={(e) => setEditorialMode(e.target.checked)}
                          className="sr-only peer"
                        />
                        <div className="relative w-11 h-6 bg-slate-200 dark:bg-slate-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-slate-350 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-slate-600 peer-checked:bg-blue-600"></div>
                        <span className="text-sm font-semibold text-slate-500 dark:text-slate-400 group-hover:text-slate-800 dark:group-hover:text-slate-250 transition-colors">
                          Enable Editorial Archive Mode <span className="text-xs text-slate-400 font-medium">(spellcheck overrides)</span>
                        </span>
                      </label>
                    ) : (
                      <div className="text-sm text-slate-400 font-medium flex items-center gap-1.5">
                        <Info className="w-4 h-4" /> Editorial check disabled during reverse transdecoding
                      </div>
                    )}
                  </div>

                  {/* Translate CTA */}
                  <button
                    onClick={handleTranslate}
                    disabled={isTranslating}
                    className="w-full sm:w-auto px-8 py-3.5 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-600/50 hover:shadow-lg hover:shadow-blue-500/25 active:scale-95 disabled:scale-100 text-white rounded-2xl font-bold flex items-center justify-center gap-2 transition-all cursor-pointer disabled:cursor-not-allowed"
                  >
                    {isTranslating ? (
                      <>
                        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        Translating...
                      </>
                    ) : (
                      <>
                        Translate <ArrowRight className="w-4 h-4" />
                      </>
                    )}
                  </button>

                </div>

              </div>
            )}

            {/* Tab 2: File Document Translator */}
            {activeTab === 'file' && (
              <div className="max-w-2xl mx-auto py-4">
                <div className="text-center mb-6">
                  <h3 className="text-lg font-bold text-slate-900 dark:text-white">Document Translation Service</h3>
                  <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                    Upload your Word or text documents. The engine will translate Telugu text runs while fully preserving fonts, typography, layout, and document structure.
                  </p>
                </div>

                {/* Upload Area */}
                {!selectedFile ? (
                  <div
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    onClick={() => fileInputRef.current?.click()}
                    className={`border-2 border-dashed rounded-3xl p-8 flex flex-col items-center justify-center gap-4 cursor-pointer transition-all ${
                      isDragging
                        ? 'border-blue-500 bg-blue-500/5'
                        : 'border-slate-200 dark:border-slate-800 hover:border-blue-400 dark:hover:border-slate-700 hover:bg-slate-50/50 dark:hover:bg-slate-900/30'
                    }`}
                  >
                    <input
                      type="file"
                      ref={fileInputRef}
                      onChange={(e) => handleFileChange(e.target.files[0])}
                      accept=".txt,.docx"
                      hidden
                    />
                    <div className="w-16 h-16 rounded-2xl bg-blue-50 dark:bg-slate-850 flex items-center justify-center text-blue-600 dark:text-blue-400">
                      <UploadCloud className="w-8 h-8" />
                    </div>
                    <div>
                      <h4 className="font-bold text-slate-900 dark:text-white text-sm">
                        Drag and drop your file here, or <span className="text-blue-600 dark:text-blue-400">browse</span>
                      </h4>
                      <p className="text-xs text-slate-400 font-medium mt-1">
                        Supports Microsoft Word (.docx) and Plain Text (.txt) files (Max 5MB)
                      </p>
                    </div>
                  </div>
                ) : (
                  /* Selected File Display Card */
                  <div className="border border-slate-100 dark:border-slate-800/80 rounded-2xl p-5 bg-slate-50/50 dark:bg-slate-950/40">
                    <div className="flex items-center gap-4">
                      
                      <div className="w-12 h-12 rounded-xl bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 flex items-center justify-center">
                        <FileText className="w-6 h-6" />
                      </div>

                      <div className="flex-grow min-w-0">
                        <h4 className="text-sm font-bold text-slate-900 dark:text-white truncate">
                          {selectedFile.name}
                        </h4>
                        <p className="text-xs text-slate-400 mt-0.5">
                          {(selectedFile.size / 1024).toFixed(1)} KB
                        </p>
                      </div>

                      <button
                        onClick={handleRemoveFile}
                        disabled={uploadStatus === 'uploading' || uploadStatus === 'processing'}
                        className="p-1.5 rounded-lg border border-slate-200 dark:border-slate-850 bg-white dark:bg-slate-900 text-slate-500 hover:text-rose-500 hover:border-rose-200 transition-all cursor-pointer disabled:opacity-50"
                        title="Remove file"
                      >
                        <X className="w-4 h-4" />
                      </button>

                    </div>

                    {/* Progress Loader */}
                    {(uploadStatus === 'uploading' || uploadStatus === 'processing') && (
                      <div className="mt-6 pt-4 border-t border-slate-100 dark:border-slate-850">
                        <div className="flex justify-between text-xs text-slate-500 font-semibold mb-2">
                          <span>
                            {uploadStatus === 'uploading'
                              ? `Uploading: ${uploadProgress}%`
                              : 'Processing document...'}
                          </span>
                        </div>
                        <div className="w-full h-2 bg-slate-100 dark:bg-slate-850 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-blue-600 rounded-full transition-all duration-300"
                            style={{
                              width: uploadStatus === 'uploading' ? `${uploadProgress}%` : '95%',
                            }}
                          />
                        </div>
                      </div>
                    )}

                    {/* Status Info (Error/Success) */}
                    {uploadStatus === 'error' && (
                      <div className="mt-4 p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-600 dark:text-rose-400 text-xs font-semibold flex items-center gap-2">
                        <AlertCircle className="w-4 h-4 flex-shrink-0" />
                        <span>{errorMessage || 'File conversion failed.'}</span>
                      </div>
                    )}

                    {/* Actions panel */}
                    {uploadStatus !== 'uploading' && uploadStatus !== 'processing' && (
                      <div className="mt-6 flex items-center justify-between gap-4 pt-4 border-t border-slate-100 dark:border-slate-850">
                        
                        <div className="text-xs text-slate-400 font-medium">
                          Preserves font mappings & spacing
                        </div>

                        <button
                          onClick={handleTranslateFile}
                          className="px-6 py-3 bg-blue-600 hover:bg-blue-500 active:scale-95 text-white font-bold text-sm rounded-xl flex items-center gap-2 cursor-pointer shadow-sm hover:shadow-md transition-all"
                        >
                          Translate & Download <Download className="w-4 h-4" />
                        </button>

                      </div>
                    )}

                  </div>
                )}
              </div>
            )}

          </div>

        </div>

        {/* Informational About Section */}
        <section id="about" className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center bg-slate-100/40 dark:bg-slate-900/30 rounded-3xl border border-slate-100 dark:border-slate-850/80 p-8 md:p-12 mb-8">
          <div>
            <h3 className="text-2xl font-bold text-slate-900 dark:text-white mb-4">How it works</h3>
            <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed mb-4">
              Historically, newsrooms like *Eenadu* composed content in legacy layouts using CP1252-based font layers (like 4C Lipika) that mapped English characters visually onto Telugu glyphs. While this worked for print layouts, the raw text is unsearchable, unindexed, and unreadable on standard digital platforms.
            </p>
            <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
              This suite performs high-fidelity, bidirectional transdecoding. It translates text layouts to/from Telugu Unicode, resolving complex clusters, consonants, and vowel matras correctly, both for raw text fields and document layers.
            </p>
          </div>
          <div className="flex flex-col gap-4 border-l border-slate-200 dark:border-slate-800 pl-0 md:pl-8">
            <div className="flex gap-4">
              <div className="w-10 h-10 rounded-xl bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center flex-shrink-0">
                <Sparkles className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-slate-900 dark:text-white">Editorial Overrides</h4>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                  Enables dictionary mapping spellcheck corrections specifically optimized for print typography runs.
                </p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center flex-shrink-0">
                <FileText className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-slate-900 dark:text-white">Word Run Preservation</h4>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                  Correctly processes `.docx` files by parsing paragraphs and run segments individually, keeping inline fonts and styling intact.
                </p>
              </div>
            </div>
          </div>
        </section>

      </main>

      {/* Footer */}
      <footer className="w-full bg-white dark:bg-slate-950 border-t border-slate-100 dark:border-slate-850 py-8 transition-colors">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-slate-500 dark:text-slate-400 font-semibold">
          <p>© 2026 Eenadu 4C Lipika Translator Suite • Developed by Vardhan Naidu • Production Stable v60.0</p>
          <div className="flex items-center gap-6">
            <a href="https://github.com/vardhan30016/EEnadu_Translator" target="_blank" rel="noopener noreferrer" className="hover:text-slate-850 dark:hover:text-white transition-colors">
              GitHub Repo
            </a>
            <a href="https://github.com/vardhan30016/EEnadu_Translator/blob/main/LICENSE" target="_blank" rel="noopener noreferrer" className="hover:text-slate-850 dark:hover:text-white transition-colors">
              MIT License
            </a>
          </div>
        </div>
      </footer>

    </div>
  );
}

export default App;
