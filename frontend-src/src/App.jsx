import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertCircle, Sparkles } from 'lucide-react';
import Lenis from 'lenis';

// Import modularized components
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import TranslatorWorkspace from './components/TranslatorWorkspace';
import AboutSection from './components/AboutSection';
import Footer from './components/Footer';
import ParticlesBackground from './components/ParticlesBackground';

function App() {
  // --- AUTH STATE ---
  const [isLoggedIn, setIsLoggedIn] = useState(() => {
    if (typeof window !== 'undefined') {
      return sessionStorage.getItem('authToken') === 'eenadu_1976';
    }
    return false;
  });
  const [loginUser, setLoginUser] = useState('');
  const [loginPass, setLoginPass] = useState('');

  // --- GENERAL STATE ---
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

  // --- EFFECT: Lenis Smooth Scrolling ---
  useEffect(() => {
    if (!isLoggedIn) return;
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) return;

    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
    });

    function raf(time) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }

    requestAnimationFrame(raf);

    return () => {
      lenis.destroy();
    };
  }, [isLoggedIn]);

  // --- TOAST HELPER ---
  const showToast = (message, type = 'info') => {
    const id = Date.now().toString();
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4000);
  };

  // --- LOGIN SUBMIT ---
  const handleLoginSubmit = (e) => {
    e.preventDefault();
    if (loginUser === 'eenadu' && loginPass === '1976') {
      sessionStorage.setItem('authToken', 'eenadu_1976');
      setIsLoggedIn(true);
      showToast('Welcome back, admin', 'success');
    } else {
      showToast('Invalid credentials', 'error');
    }
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
          'X-Auth-Token': sessionStorage.getItem('authToken') || '',
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

      if (response.status === 401) {
        showToast('Unauthorized access. Redirecting...', 'error');
        sessionStorage.removeItem('authToken');
        setIsLoggedIn(false);
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
      } else if (xhr.status === 401) {
        setUploadStatus('error');
        setErrorMessage('Unauthorized access. Please login.');
        showToast('Unauthorized access. Redirecting...', 'error');
        sessionStorage.removeItem('authToken');
        setIsLoggedIn(false);
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
    xhr.setRequestHeader('X-Auth-Token', sessionStorage.getItem('authToken') || '');
    xhr.responseType = 'blob';
    xhr.send(formData);
  };

  // --- RENDER UNAUTHORIZED / LOGIN PORTAL ---
  if (!isLoggedIn) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50 text-slate-800 dark:bg-slate-950 dark:text-slate-200 transition-colors duration-300 relative overflow-hidden font-sans">
        <ParticlesBackground theme={theme} />
        
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

        {/* Login Glassmorphic Card */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="w-full max-w-md bg-white/40 dark:bg-slate-900/40 border border-white/20 dark:border-slate-800/80 p-8 rounded-3xl shadow-2xl backdrop-blur-2xl text-center mx-4"
        >
          <div className="w-12 h-12 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center text-white mx-auto mb-4 shadow-lg shadow-blue-500/25">
            <Sparkles className="w-6 h-6" />
          </div>
          <h2 className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">Admin Authentication</h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 font-semibold">
            Private Translation Suite • Authorized access only
          </p>

          <form onSubmit={handleLoginSubmit} className="mt-6 flex flex-col gap-4 text-left">
            <div>
              <label className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                Username
              </label>
              <input
                type="text"
                required
                value={loginUser}
                onChange={(e) => setLoginUser(e.target.value)}
                placeholder="Enter username"
                className="w-full px-4 py-3 rounded-xl border border-slate-200/60 dark:border-slate-800/80 bg-white/50 dark:bg-slate-950/40 text-slate-850 dark:text-white outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-sm mt-1 transition-all duration-200"
              />
            </div>
            <div>
              <label className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                Password
              </label>
              <input
                type="password"
                required
                value={loginPass}
                onChange={(e) => setLoginPass(e.target.value)}
                placeholder="Enter password"
                className="w-full px-4 py-3 rounded-xl border border-slate-200/60 dark:border-slate-800/80 bg-white/50 dark:bg-slate-950/40 text-slate-850 dark:text-white outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 text-sm mt-1 transition-all duration-200"
              />
            </div>
            <button
              type="submit"
              className="w-full py-3.5 mt-2 bg-blue-600 hover:bg-blue-500 active:scale-98 text-white rounded-xl font-bold text-sm shadow-md transition-all duration-200 cursor-pointer"
            >
              Access Portal
            </button>
          </form>
        </motion.div>
      </div>
    );
  }

  // --- RENDER FULL WEB APP ---
  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-800 dark:bg-slate-950 dark:text-slate-200 transition-colors duration-300 relative overflow-hidden font-sans">
      <ParticlesBackground theme={theme} />
      
      {/* Toast Stack */}
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

      <Navbar theme={theme} setTheme={setTheme} />
      <Hero />
      
      <main className="flex-grow">
        <TranslatorWorkspace
          direction={direction}
          setDirection={setDirection}
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          inputText={inputText}
          setInputText={setInputText}
          outputText={outputText}
          setOutputText={setOutputText}
          editorialMode={editorialMode}
          setEditorialMode={setEditorialMode}
          isTranslating={isTranslating}
          stats={stats}
          selectedFile={selectedFile}
          setSelectedFile={setSelectedFile}
          isDragging={isDragging}
          setIsDragging={setIsDragging}
          uploadProgress={uploadProgress}
          uploadStatus={uploadStatus}
          errorMessage={errorMessage}
          handleTranslate={handleTranslate}
          handleClearText={handleClearText}
          handleCopyOutput={handleCopyOutput}
          handleFileChange={handleFileChange}
          handleRemoveFile={handleRemoveFile}
          handleTranslateFile={handleTranslateFile}
          fileInputRef={fileInputRef}
        />
        <AboutSection />
      </main>

      <Footer />
    </div>
  );
}

export default App;
