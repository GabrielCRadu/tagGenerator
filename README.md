
# 🏷️ tagGenerator for KREATE

Un microserviciu/back‑end/tool care generează automat tag-uri relevante pentru conținut (postări, imagini, text) în aplicația **KREATE**.

---

## 🔍 Scop

În **KREATE**, utilizatorii postează conținut multimedia (imagini, texte). Acest modul analizează aceste postări și generează automat tag-uri relevante, pentru:

- Filtrare și căutare eficientă în feed  
- Organizarea automată în categorii  
- Sugestii de tag-uri în interfață

---

## 🧩 Funcționare

1. Primește un document (text brut) sau descriere asociată unui conținut  
2. Preprocesează textul: tokenizare, eliminare stop-words  
3. Calculează TF-IDF* și selectează cele mai semnificative cuvinte  
4. Returnează un set de N tag-uri

*TF-IDF scoate în evidență cuvintele specifice unui text, ignorând cuvintele comune (gen „este”, „și”, „în”, „the”, „is”)

---

## 🚀 Instalare & Utilizare

### Clonare
```bash
git clone https://github.com/GabrielCRadu/tagGenerator.git
cd tagGenerator
```

### Instalare dependențe
Proiectul este scris în **Python**. Instalează dependențele:
```bash
pip install -r requirements.txt
```

### Exemple de rulare
#### CLI:
```bash
python tagGenerator.py --input "Acesta este textul pe care vrei să-l tag‑ezi" --num-tags 5
```

#### Ca modul Python:
```python
from tagGenerator import TagGenerator

tg = TagGenerator()
tags = tg.generate("Un exemplu de conținut pentru tag generator", 5)
print(tags)  # ex: ['exemplu', 'tag', 'generator', ...]
```

---

## 🛠️ Configurații

- `--num-tags`: numărul de tag-uri de returnat (implicit: 5)  
- `--language`: specifică limba pentru stop‑words (ex: ro, en)  
- Alte opțiuni: praguri TF-IDF, regex, normalizare, etc.

---

## 🧪 Testare

```bash
pytest tests/
```

Acoperă cazuri tipice, generare pentru texte română/engleză și filtrare diacritice.

---

## 🌱 Exemple

| Intrare                                      | Output (tags)                      |
|----------------------------------------------|------------------------------------|
| `"Astăzi am vorbit despre inteligență artificială și machine learning"` | ["inteligență", "artificială", "machine", "learning"] |
| `"Festival de muzică, concerte și artă"`     | ["festival", "muzică", "concerte", "artă"] |

---


## ⚙️ Roadmap / Direcții viitoare

- Suport pentru tag-uri generate din imagine (CV + NLP)  
- Model semantic (Word2Vec/Transformers) în loc de TF-IDF  
- API RESTful pentru integrare directă în backend  



# Deploy FastAPI on Render

Use this repo as a template to deploy a Python [FastAPI](https://fastapi.tiangolo.com) service on Render.

See https://render.com/docs/deploy-fastapi or follow the steps below:

## Manual Steps

1. You may use this repository directly or [create your own repository from this template](https://github.com/render-examples/fastapi/generate) if you'd like to customize the code.
2. Create a new Web Service on Render.
3. Specify the URL to your new repository or this repository.
4. Render will automatically detect that you are deploying a Python service and use `pip` to download the dependencies.
5. Specify the following as the Start Command.

    ```shell
    uvicorn main:app --host 0.0.0.0 --port $PORT
    ```

6. Click Create Web Service.

Or simply click:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/render-examples/fastapi)

## Thanks

Thanks to [Harish](https://harishgarg.com) for the [inspiration to create a FastAPI quickstart for Render](https://twitter.com/harishkgarg/status/1435084018677010434) and for some sample code!
