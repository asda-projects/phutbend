from classifier import PhrasesComplexityClassifier
from extractor import ExtractorServices
from lexicographer import LexicalAnalyzer

import logs
import logging

logger = logging.getLogger(logs.LOG_NAME)



extractor = ExtractorServices(show_logs=True)

pcc = PhrasesComplexityClassifier(
        coleman_liau_index_weight=0.1,
        automated_readability_index_weight=0.1,
        difficult_words_weight=0.1, 
        linsear_write_formula_weight=0.1, 
        gunning_fog_weight=0.01,
        show_logs=True
        )

lexical = LexicalAnalyzer( transliteration_engine= "ita", show_logs=True)

filename = "englishanyone"
url = "https://englishanyone.com/english-phrases/"

valid_phrases = extractor.extract_valid_phrases(url=url, filename=filename)


for phrase in valid_phrases:
    level = pcc.classify_phrase_level(phrase)
    thai_phrase, romanized_phrase = lexical.thai_and_romanized(phrase)
    
    logger.info(f"Phrase: {phrase} || Level {level}\nThai Alphabet {thai_phrase} ||  RTGS transliteration {romanized_phrase}\n\n")