import sqlite3

def create_table():
    conn = sqlite3.connect("translations.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS translations
                 (word TEXT PRIMARY KEY, translation TEXT)''')
    conn.commit()
    conn.close()

def save_translations(translations):
    conn = sqlite3.connect("translations.db")
    c = conn.cursor()
    for word, translation in translations.items():
        if translation == "":
            continue
        c.execute("INSERT OR REPLACE INTO translations (word, translation) VALUES (?, ?)", (word, translation))
    conn.commit()
    conn.close()

def load_translations():
    translations = {}
    conn = sqlite3.connect("translations.db")
    c = conn.cursor()
    c.execute("SELECT * FROM translations")
    rows = c.fetchall()
    for row in rows:
        translations[row[0]] = row[1]
    conn.close()
    
    return translations
