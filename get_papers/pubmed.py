from typing import List
from Bio import Entrez
import logging
from get_papers.types import Author, Paper
from concurrent.futures import ThreadPoolExecutor, as_completed
from ratelimit import limits, sleep_and_retry
import re

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

Entrez.email = "vinothraja.t3@gmail.com"
MAX_RESULTS = 300  # Total max papers to fetch
BATCH_SIZE = 50    # Number of IDs per batch
MAX_THREADS = 5     # Concurrent fetches

# Rate limit: Max 3 requests per second
@sleep_and_retry
@limits(calls=3, period=1)
def rate_limited_efetch(**kwargs):
    return Entrez.efetch(**kwargs)

def fetch_papers_with_metadata(query: str, max_results: int = MAX_RESULTS) -> List[Paper]:
    """
    Search PubMed and fetch metadata for papers matching the query (multi-threaded).
    """
    logging.debug(f"Searching PubMed for: {query}")
    search_handle = Entrez.esearch(
        db="pubmed", term=query, retmax=max_results, usehistory="y"
    )
    search_results = Entrez.read(search_handle)
    count = int(search_results["Count"])
    logging.debug(f"Total available: {count} | Fetching up to {min(count, max_results)}")

    webenv = search_results["WebEnv"]
    query_key = search_results["QueryKey"]

    all_papers: List[Paper] = []
    tasks = []

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for start in range(0, min(count, max_results), BATCH_SIZE):
            tasks.append(executor.submit(fetch_batch, query_key, webenv, start, BATCH_SIZE))

        for future in as_completed(tasks):
            try:
                papers = future.result()
                all_papers.extend(papers)
            except Exception as e:
                logging.warning(f"Batch fetch failed: {e}")

    return all_papers

def fetch_batch(query_key: str, webenv: str, start: int, batch_size: int) -> List[Paper]:
    logging.debug(f"Fetching batch: start={start}, size={batch_size}")
    handle = rate_limited_efetch(
        db="pubmed",
        query_key=query_key,
        WebEnv=webenv,
        retstart=start,
        retmax=batch_size,
        rettype="medline",
        retmode="xml",
    )
    records = Entrez.read(handle)

    papers: List[Paper] = []
    for article in records["PubmedArticle"]:
        try:
            medline = article["MedlineCitation"]
            article_data = medline["Article"]

            pubmed_id = medline.get("PMID", "?")
            title = article_data.get("ArticleTitle", "No title")
            pub_date = extract_pub_date(article_data)
            authors = extract_authors(article_data)

            paper = Paper(
                pubmed_id=str(pubmed_id),
                title=str(title),
                pub_date=pub_date,
                authors=authors,
                non_academic_authors=[],
                company_affiliations=[],
                corresponding_email=find_corresponding_email(authors),
            )
            papers.append(paper)

        except Exception as e:
            logging.warning(f"Failed to parse article: {e}")
            continue

    return papers

def extract_pub_date(article_data) -> str:
    try:
        date = article_data["Journal"]["JournalIssue"]["PubDate"]
        year = date.get("Year", "")
        month = date.get("Month", "")
        return f"{month} {year}".strip()
    except Exception:
        return "Unknown"

def extract_authors(article_data) -> List[Author]:
    authors_list = []
    author_entries = article_data.get("AuthorList", [])
    for person in author_entries:
        if "LastName" not in person:
            continue
        name = f"{person.get('ForeName', '')} {person.get('LastName', '')}".strip()
        email = None
        affiliation = None

        aff_info = person.get("AffiliationInfo", [])
        if aff_info:
            affiliation = aff_info[0].get("Affiliation", None)
            if affiliation:
                match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", affiliation)
                if match:
                    email = match.group(0)

        authors_list.append(Author(name=name, email=email, affiliation=affiliation))
    return authors_list


def find_corresponding_email(authors: List[Author]) -> str | None:
    for author in authors:
        if author.email:
            return author.email
    return None
