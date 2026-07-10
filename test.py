import spacy
from spacy import displacy
nlp = spacy.load("en_core_web_sm")
doc_dobj = nlp("I love the delivery and hate the packaging.")
doc_amod = nlp("The quick delivery")
doc_acomp = nlp("the delivery was very good and the packaging was very bad")
doc_neg = nlp("The delivery was not good")
doc_dobj2 = nlp("I do not love the delivery")
doc_nsubpass = nlp("The delivery was broken and the packaging was crushed.")
displacy.serve([doc_dobj, doc_amod, doc_acomp, doc_neg, doc_dobj2, doc_nsubpass], style="dep")
