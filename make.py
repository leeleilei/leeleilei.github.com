# -*- coding: utf-8 -*-
'''
file name: make.py
description: generate my simple site pages
usage: # python make.py
'''

import os
import sys
import jinja2 as jj
import markdown as md
import tidylib

CURRENT_PATH = os.path.dirname(__file__)
PAGES_PATH = os.path.join(CURRENT_PATH, 'pages')
INDEX_MD = 'index.md'
INDEX_HTML = 'index.html'

def make_pages():
    '''update the ./pages markdown files'''

    #get the list of markdown files in ./pages
    md_pages = [page for page in os.listdir(PAGES_PATH) 
                if page.endswith('md')]

    #generate the html
    for md_page in md_pages:
        md_page = os.path.join(PAGES_PATH, md_page)
        html_page = os.path.splitext(md_page)[0] + '.html'

        #remove all old files
        try:
            os.remove(html_page)
        except OSError:
            pass

        #generate the files
        html = md.markdown(open(md_page, 'r').read().decode('utf-8'))
        html, errors = tidylib.tidy_document(html,
                                             options={'doctype':'strict'})
        open(html_page, 'w+').write(html.encode('utf-8'))
        print '... processed %s ' % html_page

def make_index():
    '''update the index.md'''

    #get the list of html files
    html_pages = [page for page in os.listdir(PAGES_PATH) 
                  if page.endswith('html')]

    #generate the index html
    index_html_tmp = md.markdown(open(INDEX_MD, 'r').read())
    index_template = jj.Template(index_html_tmp)
    #replace the index articles
    index_html = index_template.render(articles = html_pages)
    index_html, errors = tidylib.tidy_document(index_html, 
                                               options={'doctype':'strict'})

    open(INDEX_HTML, 'w+').write(index_html)
    print '... processed %s home page' % INDEX_HTML

def main():
    print '# update begins #'
    make_pages()
    make_index()
    print '# update done #'

if __name__ == '__main__':
    main()
