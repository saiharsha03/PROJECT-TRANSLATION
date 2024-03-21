# processing/document_processing.py
from docx import Document
import nltk
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd
from data.database import load_translations 
import streamlit as st
from deep_translator import GoogleTranslator
nltk.download('stopwords')
nltk.download('punkt')

def process_document(file):
    doc = Document(file)
    
    translations = load_translations() #To load existing translations
    
    text = [paragraph.text for paragraph in doc.paragraphs]
    
    full_text = ' '.join(text)
    
    words = nltk.word_tokenize(full_text)
    words = [word.lower() for word in words if word.isalpha()]

    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    word_counts = Counter(words)

    top_words = word_counts.most_common(100)

    df = pd.DataFrame(top_words, columns=["Word", "Frequency"])
 
    translations_new = {}
    st.subheader("Enter Translations:")
    
    for word_index, word in enumerate(df["Word"]):
        if st.button(f"Get Suggestions from Google ({word})", key=f"suggestion_button_{word_index}"):
            translation = suggest_translation(word)
        else:
            translation = translations.get(word, '')
        translations_new[word.lower()] = st.text_input(f"Enter translation for '{word}':", value=translation)
    
    return doc, translations_new

def suggest_translation(word):
    translated = GoogleTranslator(source='auto', target='te').translate(word)
    return translated
