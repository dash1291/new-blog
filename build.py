import re

from jinja2 import Template
import markdown

# Walk through the directories
# Convert .md's to .html's
# Build homepage links
# Build archive page

def build_options(doc_string):
    # build a json object of doc options for easy access
    opt_start = re.search('-+\n', doc_string).end()
    opt_end = re.search('\n-+', doc_string).start()
    opt_string = doc_string[opt_start: opt_end].replace('\n', ',')
    options = eval('{' + opt_string + '}')
    return options

def strip_options(doc_string):
    # coz I don't need those options to render as HTML
    opt_end = re.search('\n-+', doc_string).start()
    return doc_string[opt_end:]

def build_page(doc_path):
    doc_string = doc_path.read()
    options = build_options(doc_string)
    doc_string = strip_options(doc_string)
    html = markdown.markdown(doc_string)

    # build further with jinja2
