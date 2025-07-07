# 🧠 PubMed Insights Extractor

A full-stack Python application (CLI + Web) to search **PubMed**, filter research papers with **non-academic affiliations** (e.g., pharma, biotech, private companies), and download structured results as a CSV file.

This is helpful for:
- 📊 Competitive intelligence teams
- 🧪 Biotech analysts
- 🔬 Research leads tracking industry collaborations


## 📌 What This Tool Does

- ✅ Queries PubMed using the official **NCBI E-Utilities API**
- ✅ Filters papers with at least one non-academic author
- ✅ Extracts key fields like title, authors, affiliations, and email
- ✅ Saves results in a structured **CSV format**
- ✅ Includes both **command-line interface** (Typer) and **web interface** (FastAPI)


## 🚀 Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/your-username/pubmed-fetcher.git
cd pubmed-fetcher
```

### 2. Install dependencies using Poetry

```bash
poetry install
```


## 💻 Usage Options

### ▶️ CLI Usage

```bash
poetry run get-papers-list "cancer vaccine" --file results.csv --debug
```

This will:
- Fetch top PubMed results
- Filter papers with non-academic authors
- Save them to results.csv


## 🌐 Web App (Frontend)

```bash
poetry run uvicorn webapp.main:app --reload
```

Then open http://127.0.0.1:8000 <br>
You can:
- Enter a PubMed query
- Click Search to view results
- Click Download CSV to save results into /results/your_query.csv


## 📄 Output Fields
The exported CSV will contain:
* PubmedID
* Title
* Date (Publication Year)
* Non-academic Author(s)
* Company Affiliation(s)
* Corresponding Author Email


## 🧠 Key Features
* 🔍 Filter out purely academic papers <br>
* 📑 Extract affiliations and authors from XML
* 📂 Download data with one click
* 🖥️ Responsive UI using Bootstrap
* ⚡ Built with FastAPI + Typer + Poetry


## 📁 Folder Structure
pubmed-fetcher/ <br>
├── pubmed/                   <br>
│   ├── fetcher.py            <br>
│   ├── utils.py              <br>
│   └── main.py               <br>
├── webapp/                   <br>
│   ├── main.py               <br>
│   └── templates/ <br>
│       └── index.html        <br>
├── results/                  <br>
├── pyproject.toml            <br>
└── README.md 


## 🧰 Tools Used
* FastAPI — for building web backend
* Typer — for CLI command interface
* Pandas — for data manipulation
* Requests — for making HTTP calls
* LXML — for parsing PubMed XML data
* Jinja2 — for rendering HTML templates
* Poetry — for dependency & environment management
* PubMed E-Utilities — official PubMed API


### 🤝 Contributions
Feel free to fork the repo, submit PRs, or open issues if you want to collaborate!
