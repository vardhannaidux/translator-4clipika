// script.js — Frontend Script for Theme, Tab, Text Translation and File Uploads.

document.addEventListener("DOMContentLoaded", () => {
    // --- STATE MANAGEMENT ---
    let currentDirection = "unicode_to_legacy";
    let currentTab = "text";
    let selectedFile = null;

    // --- DOM ELEMENTS ---
    const themeToggle = document.getElementById("theme-toggle");
    const htmlElement = document.documentElement;

    // Translation directions
    const dirUniToLeg = document.getElementById("dir-uni-to-leg");
    const dirLegToUni = document.getElementById("dir-leg-to-uni");

    // Tab buttons and main content containers
    const tabText = document.getElementById("tab-text");
    const tabFile = document.getElementById("tab-file");
    const contentText = document.getElementById("content-text");
    const contentFile = document.getElementById("content-file");

    // Labels
    const inputLabel = document.getElementById("input-label");
    const outputLabel = document.getElementById("output-label");
    const editorialContainer = document.getElementById("editorial-container");

    // Text Translate Elements
    const textInput = document.getElementById("text-input");
    const textOutput = document.getElementById("text-output");
    const translateBtn = document.getElementById("translate-btn");
    const clearBtn = document.getElementById("clear-btn");
    const copyBtn = document.getElementById("copy-btn");
    const editorialCheck = document.getElementById("editorial-check");
    const inputStats = document.getElementById("input-stats");
    const outputStats = document.getElementById("output-stats");

    // File Translate Elements
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");
    const browseBtn = document.getElementById("browse-btn");
    const fileCard = document.getElementById("file-card");
    const fileName = document.getElementById("file-name");
    const fileSize = document.getElementById("file-size");
    const fileIcon = document.getElementById("file-icon");
    const removeFileBtn = document.getElementById("remove-file-btn");
    const translateFileBtn = document.getElementById("translate-file-btn");
    const progressContainer = document.getElementById("progress-container");
    const progressBar = document.getElementById("progress-bar");
    const progressStatus = document.getElementById("progress-status");
    const toastContainer = document.getElementById("toast-container");

    // --- THEME SWITCHER ---
    themeToggle.addEventListener("click", () => {
        const currentTheme = htmlElement.getAttribute("data-theme");
        const newTheme = currentTheme === "dark" ? "light" : "dark";
        htmlElement.setAttribute("data-theme", newTheme);
        
        // Update Moon/Sun Icon
        const icon = themeToggle.querySelector("i");
        if (newTheme === "light") {
            icon.className = "fa-solid fa-sun";
        } else {
            icon.className = "fa-solid fa-moon";
        }
        showToast("Theme changed successfully", "info");
    });

    // --- TAB SWITCHER ---
    function switchTab(tab) {
        currentTab = tab;
        if (tab === "text") {
            tabText.classList.add("active");
            tabFile.classList.remove("active");
            contentText.classList.add("active");
            contentFile.classList.remove("active");
        } else {
            tabText.classList.remove("active");
            tabFile.classList.add("active");
            contentText.classList.remove("active");
            contentFile.classList.add("active");
        }
    }
    tabText.addEventListener("click", () => switchTab("text"));
    tabFile.addEventListener("click", () => switchTab("file"));

    // --- DIRECTION MANAGER ---
    function setDirection(direction) {
        currentDirection = direction;
        if (direction === "unicode_to_legacy") {
            dirUniToLeg.classList.add("active");
            dirLegToUni.classList.remove("active");
            
            inputLabel.textContent = "Telugu Unicode Input";
            outputLabel.textContent = "4C Lipika Output";
            textInput.placeholder = "Type or paste Telugu Unicode text here...";
            textOutput.placeholder = "Translated legacy visual bytes will appear here...";
            editorialContainer.style.display = "block";
        } else {
            dirUniToLeg.classList.remove("active");
            dirLegToUni.classList.add("active");
            
            inputLabel.textContent = "4C Lipika Input";
            outputLabel.textContent = "Telugu Unicode Output";
            textInput.placeholder = "Paste legacy visual bytes (e.g. ë¯yô¢í£²) here...";
            textOutput.placeholder = "Transdecoded standard Telugu Unicode text will appear here...";
            editorialContainer.style.display = "none";
            editorialCheck.checked = false; // Disable editorial corrections on reverse transdecode
        }
        
        // Clear outputs
        textOutput.value = "";
        updateStats();
    }
    dirUniToLeg.addEventListener("click", () => setDirection("unicode_to_legacy"));
    dirLegToUni.addEventListener("click", () => setDirection("legacy_to_unicode"));

    // --- STATS AND CHAR COUNTS ---
    function updateStats() {
        const inVal = textInput.value;
        const outVal = textOutput.value;
        
        const inChars = inVal.length;
        const inWords = inVal.trim() ? inVal.trim().split(/\s+/).length : 0;
        
        inputStats.textContent = `Chars: ${inChars} | Words: ${inWords}`;
        
        if (!outVal) {
            outputStats.textContent = "Chars: 0 | Speed: 0 ms";
        }
    }
    textInput.addEventListener("input", updateStats);

    // --- TOAST NOTIFICATIONS ---
    function showToast(message, type = "info") {
        const toast = document.createElement("div");
        toast.className = `toast ${type}`;
        
        let iconClass = "fa-circle-info";
        if (type === "success") iconClass = "fa-circle-check";
        if (type === "error") iconClass = "fa-circle-exclamation";
        
        toast.innerHTML = `
            <i class="fa-solid ${iconClass} toast-icon"></i>
            <span>${message}</span>
        `;
        
        toastContainer.appendChild(toast);
        
        // Remove toast automatically
        setTimeout(() => {
            toast.style.opacity = "0";
            toast.style.transform = "translateX(100%)";
            toast.style.transition = "all 0.5s ease";
            setTimeout(() => toast.remove(), 500);
        }, 3500);
    }

    // --- CLEAR BUTTON ---
    clearBtn.addEventListener("click", () => {
        textInput.value = "";
        textOutput.value = "";
        updateStats();
        showToast("Text cleared", "info");
    });

    // --- COPY BUTTON ---
    copyBtn.addEventListener("click", () => {
        const val = textOutput.value;
        if (!val) {
            showToast("No translated output to copy", "error");
            return;
        }
        navigator.clipboard.writeText(val)
            .then(() => showToast("Copied to clipboard!", "success"))
            .catch(() => showToast("Failed to copy text", "error"));
    });

    // --- TEXT TRANSLATE ACTION ---
    translateBtn.addEventListener("click", async () => {
        const text = textInput.value.strip ? textInput.value.strip() : textInput.value.trim();
        if (!text) {
            showToast("Please enter some text to translate", "error");
            return;
        }
        
        translateBtn.disabled = true;
        translateBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Translating...';
        
        try {
            const response = await fetch("/api/translate/text", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    text: text,
                    direction: currentDirection,
                    editorial_mode: editorialCheck.checked
                })
            });
            
            if (response.status === 429) {
                showToast("Rate limit exceeded. Try again in 60s.", "error");
                return;
            }
            
            const data = await response.json();
            if (response.ok) {
                textOutput.value = data.translated_text;
                outputStats.textContent = `Chars: ${data.stats.chars} | Speed: ${data.stats.time_ms.toFixed(1)} ms`;
                showToast("Translation successful", "success");
            } else {
                showToast(data.detail || "Translation failed", "error");
            }
        } catch (error) {
            logger_error(error);
            showToast("Network connection error", "error");
        } finally {
            translateBtn.disabled = false;
            translateBtn.innerHTML = '<i class="fa-solid fa-bolt"></i> Translate';
        }
    });

    // --- FILE DRAG & DROP LOGIC ---
    
    // Browse trigger
    browseBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        fileInput.click();
    });
    
    dropZone.addEventListener("click", () => fileInput.click());
    
    fileInput.addEventListener("change", (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });
    
    // Drag events
    ["dragenter", "dragover"].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add("dragover");
        }, false);
    });
    
    ["dragleave", "drop"].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove("dragover");
        }, false);
    });
    
    dropZone.addEventListener("drop", (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });
    
    function formatBytes(bytes, decimals = 2) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    }
    
    function handleFile(file) {
        const ext = file.name.substring(file.name.lastIndexOf(".")).toLowerCase();
        if (ext !== ".txt" && ext !== ".docx") {
            showToast("Unsupported file extension. Only .txt and .docx are permitted.", "error");
            return;
        }
        
        if (file.size > 5 * 1024 * 1024) {
            showToast("File size exceeds 5MB limit", "error");
            return;
        }
        
        selectedFile = file;
        
        // Update file card
        fileName.textContent = file.name;
        fileSize.textContent = formatBytes(file.size);
        
        if (ext === ".docx") {
            fileIcon.className = "fa-solid fa-file-word";
        } else {
            fileIcon.className = "fa-solid fa-file-lines";
        }
        
        // Transition screens
        dropZone.classList.add("hidden");
        fileCard.classList.remove("hidden");
        
        // Hide progress
        progressContainer.classList.add("hidden");
        progressBar.style.width = "0%";
    }
    
    removeFileBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        selectedFile = null;
        fileInput.value = "";
        
        dropZone.classList.remove("hidden");
        fileCard.classList.add("hidden");
    });
    
    // --- FILE TRANSLATION SERVICE (XMLHTTPREQUEST PROGRESS) ---
    translateFileBtn.addEventListener("click", () => {
        if (!selectedFile) return;
        
        translateFileBtn.disabled = true;
        progressContainer.classList.remove("hidden");
        progressBar.style.width = "0%";
        progressStatus.textContent = "Uploading document...";
        
        const formData = new FormData();
        formData.append("file", selectedFile);
        formData.append("direction", currentDirection);
        formData.append("editorial_mode", editorialCheck.checked);
        
        const xhr = new XMLHttpRequest();
        
        // Track upload progress
        xhr.upload.addEventListener("progress", (e) => {
            if (e.lengthComputable) {
                const percent = (e.loaded / e.total) * 100;
                progressBar.style.width = `${percent}%`;
                if (percent >= 100) {
                    progressStatus.textContent = "Processing and converting document...";
                } else {
                    progressStatus.textContent = `Uploading: ${percent.toFixed(0)}%`;
                }
            }
        });
        
        xhr.addEventListener("load", () => {
            translateFileBtn.disabled = false;
            
            if (xhr.status === 200) {
                // Trigger download
                const blob = new Blob([xhr.response], { type: xhr.getResponseHeader("Content-Type") });
                
                // Get filename from Content-Disposition header
                let outFilename = `translated_${selectedFile.name}`;
                const disp = xhr.getResponseHeader("Content-Disposition");
                if (disp && disp.indexOf("filename=") !== -1) {
                    outFilename = disp.substring(disp.indexOf("filename=") + 9);
                }
                
                const link = document.createElement("a");
                link.href = window.URL.createObjectURL(blob);
                link.download = outFilename;
                link.click();
                
                showToast("File translated and downloaded!", "success");
                progressStatus.textContent = "Completed";
                
                // Auto reset uploader
                setTimeout(() => {
                    selectedFile = null;
                    fileInput.value = "";
                    dropZone.classList.remove("hidden");
                    fileCard.classList.add("hidden");
                }, 1000);
                
            } else if (xhr.status === 429) {
                showToast("Rate limit exceeded. Please wait a minute.", "error");
                progressStatus.textContent = "Failed";
            } else {
                showToast("File translation failed", "error");
                progressStatus.textContent = "Failed";
            }
        });
        
        xhr.addEventListener("error", () => {
            translateFileBtn.disabled = false;
            showToast("Network upload error", "error");
            progressStatus.textContent = "Failed";
        });
        
        xhr.open("POST", "/api/translate/file");
        xhr.responseType = "blob";
        xhr.send(formData);
    });
});

function logger_error(err) {
    console.error("Client Error: ", err);
}
