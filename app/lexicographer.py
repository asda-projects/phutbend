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



    def brotli_parse(self, request_response: requests.Response) -> str:
        self.logger.log_debug("Brotli decompression started....")

        try:
            decompressed_content = brotli.decompress(request_response.content)
            return decompressed_content.decode('utf-8')
        except brotli.error:
            self.logger.log_debug("Brotli decompression failed....")
            return request_response.text

    def json_parse(self, respose_text) -> dict:
        self.logger.log_debug("JSON decode started....")        

        type_response_text = type(respose_text)

        if type_response_text != type(dict):
            try:
                return json.loads(respose_text)
            except (json.JSONDecodeError, json.decoder.JSONDecodeError) as jde:
                self.logger.log_debug(f"Error ({jde}) to decode response ({respose_text}) of type ({type_response_text}) into JSON ....")
                return {}
            except TypeError as te:
                self.logger.log_debug(f"Error ({te}) to decode response ({respose_text}) of type ({type_response_text}) into JSON ....")
                return {}   
        
        else:
            return respose_text
    
    def handle_response(self, request_response: requests.Response) -> str:
        
        self.logger.log_debug("Handling with response parse...")

        request_response_text = request_response

        if request_response.headers.get('Content-Encoding') == 'br':
            request_response_text = self.brotli_parse(request_response)

        return self.json_parse(request_response_text)


  
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
        
        

        return self.handle_response(r)

    def get_words_from_phrase(self, phrase) -> dict:

        self.logger.log_debug("Geetting word meanings...")

        params = {
            "q": phrase
        }

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-us",
            "Connection": "keep-alive",
        }

        r = requests.get(self.dictonary_site_url, headers=headers, params=params)
        
        return self.handle_response(r)

    def tokenize_thai_alphabet(self, phrase: str) -> list:
        self.logger.log_debug("Tokenizing thai alphabet...")
        return word_tokenize(phrase, engine= self.tokenize_thai_engine)

    def romanize_transliteration(self, tokens: list) -> str:
        self.logger.log_debug("Romanizing transliteration...")
        return " ".join(romanize(token, engine=self.transliteration_engine) for token in tokens)

    def thai_and_romanized(self, phrase) -> tuple:
        self.logger.log_debug("Return Thai and Romanized phrase...")
        
        answer = self.get_thai_translation_in_thai_alphabet(phrase)
        thai_phrase = answer.get("translated_text", None)

        if not thai_phrase:
            return "", ""

        tokenize_thai_phrase = self.tokenize_thai_alphabet(thai_phrase)
        romanized_phrase = self.romanize_transliteration(tokenize_thai_phrase)

        return thai_phrase, romanized_phrase




if __name__ == "__main__":

    lexical = LexicalAnalyzer()

    phrase = "Can we have the bill, please?"

    # answer = lexical.get_words_from_phrase(phrase)
    answer = lexical.get_thai_translation_in_thai_alphabet(phrase)
    
    thai_phrase = answer.get("translated_text", None)

    tokenize_thai_phrase = lexical.tokenize_thai_alphabet(thai_phrase)

    romanized_phrase = lexical.romanize_transliteration(tokenize_thai_phrase)

    lexical.logger.log_info(f"Thai Alphabet {thai_phrase} ||  RTGS transliteration {romanized_phrase}")
