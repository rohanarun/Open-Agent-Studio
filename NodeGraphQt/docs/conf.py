# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
from datetime import datetime

base_path = os.path.abspath('.')
root_path = os.path.split(base_path)[0]
sys.path.insert(0, root_path)

import NodeGraphQt

# -- Project information -----------------------------------------------------

project = 'NodeGraphQt'
author = NodeGraphQt.pkg_info.__author__
copyright = '{}, {}'.format(datetime.now().year, author)

# The full version, including alpha/beta/rc tags
release = '{}'.format(NodeGraphQt.VERSION)
# The short X.Y version
version = '{0}.{1}'.format(*NodeGraphQt.VERSION.split('.'))


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
]

intersphinx_mapping = {
    # 'python': ('https://docs.python.org/3', None),
    'PySide2': ('https://doc.qt.io/qtforpython/', None),
}

# order of members.
autodoc_member_order = 'groupwise'

# autosummary generate stubs.
autosummary_generate = True

# autosummary overwrite generated stubs files.
autosummary_generate_option = True

rst_prolog = '''
.. |version_str| replace:: v{0}
'''.format(release)

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'monokai'


# -- Options for HTML output -------------------------------------------------

# If given, this must be the name of an image file (path relative to the
# configuration directory) that is the favicon of the docs.
# Modern browsers use this as the icon for tabs, windows and bookmarks.
# It should be a Windows-style icon file (.ico), which is 16x16 or 32x32
# pixels large. Default: None.
html_favicon = '_images/favicon.png'
html_logo = '_images/logo.png'

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_theme_path = ['_themes']
html_show_sourcelink = False
html_show_sphinx = False
html_context = {
    'display_github': True,
    'github_user': 'jchanvfx',
    'github_repo': 'NodeGraphQt',
    'github_version': "master",
    'conf_py_path': '/docs/',
    'source_suffix': '.rst',
}

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    # 'analytics_id': 'UA-XXXXXXX-1',  # Provided by Google in your dashboard
    # 'analytics_anonymize_ip': False,
    # 'logo_only': False,
    # 'display_version': True,
    # 'prev_next_buttons_location': 'both',
    # 'style_external_links': False,
    # 'vcs_pageview_mode': '',
    # 'style_nav_header_background': 'white',

    ### Toc options ###
    # 'collapse_navigation': True,
    # 'sticky_navigation': True,
    # 'navigation_depth': 4,
    # 'includehidden': True,
    # 'titles_only': False
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static', '_images']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.

html_sidebars = {
    '**': ['globaltoc.html',
           'relations.html',
           'sourcelink.html',
           'searchbox.html']
}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'NodeGraphQTdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'NodeGraphQT.tex', 'NodeGraphQt Documentation',
     author, 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'nodegraphqt', 'NodeGraphQt Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc,
     'NodeGraphQt', 'NodeGraphQT Documentation',
     author,
     'NodeGraphQt',
     'Node graph framework that can be re-implemented into apps that supports PySide2.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# -- Options for autodoc ----------------------------------------------------
autodoc_member_order = 'groupwise'

# -- Options for image link -------------------------------------------------
html_scaled_image_link = False
