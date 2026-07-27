import spacy
from spacy import displacy
nlp = spacy.load("en_core_web_sm")

doc = nlp("The delivery was not good and the packaging was not bad.")
doc1 = nlp("I don't love the delivery and hate the packaging.")
doc2 = nlp("Not good delivery and not bad packaging.")
doc3 = nlp("The delivery was not broken and the packaging was not crushed.")
displacy.serve([doc, doc1, doc2, doc3], style="dep")