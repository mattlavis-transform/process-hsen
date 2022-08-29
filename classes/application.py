import csv
import nltk
import glob
import os
import ssl
import spacy
from dotenv import load_dotenv
from pathlib import Path
from classes.hsen_document import HsenDocument


class Application(object):
    def __init__(self):
        load_dotenv('.env')

        self.create_ssl_unverified_context()
        self.get_folders()

        self.template_file = os.path.join(self.resource_folder, "99 template", "template.docx")
        self.SEARCH_TERM_FILE = os.getenv('SEARCH_TERM_FILE')

        self.setup_nlp()

    def setup_nlp(self):
        self.nlp = spacy.load("en_core_web_lg")
        nltk.download('words')
        self.words = set(nltk.corpus.words.words())

    def create_ssl_unverified_context(self):
        ssl._create_default_https_context = ssl._create_unverified_context

    def get_folders(self):
        self.resource_folder = os.path.join(os.getcwd(), "resources")
        self.make_folder(self.resource_folder)

        self.hsen_source_folder = os.path.join(self.resource_folder, "01 hsen source")
        self.make_folder(self.hsen_source_folder)

        self.processed_hsen_folder = os.path.join(self.resource_folder, "02 processed hsen")
        self.make_folder(self.processed_hsen_folder)

        self.word_folder = os.path.join(self.resource_folder, "03 words")
        self.make_folder(self.word_folder)

        self.weighted_word_folder = os.path.join(self.resource_folder, "04 weighted words")
        self.make_folder(self.weighted_word_folder)

    def make_folder(self, folder):
        if not os.path.exists(folder):
            os.mkdir(folder)

    def process_documents(self):
        self.hsen_documents = []
        os.chdir(self.hsen_source_folder)
        for file in glob.glob("*.docx"):
            self.hsen_documents.append(file)

        self.hsen_documents = sorted(self.hsen_documents)
        for filename in self.hsen_documents:
            hsen_document = HsenDocument(filename)
            # hsen_document.open()
            hsen_document.process()
            hsen_document.save()

    def extract_documents(self):
        self.document_terms = []
        files = Path(self.hsen_source_folder).glob('*.docx')
        self.hsen_documents = []
        for file in files:
            self.hsen_documents.append(file)

        self.hsen_documents = sorted(self.hsen_documents)
        index = 0
        for filename in self.hsen_documents:
            index += 1
            hsen_document = HsenDocument(filename)
            returned_terms, returned_term_dict = hsen_document.extract(self.nlp)
            self.document_terms += returned_terms
            if index > 2:
                break

        self.document_terms = list(set(self.document_terms))
        self.document_terms = sorted(self.document_terms)
        with open('your_file.txt', 'w') as f:
            for item in self.document_terms:
                f.write("%s\n" % item)

    def process_search_terms(self):
        file = open(self.SEARCH_TERM_FILE)
        csvreader = csv.reader(file, delimiter=',')
        self.search_terms_nouns = []
        self.search_terms_adjectives = []
        index = 0
        document = ""
        for row in csvreader:
            if index > 0:
                if (int(row[1])) > 2:
                    term = row[0]
                    document += term + "\n"

            index += 1

        document = "She wore a cashmere sweater. He wore a woollen sweater. He wore a cotton sweater"
        ruler = self.nlp.add_pipe("entity_ruler", before="tok2vec")
        patterns = [
            {"label": "ADJ", "pattern": "cashmere"}
        ]
        ruler.add_patterns(patterns)

        doc = self.nlp(document)
        for chunk in doc.noun_chunks:
            self.search_terms_nouns.append(chunk.root.text)

        # Do overrides for materials
        materials = ["cashmere", "cotton"]
        for token in doc:
            value = token.lemma_.lower().replace(".", "")
            if value in materials:
                token.pos_ = "ADJ"

        for token in doc:
            if token.pos_ in ("NOUN", "PROPN"):
                value = token.lemma_.lower().replace(".", "")
                if len(value) > 2:
                    if not value.isnumeric():
                        if value in self.words:
                            self.search_terms_nouns.append(value)

            elif token.pos_ in ("ADJ"):
                value = token.lemma_.lower().replace(".", "")
                if len(value) > 2:
                    if not value.isnumeric():
                        if value in self.words:
                            self.search_terms_adjectives.append(value)

        # Extract all the nouns
        self.search_terms_nouns = list(set(self.search_terms_nouns))
        with open('search_terms_nouns.txt', 'w') as f:
            for item in self.search_terms_nouns:
                f.write("%s\n" % item)

        # Extract all the adjectives
        self.search_terms_adjectives = list(set(self.search_terms_adjectives))
        with open('search_terms_adjectives.txt', 'w') as f:
            for item in self.search_terms_adjectives:
                f.write("%s\n" % item)

    def merge_corpus(self):
        return
        self.merged = []
        self.merged += self.search_terms
        self.merged += self.document_terms
        self.merged = list(set(self.merged))
        self.merged = sorted(self.merged)
        with open('merged.txt', 'w') as f:
            for item in self.merged:
                f.write("%s\n" % item)
