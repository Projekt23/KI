FROM python:3.9

# Kopieren der requirements
COPY ./requirements.txt /app/requirements.txt
# Wechseln des Verzeichnisses in app
WORKDIR /app
#Installieren der Abhaengigkeiten
RUN pip install -r requirements.txt

# Kopieren des source-code
COPY . /app

# starten von Python
ENTRYPOINT [ "python" ]

# starten der Applikation
CMD [ "app.py" ]

# Port 5000 freigeben
EXPOSE 5000
