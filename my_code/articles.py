# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 12:14:01 2024

@author: balav
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Loading the url
input_df = pd.read_excel(r'C:\Users\balav\OneDrive\Desktop\project\Input.xlsx')

# Create a directory for the extracted articles
if not os.path.exists(r'C:\Users\balav\OneDrive\Desktop\project\ExtractedArticles'):
    os.makedirs(r'C:\Users\balav\OneDrive\Desktop\project\ExtractedArticles')
    

# Function to extract article text
def extract_article_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = soup.find('h1').get_text() if soup.find('h1') else "No Title"
        
        # Extract article text
        article_text = ' '.join([p.get_text() for p in soup.find_all('p')])
        
        return title + "\n" + article_text
    except Exception as e:
        print(f"Error extracting {url}: {e}")
        return None

# Extract articles and save to text files
for index, row in input_df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    
    article_text = extract_article_text(url)
    
    if article_text:
        with open(os.path.join(r'C:\Users\balav\OneDrive\Desktop\project\ExtractedArticles', f'{url_id}.txt'), 'w', encoding='utf-8') as file:
            file.write(article_text)
    else:
        print(f"Failed to extract article for URL_ID: {url_id}")
