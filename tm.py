from target_matcher import TargetMatcher, TargetRule
import spacy
from spacy.tokens import Span

# Register a new custom attribute to store ICD-10 diagnosis codes
Span.set_extension("icd10_code", default="")

nlp = spacy.blank("en")
target_matcher = TargetMatcher(nlp)
nlp.add_pipe(target_matcher)

rules = [
    TargetRule(
        literal="Type II Diabetes Mellitus", category="PROBLEM",
        attributes={"icd10_code": "E11.9"}
    ),
    TargetRule(
        literal="Type II Diabetes Mellitus", category="PROBLEM",
        pattern=[{"LOWER": "type"}, {"LOWER": {"IN": ["two", "ii", "2"]}}, {"LOWER": "dm"}],
        attributes={"icd10_code": "E11.9"}
    ),
]
target_matcher.add(rules)

text = """
DIAGNOSIS: Type II Diabetes Mellitus
The patient presents today for management of Type 2 DM.
"""

doc = nlp(text)

# Even though different rules were used to match the ents,
# they have the same 'literal' value, and both are assigned "E11.9" 
# as an icd10 code
for ent in doc.ents:
    print(ent, ent._.target_rule.literal, ent._.icd10_code, sep="\t")
