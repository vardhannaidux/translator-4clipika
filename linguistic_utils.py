# -*- coding: utf-8 -*-
"""
linguistic_utils.py — Unified Telugu Parser and Linguistic Utilities.
Consolidates Telugu Unicode segmentation, robust encoding, and linguistic models.
"""

import sys
import re
import functools
from typing import List, Dict, Tuple, Optional, Any
from translation_mappings import (
    CONSONANTS, MATRAS, HALANT, ANUSVARA, VISARGA,
    PRE_BASE_SUBS, POST_BASE_SUBS, VOWELS, RA
)
from config import setup_logger

# Initialize logger
logger = setup_logger("linguistic_utils")

# =====================================================================
# 1. Telugu Unicode Syllable Segmenter (from parser.py)
# =====================================================================

def _is_consonant(ch: str) -> bool:
    """Checks if a character is a Telugu consonant."""
    return ch in CONSONANTS

def _is_matra(ch: str) -> bool:
    """Checks if a character is a Telugu matra."""
    return ch in MATRAS

def _is_vowel(ch: str) -> bool:
    """Checks if a character is an independent Telugu vowel."""
    return ch in VOWELS

def _is_telugu(ch: str) -> bool:
    """Checks if a character is in the Telugu Unicode range."""
    return 0x0C00 <= ord(ch) <= 0x0C7F


def segmentize(text: str) -> List[Dict[str, Any]]:
    """
    Segments a Telugu Unicode string into a list of syllable dictionaries.
    
    Args:
        text (str): Modern Telugu Unicode string.
        
    Returns:
        List[Dict[str, Any]]: A list of parsed syllable dictionaries.
    """
    logger.debug(f"Starting syllable segmentation for text of length: {len(text)}")
    chars = list(text)
    n = len(chars)
    i = 0
    result = []

    while i < n:
        ch = chars[i]

        # Passthrough non-Telugu characters
        if not _is_telugu(ch):
            result.append({'literal': ch})
            i += 1
            continue

        # Independent vowel
        if _is_vowel(ch):
            raw = ch
            i += 1
            post_mods = []
            while i < n and chars[i] in (ANUSVARA, VISARGA):
                post_mods.append(chars[i])
                raw += chars[i]
                i += 1
            result.append({
                'vowel': ch,
                'post_mods': post_mods,
                'raw': raw,
            })
            continue

        # Non-consonant Telugu (orphan halant/anusvara/visarga/matra)
        if not _is_consonant(ch):
            # Orphan matras: engine handles via 'literal' -> ord()
            result.append({'literal': ch})
            i += 1
            continue

        # Collect consonant cluster (C1 + halant + C2 + ...)
        raw = ch
        cluster = [ch]
        i += 1
        while i < n and chars[i] == HALANT:
            raw += chars[i]
            i += 1
            if i < n and _is_consonant(chars[i]):
                raw += chars[i]
                cluster.append(chars[i])
                i += 1

        # Classify cluster into base / pre_subs / post_subs
        pre_subs = []
        post_subs = []

        if len(cluster) == 1:
            base = cluster[0]
        else:
            # RA as first consonant IS a pre-base (reph).
            first_is_other_pre = (
                cluster[0] in PRE_BASE_SUBS
                and cluster[-1] not in POST_BASE_SUBS
            )

            if first_is_other_pre:
                base = cluster[-1]
                for c in cluster[:-1]:
                    if c in POST_BASE_SUBS:
                        post_subs.append(c)
                    else:
                        pre_subs.append(c)
            else:
                base = cluster[0]
                for c in cluster[1:]:
                    if c == RA or c in PRE_BASE_SUBS:
                        pre_subs.append(c)
                    elif c in POST_BASE_SUBS:
                        post_subs.append(c)
                    else:
                        post_subs.append(c)

        trailing_halant = raw.endswith(HALANT)

        # Matra
        matra = None
        if i < n and _is_matra(chars[i]) and chars[i] not in (ANUSVARA, VISARGA):
            matra = chars[i]
            raw += chars[i]
            i += 1

        # Post-modifiers (anusvara, visarga)
        post_mods = []
        while i < n and chars[i] in (ANUSVARA, VISARGA):
            post_mods.append(chars[i])
            raw += chars[i]
            i += 1

        result.append({
            'base':      base,
            'pre_subs':  pre_subs,
            'post_subs': post_subs,
            'matra':     matra,
            'post_mods': post_mods,
            'halant':    trailing_halant,
            'raw':       raw,
        })

    logger.debug(f"Segmented into {len(result)} syllables")
    return result


