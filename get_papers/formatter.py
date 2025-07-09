from typing import List, Optional
from get_papers.types import Paper
import csv
import logging
from rich.console import Console
from rich.table import Table

def output_results(papers: List[Paper], filename: Optional[str]) -> None:
    if filename:
        logging.debug(f"Writing output to CSV file: {filename}")
        write_csv(papers, filename)
        print(f"\n✅ Results written to: {filename}")
    else:
        print_table(papers)

def write_csv(papers: List[Paper], filename: str) -> None:
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "PubmedID",
            "Title",
            "Publication Date",
            "Non-academic Author(s)",
            "Company Affiliation(s)",
            "Corresponding Author Email",
        ])

        for paper in papers:
            writer.writerow([
                paper.pubmed_id,
                paper.title,
                paper.pub_date,
                "; ".join(paper.non_academic_authors),
                "; ".join(paper.company_affiliations),
                paper.corresponding_email or "",
            ])

console = Console()

def print_table(papers: List[Paper]) -> None:
    table = Table(title="Non-Academic Research Papers", show_lines=True)

    table.add_column("PubmedID", style="cyan", no_wrap=True)
    table.add_column("Title", style="bold")
    table.add_column("Date", style="green")
    table.add_column("Non-Academic Authors", style="yellow")
    table.add_column("Company", style="magenta")
    table.add_column("Email", style="blue")

    for paper in papers:
        table.add_row(
            paper.pubmed_id,
            paper.title[:60] + ("..." if len(paper.title) > 60 else ""),
            paper.pub_date,
            ", ".join(paper.non_academic_authors),
            ", ".join(paper.company_affiliations),
            paper.corresponding_email or "-"
        )

    console.print(table)