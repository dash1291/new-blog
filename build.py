from datetime import date
from operator import itemgetter
import os
import os.path
import re
import sys

from jinja2 import Template, FileSystemLoader, Environment
import markdown
        
templates_path = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(templates_path))
posts = []
  		
def get_date(doc_path):
    date_reg = '(\d+)/(\d+)/(\d+)'
    res = re.search(date_reg, doc_path[7:])
    year = res.group(1)
    month = res.group(2)
    day = res.group(3)
    return date(int(year), int(month), int(day))

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
    context = {}
    doc_string = open(doc_path).read()
    options = build_options(doc_string)
    doc_string = strip_options(doc_string)
    doc_html = markdown.markdown(doc_string)
    page_title = options['title']
    context = {'site_prefix': SITE_PREFIX, 'title': page_title,
            'content': doc_html}
    template_name = options['layout'] + '.html'
    template = env.get_template(template_name)
    rendered = template.render(context)
    if '/' in doc_path[7:]:
        # DIRTY: This means its a blog post.
        post_date = get_date(doc_path)
        posts.append({'title': page_title, 'content': doc_html, 
                    'date': post_date, 'path': doc_path[7:-3] + '.html',
                    'date_str': post_date.strftime('%B %d, %Y')})
        context['date'] = post_date.strftime('%B %d, %Y')
    return rendered

def build_home():
    template = env.get_template('home.html')
    rendered = template.render(site_prefix=SITE_PREFIX, recent_posts=posts[:4])
    open('./site/index.html', 'w').write(rendered)

def build_posts_list():
    template = env.get_template('posts.html')
    rendered = template.render(site_prefix=SITE_PREFIX, posts=posts)
    open('./site/posts.html', 'w').write(rendered)

def build_rss():
    template = env.get_template('rss.xml')
    rendered = template.render(site_prefix=SITE_PREFIX, posts=posts)
    open('./site/atom.xml', 'w').write(rendered)

def init():
    for root, dirs, files in os.walk('./docs'):
        dirname = './site/' + root[7:]
        if os.path.exists(dirname) != True:
            os.mkdir(dirname)
        for name in files:
            if '.md' in name:        
                html = build_page(root + '/' + name)
                open(dirname + '/' + name[:-3] + '.html', 'w').write(html)
    posts.sort(key=itemgetter('date'), reverse=True)
    print posts
    build_home()
    build_posts_list()
    build_rss()

if __name__=='__main__':
    if len(sys.argv) > 1:
        SITE_PREFIX = sys.argv[1]
    else:
        SITE_PREFIX = ''
    init()
