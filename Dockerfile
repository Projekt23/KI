FROM python:3.10

# Kopieren der requirements
COPY ./requirements.txt /app/requirements.txt
# Wechseln des Verzeichnisses in app
WORKDIR /app
#Installieren der Abhaengigkeiten
RUN pip install -r requirements.txt

# Download Tokenizer von spaCy
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download de_core_news_sm
RUN python -m nltk.downloader all

# Kopieren des source-code
COPY . /app

# starten von Python
ENTRYPOINT [ "python" ]

# starten der Applikation
CMD [ "run.py" ]

# Port 5000 freigeben
EXPOSE 5000
