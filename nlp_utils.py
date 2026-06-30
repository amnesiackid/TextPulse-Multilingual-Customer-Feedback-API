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
    # TO DO: solve multi-word aspect and multiple sentment words for one aspect
    aspects = [token for token in doc if token.lemma_ in ASPECT_VOCAB]
    aspect_results = []
    for aspect in aspects:
        # amod scenario where aspect is the object of a verb, e.g. "I love the delivery"
        sentiment_word = next((child for child in aspect.children if child.dep_ == "amod"), None)
        # passive scenario where aspect is the subject of a passive verb, e.g. "the delivery was broken"
        if not sentiment_word and aspect.dep_ == "nsubjpass":
            sentiment_word = aspect.head
        # adjectival complement scenario, e.g. "the delivery was very good"
        if not sentiment_word and aspect.dep_ == "nsubj":
            sentiment_word = next((child for child in aspect.head.children if child.dep_ == "acomp"), None)
        if sentiment_word:
            sentiment_excerpt = " ".join(w.text for w in sentiment_word.subtree)
            polarity = sia.polarity_scores(sentiment_excerpt)["compound"]
            excerpt = " ".join(w.text for w in aspect.subtree)
            aspect_results.append(models.AspectResult(aspect=aspect.lemma_, polarity=polarity, excerpt=excerpt))
        else:
            print("Sentiment word not found")
            
    return aspect_results