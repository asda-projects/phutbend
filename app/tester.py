import textstat
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Initialize scaler
scaler = MinMaxScaler()

# Function to normalize the scores
def normalize_scores(scores):
    scores_array = np.array(scores).reshape(-1, 1)
    scaled_scores = scaler.fit_transform(scores_array)
    return scaled_scores.flatten()


mapped_compound = {}
inverted_mapped_compound = {}
# Function to determine the level of a phrase
def get_phrase_level(phrase):
    # Obtain readability metrics
    
    
    flesch_reading_ease = textstat.flesch_reading_ease(phrase)
    # Flesch Reading Ease: Higher scores indicate easier readability.
    
    flesch_kincaid_grade = textstat.flesch_kincaid_grade(phrase)
    # Flesch-Kincaid Grade: Corresponds to U.S. school grade levels.
    
    #smog_index = textstat.smog_index(phrase)
    # SMOG Index: Estimates the years of education needed to understand the text.

    coleman_liau_index = textstat.coleman_liau_index(phrase)
    # Coleman-Liau Index: Estimates the U.S. grade level needed to understand the text.

    # Automated Readability Index: Estimates the U.S. grade level.
    automated_readability_index = textstat.automated_readability_index(phrase)
    
    # Dale-Chall Readability Score: Uses a list of common words to assess readability.
    dale_chall_readability_score = textstat.dale_chall_readability_score(phrase)
    
    # Difficult Words: Counts the number of complex words in the text.
    difficult_words = textstat.difficult_words(phrase)
    
    # Linsear Write Formula: Estimates the U.S. grade level.
    linsear_write_formula = textstat.linsear_write_formula(phrase)
    
    # Gunning Fog Index: Estimates the years of formal education needed to understand the text.
    gunning_fog = textstat.gunning_fog(phrase)
    
    

    metric_weights = {
        flesch_reading_ease: 0.1,
        flesch_kincaid_grade: 0.1,
        # smog_index: 0.001,
        coleman_liau_index: 1,
        automated_readability_index: 0.01,
        dale_chall_readability_score: 0.015,
        difficult_words: 0.3, 
        linsear_write_formula: 0.01, 
        gunning_fog: 0.015
    }

    
    
    scores = list(metric_weights.keys())
    weights = list(metric_weights.values())
    
    

    normalized_scores = normalize_scores(scores)
    
    
    

   
    
    # Calculate the weighted composite index
    
    
    mapped_compound = {
        (0, 0.2): "A1",
        (0.2, 0.35): "A2",
        (0.35, 0.5): "B1",
        (0.5, 0.65): "B2",
        (0.65, 0.8): "C1",
        (0.8, 1): "C2",
    }

    breakpoint()    

    composite_index = sum(score * weight for score, weight in zip(normalized_scores, weights))
    
    print(f"Flesch Reading Ease: {flesch_reading_ease} - {metric_weights.get(flesch_reading_ease)}\nHigher scores indicate easier readability. \n")
    print(f"Flesch-Kincaid Grade: {flesch_kincaid_grade} - {metric_weights.get(flesch_kincaid_grade)}\nCorresponds to U.S. school grade levels. \n")
    # print(f"SMOG Index: {smog_index} - {metric_weights.get(smog_index)}\nEstimates the years of education needed to understand the text.\n")
    print(f"Coleman-Liau Index: {coleman_liau_index} - {metric_weights.get(coleman_liau_index)}\nEstimates the U.S. grade level needed to understand the text. \n")
    print(f"Automated Readability Index: {automated_readability_index} - {metric_weights.get(automated_readability_index)}\n Estimates the U.S. grade level. \n")
    print(f"Dale-Chall Readability Score: {dale_chall_readability_score} - {metric_weights.get(dale_chall_readability_score)}\nUses a list of common words to assess readability. \n")
    print(f"Difficult Words: {difficult_words} - {metric_weights.get(difficult_words)}\nCounts the number of complex words in the text. \n")
    print(f"Linsear Write Formula: {linsear_write_formula} - {metric_weights.get(linsear_write_formula)}\nEstimates the U.S. grade level. \n")
    print(f"Gunning Fog Index: {gunning_fog} - {metric_weights.get(gunning_fog)}\nEstimates the years of formal education needed to understand the text. \n")
    print("-"*204)
    print(f"Actual Composite Index: {composite_index}")

    for (min_range, max_range), level in mapped_compound.items():
        if min_range <= composite_index < max_range:
            
            return level
        




# Example usage


phrases = {
    "A1": "The cat is on the table.",
    "A2": "She likes to watch movies on weekends.",
    "B1": "I have been learning English for three years.",
    "B2": "She enjoys playing the piano in her free time and often performs at local events.",
    "C1": "Despite the challenges, she managed to complete the project on time and impressed her supervisors.",
    "C2": "Having studied abroad for several years, he possesses a profound understanding of cultural nuances and linguistic subtleties."
}





for goal_level, phrase in phrases.items():
    level = get_phrase_level(phrase)
    print(f"Desired Composite Index: {inverted_mapped_compound.get(goal_level)}")
    print(f"Actual Level {level} | Desired Level {goal_level}")
    print(f"Phrase: {phrase}")
    print("="*408)