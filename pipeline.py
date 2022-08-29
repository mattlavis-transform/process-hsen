import spacy
import en_core_web_lg


text = "Manchester United is a football team"
nlp = spacy.load("en_core_web_lg")
ruler = nlp.add_pipe("entity_ruler", before="ner")
patterns = [
    {"label": "GPE", "pattern": "Manchester United"}
]
# ruler.add_patterns(patterns)
doc = nlp(text)
for ent in doc.ents:
    print(ent.text, ent.label_)
