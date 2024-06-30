import logs
import os
import re
import requests
from bs4 import BeautifulSoup
import gzip
import language_tool_python
import logging

logger = logging.getLogger(__name__)


class ExtractorServices:

    def __init__(self, language_tool: str = 'en-US', show_logs = True) -> None:
        self.tool = language_tool_python.LanguageTool(language_tool)
        self.dir_path_base_set = "./base_sets/"
        self.gzip_separator = " # "
        self.replacers = {
        "?": "? @ ",
        "!": "! @ ",
        ".": ". @ "
        }
        self.logger = logs.LogController(show_logs)
        self.logger.log_info("Starting Extraction Services...")
    


    def check_phrase(self, phrase):
        self.logger.log_debug("Checking phrases")
        # Check the phrase
        matches = self.tool.check(phrase)
        if not matches:
            return True  # No errors found
        else:
            return False

    def get_brute_html(self, url):
        self.logger.log_debug("Getting html...")
        r = requests.get(url=url)
        return r.text


    
    def remove_html_tags(self, html_text):
        self.logger.log_debug("Removing html tags...")
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.get_text()

    def save_as_gzip(self, cleaned_sentences, filename):
        self.logger.log_debug("Saving as Gzip...")
        with gzip.open(f'{self.dir_path_base_set}{filename}', 'wt', encoding='utf-8') as f:
            for sentence in cleaned_sentences:
                f.write(sentence + self.gzip_separator)

    
    def save_cache(self, brute_html, filename):
        self.logger.log_debug("Processing cache saving...")        

        cleaned_sentences = self.semi_cleaned_sentences(brute_html)
        
        self.save_as_gzip(cleaned_sentences=cleaned_sentences, filename=filename)


    def read_gzip(self, filename):
        self.logger.log_debug("Reading full Gzip file...")
        with gzip.open(f'{self.dir_path_base_set}{filename}', 'rt', encoding='utf-8') as f:
            return f.read()

    def read_lines_gzip(self, filename):
        self.logger.log_debug("Reading lines Gzip file...")
        with gzip.open(f'{self.dir_path_base_set}{filename}', 'rt', encoding='utf-8') as f:
            return f.readlines()
        
    def replaces(self, string_text: str):
        
        for (key, value) in self.replacers.items():
        
            string_text =  string_text.replace(key, value)

        return string_text

    def semi_cleaned_sentences(self, html_text):
        self.logger.log_info("Pre-cleaning sentences...")
        html_text_without_tags = self.remove_html_tags(html_text)
        splited_lines = html_text_without_tags.splitlines()
        cleaned_sentences = list()
        for line in splited_lines:
                striped = line.strip()
                if striped:  # Verifica se a linha não está vazia após o strip
                    cleaned = re.sub(r"[^a-zA-Z0-9 .,!?\"'\"-]", '', striped)
                    if cleaned:
                        cleaned_sentences.append(self.replaces(cleaned))
        
        return cleaned_sentences

    def add_space_before_uppercase(self, text):
        return re.sub(r'(?<!^)(?=[A-Z])', ' ', text)


    def count_uppercase_letters(self, text):
        return sum(1 for c in text if c.isupper())
        
        #return not_duplicated_phrases

    def filter_valid_phrases(self, base_set):
        self.logger.log_info("Filtering valid sentences...")
        added_space_list = []
        for line in base_set:
            
            phrases = line.split("@")
            for inner_phrases in phrases:
                
                if "#" not in inner_phrases:
                    
                    non_sharp_inner_phrases = [word for word in inner_phrases.split(" ") if word]
                    if len(non_sharp_inner_phrases) > 1:
                        # Adiciona espaço antes de letras maiúsculas
                        
                        for i, add_space_non_sharp in enumerate(non_sharp_inner_phrases):
                            
                            if self.count_uppercase_letters(add_space_non_sharp) > 1:
                                
                                non_sharp_inner_phrases[i] = self.add_space_before_uppercase(add_space_non_sharp)
                               
                        # Junta as palavras novamente em uma frase

                        final_phrase = " ".join(non_sharp_inner_phrases)
                        
                        if self.check_phrase(final_phrase):
                            self.logger.log_debug(f"NON-SHARP PHRASE: {final_phrase}")
                            added_space_list.append(final_phrase)
                
                if "#" in inner_phrases:
                    
                    sharp_inner_phrases = inner_phrases.split("#")

                    for s_i_p in sharp_inner_phrases:

                        slipped_sip = [word for word in s_i_p.split(" ") if word]
                        if len(slipped_sip) > 1:
                            for i, add_space_sharp in enumerate(slipped_sip):
                                if self.count_uppercase_letters(add_space_sharp) > 1:
                                
                                    slipped_sip[i] = self.add_space_before_uppercase(add_space_sharp)
                            
                            final_phrase_sharp = " ".join(slipped_sip)
                            if self.check_phrase(final_phrase_sharp):
                                self.logger.log_debug(f"SHARP PHRASE: {final_phrase_sharp}")
                                added_space_list.append(final_phrase_sharp)


                            #self.logger.log_info(s_i_p)



        return added_space_list


    def check_if_exist_file(self, filename):
        self.logger.log_debug("Checking if file exist...")
        return os.path.isfile(f'{self.dir_path_base_set}{filename}')
    

    def extract_valid_phrases(self, url, filename, force: bool = False):
        self.logger.log_debug("Extracting valid phrases...")
        if not self.check_if_exist_file(filename=filename) or force:
            brute_html = self.get_brute_html(url=url)
            self.save_cache(brute_html=brute_html, filename=filename)


        base_set = self.read_lines_gzip(filename=filename)
    
        return self.filter_valid_phrases(base_set=base_set)
        

            







if __name__ == "__main__":

    
    extractor = ExtractorServices(show_logs=True)
    

    


    
    filename = "modern_family"
    url = "https://www.yourmodernfamily.com/your-modern-family-blog/"

    valid_phrases = extractor.extract_valid_phrases(url=url, filename=filename)
    for phrase in valid_phrases:
        extractor.logger.log_info(phrase)


    """
    for phrase in valid_phrases:
        extractor.logger.log_info(phrase)

    to_extract = {
        "Shrek": "https://imsdb.com/scripts/Shrek.html",
        "Greetings": "https://www.englishspeak.com/en/english-phrases",
        "learnenglishteam": "https://www.learnenglishteam.com/common-daily-english-phrases-for-beginners/",
        "englishanyone": "https://englishanyone.com/english-phrases/"

    }
    
    """
    
                    