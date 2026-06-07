import spacy
from spacy.lang.en.stop_words import STOP_WORDS




def extract_keywords(doc: spacy.tokens.Doc) -> list[str]:
    keywords = []
    for token in doc:
        if token.pos_ in {"NOUN","ADJ","ADV"} and token.lemma_ not in STOP_WORDS:
            keywords.append(token.lemma_)
    return keywords

def extract_entities(doc: spacy.tokens.Doc) -> list[dict]:
    entities = []
    for ent in doc.ents:
        entities.append({"text": ent.text, "label": ent.label_})
    return entities

def extract_linguistic_metrics(doc: spacy.tokens.Doc) -> dict[str, float | bool]:
    # caculate lexical density as the ratio of content words to total words, punctuations are not counted as words
    lexical_density = len([token for token in doc if token.pos_ in {"NOUN","ADJ","ADV", "VERB"}])/len([token for token in doc if token.is_alpha])
    
    negation_detected = any(token.dep_ == "neg" for token in doc)
    return {"lexical_density": lexical_density, "negation_detected": negation_detected}