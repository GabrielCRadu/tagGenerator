import subprocess

# Defineți comenzile pentru descărcarea modelelor SpaCy pentru limba engleză și română
commands = [
    "python -m spacy download en_core_web_md",
    "python -m spacy download ro_core_news_md"
]

# Rulați fiecare comandă folosind subprocess
for command in commands:
    subprocess.run(command, shell=True)
