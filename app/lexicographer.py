import re
from time import sleep
import requests
import brotli
import json
from pythainlp.transliterate import romanize
from pythainlp.tokenize import word_tokenize

import logs
import logging

logger = logging.getLogger(logs.LOG_NAME)

class LexicalAnalyzer:

    def __init__(self, transliteration_engine = "royin", tokenize_thai_engine= "newmm", show_logs: bool = True, ) -> None:
        self.dictonary_site_url = "https://www.thai2english.com/api/search"
        self.translator_site_url = "https://www.translate.com/ajax/machine-translation/translate"
        self.transliteration_engine = transliteration_engine
        self.tokenize_thai_engine = tokenize_thai_engine
        
        self.logger = logs.LogController(show_logs)
        self.logger.log_info("Starting Lexical Analyzer...")


    def split_phrase(self, phrase: str, separator: str):
        self.logger.log_debug("Splitting the phrase...")

        slipped_phrase = phrase.split(separator)
        return slipped_phrase

    def tokenize_thai_alphabet(self, phrase: str) -> list:
        self.logger.log_debug("Tokenizing thai alphabet...")
        return word_tokenize(phrase, engine= self.tokenize_thai_engine)

    def romanize_transliteration(self, tokens: list) -> str:
        self.logger.log_debug("Romanizing transliteration...")
        return " ".join(romanize(token, engine=self.transliteration_engine) for token in tokens)
    


    def remove_special_chars_from_splitted_phrase(self, word_list: list, force_word_clearance=True) -> list:

        cleaned_words = []

        special_chars_pattern = r"[!@#$%^&*()_+{}\|\[\]<>/.,?]"
        
        for word in word_list:
            if force_word_clearance:
                word = re.sub(special_chars_pattern, "", word)
            if word:
                cleaned_words.append(word)
        
        
        return cleaned_words

    def thai_and_romanized(self, thai_phrase: str) -> tuple:
        self.logger.log_debug("Return Thai and Romanized phrase...")
        

        if not thai_phrase:
            return "", ""

        tokenize_thai_phrase = self.tokenize_thai_alphabet(thai_phrase)
        romanized_phrase = self.romanize_transliteration(tokenize_thai_phrase)

        return thai_phrase, romanized_phrase




if __name__ == "__main__":
    pass


    """

    # semi full process of searching in both sites

    lexical = LexicalAnalyzer()

    phrase = "How spicy is it?"

   
    answer = lexical.librarian.get_thai_translation_in_thai_alphabet(phrase)
    
    thai_phrase = answer.get("translated_text", None)

    tokenize_thai_phrase = lexical.tokenize_thai_alphabet(thai_phrase)

    lexical.logger.log_info(f"\nThai Alphabet {thai_phrase}")

    for word in lexical.remove_special_chars_from_list(tokenize_thai_phrase):

        search_result = lexical.librarian.search_in_dictonary_words_phrase(word)
        search_result_prettyfied = json.dumps(search_result, indent=4, ensure_ascii=False)
        lexical.logger.log_info(f"\n\n{search_result_prettyfied}")
    
    """

    
