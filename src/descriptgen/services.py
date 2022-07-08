"""Services for description generation"""
import spacy
from spacy.lang.en.stop_words import STOP_WORDS as STOP_WORDS_EN
from spacy.lang.de.stop_words import STOP_WORDS as STOP_WORDS_DE
from string import punctuation
from collections import Counter
from heapq import nlargest

import wikipedia
import requests
from bs4 import BeautifulSoup

# import tokenizers
nlp_en = spacy.load('en_core_web_sm')
nlp_de = spacy.load('de_core_news_sm')


def search_wiki(term):
    """
    Unused search of wikipedia by external library.
    """
    return wikipedia.search(term)


def get_wiki_site_text(sitename):
    """
    Unused function to extract the content from a wikipedia site by name.
    """

    try:
        page = wikipedia.page(sitename)
    except wikipedia.exceptions.DisambiguationError as e:
        sitename = '\n'.join(str(e).split('\n')[1:])[0]
    return wikipedia.page(sitename).content


def get_wiki_text(term, sent=5, lang='en'):
    """
    Fetches the summarized text from a wikipedia article.
    """

    list = search_wiki(term)
    print(clean_wiki_content(api_search(term)))
    print("List = ", list)
    if len(list) == 0:
        return 'No result found.'
    return summarize_text(get_wiki_site_text(list[0]), sent=sent, lang='en')


def summarize_text(text, sent=5, lang='en'):
    """
    Summarizes a text to a predetermined length. If input text is shorter, returns full text.

    Parameters
    ----------
    text: text to be summarized
    sent: maximum number of sentences of result text
    lang: language of the text

    Returns
    -------
    a tuple of the summarized text and the number of sentences
    """
    if lang == 'de':
        stopwords = list(STOP_WORDS_DE)
        doc = nlp_de(text)
    else:
        stopwords = list(STOP_WORDS_EN)
        doc = nlp_de(text)
    length_sent = min(sent, len(list(doc.sents)))
    print('Number of sentences = ', len(list(doc.sents)))

    if sent == 0:
        return text

    keyword = []

    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    for token in doc:
        if token.text in stopwords or token.text in punctuation:
            continue
        if token.pos_ in pos_tag:
            keyword.append(token.text)

    freq_word = Counter(keyword)

    # get most common token
    max_freq = Counter(keyword).most_common(1)[0][1]

    # normalize token frequency
    for word in freq_word.keys():
        freq_word[word] = (freq_word[word] / max_freq)

    # calculate sentence strength
    sent_strength = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent] += freq_word[word.text]
                else:
                    sent_strength[sent] = freq_word[word.text]

    print('n = ', length_sent)
    print('iterable = ', sent_strength)
    summarized_sentences = nlargest(n=length_sent, iterable=sent_strength, key=sent_strength.get)

    # convert to string
    final_sentences = [w.text for w in summarized_sentences]
    summary = ' '.join(final_sentences)

    return (summary, length_sent)


def api_search(query):
    """
    Calls wikipedia search and fetch page content of the most fitting article.

    Parameters
    ----------
    query: query term

    Returns
    -------
    content as string
    """

    search_response = requests.get(
        "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=" + query + "&format=json")
    search_data = search_response.json()
    page_id = str((search_data['query']['search'][0]['pageid']))
    title = (search_data['query']['search'][0]['title']).replace(" ", "%20")

    # Aufruf um die Inhalte der Wikipedia-Seite zu extrahieren
    page_response = requests.get(
        "https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&rvsection=0&titles="
        + title + "&format=json")
    page_data = page_response.json()
    # Content aus JSON herausfiltern
    content = (page_data['query']['pages'][page_id]['revisions'][0]['*'])
    return content


def scraper_search(query):
    # Aufruf auf die Wikipedia-Suche um die genaue Wikipedia-Seite zu finden
    search_url = 'https://en.wikipedia.org/w/index.php?search=' + query + '&title=Spezial%3ASuche&profile=advanced&fulltext=1&ns0=1'
    print(search_url)
    website = requests.get(search_url)
    search_results = BeautifulSoup(website.content, 'html.parser')
    # Extrahieren des Inhalts vom ersten Listeneintrag der Such-Ergebnisse
    search_page = search_results.find("li", class_="mw-search-result").find("a", href=True)['href']
    # Aufruf auf die exakte Wikipedia-Seite
    page_url = "https://en.wikipedia.org" + search_page
    print(page_url)
    website2 = requests.get(page_url)
    page_results = BeautifulSoup(website2.content, 'html.parser')
    # Extrahieren des ersten paragraphen auf der Seite
    content = page_results.find("p")
    return str(content)


