import csv
import json
import os
import requests


# filename = "/Users/mattlavis/sites and projects/1. Online Tariff/process-hsen/searchterms/Trade Tariffs_Site Search_Table.csv"
filename = "/Users/mattlavis/sites and projects/1. Online Tariff/process-hsen/searchterms/zero.csv"

uri_template_means_like = "https://api.datamuse.com/words?ml="  # means like
uri_template_sounds_like = "https://api.datamuse.com/words?sl="  # sounds like
uri_template_spelled_like = "https://api.datamuse.com/words?sp="  # spelled like
uri_template_triggered_by = "https://api.datamuse.com/words?rel_trg="  # triggered by
uri_template_suggestions = "https://api.datamuse.com/sug?s="  # suggestions


with open(filename) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    index = 1
    for row in spamreader:
        term = row[0].strip()
        if not term.isnumeric():
            if len(term) > 3:
                index += 1
                if index > 2:
                    item = {
                        "term": term,
                        "means_like": [],
                        "sounds_like": [],
                        "spelled_like": [],
                        "triggered_by": [],
                        "suggestions": [],
                    }
                    print(term)

                    response = requests.get(uri_template_means_like + term)
                    item["means_like"] = response.json()

                    response = requests.get(uri_template_sounds_like + term)
                    item["sounds_like"] = response.json()

                    response = requests.get(uri_template_spelled_like + term)
                    item["spelled_like"] = response.json()

                    response = requests.get(uri_template_triggered_by + term)
                    item["triggered_by"] = response.json()

                    response = requests.get(uri_template_suggestions + term)
                    item["uri_template_suggestions"] = response.json()

                    filename = os.path.join(os.getcwd(), "synonyms", term + ".json")
                    out_file = open(filename, "w")
                    json.dump(item, out_file, indent=4)
                    out_file.close()
                    a = 1

            if index > 1000:
                break
