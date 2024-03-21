import streamlit as st
from docx import Document
import nltk
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd
from data.database import load_translations
from deep_translator import GoogleTranslator

nltk.download('stopwords')
nltk.download('punkt')


stop_words = set(stopwords.words('english'))
stop_words_lower = set(word.lower() for word in stop_words)

def process_document(file):
    doc = Document(file)

    translations = load_translations()  

    text = [paragraph.text for paragraph in doc.paragraphs]

    full_text = ' '.join(text)

    words = nltk.word_tokenize(full_text)
    words = [word.lower() for word in words if word.isalpha()]

    words = [word for word in words if word not in stop_words_lower]

    word_counts = Counter(words)

    top_words = word_counts.most_common(100)

    df = pd.DataFrame(top_words, columns=["Word", "Frequency"])

    translations_new = {}
    st.subheader("Enter Translations:")

    words_per_page = 20  
    total_pages = (len(df) - 1) // words_per_page + 1
    current_page = st.session_state.get("current_page", 0)

    start_index = current_page * words_per_page
    end_index = min((current_page + 1) * words_per_page, len(df))
    words_to_display = df[start_index:end_index]

    for word_index, (word, _) in words_to_display.iterrows():
        if st.button(f"Get Suggestions from Google ({word})", key=f"suggestion_button_{word_index}"):
            translation = suggest_translation(word)
        else:
            translation = translations.get(word, '')
        translations_new[word.lower()] = st.text_input(f"Enter translation for '{word}':", value=translation)

    col1, col2 = st.columns([1, 2])
    with col1:
        if current_page > 0:
            if st.button("Previous", key="previous_button"):
                current_page -= 1
    with col2:
        if current_page < total_pages - 1:
            if st.button("Next", key="next_button"):
                current_page += 1

    st.session_state["current_page"] = current_page

    return doc, translations_new


def suggest_translation(word):
    translated = GoogleTranslator(source='auto', target='te').translate(word)
    return translated
