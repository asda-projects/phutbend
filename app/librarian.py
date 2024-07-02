import requests
import interpreter 

import logs
import logging

logger = logging.getLogger(logs.LOG_NAME)

class LibrianLocatator:


    def __init__(self, show_logs: bool =True) -> None:
        self.dictonary_site_url = "https://www.thai2english.com/api/search"
        self.translator_site_url = "https://www.translate.com/ajax/machine-translation/translate"
        self.interpreter = interpreter.RequestResponseInterpreter(show_logs)
        self.logger = logs.LogController(show_logs)
        self.logger.log_info("Starting Librian Locatator...")


    def search_in_dictonary_words_phrase(self, phrase_or_word: str) -> dict:

        self.logger.log_debug("Geetting word meanings...")

        params = {
            "q": phrase_or_word
        }

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-us",
            "Connection": "keep-alive",
        }

        r = requests.get(self.dictonary_site_url, headers=headers, params=params)

        return self.interpreter.handle_response(r)
    


    def get_thai_translation_in_thai_alphabet(self, phrase, source_lang="en", translated_lang="th") -> dict:
        self.logger.log_debug("Geetting thai translation in thai alphabet...")
        
        params = {
            "text_to_translate": phrase,
            "source_lang": source_lang,
            "translated_lang": translated_lang,
            "use_cache_only": "false"
        }

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-us",
            "Connection": "keep-alive",
        }

        r = requests.post(self.translator_site_url, headers=headers, data=params)

        return self.interpreter.handle_response(r)


if __name__ == "__main__":
    pass

