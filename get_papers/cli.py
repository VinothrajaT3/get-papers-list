import click
import logging
from get_papers.pubmed import fetch_papers_with_metadata
from get_papers.filters import extract_non_academic_authors
from get_papers.formatter import output_results
from get_papers.types import Paper
from rich.logging import RichHandler

@click.command()
@click.argument("query", nargs=-1, required=True)
@click.option("--file", "-f", type=click.Path(), help="Filename to save results as CSV")
@click.option("--debug", "-d", is_flag=True, help="Enable debug logging")
def main(query: tuple[str], file: str | None, debug: bool):
    """
    Fetch PubMed papers for a QUERY and filter those with non-academic authors.

    Example:
        get-papers-list "cancer AND 2023[dp]" -f results.csv --debug
    """
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

    query_string = " ".join(query)
    logging.debug(f"Query: {query_string}")

    try:
        papers: list[Paper] = fetch_papers_with_metadata(query_string)
        logging.info(f"Fetched {len(papers)} papers.")

        filtered_papers = []
        for paper in papers:
            non_academic_authors, companies = extract_non_academic_authors(paper.authors)
            if non_academic_authors:
                paper.non_academic_authors = non_academic_authors
                paper.company_affiliations = companies
                filtered_papers.append(paper)

        logging.info(f"{len(filtered_papers)} papers have at least one non-academic author.")
        output_results(filtered_papers, file)

    except Exception as e:
        logging.exception("An error occurred while processing:")
        raise click.Abort()

if __name__ == "__main__":
    main()
