import spacy
from spacy import displacy
from spacy.lang.en import stop_words
nlp = spacy.load("en_core_web_sm")
stop_words = stop_words.STOP_WORDS
doc = nlp("DHL lost my package in Berlin.")


def extract_keywords(doc) -> list[str]:
    keywords = []
    for token in doc:
        if token.pos_ in {"NOUN","ADJ","ADV"} and token.lemma_ not in stop_words:
            keywords.append(token.lemma_)
    return keywords

def extract_entities(doc) -> list[dict]:
    entities = []
    for ent in doc.ents:
        entities.append({"text": ent.text, "label": ent.label_})
    return entities

def extract_linguistic_metrics(doc) -> dict[str, float | bool]:
    # caculate lexical density as the ratio of content words to total words, punctuations are not counted as words
    lexical_density = len([token for token in doc if token.pos_ in {"NOUN","ADJ","ADV", "VERB"}])/len([token for token in doc if token.is_alpha])
    
    negation_detected = any(token.dep_ == "neg" for token in doc)
    return {"lexical_density": lexical_density, "negation_detected": negation_detected}