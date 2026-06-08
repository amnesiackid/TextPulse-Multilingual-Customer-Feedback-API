import spacy
import models
from spacy.lang.en.stop_words import STOP_WORDS
from dependencies import ASPECT_VOCAB
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()


def extract_keywords(doc: spacy.tokens.Doc) -> list[str]:
    keywords = []
    for token in doc:
        if token.pos_ in {"NOUN","ADJ","ADV"} and token.lemma_ not in STOP_WORDS:
            keywords.append(token.lemma_)
    return keywords

def extract_entities(doc: spacy.tokens.Doc) -> list[models.EntityResult]:
    return [models.EntityResult(text=ent.text, label=ent.label_) for ent in doc.ents]

def extract_linguistic_metrics(doc: spacy.tokens.Doc) -> models.LinguisticMetrics:
    # caculate lexical density as the ratio of content words to total words, punctuations are not counted as words
    lexical_density = len([token for token in doc if token.pos_ in {"NOUN","ADJ","ADV", "VERB"}])/len([token for token in doc if token.is_alpha])
    
    negation_detected = any(token.dep_ == "neg" for token in doc)
    return models.LinguisticMetrics(lexical_density=lexical_density, negation_detected=negation_detected)

def extract_aspects(doc: spacy.tokens.Doc) -> list[models.AspectResult]:
    aspects = [token for token in doc if token.lemma_ in ASPECT_VOCAB]
    aspect_results = []
    for aspect in aspects:
        sentiment_word = next((child for child in aspect.children if child.dep_ == "amod"), None)
        # passive scenario where aspect is the subject of a passive verb, e.g. "the delivery was broken"
        if not sentiment_word and aspect.dep_ == "nsubjpass":
            sentiment_word = next((child for child in aspect.children if child.dep_ == "ROOT"), None)
        # adverbial modifier scenario, e.g. "the delivery was very good"
        if not sentiment_word:
            sentiment_word = next((child for child in aspect.children if child.dep_ == "advmod"), None)    
        # amod scenario where aspect is the object of a verb, e.g. "I love the delivery"
        if sentiment_word:
            polarity = sia.polarity_scores(sentiment_word.text)["compound"]
            head = aspect.head
            excerpt = " ".join(w.text for w in aspect.subtree)
            aspect_results.append(models.AspectResult(aspect=aspect.lemma_, polarity=polarity, excerpt=excerpt))
    return aspect_results