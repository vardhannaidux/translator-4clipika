import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Languages,
  FileText,
  Trash2,
  Copy,
  UploadCloud,
  X,
  Info,
  Download,
  AlertCircle,
  ArrowRight,
  Sparkles,
  Mic,
  Pause,
  Play,
  Square
} from 'lucide-react';

export default function TranslatorWorkspace({
  direction,
  setDirection,
  activeTab,
  setActiveTab,
  inputText,
  setInputText,
  outputText,
  setOutputText,
  editorialMode,
  setEditorialMode,
  isTranslating,
  stats,
  selectedFile,
  setSelectedFile,
  isDragging,
  setIsDragging,
  uploadProgress,
  uploadStatus,
  errorMessage,
  handleTranslate,
  handleClearText,
  handleCopyOutput,
  handleFileChange,
  handleRemoveFile,
  handleTranslateFile,
  fileInputRef,
  speechState,
  handleStartSpeech,
  handlePauseSpeech,
  handleResumeSpeech,
  handleStopSpeech
}) {
  const inputCharCount = inputText.length;
  const inputWordCount = inputText.trim() ? inputText.trim().split(/\s+/).length : 0;

  // Drag and drop handlers
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

  return (
    <section id="translator" className="py-12 md:py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      
      {/* Workspace Card */}
      <div className="bg-white/40 dark:bg-slate-900/40 border border-white/20 dark:border-slate-800/80 rounded-3xl shadow-2xl p-6 md:p-8 backdrop-blur-2xl transition-all duration-300">
        
        {/* Workspace Controls Header */}
        <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4 pb-6 border-b border-slate-200/50 dark:border-slate-800/50">
          
          {/* Direction Switcher */}
          <div className="bg-slate-200/60 dark:bg-slate-950/60 p-1.5 rounded-2xl flex gap-1.5 self-start md:self-auto w-full md:w-auto">
            <button
              onClick={() => {
                setDirection('unicode_to_legacy');
                setOutputText('');
              }}
              className={`flex-grow md:flex-grow-0 px-5 py-2.5 rounded-xl text-sm font-bold transition-all duration-200 cursor-pointer ${
                direction === 'unicode_to_legacy'
                  ? 'bg-white dark:bg-slate-800 text-blue-600 dark:text-blue-400 shadow-md scale-[1.02]'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'
              }`}
            >
              Unicode → 4C Lipika
            </button>
            <button
              onClick={() => {
                setDirection('legacy_to_unicode');
                setOutputText('');
                setEditorialMode(false);
              }}
              className={`flex-grow md:flex-grow-0 px-5 py-2.5 rounded-xl text-sm font-bold transition-all duration-200 cursor-pointer ${
                direction === 'legacy_to_unicode'
                  ? 'bg-white dark:bg-slate-800 text-blue-600 dark:text-blue-400 shadow-md scale-[1.02]'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'
              }`}
            >
              4C Lipika → Unicode
            </button>
          </div>

          {/* Tab Selection */}
          <div className="bg-slate-200/60 dark:bg-slate-950/60 p-1.5 rounded-2xl flex gap-1.5 w-full md:w-auto">
            <button
              onClick={() => setActiveTab('text')}
              className={`flex-grow md:flex-grow-0 px-6 py-2.5 rounded-xl text-sm font-bold flex items-center justify-center gap-2 transition-all duration-200 cursor-pointer ${
                activeTab === 'text'
                  ? 'bg-white dark:bg-slate-800 text-slate-800 dark:text-white shadow-md scale-[1.02]'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'
              }`}
            >
              <Languages className="w-4.5 h-4.5" /> Text Area
            </button>
            <button
              onClick={() => setActiveTab('file')}
              className={`flex-grow md:flex-grow-0 px-6 py-2.5 rounded-xl text-sm font-bold flex items-center justify-center gap-2 transition-all duration-200 cursor-pointer ${
                activeTab === 'file'
                  ? 'bg-white dark:bg-slate-800 text-slate-800 dark:text-white shadow-md scale-[1.02]'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'
              }`}
            >
              <FileText className="w-4.5 h-4.5" /> Documents
            </button>
          </div>

        </div>

        {/* Translation Mode Workspaces */}
        <div className="pt-6">
          <AnimatePresence mode="wait">
            
            {/* Tab 1: Text translation */}
            {activeTab === 'text' && (
              <motion.div
                key="text-tab"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                transition={{ duration: 0.25 }}
              >
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">
                  
                  {/* Input Side */}
                  <div className="flex flex-col border border-slate-200/50 dark:border-slate-800/80 rounded-2xl overflow-hidden bg-slate-50/50 dark:bg-slate-950/30 transition-all duration-200 focus-within:ring-2 focus-within:ring-blue-500/20 focus-within:border-blue-500">
                    <div className="px-4 py-3 border-b border-slate-200/50 dark:border-slate-800/80 flex items-center justify-between bg-white/60 dark:bg-slate-900/50">
                      <span className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                        {direction === 'unicode_to_legacy' ? 'Telugu Unicode' : '4C Lipika Legacy'}
                      </span>
                      <div className="flex items-center gap-2">
                        {direction === 'unicode_to_legacy' && (
                          <div className="flex items-center bg-slate-200/50 dark:bg-slate-800/50 border border-slate-300/30 dark:border-slate-700/50 rounded-xl p-1 shadow-inner gap-1">
                            {speechState === 'inactive' && (
                              <button
                                onClick={handleStartSpeech}
                                className="text-xs font-bold flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-slate-600 dark:text-slate-350 hover:bg-slate-300/40 dark:hover:bg-slate-700/60 hover:text-blue-600 dark:hover:text-blue-400 transition-all duration-200 cursor-pointer"
                                title="Start speaking Telugu"
                              >
                                <Mic className="w-3.5 h-3.5" />
                                <span>Speak</span>
                              </button>
                            )}
                            
                            {speechState === 'listening' && (
                              <>
                                <span className="flex h-2.5 w-2.5 relative mx-2">
                                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                                  <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-rose-500"></span>
                                </span>
                                <button
                                  onClick={handlePauseSpeech}
                                  className="p-1.5 rounded-lg text-slate-500 hover:text-amber-500 hover:bg-slate-300/40 dark:hover:bg-slate-700/60 transition-all duration-200 cursor-pointer"
                                  title="Pause dictation"
                                >
                                  <Pause className="w-3.5 h-3.5" />
                                </button>
                                <button
                                  onClick={handleStopSpeech}
                                  className="p-1.5 rounded-lg text-slate-500 hover:text-rose-500 hover:bg-slate-300/40 dark:hover:bg-slate-700/60 transition-all duration-200 cursor-pointer"
                                  title="Stop dictation"
                                >
                                  <Square className="w-3.5 h-3.5" />
                                </button>
                              </>
                            )}

                            {speechState === 'paused' && (
                              <>
                                <span className="text-[10px] uppercase font-bold text-slate-400 dark:text-slate-500 px-2 animate-pulse">Paused</span>
                                <button
                                  onClick={handleResumeSpeech}
                                  className="p-1.5 rounded-lg text-slate-500 hover:text-blue-500 hover:bg-slate-300/40 dark:hover:bg-slate-700/60 transition-all duration-200 cursor-pointer"
                                  title="Resume dictation"
                                >
                                  <Play className="w-3.5 h-3.5" />
                                </button>
                                <button
                                  onClick={handleStopSpeech}
                                  className="p-1.5 rounded-lg text-slate-500 hover:text-rose-500 hover:bg-slate-300/40 dark:hover:bg-slate-700/60 transition-all duration-200 cursor-pointer"
                                  title="Stop dictation"
                                >
                                  <Square className="w-3.5 h-3.5" />
                                </button>
                              </>
                            )}
                          </div>
                        )}
                        {inputText && (
                          <button
                            onClick={handleClearText}
                            className="text-xs font-bold text-slate-500 hover:text-rose-500 flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg hover:bg-slate-200/50 dark:hover:bg-slate-800/80 transition-all duration-200 cursor-pointer"
                            title="Clear input text"
                          >
                            <Trash2 className="w-3.5 h-3.5" /> Clear
                          </button>
                        )}
                      </div>
                    </div>
                    <textarea
                      value={inputText}
                      onChange={(e) => setInputText(e.target.value)}
                      placeholder={
                        direction === 'unicode_to_legacy'
                          ? 'Type or paste Telugu Unicode text here...'
                          : 'Paste legacy 4C Lipika visual character strings (e.g. ë¯yô¢í£²) here...'
                      }
                      className="w-full min-h-[220px] md:min-h-[260px] p-4 bg-transparent outline-none border-none resize-y text-slate-800 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-600 text-sm leading-relaxed"
                    />
                    <div className="px-4 py-2 bg-white/60 dark:bg-slate-900/50 border-t border-slate-200/50 dark:border-slate-800/80 flex items-center justify-between text-xs text-slate-400 font-bold">
                      <span>Characters: {inputCharCount}</span>
                      <span>Words: {inputWordCount}</span>
                    </div>
                  </div>

                  {/* Output Side */}
                  <div className="flex flex-col border border-slate-200/50 dark:border-slate-800/80 rounded-2xl overflow-hidden bg-slate-50/50 dark:bg-slate-950/30 transition-all duration-200">
                    <div className="px-4 py-3 border-b border-slate-200/50 dark:border-slate-800/80 flex items-center justify-between bg-white/60 dark:bg-slate-900/50">
                      <span className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                        {direction === 'unicode_to_legacy' ? '4C Lipika Legacy' : 'Telugu Unicode'}
                      </span>
                      {outputText && (
                        <button
                          onClick={handleCopyOutput}
                          className="text-xs font-bold text-blue-600 dark:text-blue-400 hover:bg-blue-500/10 flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg transition-all duration-200 cursor-pointer"
                        >
                          <Copy className="w-3.5 h-3.5" /> Copy Output
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
                      className="w-full min-h-[220px] md:min-h-[260px] p-4 bg-transparent outline-none border-none resize-y text-slate-800 dark:text-slate-200 placeholder-slate-400 dark:placeholder-slate-600 text-sm leading-relaxed"
                    />
                    <div className="px-4 py-2 bg-white/60 dark:bg-slate-900/50 border-t border-slate-200/50 dark:border-slate-800/80 flex items-center justify-between text-xs text-slate-400 font-bold">
                      <span>Translated Chars: {stats.chars}</span>
                      <span>Speed: {stats.speedMs ? `${stats.speedMs.toFixed(1)} ms` : '0 ms'}</span>
                    </div>
                  </div>

                </div>

                {/* Settings & Translate CTA Panel */}
                <div className="mt-6 flex flex-col sm:flex-row items-center justify-between gap-4 pt-6 border-t border-slate-200/50 dark:border-slate-800/50">
                  
                  {/* Left: Spellcheck Toggle */}
                  <div>
                    {direction === 'unicode_to_legacy' ? (
                      <label className="inline-flex items-center gap-2.5 cursor-pointer group">
                        <input
                          type="checkbox"
                          checked={editorialMode}
                          onChange={(e) => setEditorialMode(e.target.checked)}
                          className="sr-only peer"
                        />
                        <div className="relative w-11 h-6 bg-slate-200 dark:bg-slate-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-slate-600 peer-checked:bg-blue-600"></div>
                        <span className="text-sm font-bold text-slate-500 dark:text-slate-400 group-hover:text-slate-800 dark:group-hover:text-slate-200 transition-colors duration-200 select-none">
                          Enable Editorial Archive Mode <span className="text-xs text-slate-400 font-medium">(spellcheck overrides)</span>
                        </span>
                      </label>
                    ) : (
                      <div className="text-sm text-slate-400 font-bold flex items-center gap-1.5">
                        <Info className="w-4 h-4 text-blue-500" /> Editorial check disabled during reverse transdecoding
                      </div>
                    )}
                  </div>

                  {/* Right: Action CTA */}
                  <button
                    onClick={handleTranslate}
                    disabled={isTranslating}
                    className="w-full sm:w-auto px-8 py-3.5 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-600/50 hover:shadow-lg hover:shadow-blue-500/25 active:scale-95 disabled:scale-100 text-white rounded-2xl font-bold flex items-center justify-center gap-2 transition-all duration-200 cursor-pointer disabled:cursor-not-allowed"
                  >
                    {isTranslating ? (
                      <>
                        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        Translating...
                      </>
                    ) : (
                      <>
                        Translate <ArrowRight className="w-4.5 h-4.5" />
                      </>
                    )}
                  </button>

                </div>
              </motion.div>
            )}

            {/* Tab 2: Document translation */}
            {activeTab === 'file' && (
              <motion.div
                key="file-tab"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                transition={{ duration: 0.25 }}
                className="max-w-2xl mx-auto py-4"
              >
                <div className="text-center mb-6">
                  <h3 className="text-lg font-bold text-slate-900 dark:text-white">Document Translation Service</h3>
                  <p className="text-sm text-slate-500 dark:text-slate-400 mt-1 font-medium">
                    Upload your Word or text documents. The engine will translate Telugu text runs while fully preserving fonts, typography, layout, and document structure.
                  </p>
                </div>

                {/* Upload Panel */}
                {!selectedFile ? (
                  <div
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    onClick={() => fileInputRef.current?.click()}
                    className={`border-2 border-dashed rounded-3xl p-8 flex flex-col items-center justify-center gap-4 cursor-pointer transition-all duration-200 ${
                      isDragging
                        ? 'border-blue-500 bg-blue-500/5'
                        : 'border-slate-200/60 dark:border-slate-800/80 hover:border-blue-400 dark:hover:border-slate-700 hover:bg-slate-100/20 dark:hover:bg-slate-900/10'
                    }`}
                  >
                    <input
                      type="file"
                      ref={fileInputRef}
                      onChange={(e) => handleFileChange(e.target.files[0])}
                      accept=".txt,.docx"
                      hidden
                    />
                    <div className="w-16 h-16 rounded-2xl bg-blue-50 dark:bg-slate-800/60 flex items-center justify-center text-blue-600 dark:text-blue-400">
                      <UploadCloud className="w-8 h-8" />
                    </div>
                    <div>
                      <h4 className="font-bold text-slate-900 dark:text-white text-sm">
                        Drag and drop your file here, or <span className="text-blue-600 dark:text-blue-400">browse</span>
                      </h4>
                      <p className="text-xs text-slate-400 font-semibold mt-1">
                        Supports Microsoft Word (.docx) and Plain Text (.txt) files (Max 5MB)
                      </p>
                    </div>
                  </div>
                ) : (
                  /* Upload Status Card */
                  <div className="border border-slate-200/50 dark:border-slate-800/80 rounded-2xl p-5 bg-slate-50/50 dark:bg-slate-950/40">
                    <div className="flex items-center gap-4">
                      
                      <div className="w-12 h-12 rounded-xl bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center">
                        <FileText className="w-6 h-6" />
                      </div>

                      <div className="flex-grow min-w-0">
                        <h4 className="text-sm font-bold text-slate-900 dark:text-white truncate">
                          {selectedFile.name}
                        </h4>
                        <p className="text-xs text-slate-400 font-bold mt-0.5">
                          {(selectedFile.size / 1024).toFixed(1)} KB
                        </p>
                      </div>

                      <button
                        onClick={handleRemoveFile}
                        disabled={uploadStatus === 'uploading' || uploadStatus === 'processing'}
                        className="p-1.5 rounded-lg border border-slate-200 dark:border-slate-855 bg-white dark:bg-slate-900 text-slate-550 hover:text-rose-500 hover:border-rose-300 transition-all duration-200 cursor-pointer disabled:opacity-50"
                        title="Remove uploaded file"
                      >
                        <X className="w-4 h-4" />
                      </button>

                    </div>

                    {/* Progress Loader bar */}
                    {(uploadStatus === 'uploading' || uploadStatus === 'processing') && (
                      <div className="mt-6 pt-4 border-t border-slate-100 dark:border-slate-850">
                        <div className="flex justify-between text-xs text-slate-500 font-bold mb-2">
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

                    {/* API Errors */}
                    {uploadStatus === 'error' && (
                      <div className="mt-4 p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-600 dark:text-rose-400 text-xs font-bold flex items-center gap-2">
                        <AlertCircle className="w-4 h-4 flex-shrink-0" />
                        <span>{errorMessage || 'File conversion failed.'}</span>
                      </div>
                    )}

                    {/* Translate Button trigger */}
                    {uploadStatus !== 'uploading' && uploadStatus !== 'processing' && (
                      <div className="mt-6 flex items-center justify-between gap-4 pt-4 border-t border-slate-200/50 dark:border-slate-800/80">
                        
                        <div className="text-xs text-slate-400 font-bold flex items-center gap-1">
                          <Sparkles className="w-3.5 h-3.5 text-blue-500 animate-pulse" /> Preserves font mapping and spacing layout
                        </div>

                        <button
                          onClick={handleTranslateFile}
                          className="px-6 py-3 bg-blue-600 hover:bg-blue-500 active:scale-95 text-white font-bold text-sm rounded-xl flex items-center gap-2 cursor-pointer shadow-md transition-all duration-200"
                        >
                          Translate & Download <Download className="w-4 h-4" />
                        </button>

                      </div>
                    )}

                  </div>
                )}
              </motion.div>
            )}

          </AnimatePresence>
        </div>

      </div>
    </section>
  );
}
