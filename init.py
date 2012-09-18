import os.path

from Builder import Builder

config = {
    'SITE_PREFIX': 'http://localhost',
    'BLOG_PATH': '.',
    'TEMPLATES_PATH': os.path.join(os.path.dirname(__file__), 'templates')
}

builder = Builder(config)
