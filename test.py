import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("the delivery was broken and bad")
dep_broken = doc[3].dep_
dep_bad = doc[5].dep_
print(dep_broken, dep_bad)
