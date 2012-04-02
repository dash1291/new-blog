#!/bin/sh
python build.py '/newblog' && cp -R static/ site/ && rsync -avz --delete site/ /opt/lampp/htdocs/newblog/

