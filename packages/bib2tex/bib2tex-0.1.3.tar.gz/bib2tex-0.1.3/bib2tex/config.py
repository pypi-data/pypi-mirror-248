import os

# Path to .bib file used as default in the CLI
# Default is the environment variable "BIB"
DEFAULT_BIB_PATH = os.environ.get("BIB")

# Encoding used to read from BibTeX and to latex files
ENCODING = "utf-8"

# Key names for columns in addition to found BibTeX tags
COL_ENTRYTYPE = "entrytype"
COL_CITATIONKEY = "citationkey"
COL_NAME_FULL = "name"
COL_NAME_FIRST = "name_first"
COL_NAME_LAST = "name_last"

# LaTeX format schemes, use valid BibTeX tags (capitalised) and AUTHORS
# wrapped in <> to define a scheme for the corresponding LaTeX item. Assign
# new format scheme to entrytype in FORMAT_SCHEMES dictionary underneath, and
# define a default scheme.
# The authors are always listed with initials, this is currently not configurable.
SCHEME_ARTICLE_SHORT = "<AUTHOR>: ``<TITLE>'', \\textit{<JOURNAL>}, <YEAR>, \\href{https://doi.org/<DOI>},}{DOI: <DOI>}."

# Formatter scheme mapping for LaTeX conversion (entrytype : formatter)
DEFAULT_FORMAT_SCHEME = SCHEME_ARTICLE_SHORT
FORMAT_SCHEMES = {
    "article": SCHEME_ARTICLE_SHORT,
}

# Indent for items within the itemize environment
LATEX_INDENT = 2

# List of BibTeX Entry Types
BIBTEX_ENTRY_TYPES = [
    "article",
    "book",
    "booklet",
    "inbook",
    "incollection",
    "inproceedings",
    "manual",
    "mastersthesis",
    "misc",
    "phdthesis",
    "proceedings",
    "techreport",
    "unpublished",
]
