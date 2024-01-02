from dataclasses import dataclass, field
import json
import logging
import os
import sys
from functools import partial

from bib2tex.config import BIBTEX_ENTRY_TYPES, FORMAT_SCHEMES_DIR


def read_json_file(file_path:str) -> dict[str,str]:
    """Read json file and return as dict of strings."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

@dataclass
class FormatSchemeManager:
    format_schemes: dict[str, dict[str, str]] = field(default_factory=dict)

    def __post_init__(self):
        self.load_format_schemes()

    def load_format_schemes(self) -> None:
        """Load format schemes from directory."""
        if not os.path.exists(FORMAT_SCHEMES_DIR):
            logging.error("Format schemes directory does not exit, aborting.")
            sys.exit()

        for filename in os.listdir(FORMAT_SCHEMES_DIR):
            file_path = os.path.join(FORMAT_SCHEMES_DIR, filename)
            name, _ = os.path.splitext(filename)
            if name not in self.format_schemes:
                self.format_schemes[name] = read_json_file(file_path)
                logging.info(f"Loaded {name!r} format schemes.")

    def get_format_scheme(self, entry_type: str, name: str = "default") -> str:
        """Retrieve a format scheme for a specific entry type.

        Args:
            entry_type (str): BibTeX entry type.
            name (str): Name of the format scheme. Fallback to 'default'.
        """
        default_scheme = self.format_schemes['default'][entry_type]
        try:
            format_scheme = self.format_schemes[name][entry_type]
            logging.debug(f"Retrieved {entry_type} format scheme {name!r}.")
        except:
            format_scheme = default_scheme
            logging.warning(f"{entry_type.title()} format scheme {name!r} not found, using default.")
        return format_scheme

    def get_format_schemes(self, name: str = "default") -> dict[str, str]:
        """Get a dictionary of format schemes for all entry types.

        Args:
            name (str): Name of the format scheme. Fallback to 'default'.
        """
        get_scheme = partial(self.get_format_scheme, name=name)
        return {entry_type: get_scheme(entry_type) for entry_type in BIBTEX_ENTRY_TYPES}

    def list_format_schemes(self) -> None:
        """List existing format schemes."""
        for name, entry_type in self.format_schemes.items():
            print(f"{name!r} format schemes:")
            for scheme_name, format_scheme in schemes.items():
                print(f"  {entry_type}: {format_scheme}")
