import requests
from typing import List

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def fetch_pubmed_ids(query: str, retmax=100) -> List[str]:
    url = f"{BASE_URL}/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax
    }
    res = requests.get(url, params=params)
    res.raise_for_status()
    return res.json()["esearchresult"]["idlist"]

def fetch_paper_details(pubmed_ids: List[str]) -> str:
    url = f"{BASE_URL}/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }
    res = requests.get(url, params=params)
    res.raise_for_status()
    return res.text