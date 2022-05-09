from nltk.corpus import wordnet as wn
import pandas as pd

def SynonymsFromWordnet(searchterm):
    """ Get synonyms or related phrases """
    
    searchterm = searchterm.lower().replace(' ','_') #+ '.n.01'
    try:
        synonyms = []
        for syn in wn.synsets(searchterm):
            for lm in syn.lemmas():
                synonyms.append(lm.name().lower())                
    except ValueError:
        return [searchterm]
    
    synonyms = list(dict.fromkeys(synonyms))
    print(synonyms)
    return synonyms

#SynonymsFromWordnet('invoice')
#SynonymsFromWordnet('order')
#SynonymsFromWordnet('customer')
#SynonymsFromWordnet('receipt')

def ReadSAPGlossary():
    df = pd.read_csv('data/en_sap_glossar.csv')
    examples = df.sample(n=5)['title']
    for term in examples:
        result = []
        print(term)
        subterms = term.split(' ')
        for subterm in subterms:
            result.extend(SynonymsFromWordnet(subterm))
        print(result)

ReadSAPGlossary()


