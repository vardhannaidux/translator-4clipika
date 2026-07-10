# -*- coding: utf-8 -*-
"""
config.py — Centralized Configuration & Structured Rotating Logger.
Manages user configurations in JSON format and provides a standardized logger setup.
"""

import os
import json
import logging
from logging.handlers import RotatingFileHandler
from typing import Any, Dict

# Ensure sandbox and logs folders exist
os.makedirs("sandbox", exist_ok=True)
os.makedirs("logs", exist_ok=True)

class ConfigurationError(Exception):
    """Custom exception raised for configuration read/write/validation errors."""
    pass

class ConfigurationManager:
    """
    Manages loading, saving, and querying configuration options for the application.
    Settings are persisted to 'sandbox/config.json'.
    """
    DEFAULT_CONFIG: Dict[str, Any] = {
        "window_geometry": "750x700",
        "font_size": 12,
        "font_family": "Segoe UI",
        "theme": "mocha",
        "log_level": "INFO",
        "autosave_enabled": True,
        "backup_path": "sandbox/autosave_backup.txt",
    }
    
    CONFIG_PATH: str = "sandbox/config.json"
    
    def __init__(self) -> None:
        self.settings: Dict[str, Any] = {}
        self.load()
        
    def load(self) -> None:
        """Loads configuration from JSON file. Falls back to defaults if missing or corrupted."""
        if not os.path.exists(self.CONFIG_PATH):
            self.settings = self.DEFAULT_CONFIG.copy()
            self.save()
            return
            
        try:
            with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    raise ValueError("Configuration data must be a dictionary.")
                self.settings = self.DEFAULT_CONFIG.copy()
                self.settings.update(data)
        except Exception as e:
            # Revert to safe defaults on read failure
            self.settings = self.DEFAULT_CONFIG.copy()
            # Try to rewrite defaults
            try:
                self.save()
            except Exception:
                pass
            raise ConfigurationError(
                f"Failed to read configuration from '{self.CONFIG_PATH}'. Reverted to defaults.\nError: {e}"
            )

    def save(self) -> None:
        """Saves current configuration settings to JSON file atomically."""
        temp_path = self.CONFIG_PATH + ".tmp"
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            os.replace(temp_path, self.CONFIG_PATH)
        except Exception as e:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
            raise ConfigurationError(
                f"Failed to write configuration atomically to '{self.CONFIG_PATH}'.\nError: {e}"
            )

    def get(self, key: str) -> Any:
        """Queries a setting value, falling back to defaults if not found."""
        return self.settings.get(key, self.DEFAULT_CONFIG.get(key))

    def set(self, key: str, value: Any) -> None:
        """Sets a configuration setting and persists it."""
        self.settings[key] = value
        self.save()


def setup_logger(name: str) -> logging.Logger:
    """
    Configures and returns a rotating logger saving to 'logs/translator.log'.
    Rotates logs when file size hits 1 MB, preserving up to 5 backups.
    """
    config_mgr = ConfigurationManager()
    log_level_str = config_mgr.get("log_level")
    
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
    }
    level = level_map.get(log_level_str, logging.INFO)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers if setup_logger is called repeatedly on the same namespace
    if not logger.handlers:
        log_file = os.path.join("logs", "translator.log")
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Rotating File Handler: 1 MB rotation limit, 5 archives max
        file_handler = RotatingFileHandler(
            log_file, maxBytes=1024 * 1024, backupCount=5, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        logger.addHandler(file_handler)
        
        # Console Handler for diagnostics when running CLI
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.WARNING) # Warnings and errors to console by default
        logger.addHandler(console_handler)
        
    return logger
