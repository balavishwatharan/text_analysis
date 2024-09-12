# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 12:41:42 2024

@author: balav
"""

import os

# Function to load stop words from the StopWords folder
def load_stopwords():
    stopwords = set()
    stopwords_dir = r'C:\Users\balav\OneDrive\Desktop\project\StopWords'
    
    for filename in os.listdir(stopwords_dir):
       if filename.endswith('.txt'):
           file_path = os.path.join(stopwords_dir, filename)
           for encoding in ['utf-8', 'latin1', 'utf-16']:
               try:
                   with open(file_path, 'r', encoding=encoding, errors='replace') as file:
                       stopwords.update(file.read().splitlines())
                   break 
               except UnicodeDecodeError:
                   print(f"Error decoding file {file_path} with encoding {encoding}")
               except Exception as e:
                   print(f"Error reading stopwords file: {e}")
    return stopwords

def load_dictionaries():
    positive_words = set()
    negative_words = set()
    
    # Define paths to your dictionary files
    positive_words_file = r'C:\Users\balav\OneDrive\Desktop\project\MasterDictionary\positive-words.txt'
    negative_words_file = r'C:\Users\balav\OneDrive\Desktop\project\MasterDictionary\negative-words.txt'
    
    # Load positive words
    try:
        with open(positive_words_file, 'r', encoding='utf-8', errors='replace') as file:
            positive_words.update(file.read().splitlines())
    except FileNotFoundError:
        print(f"File not found: {positive_words_file}")
    except Exception as e:
        print(f"Error reading positive words file: {e}")

    # Load negative words
    try:
        with open(negative_words_file, 'r', encoding='utf-8', errors='replace') as file:
            negative_words.update(file.read().splitlines())
    except FileNotFoundError:
        print(f"File not found: {negative_words_file}")
    except Exception as e:
        print(f"Error reading negative words file: {e}")
    
    return positive_words, negative_words

stopwords = load_stopwords()
positive_words, negative_words = load_dictionaries()