# ui/interface.py
import streamlit as st
from data.database import create_table, save_translations
from processing.document_processing import process_document
from docx import Document

def main():
    create_table()
    st.title("Document Word Translator")
    
    st.header("Upload .docx file")
    uploaded_file = st.file_uploader("Upload a .docx file", type=["docx"])

    if uploaded_file is not None:
        doc,translations = process_document(uploaded_file)
        save_translations(translations)
        save_doc(doc, translations)
        
    with open("modified_document.docx", "rb") as file:
        st.download_button(
            label="Download Modified Document",
            data=file,
            file_name="translated_Document.docx",
            mime="application/octet-stream"
        )

def save_doc(doc, translations):    
    for paragraph in doc.paragraphs:
        for word in translations:
            if f" {word} " in paragraph.text:
                paragraph.text = paragraph.text.replace(word, translations[word])

    modified_filename = "modified_document.docx"
    doc.save(modified_filename)