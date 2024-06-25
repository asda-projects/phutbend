import requests
import brotli
import json
from pythainlp.transliterate import romanize
from pythainlp.tokenize import word_tokenize
import logs
import logging

logger = logging.getLogger(logs.LOG_NAME)

class LexicalAnalyzer:

    def __init__(self) -> None:
        self.dictonary_site_url = "https://www.thai2english.com/api/search"
        self.translator_site_url = "https://www.translate.com/ajax/machine-translation/translate"
        self.show_logs = True
    
    def log_info(self, string_info: str) -> None:
        if self.show_logs:
            logger.info(string_info)
    
    def handle_response(self, r: requests.Response) -> str:
        
        self.log_info("Handling with response parse...")

        if r.headers.get('Content-Encoding') == 'br':
            try:
                decompressed_content = brotli.decompress(r.content)
                content = decompressed_content.decode('utf-8')
            except brotli.error:
                logger.error("Brotli decompression failed....")
                content = r.text
        else:
            content = r.text

        if 'application/json' in r.headers.get('Content-Type', ''):
            try:
                json_content = json.loads(content)
                return json.dumps(json_content, indent=2, ensure_ascii=False)
            except json.JSONDecodeError:
                logger.error("Failed to decode JSON....")
                return content
        return content


    
    def get_thai_translation_in_thai_alphabet(self, phrase, source_lang="en", translated_lang="th"):
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

    def get_words_from_phrase(self, phrase):
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

    def romanize_transliteration(self, phrase: str) -> str:
        return romanize(phrase, engine='royin')

    def tokenize_thai_alphabet(self, phrase: str) -> str:
        tokenized =  word_tokenize(phrase, engine='newmm')
        return " ".join(tokenized)


if __name__ == "__main__":

    lexical = LexicalAnalyzer()

    phrase = "Can we have the bill, please?"

    # answer = lexical.get_words_from_phrase(phrase)
    answer = lexical.get_thai_translation_in_thai_alphabet(phrase)
    
    thai_phrase = json.loads(answer).get("translated_text", None)

    tokenize_thai_phrase = lexical.tokenize_thai_alphabet(thai_phrase)

    romanized_phrase = lexical.romanize_transliteration(tokenize_thai_phrase)

    logger.info(f"Thai Alphabet {thai_phrase} ||  RTGS transliteration {romanized_phrase}")
