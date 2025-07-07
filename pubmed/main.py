import typer
import pandas as pd
from pubmed.fetcher import fetch_pubmed_ids, fetch_paper_details
from pubmed.utils import is_non_academic, extract_emails
from lxml import etree
from io import StringIO
from typing import Optional

app = typer.Typer()

@app.command()
def run(
    query: str,
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Output CSV filename"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode")
):
    ids = fetch_pubmed_ids(query)
    if debug:
        typer.echo(f"Fetched {len(ids)} PubMed IDs")

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
                "Publication Date": pub_date,
                "Non-academic Author(s)": "; ".join(non_academic_authors),
                "Company Affiliation(s)": "; ".join(companies),
                "Corresponding Author Email": email or "N/A"
            })

    df = pd.DataFrame(results)
    if file:
        df.to_csv(file, index=False)
        typer.echo(f"Saved results to {file}")
    else:
        typer.echo(df.to_string(index=False))

if __name__ == "__main__":
    app()