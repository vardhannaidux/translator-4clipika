# -*- coding: utf-8 -*-
"""
app.py — Tkinter Graphical Interface for the Eenadu 4C Lipika Translator.
Provides a premium dark theme, high-DPI scaling, clipboard tools, keyboard shortcuts,
focus highlight accessibility indicators, auto-save session recovery, status bar, and about info.
"""

import os
import time
import platform
import tkinter as tk
from tkinter import messagebox
from typing import Any, Optional

# Core translation engine, configuration manager, and logger imports
from translation_engine import translate_text
from config import ConfigurationManager, setup_logger

logger = setup_logger("app")

class PremiumTranslatorApp:
    """
    The main GUI application wrapper class. Setup widgets, binds controls,
    and manages the translation/autosave loop.
    """
    def __init__(self, root: tk.Tk) -> None:
        logger.info("Initializing GUI application window")
        self.root = root
        self.config_mgr = ConfigurationManager()
        
        # Load user configuration
        geom = self.config_mgr.get("window_geometry")
        self.root.title("Eenadu 4C Lipika Translator")
        self.root.geometry(geom)
        self.root.configure(bg="#11111b")
        
        # Enable high-DPI scaling for crisp text on Windows
        if platform.system() == "Windows":
            try:
                from ctypes import windll
                windll.shcore.SetProcessDpiAwareness(1)
                logger.info("Set process DPI awareness to high-DPI on Windows")
            except Exception as e:
                logger.debug(f"Failed to enable high-DPI scaling via ctypes: {e}")
        
        # Color Palette (Premium Catppuccin Mocha theme)
        self.bg_color = "#11111b"       # Deep Obsidian
        self.card_bg = "#1e1e2e"        # Deep Violet-Grey
        self.accent_blue = "#89b4fa"    # Eenadu Brand Blue
        self.accent_green = "#a6e3a1"   # Success Green
        self.accent_red = "#f38ba8"     # Error Red
        self.text_color = "#cdd6f4"     # Soft White
        self.muted_text = "#a6adc8"     # Light Muted Grey
        self.border_color = "#313244"   # Muted Border
        
        # Typography
        self.font_family = self.config_mgr.get("font_family")
        self.font_size = self.config_mgr.get("font_size")
        
        self.font_title = (self.font_family, 18, "bold")
        self.font_subtitle = (self.font_family, 10, "italic")
        self.font_label = (self.font_family, 11, "bold")
        self.font_text = (self.font_family, self.font_size)
        self.font_btn = (self.font_family, 11, "bold")
        
        # Bind close window handler to persist position/dimensions
        self.root.protocol("WM_DELETE_WINDOW", self.on_close_window)
        
        self.setup_ui()
        self.setup_bindings()
        self.restore_previous_session()

    def setup_ui(self) -> None:
        """Constructs layout and creates visual widgets."""
        
        # --- MENU BAR ---
        menubar = tk.Menu(self.root, bg=self.card_bg, fg=self.text_color, activebackground=self.accent_blue, activeforeground=self.bg_color)
        help_menu = tk.Menu(menubar, tearoff=0, bg=self.card_bg, fg=self.text_color)
        help_menu.add_command(label="Keyboard Shortcuts Help", command=self.show_shortcuts_help)
        help_menu.add_command(label="About", command=self.show_about_dialog)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=menubar)

        # --- HEADER SECTION ---
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(fill="x", padx=30, pady=(25, 5))
        
        title_label = tk.Label(
            header_frame, 
            text="Eenadu 4C Lipika Translator", 
            font=self.font_title, 
            fg=self.accent_blue, 
            bg=self.bg_color
        )
        title_label.pack(anchor="w")
        
        subtitle_label = tk.Label(
            header_frame, 
            text="High-fidelity newsroom translation suite • 100% byte-accurate calibration", 
            font=self.font_subtitle, 
            fg=self.muted_text, 
            bg=self.bg_color
        )
        subtitle_label.pack(anchor="w", pady=(2, 0))

        # --- SETTINGS / CONTROL SECTION ---
        settings_frame = tk.LabelFrame(
            self.root, 
            text=" Translation Settings ", 
            font=self.font_label,
            fg=self.accent_blue,
            bg=self.bg_color,
            bd=1,
            relief="solid",
            highlightthickness=0
        )
        settings_frame.config(labelanchor="nw")
        settings_frame.pack(fill="x", padx=30, pady=(10, 10), ipady=8, ipadx=10)
        
        self.editorial_var = tk.BooleanVar(value=False)
        
        chk = tk.Checkbutton(
            settings_frame, 
            text="Enable Editorial Archive Mode (optional spelling normalization & transition corrections)",
            variable=self.editorial_var,
            font=(self.font_family, 10),
            fg=self.text_color,
            bg=self.bg_color,
            selectcolor=self.card_bg,
            activeforeground=self.accent_blue,
            activebackground=self.bg_color,
            bd=0,
            highlightthickness=0,
            cursor="hand2"
        )
        chk.pack(anchor="w", padx=10)

        # --- INPUT SECTION ---
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(fill="both", expand=True, padx=30, pady=5)
        
        tk.Label(
            input_frame, 
            text="Telugu Unicode Input (Paste Standard Unicode Telugu):", 
            font=self.font_label, 
            fg=self.text_color, 
            bg=self.bg_color
        ).pack(anchor="w", pady=(0, 5))
        
        self.input_text = tk.Text(
            input_frame, 
            height=6, 
            font=self.font_text, 
            wrap="word", 
            bg=self.card_bg, 
            fg=self.text_color, 
            insertbackground=self.text_color,
            bd=0,
            highlightthickness=1,
            highlightbackground=self.border_color,
            highlightcolor=self.accent_blue,
            padx=10,
            pady=10
        )
        self.input_text.pack(fill="both", expand=True)

        # --- CONTROLS / ACTION BUTTONS ---
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(fill="x", padx=30, pady=10)
        
        self.translate_btn = tk.Button(
            btn_frame, 
            text="⬇  Translate Text  ⬇", 
            font=self.font_btn, 
            bg=self.accent_blue, 
            fg="#11111b",
            activebackground="#a6e3a1",
            activeforeground="#11111b",
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.perform_translation
        )
        self.translate_btn.pack(side="left")
        self.bind_hover(self.translate_btn, self.accent_blue, "#b4befe")
        
        self.copy_btn = tk.Button(
            btn_frame, 
            text="📋  Copy to Clipboard", 
            font=(self.font_family, 10, "bold"), 
            bg=self.card_bg, 
            fg=self.text_color,
            activebackground=self.accent_blue,
            activeforeground="#11111b",
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.copy_to_clipboard
        )
        self.copy_btn.pack(side="right")
        self.bind_hover(self.copy_btn, self.card_bg, self.border_color)

        # --- OUTPUT SECTION ---
        output_frame = tk.Frame(self.root, bg=self.bg_color)
        output_frame.pack(fill="both", expand=True, padx=30, pady=(5, 10))
        
        tk.Label(
            output_frame, 
            text="4C Lipika Encoded Output (Ready for InDesign / PageMaker):", 
            font=self.font_label, 
            fg=self.text_color, 
            bg=self.bg_color
        ).pack(anchor="w", pady=(0, 5))
        
        self.output_text = tk.Text(
            output_frame, 
            height=6, 
            font=self.font_text, 
            wrap="word", 
            bg=self.card_bg, 
            fg=self.accent_green, 
            insertbackground=self.text_color,
            bd=0,
            highlightthickness=1,
            highlightbackground=self.border_color,
            highlightcolor=self.accent_blue,
            padx=10,
            pady=10
        )
        self.output_text.pack(fill="both", expand=True)
        
        # --- DYNAMIC STATUS BAR ---
        self.status_frame = tk.Frame(self.root, bg=self.card_bg, bd=0, height=24)
        self.status_frame.pack(fill="x", side="bottom")
        
        self.status_label = tk.Label(
            self.status_frame, 
            text="  Status: Ready", 
            font=(self.font_family, 9), 
            fg=self.muted_text, 
            bg=self.card_bg
        )
        self.status_label.pack(side="left", padx=5)
        
        self.stats_label = tk.Label(
            self.status_frame, 
            text="Chars: 0 | Speed: 0 ms  ", 
            font=(self.font_family, 9), 
            fg=self.muted_text, 
            bg=self.card_bg
        )
        self.stats_label.pack(side="right", padx=5)

    def setup_bindings(self) -> None:
        """Sets up key shortcuts and focus indicators for accessibility."""
        
        # Bind keyboard shortcuts
        self.root.bind("<Control-Return>", lambda e: self.perform_translation())
        self.root.bind("<Control-t>", lambda e: self.perform_translation())
        self.root.bind("<Control-T>", lambda e: self.perform_translation())
        self.root.bind("<Control-c>", lambda e: self.handle_ctrl_c_copy(e))
        self.root.bind("<Control-C>", lambda e: self.handle_ctrl_c_copy(e))
        
        # Bind focus highlights on Text boxes for high-contrast accessibility indication
        self.input_text.bind("<FocusIn>", lambda e: self.input_text.config(highlightbackground=self.accent_blue))
        self.input_text.bind("<FocusOut>", lambda e: self.input_text.config(highlightbackground=self.border_color))
        
        self.output_text.bind("<FocusIn>", lambda e: self.output_text.config(highlightbackground=self.accent_blue))
        self.output_text.bind("<FocusOut>", lambda e: self.output_text.config(highlightbackground=self.border_color))
        
        # Bind KeyRelease on Input for continuous autosave
        self.input_text.bind("<KeyRelease>", self.autosave_input)

    def bind_hover(self, widget: tk.Widget, normal_bg: str, hover_bg: str) -> None:
        """Binds simple hover background transitions to widgets."""
        widget.bind("<Enter>", lambda e: widget.config({"bg": hover_bg}))
        widget.bind("<Leave>", lambda e: widget.config({"bg": normal_bg}))
        
        # Register focus events on buttons for accessibility
        widget.bind("<FocusIn>", lambda e: widget.config({"bg": hover_bg}))
        widget.bind("<FocusOut>", lambda e: widget.config({"bg": normal_bg}))

    def update_status(self, message: str, is_error: bool = False) -> None:
        """Updates the status bar message."""
        color = self.accent_red if is_error else self.muted_text
        self.status_label.config(text=f"  Status: {message}", fg=color)
        logger.debug(f"Status bar updated: {message}")

    def update_stats(self, char_count: int, speed_ms: float) -> None:
        """Updates characters counts and calculation metrics."""
        self.stats_label.config(text=f"Chars: {char_count} | Speed: {speed_ms:.1f} ms  ")

    def perform_translation(self) -> None:
        """Runs the translation sequence, measures performance, and handles errors."""
        input_val = self.input_text.get("1.0", tk.END).strip()
        
        if not input_val:
            logger.warning("Attempted to translate empty input")
            self.update_status("Input is empty", is_error=True)
            messagebox.showwarning("Empty Input", "Please enter some Telugu text to translate.")
            return
            
        self.update_status("Translating...")
        self.root.update_idletasks()
        
        start_time = time.perf_counter()
        try:
            mode = self.editorial_var.get()
            result = translate_text(input_val, editorial_mode=mode)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            
            # Update output
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
            
            self.update_status("Translation completed successfully")
            self.update_stats(len(input_val), elapsed_ms)
            logger.info(f"Translated {len(input_val)} chars in {elapsed_ms:.2f} ms")
            
            # Flash success feedback
            original_bg = self.accent_blue
            self.translate_btn.config(bg=self.accent_green)
            self.root.after(300, lambda: self.translate_btn.config(bg=original_bg))
            
        except Exception as e:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            logger.error(f"Translation failure: {e}", exc_info=True)
            self.update_status("Translation failed", is_error=True)
            self.update_stats(0, elapsed_ms)
            messagebox.showerror(
                "Translation Error",
                f"Translation engine encountered an error:\n\n{str(e)}\n\n"
                "Suggestion: Verify that the input contains valid modern Telugu Unicode."
            )

    def handle_ctrl_c_copy(self, event: tk.Event) -> str:
        """Custom handler for Ctrl+C. Copies output box content if it has focus, otherwise falls back."""
        # If output widget or copy button has focus, copy translated output instead
        focused = self.root.focus_get()
        if focused == self.output_text:
            self.copy_to_clipboard()
            return "break" # Suppress normal copy action
        return ""

    def copy_to_clipboard(self) -> None:
        """Copies the translated text to the system clipboard with feedback."""
        output_val = self.output_text.get("1.0", tk.END).strip()
        if output_val:
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(output_val)
                self.root.update()
                
                logger.info("Output copied successfully to clipboard")
                self.update_status("Copied to clipboard")
                
                # Feedback animation
                original_text = self.copy_btn["text"]
                self.copy_btn.config(text="✓  Copied Successfully!", fg=self.accent_green)
                self.root.after(1500, lambda: self.copy_btn.config(text=original_text, fg=self.text_color))
            except Exception as e:
                logger.error(f"Clipboard access error: {e}")
                self.update_status("Failed to access clipboard", is_error=True)
        else:
            logger.warning("Copy requested but output field is empty")
            self.update_status("No text to copy", is_error=True)
            messagebox.showwarning("Empty Output", "There is no translated text to copy yet.")

    # --- AUTOSAVE / RELIABILITY ---
    def autosave_input(self, event: Optional[tk.Event] = None) -> None:
        """Saves current input text to backup file atomically as the user types."""
        if not self.config_mgr.get("autosave_enabled"):
            return
            
        input_val = self.input_text.get("1.0", tk.END)
        backup_path = self.config_mgr.get("backup_path")
        temp_path = backup_path + ".tmp"
        
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(input_val)
            os.replace(temp_path, backup_path)
        except Exception as e:
            logger.error(f"Autosave failure for path '{backup_path}': {e}")

    def restore_previous_session(self) -> None:
        """Attempts to load backup session text if recovery files exist on disk."""
        if not self.config_mgr.get("autosave_enabled"):
            return
            
        backup_path = self.config_mgr.get("backup_path")
        if os.path.exists(backup_path):
            try:
                with open(backup_path, "r", encoding="utf-8") as f:
                    content = f.read()
                # Only load if there's actual content
                if content.strip():
                    self.input_text.delete("1.0", tk.END)
                    self.input_text.insert("1.0", content)
                    self.update_status("Restored previous session unsaved work")
                    logger.info(f"Restored previous unsaved session of length {len(content)} from '{backup_path}'")
            except Exception as e:
                logger.error(f"Failed to restore previous session from '{backup_path}': {e}")

    # --- DIALOGS AND MENUS ---
    def show_shortcuts_help(self) -> None:
        """Displays GUI shortcut descriptions."""
        messagebox.showinfo(
            "Keyboard Shortcuts Help",
            "The following shortcut key combinations are active:\n\n"
            "  • Ctrl + Return   : Translate Input Text\n"
            "  • Ctrl + T        : Translate Input Text\n"
            "  • Ctrl + C        : Copy Output Text (when focus is on Output box)\n\n"
            "Use 'Tab' and 'Shift+Tab' to shift keyboard focus highlighting."
        )

    def show_about_dialog(self) -> None:
        """Displays product information and credits dialog."""
        messagebox.showinfo(
            "About Translator",
            "Eenadu 4C Lipika Translator\n"
            "Version: v60.0 (Production Stable)\n\n"
            "A high-fidelity translation suite designed to map modern Telugu Unicode "
            "to and from legacy 4C Lipika typesetting encodings.\n\n"
            "Credits: Open-source Telugu Digitization Maintainers\n"
            "This project currently does not specify a license."
        )

    def on_close_window(self) -> None:
        """Saves current window geometry configuration to settings before terminating."""
        try:
            # Get geometry from Tkinter (e.g. '750x670+200+150')
            geom = self.root.geometry()
            self.config_mgr.set("window_geometry", geom)
            logger.info(f"Window configuration persisted: geometry={geom}")
            
            # Clean up autosave backup file if clean termination and input is empty
            input_val = self.input_text.get("1.0", tk.END).strip()
            if not input_val:
                backup_path = self.config_mgr.get("backup_path")
                if os.path.exists(backup_path):
                    try:
                        os.remove(backup_path)
                        logger.info("Cleared empty session backup file on exit")
                    except Exception:
                        pass
        except Exception as e:
            logger.error(f"Error persisting configurations on exit: {e}")
        finally:
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PremiumTranslatorApp(root)
    root.mainloop()
