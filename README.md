# 📄 PubMed Paper Fetcher

Command-line tool to search PubMed and extract papers with at least one non-academic author (e.g., biotech/pharma).

## 📦 Setup

```bash
poetry install
```

## 🚀 Usage

```bash
get-papers-list "covid vaccine" --file results.csv --debug
```

## 🔍 Output Columns

- PubmedID
- Title
- Publication Date
- Non-academic Author(s)
- Company Affiliation(s)
- Corresponding Author Email

## 🛠️ Tools Used

- [Typer](https://typer.tiangolo.com/)
- [Requests](https://requests.readthedocs.io/)
- [Pandas](https://pandas.pydata.org/)