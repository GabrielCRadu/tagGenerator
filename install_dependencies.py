import subprocess

# Instalați pachetele necesare folosind pip
subprocess.run(["pip", "install", "uvicorn", "spacy==3.7.4", "langdetect==1.0.9", "firebase_admin==6.5.0", "fastapi==0.110.3"])

# Descărcați modelele de limbă pentru engleză și română folosind spaCy
subprocess.run(["python", "-m", "spacy", "download", "en_core_web_md"])
subprocess.run(["python", "-m", "spacy", "download", "ro_core_news_md"])
