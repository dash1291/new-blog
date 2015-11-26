import os.path

from Builder import Builder


config = {
    'SITE_PREFIX': 'https://ashishdubey.xyz/',
    'BLOG_PATH': '.',
    'TEMPLATES_PATH': os.path.join(os.path.dirname(__file__), 'templates')
}

builder = Builder(config)
