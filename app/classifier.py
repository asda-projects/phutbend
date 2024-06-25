import logs
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from textstat import flesch_reading_ease, flesch_kincaid_grade, coleman_liau_index, automated_readability_index,dale_chall_readability_score,difficult_words,linsear_write_formula,gunning_fog
from extractor import ExtractorServices

import logging


logger = logging.getLogger(__name__)

class PhrasesComplexityClassifier():

    def __init__(self, 
                 flesch_reading_ease_weight, 
                 flesch_kincaid_grade_weight, 
                 coleman_liau_index_weight, 
                 automated_readability_index_weight, 
                 dale_chall_readability_score_weight, 
                 difficult_words_weight, 
                 linsear_write_formula_weight, 
                 gunning_fog_weight,
                 show_logs = True
                 ) -> None:
        
        self.scaler = MinMaxScaler()
        self.flesch_reading_ease_weight = flesch_reading_ease_weight
        self.flesch_kincaid_grade_weight = flesch_kincaid_grade_weight
        # smog_index: 0.001,
        self.coleman_liau_index_weight = coleman_liau_index_weight
        self.automated_readability_index_weight = automated_readability_index_weight
        self.dale_chall_readability_score_weight = dale_chall_readability_score_weight
        self.difficult_words_weight = difficult_words_weight
        self.linsear_write_formula_weight =  linsear_write_formula_weight 
        self.gunning_fog_weight = gunning_fog_weight
        self.show_logs = show_logs

    def normalize_scores(self, scores):
        #logger.info(f"Before Normalize: {scores}")
        scores_array = np.array(scores).reshape(-1, 1)
        scaled_scores = self.scaler.fit_transform(scores_array)
        scd_flatten = scaled_scores.flatten()    
        #logger.info(f"Before Normalize: {scd_flatten}")
        return scd_flatten


    def metric_weight_dict(self, phrase) -> dict:
        # Flesch Reading Ease: Higher scores indicate easier readability.
        _flesch_reading_ease = flesch_reading_ease(phrase) 
        
        # Flesch-Kincaid Grade: Corresponds to U.S. school grade levels.
        _flesch_kincaid_grade = flesch_kincaid_grade(phrase)
        
        #smog_index = textstat.smog_index(phrase)
        # SMOG Index: Estimates the years of education needed to understand the text.

        # Coleman-Liau Index: Estimates the U.S. grade level needed to understand the text.
        _coleman_liau_index = coleman_liau_index(phrase)

        # Automated Readability Index: Estimates the U.S. grade level.
        _automated_readability_index = automated_readability_index(phrase)
        
        # Dale-Chall Readability Score: Uses a list of common words to assess readability.
        _dale_chall_readability_score = dale_chall_readability_score(phrase)
        
        # Difficult Words: Counts the number of complex words in the text.
        _difficult_words = difficult_words(phrase) 
        
        # Linsear Write Formula: Estimates the U.S. grade level.
        _linsear_write_formula = linsear_write_formula(phrase)
        
        # Gunning Fog Index: Estimates the years of formal education needed to understand the text.
        _gunning_fog = gunning_fog(phrase)


        return {
        #"flesch_reading_ease": (_flesch_reading_ease, self.flesch_reading_ease_weight),
        #"flesch_kincaid_grade": (_flesch_kincaid_grade, self.flesch_kincaid_grade_weight),
        # smog_index: 0.001,
        "coleman_liau_index": (_coleman_liau_index, self.coleman_liau_index_weight),
        "automated_readability_index": (_automated_readability_index, self.automated_readability_index_weight),
        #"dale_chall_readability_score": (_dale_chall_readability_score, self.dale_chall_readability_score_weight),
        "difficult_words": (_difficult_words, self.difficult_words_weight), 
        "linsear_write_formula": (_linsear_write_formula,self.linsear_write_formula_weight), 
        "gunning_fog": (_gunning_fog, self.gunning_fog_weight)
        }
    
    def get_weights(self, metric_weights: dict) -> list:

        #scores = [score for score, _ in metric_weights.values()]

        return [weight for _, weight in metric_weights.values()]

        #return  self.normalize_scores(scores)

    def get_scores(self,  metric_weights: dict) -> list:

        scs =  [score for score, _ in metric_weights.values()]
    
        return scs
    
    def compose_index(self, normalized_scores, weights) -> int:

        cpi = sum(score * weight for score, weight in zip(normalized_scores, weights))
        
        if self.show_logs:
            logger.info("-"*171)
            logger.info(f"Actual Composite Index: {cpi}")
        
        return cpi
    
    def map_compound(self, swap=False) -> dict:

        
        mapped_compound_dict = {
        (0, 1): "A1",
        (1, 1.5): "A2",
        (1.5, 2): "B1",
        (2, 3.5): "B2",
        (3.5, 4.5): "C1",
        (4.5, 10): "C2",
        }

        if swap:
            return {value:key for key, value in mapped_compound_dict.items()}
        
        else: 
            return mapped_compound_dict
        
    def log_metrics_info(self, metric_weight: dict) -> None:
        
        if self.show_logs:
            #logger.info(f'Flesch Reading Ease: {metric_weight.get("flesch_reading_ease")[0]} - {metric_weight.get("flesch_reading_ease")[1]} Higher scores indicate easier readability. \n')
            #logger.info(f'Flesch-Kincaid Grade: {metric_weight.get("flesch_kincaid_grade")[0]} - {metric_weight.get("flesch_kincaid_grade")[1]} Corresponds to U.S. school grade levels. \n')
            # print(f"SMOG Index: {smog_index} - {metric_weights.get(smog_index)}\nEstimates the years of education needed to understand the text.\n")
            logger.info(f'Coleman-Liau Index: {metric_weight.get("coleman_liau_index")[0]} - {metric_weight.get("coleman_liau_index")[1]} Estimates the U.S. grade level needed to understand the text. \n')
            logger.info(f'Automated Readability Index: {metric_weight.get("automated_readability_index")[0]} - {metric_weight.get("automated_readability_index")[1]} Estimates the U.S. grade level. \n')
            #logger.info(f'Dale-Chall Readability Score: {metric_weight.get("dale_chall_readability_score")[0]} - {metric_weight.get("dale_chall_readability_score")[1]} Uses a list of common words to assess readability. \n')
            logger.info(f'Difficult Words: {metric_weight.get("difficult_words")[0]} - {metric_weight.get("difficult_words")[1]} Counts the number of complex words in the text. \n')
            logger.info(f'Linsear Write Formula: {metric_weight.get("linsear_write_formula")[0]} - {metric_weight.get("linsear_write_formula")[1]} Estimates the U.S. grade level. \n')
            logger.info(f'Gunning Fog Index: {metric_weight.get("gunning_fog")[0]} - {metric_weight.get("gunning_fog")[1]} Estimates the years of formal education needed to understand the text. \n')    


    def classify_phrase_level(self, phrase) -> str:

        metric_weight = self.metric_weight_dict(phrase)
        
        self.log_metrics_info(metric_weight)

        weights = self.get_weights(metric_weight)
        
        scores = self.get_scores(metric_weight)

        # normalized_scores = self.normalize_scores(scores)

        composed_index = self.compose_index(scores, weights)


        mapped_compound = self.map_compound(swap=False)

        

        for (min_range, max_range), level in mapped_compound.items():
            if min_range <= composed_index < max_range:
                
                return level
            
            elif composed_index < min_range and min_range == 0:

                return level
            
            elif composed_index > max_range and max_range == 10:

                return level
            



    
    def adjust_classifyer(self, example_phrases: dict) -> None:

        for goal_level, phrase in example_phrases.items():
            level = self.classify_phrase_level(phrase)
            if self.show_logs:
                logger.info(f"Desired Composite Index: {self.map_compound(swap=True).get(goal_level)}")
                logger.info(f"Actual Level {level} | Desired Level {goal_level}")
                logger.info(f"Phrase: {phrase}")
                logger.info("="*375)

        


