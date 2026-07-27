import spacy

from nlp_utils import extract_aspects


nlp = spacy.load("en_core_web_sm")


def test_extracts_delivery_from_direct_object():
    doc = nlp("I love the delivery.")

    results = extract_aspects(doc)

    assert len(results) == 1
    assert results[0].aspect == "delivery"
    assert results[0].polarity > 0

def test_extracts_from_two_direct_objects():
    doc = nlp("I love the delivery and hate the packaging.")
    results = extract_aspects(doc)
    assert len(results) == 2
    assert results[0].aspect == "delivery"
    assert results[1].aspect == "packaging"
    assert results[0].polarity > 0
    assert results[1].polarity < 0

def test_extracts_from_amod():
    doc = nlp("The excellent delivery and the terrible packaging.")
    results = extract_aspects(doc)
    assert len(results) == 2
    assert results[0].aspect == "delivery"
    assert results[1].aspect == "packaging"
    assert results[0].polarity > 0
    assert results[1].polarity < 0

def test_extracts_from_nsubj():
    doc = nlp("The delivery was very good and the packaging was very bad.")
    results = extract_aspects(doc)
    assert len(results) == 2
    assert results[0].aspect == "delivery"
    assert results[1].aspect == "packaging"
    assert results[0].polarity > 0
    assert results[1].polarity < 0

def test_extracts_from_nsubjpass():
    doc = nlp("The delivery was broken and the packaging was crushed.")
    results = extract_aspects(doc)
    assert len(results) == 2
    assert results[0].aspect == "delivery"
    assert results[1].aspect == "packaging"
    assert results[0].polarity < 0
    assert results[1].polarity < 0

def test_extracts_from_negation():
    doc = nlp("The delivery was not good and the packaging was not bad.")
    results = extract_aspects(doc)
    assert len(results) == 2
    assert results[0].aspect == "delivery"
    assert results[1].aspect == "packaging"
    assert results[0].polarity < 0
    assert results[1].polarity > 0