# =====================================================================
# 2. Robust CP1252/Cyrillic Encoder (from encode_user_correct.py)
# =====================================================================

def robust_encode(s: str) -> bytes:
    """
    Custom robust encoder that maps Cyrillic, standard CP1252,
    and special characters to their correct legacy byte values.
    
    Args:
        s (str): String containing custom symbols or Cyrillic.
        
    Returns:
        bytes: Encoded bytes representation.
    """
    res = []
    custom = {
        8364: 128,  # €
        8218: 130,  # ‚
        402: 131,   # ƒ
        8222: 132,  # „
        8230: 133,  # …
        8224: 134,  # †
        8225: 135,  # ‡
        710: 136,   # ˆ
        8240: 137,  # ‰
        352: 138,   # Š
        8249: 139,  # ‹
        338: 140,   # Œ
        381: 142,   # Ž
        8216: 145,  # ‘
        8217: 146,  # ’
        8220: 147,  # “
        8221: 148,  # ”
        8226: 149,  # •
        8211: 150,  # –
        8212: 151,  # —
        732: 152,   # ˜
        8482: 153,  # ™
        353: 154,   # š
        8250: 155,  # ›
        339: 156,   # œ
        382: 158,   # ž
        376: 159,   # Ÿ
    }
    for c in s:
        o = ord(c)
        if o in custom:
            res.append(custom[o])
        elif 0x0400 <= o <= 0x04FF:
            # Cyrillic characters - encode using CP1251!
            try:
                b = c.encode('cp1251')[0]
                res.append(b)
            except Exception:
                res.append(63)
        elif o < 256:
            res.append(o)
        else:
            res.append(63)
    return bytes(res)


# =====================================================================
# 3. Telugu Glyph Composer (from ocr_advanced_segmenter.py)
# =====================================================================

class TeluguGlyphComposer:
    """
    Decomposes and composes complex Telugu glyphs into regional components:
      - Left: Pre-base vowel signs (ె, ే, ై)
      - Top: Upper vowel signs (ి, ీ, ు, ూ)
      - Right: Right-side markers (ా, ో, ౌ)
      - Bottom: Vattulu (subjoined consonants)
      - Center: Base consonant
    """
    def __init__(self) -> None:
        self.decomposition_db = {
            "భా": {"base": "భ", "left": None, "top": None, "right": "ా", "bottom": None},
            "జీ": {"base": "జ", "left": None, "top": "ీ", "right": None, "bottom": None},
            "రూ": {"base": "ర", "left": None, "top": "ూ", "right": None, "bottom": None},
            "హె": {"base": "హ", "left": "ె", "top": None, "right": None, "bottom": None},
            "హై": {"base": "హ", "left": "ై", "top": None, "right": None, "bottom": None},
            "న్న": {"base": "న", "left": None, "top": None, "right": None, "bottom": "న"},
            "మ్మ": {"base": "మ", "left": None, "top": None, "right": None, "bottom": "మ"},
            "ల్ల": {"base": "ల", "left": None, "top": None, "right": None, "bottom": "ల"},
        }
        
    def decompose(self, unicode_char: str) -> Dict[str, Optional[str]]:
        """Decomposes a single Telugu glyph cluster into logical component directions."""
        if unicode_char in self.decomposition_db:
            return self.decomposition_db[unicode_char]
            
        base = unicode_char[0]
        mods = unicode_char[1:] if len(unicode_char) > 1 else ""
        
        result = {"base": base, "left": None, "top": None, "right": None, "bottom": None}
        
        for ch in mods:
            if ch in ["ె", "ే", "ై"]:
                result["left"] = ch
            elif ch in ["ి", "ీ", "ు", "ూ"]:
                result["top"] = ch
            elif ch in ["ా", "ో", "ౌ"]:
                result["right"] = ch
            elif ch == "్":
                pass
            else:
                result["bottom"] = ch
                
        return result

    def compose(self, base: str, left: Optional[str] = None, top: Optional[str] = None, 
                right: Optional[str] = None, bottom: Optional[str] = None) -> str:
        """Composes components back into a canonical Telugu Unicode glyph cluster."""
        for target, comp in self.decomposition_db.items():
            if (comp["base"] == base and 
                comp["left"] == left and 
                comp["top"] == top and 
                comp["right"] == right and 
                comp["bottom"] == bottom):
                return target
                
        out = base
        if bottom:
            out += "్" + bottom
        if left:
            out += left
        if top:
            out += top
        if right:
            out += right
            
        return out


