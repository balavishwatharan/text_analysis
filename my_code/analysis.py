# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 12:51:03 2024

@author: balav
"""
import load_resources
dir(load_resources)

import nltk
nltk.download('punkt') 
import os
import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize
import re
from load_resources import stopwords, positive_words, negative_words  # Import the loaded resources

# Load extracted article text files
extracted_articles_dir = r'C:\Users\balav\OneDrive\Desktop\project\ExtractedArticles'
output_data = []

# Utility functions for text analysis
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords]
    return tokens

def calculate_sentiment_scores(tokens):
    positive_score = sum(1 for word in tokens if word in positive_words)
    negative_score = sum(1 for word in tokens if word in negative_words)
    
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(tokens) + 0.000001)
    
    return positive_score, negative_score, polarity_score, subjectivity_score

def calculate_readability_metrics(tokens, sentences):
    word_count = len(tokens)
    sentence_count = len(sentences)
    complex_word_count = sum(1 for word in tokens if count_syllables(word) > 2)
    
    avg_sentence_length = word_count / sentence_count
    percentage_complex_words = complex_word_count / word_count
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    
    return avg_sentence_length, percentage_complex_words, fog_index, complex_word_count, word_count

def count_syllables(word):
    word = word.lower()
    syllable_count = 0
    vowels = "aeiou"
    if word[0] in vowels:
        syllable_count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            syllable_count += 1
    if word.endswith("es") or word.endswith("ed"):
        syllable_count -= 1
    return max(syllable_count, 1)

def count_personal_pronouns(text):
    pronouns = re.findall(r'\b(I|we|my|ours|us)\b', text, re.I)
    return len(pronouns)

def calculate_avg_word_length(tokens):
    total_characters = sum(len(word) for word in tokens)
    avg_word_length = total_characters / len(tokens)
    return avg_word_length

# Process each article and calculate metrics
for file_name in os.listdir(r'C:\Users\balav\OneDrive\Desktop\project\ExtractedArticles'):
    file_path = os.path.join(r'C:\Users\balav\OneDrive\Desktop\project\ExtractedArticles', file_name)
    
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    sentences = sent_tokenize(text)
    tokens = clean_text(text)
    
    # Calculate sentiment scores
    positive_score, negative_score, polarity_score, subjectivity_score = calculate_sentiment_scores(tokens)
    
    # Calculate readability metrics
    avg_sentence_length, percentage_complex_words, fog_index, complex_word_count, word_count = calculate_readability_metrics(tokens, sentences)
    
    # Count personal pronouns
    personal_pronouns_count = count_personal_pronouns(text)
    
    # Calculate average word length
    avg_word_length = calculate_avg_word_length(tokens)
    
    # Store the results in a dictionary
    result = {
        'URL_ID': file_name.split('.')[0],  # Extract URL_ID from file name
        'POSITIVE_SCORE': positive_score,
        'NEGATIVE_SCORE': negative_score,
        'POLARITY_SCORE': polarity_score,
        'SUBJECTIVITY_SCORE': subjectivity_score,
        'AVG_SENTENCE_LENGTH': avg_sentence_length,
        'PERCENTAGE_COMPLEX_WORDS': percentage_complex_words,
        'FOG_INDEX': fog_index,
        'COMPLEX_WORD_COUNT': complex_word_count,
        'WORD_COUNT': word_count,
        'SYLLABLE_PER_WORD': sum(count_syllables(word) for word in tokens) / word_count,
        'PERSONAL_PRONOUNS': personal_pronouns_count,
        'AVG_WORD_LENGTH': avg_word_length
    }
    
    output_data.append(result)

# Create a DataFrame from the results and save to CSV
output_df = pd.DataFrame(output_data)
output_df.to_csv('Output.csv', index=False)

print("Text analysis completed and output saved to Output.csv")
