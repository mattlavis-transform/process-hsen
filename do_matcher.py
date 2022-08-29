import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_md")
matcher = Matcher(nlp.vocab)
pattern = [
    {"LIKE_EMAIL": True}
]
matcher.add("EMAIL_ADDRESS", [pattern])
doc = nlp("This is an email address: geoff@goeereyson.com")
matches = matcher(doc)
print(matches)
print(nlp.vocab[matches[0][0]].text)
