import os.path

from Builder import Builder
from syntax_processor import SyntaxProcessor

config = {
    'SITE_PREFIX': 'http://localhost:8000',
    'BLOG_PATH': '.',
    'TEMPLATES_PATH': os.path.join(os.path.dirname(__file__), 'templates')
}

builder = Builder(config)
SyntaxProcessor(builder)