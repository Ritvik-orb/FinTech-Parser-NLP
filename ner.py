import spacy
import re

try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    # fall back to blank english model if small model isn't installed
    nlp = spacy.blank("en")


def fintech_ner(text):
    doc = nlp(text)
    data = {"Name": [], "Bank": [], "Date": [], "Amount": [], "Account": []}

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            data["Name"].append(ent.text)
        elif ent.label_ == "ORG":
            data["Bank"].append(ent.text)
        elif ent.label_ == "DATE":
            data["Date"].append(ent.text)
        elif ent.label_ == "MONEY":
            data["Amount"].append(ent.text)

    acc = re.findall(r"\b\d{9,16}\b", text)
    if acc:
        data["Account"] = acc

    # remove empty lists and return None for missing fields
    return {k: (v if v else None) for k, v in data.items()}


def classify_doc(text):
    t = text.lower()
    if "account" in t or "statement" in t:
        return "Bank Statement"
    if "invoice" in t or "bill" in t:
        return "Invoice"
    return "Unknown"
