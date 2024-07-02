from classifier import PhrasesComplexityClassifier
from extractor import ExtractorServices
from lexicographer import LexicalAnalyzer
from librarian import LibrianLocatator
from time import sleep
import logs
import logging

logger = logging.getLogger(logs.LOG_NAME)


class AppController:

    def __init__(self, show_logs: bool = True) -> None:
        self.extractor = ExtractorServices(show_logs=show_logs)
        self.phrase_classifier = PhrasesComplexityClassifier(
        coleman_liau_index_weight=0.1,
        automated_readability_index_weight=0.1,
        difficult_words_weight=0.1, 
        linsear_write_formula_weight=0.1, 
        gunning_fog_weight=0.01,
        show_logs=show_logs
        )
        self.lexical_analyzer = LexicalAnalyzer( transliteration_engine= "ita", show_logs=show_logs)
        self.librarian = LibrianLocatator(show_logs)
        self.logger = logs.LogController(show_logs=show_logs)
        self.logger.log_info("Started App...")



    def get_thai_phrase_with_retry(self, phrase: str, tries=2, seconds_interval_to_try=4) -> str:

        for _ in range(0, tries):
            answer = self.librarian.get_thai_translation_in_thai_alphabet(phrase)
            thai_phrase = answer.get("translated_text", None)
            if thai_phrase:
                return thai_phrase
            else:
                self.logger.log_info(
                    f"Not received thai translation in thai alphabet ({thai_phrase}), \
                    retry (max tries {tries}) request in {seconds_interval_to_try} seconds..."
                    )
                sleep(seconds_interval_to_try)
        
        return None


app_controller = AppController(show_logs=True)

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

to_understand = phrases[1]

words = app_controller.lexical_analyzer.split_phrase(phrase=to_understand, separator=" ")

cleaned_words = app_controller.lexical_analyzer.remove_special_chars_from_splitted_phrase(words)



dict_info = app_controller.librarian.search_in_dictonary_words_phrase(cleaned_words[0])

processed = dict_info.get("processed", {})



for key, value in processed.items():

    app_controller.logger.log_info(f"{key}:{value}\n\n")

    

"""
for _, value in dict_info.items():
    app_controller.logger.log_info(f"{type(value)}\n\n")
    app_controller.logger.log_info(f"{value}\n\n")

    

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

filename = "python3_pep_3156"
url = "https://peps.python.org/pep-3156/"

phrases = extractor.extract_valid_phrases(url=url, filename=filename)


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
    # thai_phrase, romanized_phrase = lexical.thai_and_romanized(phrase)
    
    logger.info(f"Phrase: {phrase} || Level {level}\n")
    # logger.info(f"Thai Alphabet {thai_phrase} ||  RTGS transliteration {romanized_phrase}\n\n")

"""