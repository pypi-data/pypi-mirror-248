import logging
import os
import sys
from typing import Optional

import click

from bib2tex.bibtex_parser import parse_bibtex_file
from bib2tex.bibtex_filter import filter_entries
from bib2tex.converter import to_latex, string_to_file
from bib2tex.config import BIBTEX_ENTRY_TYPES, DEFAULT_BIB_PATH, DEFAULT_FORMAT_SCHEME, FORMAT_SCHEMES


class CustomFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno in (logging.WARNING, logging.ERROR, logging.CRITICAL):
            # Include level name for WARNING, ERROR, and CRITICAL levels
            self._style._fmt = "%(levelname)s: %(message)s"
        else:
            # Exclude level name for other levels
            self._style._fmt = "%(message)s"
        return super().format(record)


def setup_logger(verbose: bool):
    """Set up logging configuration."""
    log_level = logging.INFO if verbose else logging.ERROR
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s",
    )

    # Create a handler with the custom formatter
    console_handler = logging.StreamHandler()
    formatter = CustomFormatter()
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logging.getLogger().handlers = []  # Clear existing handlers to avoid duplicates
    logging.getLogger().addHandler(console_handler)


def main(
    bibtex_path: str,
    latex_path: str,
    author: str,
    entrytype: Optional[str],
    format_scheme: Optional[str],
    item: str = "",
    itemize: str = "",
    highlight: bool = True,
    reverse: bool = False,
    verbose: bool = True,
) -> None:
    """Convert entries of specified author (and entrytype) into LaTeX item environment."""
    setup_logger(verbose=verbose)

    # load data from BibTeX file
    bibtex_filename = os.path.basename(bibtex_path)
    entries = parse_bibtex_file(bibtex_path)
    logging.info(f"Loaded {len(entries)} entries from BibTeX file {bibtex_filename!r}.")

    # filter entries for author (and type)
    if entrytype not in BIBTEX_ENTRY_TYPES + [None]:
        logging.warning(f"{entrytype!r} is not a valid BibTeX type.")
    filtered_entries = filter_entries(entries, author, entrytype, reverse=reverse)

    if len(filtered_entries) == 0:
        logging.info(
            f"Found no BibTeX{' ' + entrytype if entrytype is not None else ''} entries for {author!r}, aborting!"
        )
        sys.exit()
    logging.info(
        f"Converting {len(filtered_entries)} BibTeX{' ' + entrytype if entrytype is not None else ''} entries for {author!r} into LaTeX string..."
    )
    if format_scheme is None:
        format_scheme = DEFAULT_FORMAT_SCHEME
        if entrytype is not None:
            try:
                format_scheme = FORMAT_SCHEMES[entrytype]
            except:
                logging.info(
                    f"No LaTeX format scheme exists for {entrytype!r} entries, using default scheme."
                )
    underline = author if highlight else None
    latex_string = to_latex(
        filtered_entries,
        underline=underline,
        item_options=item,
        itemize_options=itemize,
        format_scheme=format_scheme,
    )
    string_to_file(latex_path, latex_string)
    logging.info(f"LaTeX string written to {latex_path!r}.")


@click.command(
    context_settings=dict(help_option_names=["-h", "--help"]),
    epilog="by Cs137, 2023 - development on Codeberg: https://codeberg.org/Cs137/bib2tex",
)
@click.option(
    "-i",
    "--bibtex-path",
    default=DEFAULT_BIB_PATH,
    show_default=True,
    required=True,
    type=click.Path(exists=True),
    help="(input) Path to the BibTeX file.",
    # prompt="Enter the path to the BibTeX file (input)",
)
@click.option(
    "-o",
    "--latex-path",
    required=True,
    type=click.Path(),
    help="(output) Path to the LaTeX file",
    prompt="Enter the path to the LaTeX file (output)",
)
@click.option(
    "-a",
    "--author",
    required=True,
    help="Author name for filtering entries.",
    prompt="Enter the author name for filtering BibTeX entries",
)
@click.option("-e", "--entrytype", help="BibTeX entry type for filtering.")
@click.option("-f", "--format-scheme", help="Format scheme for LaTeX item.")
@click.option("-r", "--reverse", is_flag=True, help="Sort entries from old to new.")
@click.option("-u", "--underline", "highlight", is_flag=True, help="Underline the author in LaTeX.")
@click.option("-v", "--verbose", is_flag=True, help="Print verbose output.")
@click.option("--item", default="", help="Options for LaTeX item, e.g. '[--]'.")
@click.option(
    "--itemize", default="[leftmargin=*,itemsep=3pt]", help="Options for LaTeX itemze."
)
def cli(**kwargs) -> None:
    """CLI to filter and convert BibTeX entries to a LaTeX list.

    This command allows to filter BibTeX entries by an author's name (and entrytype).
    The resulting subset is coverted into a LaTeX list. The defined author can be
    highlighted with an underline in the result. By default, the list is sorted
    from the newest to the oldest entry.
    """
    main(**kwargs)


if __name__ == "__main__":
    cli()
