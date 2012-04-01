import os
import os.path
import re
import sys

from jinja2 import Template, FileSystemLoader, Environment
import markdown

templates_path = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(templates_path))

def build_options(doc_string):
    # build a dictionary object of doc options for easy access
    opt_start = re.search('-+\n', doc_string).end()
    opt_end = re.search('\n-+', doc_string).start()
    opt_string = doc_string[opt_start: opt_end].replace('\n', ',')
    options = eval('{' + opt_string + '}')
    return options

def strip_options(doc_string):
    # coz I don't want those options to render as HTML
    opt_end = re.search('\n-+', doc_string).end()
    return doc_string[opt_end:]

def build_page(doc_path):
    doc_string = open(doc_path).read()
    options = build_options(doc_string)
    doc_string = strip_options(doc_string)
    doc_html = markdown.markdown(doc_string)
    page_title = options['title']
    template_name = options['layout'] + '.html'
    template = env.get_template(template_name)
    rendered = template.render(site_prefix=SITE_PREFIX, title=page_title, content=doc_html)
    return rendered

def init():
    for root, dirs, files in os.walk('./docs'):
        dirname = './site/' + root[7:]
        if os.path.exists(dirname) != True:
            os.mkdir(dirname)
        for name in files:
            if '.md' in name:
                html = build_page(root + '/' + name)
                open(dirname + '/' + name[:-3] + '.html', 'w').write(html)

if __name__=='__main__':
    if len(sys.argv) > 1:
        SITE_PREFIX = sys.argv[1]
    else:
        SITE_PREFIX = ''
    init()
