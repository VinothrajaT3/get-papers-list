from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Author:
    name: str
    email: Optional[str] = None
    affiliation: Optional[str] = None

@dataclass
class Paper:
    pubmed_id: str
    title: str
    pub_date: str
    authors: List[Author] = field(default_factory=list)
    non_academic_authors: List[str] = field(default_factory=list)
    company_affiliations: List[str] = field(default_factory=list)
    corresponding_email: Optional[str] = None
