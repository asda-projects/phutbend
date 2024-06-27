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

# valid_phrases = extractor.extract_valid_phrases(url=url, filename=filename)

phrases = [
    "Could Would you please bring me some ?",
    "How spicy is ?",
    "And it can leave you feeling the side effects the day after.",
    "So use this phrase to check how spicy the food you want to order is.",
    "How spicy is the curry?",
    "How spicy is it?",
    "Can we have the bill, please?",
    "Can we have the bill, please?",
    "Were in a bit of a hurry.",
    "Could we split the bill, please?",
    "You can also ask Can we get separate checks?",
    "We can help you get the natural practice you need, all by yourself, with our English fluency course.",
    "With our expert guidance and resources, you can take your speaking skills to the next level."
]


for phrase in phrases:
    level = pcc.classify_phrase_level(phrase)
    thai_phrase, romanized_phrase = lexical.thai_and_romanized(phrase)
    
    logger.info(f"Phrase: {phrase} || Level {level}\nThai Alphabet {thai_phrase} ||  RTGS transliteration {romanized_phrase}\n\n")