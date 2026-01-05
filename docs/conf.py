"""Sphinx configuration for SonarQube SDK documentation."""

import os
import sys

# Add source directory to path for autodoc
sys.path.insert(0, os.path.abspath("../src"))

# Project information
project = "SonarQube SDK"
copyright = "2025, Your Name"
author = "Your Name"
release = "0.1.0"
version = "0.1.0"

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# HTML output options
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_title = "SonarQube SDK Documentation"

# Autodoc configuration
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__, API_PATH",
    "show-inheritance": True,
}

autodoc_typehints = "both"
autodoc_typehints_format = "short"

# Don't document inherited members to avoid duplicates
autodoc_inherit_docstrings = False

# Napoleon configuration (Google/NumPy style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# Intersphinx configuration
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}

# Suppress duplicate object description warnings
# This happens because the same objects are sometimes documented in multiple places
# (e.g., models referenced by API methods and documented separately)
suppress_warnings = ["autodoc.duplicate_object"]

# sphinx-autodoc-typehints configuration
typehints_defaults = "comma"
always_document_param_types = True
