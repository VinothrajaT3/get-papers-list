# 📄 get-papers-list

A command-line tool to search PubMed for research papers matching a query and identify papers with at least one author affiliated with a pharmaceutical or biotech company. Outputs results as a CSV or formatted terminal table.

---

## 🗂️ Project Structure

```
get_papers_list/
├── get_papers/
│   ├── __init__.py
│   ├── cli.py               # CLI entrypoint using argparse
│   ├── pubmed.py            # PubMed fetcher (multithreaded + rate limited)
│   ├── filters.py           # Heuristics for identifying non-academic authors
│   ├── formatter.py         # Rich table or CSV output
│   └── types.py             # Typed dataclasses for Paper, Author
│
├── pyproject.toml           # Poetry config
├── README.md                # You are here
└── LICENSE
```

---

## 🚀 Installation & Usage

### 1. Clone the repo

```bash
git clone https://github.com/VinothRajaT3/get-papers-list.git
cd get-papers-list
```

### 2. Install dependencies using Poetry

```bash
poetry install
```

### 3. Run the CLI

```bash
poetry run get-papers-list "your query here" [--file results.csv] [--debug]
```

### 4. Examples

```bash
# Print results in terminal
poetry run get-papers-list "breast cancer AND 2023[dp]"

# Save to CSV
poetry run get-papers-list "CRISPR AND 2022[dp]" --file crispr.csv

# Show debug info
poetry run get-papers-list "mRNA vaccine" --debug
```

---

## 🛠️ Tools & Libraries Used

| Tool                                             | Purpose                             |
| ------------------------------------------------ | ----------------------------------- |
| [Poetry](https://python-poetry.org/)             | Dependency management and packaging |
| [BioPython](https://biopython.org/)              | Access to NCBI PubMed Entrez API    |
| [Rich](https://github.com/Textualize/rich)       | Pretty terminal tables and logging  |
| [ratelimit](https://pypi.org/project/ratelimit/) | Respect NCBI's API request rate     |
| Python `dataclasses`                             | Typed models for structured results |

---

## 🤖 LLM Usage

This project was designed with the assistance of OpenAI's ChatGPT (GPT-4o) to:

- Architect the solution based on requirements
- Refactor into clean, typed modules
- Suggest multi-threading and rate-limiting techniques
- Enhance output formatting using Rich

---

## 📄 License

MIT License (c) 2025 Your Name
