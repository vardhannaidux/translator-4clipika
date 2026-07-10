# -*- coding: utf-8 -*-
"""
schemas.py — Pydantic Request and Response Validation Schemas.
"""

from pydantic import BaseModel, Field
from typing import Literal

class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text string to translate")
    direction: Literal["unicode_to_legacy", "legacy_to_unicode"] = Field(
        "unicode_to_legacy", 
        description="Direction of translation"
    )
    editorial_mode: bool = Field(False, description="Toggles editorial post-corrections")

class TranslationStats(BaseModel):
    chars: int = Field(..., description="Character count")
    words: int = Field(..., description="Word count")
    time_ms: float = Field(..., description="Processing time in milliseconds")

class TranslationResponse(BaseModel):
    translated_text: str = Field(..., description="Translated output string")
    stats: TranslationStats = Field(..., description="Translation performance statistics")
