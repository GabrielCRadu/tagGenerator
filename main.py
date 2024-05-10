import re
import spacy
from collections import Counter
from langdetect import detect

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import firebase_admin
from firebase_admin import credentials, firestore

# Originile permise pentru CORS
origins = [
    "https://kreateapp.com",
    "https://www.kreateapp.com",
    "https://kreate.flutterflow.app",
]

# Inițializarea Firebase Admin
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Configurarea FastAPI
app = FastAPI()

# Middleware-ul CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Funcție pentru încărcarea modelului spaCy în funcție de limbă
def load_spacy_model(language):
    if language == "en":
        return spacy.load("en_core_web_md")  # en_core_web_sm
    elif language == "ro":
        return spacy.load("ro_core_news_md")  # ro_core_news_sm
    # Adaugă alte limbi și modelele lor
    else:
        # Încarcă un model spaCy generic pentru limbi necunoscute
        return spacy.blank(language)

# Funcție pentru filtrarea tag-urilor relevante
def filter_tags(doc, tags_count):
    tags_counter = Counter()
    # Iterează prin toate entitățile identificate în text
    for ent in doc.ents:
        # Excludem tag-urile care sunt prea scurte și sunt numerice
        if len(ent.text) > 1 and not ent.text.isnumeric():
            # Verificăm dacă entitatea este un nume de oraș, persoană sau alt tip de entitate
            if ent.label_ in ["GPE", "PERSON", "ORG"]:
                tags_counter[ent.text] += 1
    # Extrage toate substantivele și le ordonează după frecvență
    sorted_nouns = extract_nouns_and_sort_by_frequency(doc)
    # Ia doar primele `tags_count` tag-uri din lista de substantive
    top_nouns = [tag for tag, _ in sorted_nouns[:tags_count]]
    tags_counter.update(top_nouns)
    # Returnează primele `tags_count` entități cele mai frecvente
    return [tag for tag, _ in tags_counter.most_common(tags_count)]

# Funcție pentru a identifica toate substantivele și a le ordona după frecvență
def extract_nouns_and_sort_by_frequency(doc):
    # Initializează un contor pentru a număra aparițiile fiecărui substantiv
    noun_counter = Counter()
    # Iterează prin toate entitățile identificate în text
    for token in doc:
        # Verifică dacă token-ul este un substantiv și adaugă-l în contor
        if token.pos_ == "NOUN":
            noun_counter[token.text.lower()] += 1
    # Returnează lista de substantive ordonată după frecvența aparițiilor
    return noun_counter.most_common()

# Funcție pentru curățarea textului de emoji-uri și simboluri folosind expresii regulate
def clean_text(text):
    cleaned_text = re.sub(r"[^\w\s]", "", text)
    return cleaned_text

# Definirea endpoint-ului API pentru obținerea tag-urilor și actualizarea listei post_tags
@app.get("/getTags/{user_id}/{post_id}/{tagsCount}")
async def get_tags(user_id: str, post_id: str, tagsCount: int):
    # Obține referința către documentul din subcolecția 'posts' a utilizatorului
    doc_ref = db.collection("users").document(user_id).collection("posts").document(post_id)
    # Obține datele documentului
    doc_data = doc_ref.get().to_dict()
    if not doc_data:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Extrage textul din document, presupunând că este stocat sub cheia 'post_description'
    inputText = doc_data.get("post_description", "")

    # Curăță textul de emoji-uri și simboluri
    cleaned_input = clean_text(inputText)
    # Detectează limba textului curățat
    language = detect(cleaned_input)
    # Încarcă modelul spaCy pentru limba detectată
    nlp = load_spacy_model(language)
    # Aplică modelul spaCy pe textul curățat
    doc = nlp(cleaned_input)
    # Filtrare tag-uri relevante
    filtered_tags = filter_tags(doc, tagsCount)
    
    # Actualizează lista post_tags în documentul Firebase
    doc_ref.update({"post_tags": filtered_tags})
    
    # Returnează rezultatul
    return {"success": True, "tags": filtered_tags}

@app.get("/wake")
async def wake_server():
    # Aici puteți adăuga orice cod pe care doriți să îl rulați când endpoint-ul este accesat
    return {"message": "Server has woken"}
