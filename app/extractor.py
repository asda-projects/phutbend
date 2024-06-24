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

    def __init__(self, language_tool: str = 'en-US') -> None:
        logger.info("Extraction service started...")
        self.tool = language_tool_python.LanguageTool(language_tool)
        self.dir_path_base_set = "./base_sets/"
        self.gzip_separator = " # "
        self.replacers = {
        "?": "? @ ",
        "!": "! @ ",
        ".": ". @ "
        }

    def check_phrase(self, phrase):
        # Check the phrase
        matches = self.tool.check(phrase)
        if not matches:
            return True  # No errors found
        else:
            return False

    def get_brute_html(self, url):
        logger.info("Getting html...")
        r = requests.get(url=url)
        return r.text


    
    def remove_html_tags(self, html_text):
        logger.info("Removing html tags...")
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.get_text()

    def save_as_gzip(self, cleaned_sentences, filename):
        logger.info("Saving as Gzip...")
        with gzip.open(f'{self.dir_path_base_set}{filename}', 'wt', encoding='utf-8') as f:
            for sentence in cleaned_sentences:
                f.write(sentence + self.gzip_separator)

    
    def save_cache(self, brute_html, filename):
        logger.info("Processing cache saving...")        

        cleaned_sentences = self.semi_cleaned_sentences(brute_html)
        
        self.save_as_gzip(cleaned_sentences=cleaned_sentences, filename=filename)


    def read_gzip(self, filename):
        logger.info("Reading full Gzip file...")
        with gzip.open(f'{self.dir_path_base_set}{filename}', 'rt', encoding='utf-8') as f:
            return f.read()

    def read_lines_gzip(self, filename):
        logger.info("Reading lines Gzip file...")
        with gzip.open(f'{self.dir_path_base_set}{filename}', 'rt', encoding='utf-8') as f:
            return f.readlines()
        
    def replaces(self, string_text: str):
        
        for (key, value) in self.replacers.items():
        
            string_text =  string_text.replace(key, value)

        return string_text

    def semi_cleaned_sentences(self, html_text):
        logger.info("Pre-cleaning sentences...")
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
        logger.info("Filtering valid sentences...")
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
                            added_space_list.append(final_phrase)
        return added_space_list


    def check_if_exist_file(self, filename):

        return os.path.isfile(f'{self.dir_path_base_set}{filename}')
    

    def extract_valid_phrases(self, url, filename, force: bool = False):

        if not self.check_if_exist_file(filename=filename) or force:
            brute_html = self.get_brute_html(url=url)
            self.save_cache(brute_html=brute_html, filename=filename)


        base_set = self.read_lines_gzip(filename=filename)
    
        return self.filter_valid_phrases(base_set=base_set)
        

            







if __name__ == "__main__":

    
    extractor = ExtractorServices()
    

    to_extract = {
        "Shrek": "https://imsdb.com/scripts/Shrek.html",
        "Greetings": "https://www.englishspeak.com/en/english-phrases",
        "learnenglishteam": "https://www.learnenglishteam.com/common-daily-english-phrases-for-beginners/",
        "englishanyone": "https://englishanyone.com/english-phrases/"

    }


    
    filename = "englishanyone"
    url = "https://englishanyone.com/english-phrases/"

    valid_phrases = extractor.extract_valid_phrases(url=url, filename=filename)
    print(valid_phrases)

    
    
                    
    # print(added_space_list)


                            
                                #print(addded_space)
                #extracted_set.add(each)
   
            #for ph in phrases:
            #    extracted_set.add(ph)
            
                
            
    
    
    