if __name__ == "__main__":

    pcc = PhrasesComplexityClassifier(
        flesch_reading_ease_weight=0,
        flesch_kincaid_grade_weight=0,
        coleman_liau_index_weight=0.1,
        automated_readability_index_weight=0.1,
        dale_chall_readability_score_weight=0,
        difficult_words_weight=0.1, 
        linsear_write_formula_weight=0.1, 
        gunning_fog_weight=0.01,
        show_logs=False
        )

    extractor = ExtractorServices()

    filename = "englishanyone"
    url = "https://englishanyone.com/english-phrases/"

    valid_phrases = extractor.extract_valid_phrases(url=url, filename=filename)


    for phrase in valid_phrases:
        level = pcc.classify_phrase_level(phrase)
        logger.info(f"Phrase: {phrase} || Level {level}")




"""
    phrases = {
    "A1": "The cat is on the table.",
    "A2": "She likes to watch movies on weekends.",
    "B1": "I have been learning English for three years.", 
    "B2": "She enjoys playing the piano in her free time and often performs at local events.", 
    "C1": "Despite the challenges, she managed to complete the project on time and impressed her supervisors.",
    "C2": "Having studied abroad for several years, he possesses a profound understanding of cultural nuances and linguistic subtleties."
    }

    pcc.adjust_classifyer(phrases)
    


"""