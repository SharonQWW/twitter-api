#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 18:20:15 2020

@author: qyang
"""

#%%google language
from google.cloud import language

def analyze_text_sentiment(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)

    response = client.analyze_sentiment(document=document)

    sentiment = response.document_sentiment
    results = dict(
        text=text,
        score=f"{sentiment.score:.1%}",
        magnitude=f"{sentiment.magnitude:.1%}",
    )
    for k, v in results.items():
        print(f"{k:10}: {v}")
        
        
text = "Guido van Rossum is great!"
analyze_text_sentiment(text)       

#%%spacy - more of a cleaner, no sentiments function
# pip install spacy
# python -m spacy download en_core_web_sm
# https://nicschrading.com/project/Intro-to-NLP-with-spaCy/

import spacy
import en_core_web_sm

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = en_core_web_sm.load()

# Process whole documents
text = ("When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week.")
doc = nlp(text)

# Analyze syntax
print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)
    
    
#%%textblob - can be used for sentiment analyzor
# pip install -U textblob
# python -m textblob.download_corpora
# https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis

from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
opinion = TextBlob("EliteDataScience.com is dope!", analyzer=NaiveBayesAnalyzer())
result_t = opinion.words #creates a word list
result_s = opinion.sentiment