def clean_content(content):
    """
    Cleans the content of the wikipedia page by removing unwanted tags and other encoded symbols.
    """
    while content.find("<!--", 0, len(content)) != -1:  # Prüft ob der gegebene Substring im gegebenen String vorliegt,
        # Schleife besteht solange der Substring gefunden wird.
        if content.find("-->", 0, len(content)) != -1:  # wenn Schliesszeichen vorhanden
            for nr2 in reversed(range(content.find("<!--", 0, len(content)), content.find("-->", 0, len(content)) + 3)):
                content = content[0: nr2:] + content[nr2 + 1::]
        else:
            raise ValueError(
                f"Schliessendes Zeichen fuer <!-- nicht vorhanden an stelle {content.find('<!--', 0, len(content))}")

    while (content.find("<ref", 0,
                        len(content)) != -1):  # Prüft ob der gegebene Substring im gegebenen String vorliegt,
        # Schleife besteht solange der Substring gefunden wird.
        if content.find("</ref>", 0, len(content)) != -1:
            replaceStart = content.find("<ref", 0, len(content))
            replaceEnd = content.find("</ref>", 0, len(content)) + 6
            for nr2 in reversed(range(replaceStart, replaceEnd)):
                content = content[0: nr2:] + content[nr2 + 1::]
        else:
            if content.find(">", 0, len(content)) != -1:  # wenn Schliesszeichen vorhanden
                for nr2 in reversed(
                        range(content.find("<ref", 0, len(content)), content.find(">", 0, len(content)) + 1)):
                    content = content[0: nr2:] + content[nr2 + 1::]
            else:
                raise ValueError(
                    f"Schliessendes Zeichen fuer <ref nicht vorhanden an stelle {content.find('<ref', 0, len(content))}")

        # Zeilenumbrüche entfernen
    content = content.replace("\n", "")
    # Tiefergestellte HTML entfernen
    content = content.replace("<sub>", "")
    content = content.replace("</sub>", "")
    # Zeichen fuer "bold" entfernen
    content = content.replace("'''", "")
    # Zeichen fuer "kursiv" entfernen
    content = content.replace("''", "")
    # übrig gebliebene Links zu normalen Wörtern machen
    content = content.replace("[[", "")
    content = content.replace("]]", "")
    # HTML-Leerzeichen ersetzen
    content = content.replace("&nbsp;", " ")
    # Leere Klammern (bspw. durch entfernte Verlinkungen entstanden) entfernen
    content = content.replace("()", "")
    return content


def KlammernZusammenordnen(Zeichenliste):
    """
    Funktion um aus einer Liste die Klammern heraus und zu Paaren zusammen zu sortieren.
    Da hierbei die Indices der Klammern gegeben werden, kann später der Inhalt der Klammer recht einfach bearbeitet werden.
    Während dem Sortieren fällt außerdem auf, wenn das Gegenstück zu einzelnen Klammern fehlt
    Parameters
    ----------
    Zeichenliste : Liste mit Strings die jeweils ein einzelnes Zeichen enthalten (Variablennamen wie n_an etc sind ok, Klammern müssen
                   jedoch als einzelnes Zeichen vorliegen)
    Raises
    ------
    ValueError wenn Zeichen fehlen.
    Returns
    -------
    KlammerlisteSortiert : Dict mit Klammerindices als Schluessel und Liste [Klammerstring,
                            bool: oeffnendes Zeichen, Partnerzeichen Index]
    """

    KlammerlisteSortiert = {}
    # Dict von Zusatzzeichen, die beachtet werden müssen, jeweils der Schlüssel das Zeichen selbst
    # Wenn das Zeichen als Paar auftritt der Wert als Partnerzeichen. Bei Zeichen ohne Partner Schüssel und Wert als das Zeichen
    # zusätzlich True für öffnende und False für schließende Zeichen
    dictValideZeichen = {"(": [")", True], ")": ["(", False], "[": ["]", True], "]": ["[", False], "{": ["}", True],
                         "}": ["{", False]}
    zeichenIndices = [zeichenNr for zeichenNr in range(len(Zeichenliste)) if
                      (Zeichenliste[zeichenNr] in dictValideZeichen.keys())]

    zeichenInListe = [Zeichenliste[nr] for nr in zeichenIndices]
    offenePaare = []
    offenePaareIndices = []
    for zeichenNr, zeichen in enumerate(zeichenInListe):
        if (dictValideZeichen[zeichen][1]):  # Wenn öffnendes Zeichen dann einfach an zu schließende Zeichen anhängen
            offenePaare.append(zeichen)
            offenePaareIndices.append(zeichenIndices[zeichenNr])
        else:
            if (len(
                    offenePaare) > 0):  # Wenn noch zu schließende Zeichen für das vorliegende schließende Zeichen vorhanden sind
                if (offenePaare[-1] == dictValideZeichen[zeichen][
                    0]):  # wenn das letzte offene Paarzeichen das Gesuchte ist, dann die Paarung speichern
                    KlammerlisteSortiert[offenePaareIndices[-1]] = [offenePaare[-1], True, zeichenIndices[zeichenNr]]
                    KlammerlisteSortiert[zeichenIndices[zeichenNr]] = [zeichen, False, offenePaareIndices[-1]]
                    del offenePaare[-1]
                    del offenePaareIndices[-1]
                else:  # Wenn noch eine andere Paarung offen ist (letztes Zeichen ungleich dem Gesuchten) liegt ein Fehler vor
                    pass
            else:
                pass
    return KlammerlisteSortiert


