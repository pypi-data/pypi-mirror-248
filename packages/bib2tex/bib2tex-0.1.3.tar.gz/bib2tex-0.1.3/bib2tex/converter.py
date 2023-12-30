from typing import Any, Optional

from bib2tex.config import ENCODING, LATEX_INDENT


def string_to_file(file_path: str, string: str, encoding: str = ENCODING) -> None:
    """Write a string to a file."""
    with open(file_path, "w", encoding=encoding) as file:
        file.write(string)


def to_latex(
    entries: list[dict[str, Any]],
    format_scheme: str,
    underline: Optional[str],
    indent: int = LATEX_INDENT,
    item_options: str = "",
    itemize_options: str = "",
) -> str:
    """Convert BibTeX entries to LaTeX itemization."""
    strings = []
    for entry in entries:
        authors = [f"{d['name_first'][:1]}.~{d['name_last']}" for d in entry["author"]]
        if underline is not None:
            authors = [
                r"\underline{" + a + "}" if underline in a else a for a in authors
            ]
        entry["author"] = ", ".join(authors)
        string = indent * " " + "\\item" + f"{item_options} " + format_scheme
        for tag in entry:
            string = string.replace(f"<{tag.upper()}>", entry[tag])
        strings.append(string)
    return (
        "\\begin{itemize}"
        + itemize_options
        + "\n"
        + "\n".join(strings)
        + "\n\\end{itemize}"
    )
