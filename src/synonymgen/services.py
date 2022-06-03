"""Services for synonym generation"""
from nltk.corpus import wordnet as wn
from wordhoard import Synonyms


def get_synonyms_wordhoard(term):
    return Synonyms(search_string=term, output_format='list') \
        .find_synonyms()


def get_synonyms_wordnet(term):
    result_wordnet = []
    for syn in wn.synsets(term.replace(' ', '_')):
        for lemma in syn.lemmas():
            if lemma.name() not in result_wordnet:
                result_wordnet.append(lemma.name().replace('_', ' '))
    return result_wordnet