# =====================================================================
# 4. Grapheme Cluster Segmentation Engine (from ocr_advanced_segmenter.py)
# =====================================================================

class GraphemeClusterSegmenter:
    """
    Splits Telugu Unicode strings into high-fidelity Visual Grapheme Clusters (syllables).
    Example: "కృత్రిమ" -> ["కృ", "త్రి", "మ"]
    """
    @staticmethod
    def split_into_graphemes(text: str) -> List[str]:
        """Segments string into raw syllable-based grapheme clusters."""
        syllables = segmentize(text)
        graphemes = []
        for syl in syllables:
            if 'literal' in syl:
                graphemes.append(syl['literal'])
            elif 'vowel' in syl:
                item = syl['vowel']
                for mod in syl.get('post_mods', []):
                    item += mod
                graphemes.append(item)
            else:
                item = syl['raw']
                graphemes.append(item)
        return graphemes


# =====================================================================
# 5. Telugu Language Model (from ocr_advanced_segmenter.py)
# =====================================================================

@functools.lru_cache(maxsize=8192)
def _levenshtein_distance_cached(s1: str, s2: str) -> int:
    """Fast memoized Levenshtein distance calculation to optimize spellchecking."""
    if len(s1) < len(s2):
        return _levenshtein_distance_cached(s2, s1)
    if len(s2) == 0:
        return len(s1)
        
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (0 if c1 == c2 else 1)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
        
    return previous_row[-1]


@functools.lru_cache(maxsize=2048)
def _autocorrect_word_cached(ocr_word: str, max_distance: int, vocabulary_tuple: Tuple[Tuple[str, int], ...]) -> str:
    """Helper that caches search corrections based on a static representation of vocabulary."""
    vocab_dict = dict(vocabulary_tuple)
    if ocr_word in vocab_dict:
        return ocr_word
        
    best_candidate = ocr_word
    best_score = float('inf')
    highest_freq = -1
    
    for vocab_word, freq in vocabulary_tuple:
        dist = _levenshtein_distance_cached(ocr_word, vocab_word)
        if dist <= max_distance:
            if dist < best_score:
                best_score = dist
                best_candidate = vocab_word
                highest_freq = freq
            elif dist == best_score and freq > highest_freq:
                best_candidate = vocab_word
                highest_freq = freq
                
    return best_candidate


class TeluguLanguageModel:
    """
    Probabilistic Spelling Correction Engine using Levenshtein distance.
    Autocorrects typographical and OCR shape variants (e.g. 'సాంకతిక' -> 'సాంకేతిక').
    """
    def __init__(self) -> None:
        self.vocabulary: Dict[str, int] = {
            "సాంకేతికత": 1500, "సాంకేతిక": 1200, "కృత్రిమ": 900, "మేధస్సు": 800,
            "అభివృద్ధి": 1100, "విస్తృతంగా": 700, "వైద్యం": 1000, "వైద్యరంగంలో": 600,
            "ప్రజలు": 2000, "ప్రభుత్వం": 1800, "వ్యవసాయం": 950, "పరిశోధనలు": 500,
            "రక్షణ": 450, "భద్రత": 850
        }
        # Pre-tuple vocabulary for hashable caching
        self._vocab_tuple = tuple(self.vocabulary.items())
        
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Calculates distance between two strings."""
        return _levenshtein_distance_cached(s1, s2)

    def autocorrect_word(self, ocr_word: str, max_distance: int = 2) -> str:
        """
        Attempts to correct spelling using static language frequencies and edit distance.
        Utilizes a memoized lookup cache.
        """
        return _autocorrect_word_cached(ocr_word, max_distance, self._vocab_tuple)