def clean_wiki_content(content):
    """
    Cleans the content of the wikipedia page by removing unwanted tags and other encoded symbols.
    """
    change = -1
    while (
            change != 0):  # Solange es eine Änderung innerhalb der Schleife gab, soll eine weitere Iteration der Schleife erfolgen.
        change = 0
        klammerDict = KlammernZusammenordnen(
            content)  # Aus dem Text sollen zusammengehörige Klammern herausgesucht werden, um zusammmenhängende Textpassagen zu identifizieren.
        for nr, z in enumerate(content):
            if (nr in klammerDict):
                if (z == "{"):
                    if (content[nr + 1:nr + 5] == "{IPA"):
                        # Entfernen der schließenden geschweiften Klammern
                        content = content[0: klammerDict[nr][2]:] + content[klammerDict[nr][2] + 1::]
                        content = content[0: klammerDict[nr][2] - 1:] + content[klammerDict[nr][2]::]
                        # Entfernen der öffnenden geschweiften Klammern und "IPA"
                        # Alles dazwischen soll beibehalten werden
                        for nr2 in reversed(range(nr, nr + 6)):
                            content = content[0: nr2:] + content[nr2 + 1::]
                        change += 1
                        break
                    else:  # Bei allen anderen Fällen soll alles innerhalb der gescheiften Klammern entfernt werden
                        for nr2 in reversed(range(nr, klammerDict[nr][2] + 1)):
                            content = content[0: nr2:] + content[nr2 + 1::]
                        change += 1
                        break

                if (z == "["):
                    # Wenn eine Textpassage mit eckigen Klammern und "Datei:" beginnt, soll die gesamte Passage entfernt werden.
                    if (content[nr + 1:nr + 8] == "[Datei:"):
                        for nr2 in reversed(range(nr, klammerDict[nr][2] + 1)):
                            content = content[0: nr2:] + content[nr2 + 1::]
                        change += 1
                        break
                    if (content[nr + 1] == "["):
                        # Wenn ein Link vorhanden ist, soll das Wort ohne den Link und die Klammern beibehalten werden
                        # Der Link befindet sich in solchen Textpassagen nach dem "/"
                        if ("|" in content[nr:klammerDict[nr][2] + 1]):
                            content = content[0: klammerDict[nr][2]:] + content[klammerDict[nr][2] + 1::]
                            content = content[0: klammerDict[nr][2] - 1:] + content[klammerDict[nr][2]::]
                            for nr2 in reversed(range(nr, nr + content[nr:klammerDict[nr][2] + 1].find('|') + 1)):
                                content = content[0: nr2:] + content[nr2 + 1::]
                            change += 1
                            break

    while content.find("<!--", 0, len(content)) != -1:  # Prüft ob der gegebene Substring im gegebenen String vorliegt,
        # Schleife besteht solange der Substring gefunden wird.
        if content.find("-->", 0, len(content)) != -1:  # wenn Schliesszeichen vorhanden
            for nr2 in reversed(range(content.find("<!--", 0, len(content)), content.find("-->", 0, len(content)) + 3)):
                content = content[0: nr2:] + content[nr2 + 1::]
        else:
            raise ValueError(
                f"Schliessendes Zeichen fuer <!-- nicht vorhanden an stelle {content.find('<!--', 0, len(content))}")

    while (content.find("<ref", 0,
                        len(content)) != -1):  # Prüft ob der gegebene Substring im gegebenen String vorliegt,
        # Schleife besteht solange der Substring gefunden wird.
        if content.find("</ref>", 0, len(content)) != -1:
            replaceStart = content.find("<ref", 0, len(content))
            replaceEnd = content.find("</ref>", 0, len(content)) + 6
            for nr2 in reversed(range(replaceStart, replaceEnd)):
                content = content[0: nr2:] + content[nr2 + 1::]
        else:
            if content.find(">", 0, len(content)) != -1:  # wenn Schliesszeichen vorhanden
                for nr2 in reversed(
                        range(content.find("<ref", 0, len(content)), content.find(">", 0, len(content)) + 1)):
                    content = content[0: nr2:] + content[nr2 + 1::]
            else:
                raise ValueError(
                    f"Schliessendes Zeichen fuer <ref nicht vorhanden an stelle {content.find('<ref', 0, len(content))}")

    # Zeilenumbrüche entfernen
    content = content.replace("\n", "")
    # Tiefergestellte HTML entfernen
    content = content.replace("<sub>", "")
    content = content.replace("</sub>", "")
    # Zeichen fuer "bold" entfernen
    content = content.replace("'''", "")
    # Zeichen fuer "kursiv" entfernen
    content = content.replace("''", "")
    # übrig gebliebene Links zu normalen Wörtern machen
    content = content.replace("[[", "")
    content = content.replace("]]", "")
    # HTML-Leerzeichen ersetzen
    content = content.replace("&nbsp;", " ")
    # Leere Klammern (bspw. durch entfernte Verlinkungen entstanden) entfernen
    content = content.replace("()", "")

    return content
