from typing import List, Tuple
from get_papers.types import Author

ACADEMIC_KEYWORDS = [
    "university", "college", "institute", "hospital", "center", "school", "faculty", "department"
]

COMPANY_KEYWORDS = [
    "pharma", "biotech", "inc", "ltd", "llc", "laboratories", "labs", "gmbh", "corp", "plc"
]

EMAIL_COMMERCIAL_DOMAINS = [".com", ".co", ".io"]

def extract_non_academic_authors(authors: List[Author]) -> Tuple[List[str], List[str]]:
    """
    Given a list of authors, return:
    - names of non-academic authors
    - list of associated company/organization names
    """
    non_academic_authors = []
    company_affiliations = set()

    for author in authors:
        affil = (author.affiliation or "").lower()
        email = (author.email or "").lower()

        if not affil:
            continue

        is_academic = any(keyword in affil for keyword in ACADEMIC_KEYWORDS)
        is_commercial_affil = any(word in affil for word in COMPANY_KEYWORDS)
        is_commercial_email = any(email.endswith(suffix) for suffix in EMAIL_COMMERCIAL_DOMAINS)

        if not is_academic and (is_commercial_affil or is_commercial_email):
            non_academic_authors.append(author.name)
            company_affiliations.add(author.affiliation.strip())

    return non_academic_authors, list(company_affiliations)
