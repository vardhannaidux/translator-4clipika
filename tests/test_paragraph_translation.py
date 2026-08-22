import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from translation_engine import translate_text

def test_paragraph_preserves_word_alignment_and_spaces():
    paragraph = "చైతన్య స్కూల్ కలర్స్ ఇంఛార్జి లక్ష్యం ల్స్ స్వీకరణ పరిషత్ బాబ్జి నాయుడు కట్ అవుట్ శుభాకాంక్షలు కాల్చి స్వీట్లు చెప్పారు ఫ్రెండ్స్ స్టోర్స్ త్ ఆర్థోపెడిక్ కృష్ణారావు కార్యాలయం రమేష్ రాజు అభివృద్ధి ఫ్లాష్ ఉపాధ్యాయులు ఫిట్ నెస్"
    
    translated_paragraph = translate_text(paragraph)
    
    telugu_words = paragraph.split()
    para_output_words = translated_paragraph.split()
    
    # Check that word count matches exactly
    assert len(para_output_words) == len(telugu_words), f"Paragraph word count mismatch: {len(para_output_words)} vs {len(telugu_words)}"
    
    # Check that every word translated in the paragraph matches single-word translation
    for i, word in enumerate(telugu_words):
        single_word_trans = translate_text(word)
        assert para_output_words[i] == single_word_trans, f"Word mismatch at position {i+1} ('{word}'): paragraph yielded '{para_output_words[i]}', standalone yielded '{single_word_trans}'"
