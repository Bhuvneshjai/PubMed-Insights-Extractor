from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pubmed.fetcher import fetch_pubmed_ids, fetch_paper_details
from pubmed.utils import is_non_academic, extract_emails
from lxml import etree
from io import StringIO
import pandas as pd

app = FastAPI()
templates = Jinja2Templates(directory="webapp/templates")

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "results": None})

@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, query: str = Form(...), action: str = Form(...)):
    ids = fetch_pubmed_ids(query)
    xml_data = fetch_paper_details(ids)
    root = etree.parse(StringIO(xml_data))

    results = []

    for article in root.xpath("//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        pub_date = article.findtext(".//PubDate/Year") or "N/A"
        affiliations = article.xpath(".//AffiliationInfo/Affiliation")
        authors = article.xpath(".//AuthorList/Author")

        non_academic_authors = []
        companies = set()
        email = None

        for aff in affiliations:
            aff_text = aff.text or ""
            if is_non_academic(aff_text):
                companies.add(aff_text)
                emails = extract_emails(aff_text)
                if emails:
                    email = emails[0]

        for auth in authors:
            name_parts = [auth.findtext("ForeName"), auth.findtext("LastName")]
            name = " ".join(part for part in name_parts if part)
            affs = auth.xpath("./AffiliationInfo/Affiliation")
            if any(is_non_academic(a.text or "") for a in affs):
                non_academic_authors.append(name)

        if non_academic_authors:
            results.append({
                "PubmedID": pmid,
                "Title": title,
                "Date": pub_date,
                "Authors": ", ".join(non_academic_authors),
                "Affiliations": "; ".join(companies),
                "Email": email or "N/A"
            })

    if action == "download":
        # Save to results/ directory
        import os
        os.makedirs("results", exist_ok=True)
        filename = f"results/{query.replace(' ', '_')}.csv"
        pd.DataFrame(results).to_csv(filename, index=False)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "results": results,
            "query": query,
            "message": f"Downloaded to {filename}"
        })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "results": results,
        "query": query
    })