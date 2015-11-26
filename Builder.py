#!/usr/bin/env python
from datetime import date
from operator import itemgetter
import os
import os.path
import re
import sys

from bs4 import BeautifulSoup
from jinja2 import Template, FileSystemLoader, Environment
import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


class Builder():
    def __init__(self, config):
        self.config = config
        self.template_env = Environment(loader=FileSystemLoader(
                            self.config['TEMPLATES_PATH']))
        self.posts = []

        self.compile_pages()
        self.build_home()
        self.build_archive()
        self.build_rss()

    def compile_pages(self):
        docs_dir = os.path.join(self.config['BLOG_PATH'], 'docs')
        for root, dirs, files in os.walk(docs_dir):
            dirname = os.path.join(self.config['BLOG_PATH'], 'site',
                    root[len(docs_dir) + 1:])
            if os.path.exists(dirname) != True:
                os.mkdir(dirname)
            for name in files:
                if '.md' in name:
                    html = self.build_page(os.path.join(root, name))
                    open(os.path.join(dirname, name[:-3] + '.html'), 'w').write(html)
        self.posts.sort(key=itemgetter('date'), reverse=True)

    def get_date(self, doc_path):
        date_reg = '(\d+)/(\d+)/(\d+)'
        res = re.search(date_reg, doc_path[7:])
        year = res.group(1)
        month = res.group(2)
        day = res.group(3)
        return date(int(year), int(month), int(day))

    def build_options(self, doc_string):
        # build a dictionary object of doc options for easy access
        opt_start = re.search('-+\n', doc_string).end()
        opt_end = re.search('\n-+', doc_string).start()
        opt_string = doc_string[opt_start: opt_end].replace('\n', ',')
        options = eval('{' + opt_string + '}')
        return options

    def strip_options(self, doc_string):
        # coz I don't want those options to render as HTML
        opt_end = re.search('\n-+', doc_string).end()
        return doc_string[opt_end:]

    def build_page(self, doc_path):
        context = {}
        doc_string = open(doc_path).read()
        options = self.build_options(doc_string)
        doc_string = self.strip_options(doc_string)
        doc_html = markdown.markdown(doc_string)
        page_title = options['title']
        context = {'site_prefix': self.config['SITE_PREFIX'],
                   'title': page_title, 'content': doc_html}
        template_name = options['layout'] + '.html'
        template = self.template_env.get_template(template_name)

        if options['layout'].startswith('post'):
            # DIRTY: This means its a blog post.
            post_date = self.get_date(doc_path)
            self.posts.append({'title': page_title, 'content': doc_html,
                        'date': post_date, 'path': doc_path[7:-3] + '.html',
                        'date_str': post_date.strftime('%B %d, %Y')})
            context['date'] = post_date.strftime('%B %d, %Y')

        rendered = template.render(context)
        rendered = self.syntax_highlight(rendered)
        return rendered

    def build_home(self):
        template = self.template_env.get_template('home.html')
        rendered = template.render(site_prefix=self.config['SITE_PREFIX'],
                                   recent_posts=self.posts[:4])
        open('./site/index.html', 'w').write(rendered)

    def build_archive(self):
        template = self.template_env.get_template('posts.html')
        rendered = template.render(site_prefix=self.config['SITE_PREFIX'],
                                   posts=self.posts)
        open('./site/posts.html', 'w').write(rendered)

    def build_rss(self):
        template = self.template_env.get_template('rss.xml')
        rendered = template.render(site_prefix=self.config['SITE_PREFIX'],
                                   posts=self.posts)
        open('./site/atom.xml', 'w').write(rendered)

    def syntax_highlight(self, html):
        soup = BeautifulSoup(html, "html.parser")
        lang_set = []
        codes = soup.find_all('pre')
        if codes:
            for code in codes:
                if 'class' in code.attrs.keys():
                    lang = code['class'][0]
                    lexer = get_lexer_by_name(lang, stripall=True)
                    formatter = HtmlFormatter(lineos=True, cssclass=lang, style='friendly')
                    result = highlight(code.text, lexer, formatter)
                    if lang not in lang_set:
                        style = '<style>' + formatter.get_style_defs('.' + lang) + (
                                '</style>')
                        lang_set.append(lang)
                    else:
                        style = ''

                    html = html.replace(unicode(code), style + result)
        return html
