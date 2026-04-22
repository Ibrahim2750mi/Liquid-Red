# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from pathlib import Path
import sys

# --- PATH SETUP ---
# Resolve project root → Liquid-Red/
ROOT = Path(__file__).resolve().parent.parent

# Add src/ to path
sys.path.insert(0, str(ROOT / "src"))

project = 'LiquidRed'
copyright = '2026, Mohammad Ibrahim and Gaganpreet Singh'
author = 'Mohammad Ibrahim and Gaganpreet Singh'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",     # REQUIRED
    "sphinx.ext.napoleon",    # for NumPy/Google docstrings
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'english'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
